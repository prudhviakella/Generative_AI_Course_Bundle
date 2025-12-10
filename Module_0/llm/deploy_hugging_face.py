import os
import time
from pathlib import Path
from huggingface_hub import create_inference_endpoint, list_inference_endpoints, HfApi
from typing import Optional, Dict, List

"""
Where to Monitor Your Endpoint in HuggingFace UI:
 https://ui.endpoints.huggingface.co
"""


class ModelDeployer:
    """Deploy math and safety models to HuggingFace Inference Endpoints"""

    def __init__(self):
        self.api = HfApi()

        # Model configurations with HuggingFace Hub equivalents
        self.model_configs = {
            "deepseek-math-base": {
                "local_path": "/app/models/deepseek-math-7b-base",
                "hub_repo": "deepseek-ai/deepseek-math-7b-base",
                "instance_size": "x1",
                "instance_type": "nvidia-a10g",  # Good for 7B models
                "task": "text-generation",
                "description": "DeepSeek Math 7B Base Model"
            },
            "deepseek-math-instruct": {
                "local_path": "/app/models/deepseek-math-7b-instruct",
                "hub_repo": "deepseek-ai/deepseek-math-7b-instruct",
                "instance_size": "x1",
                "instance_type": "nvidia-a10g",
                "task": "text-generation",
                "description": "DeepSeek Math 7B Instruction-tuned Model"
            },
            "deepseek-math-rl": {
                "local_path": "/app/models/deepseek-math-7b-rl",
                "hub_repo": "deepseek-ai/deepseek-math-7b-rl",
                "instance_size": "x1",
                "instance_type": "nvidia-a10g",
                "task": "text-generation",
                "description": "DeepSeek Math 7B with RL Training"
            },
            "llama-guard": {
                "local_path": "/app/models/Llama-Guard-3-8B",
                "hub_repo": "meta-llama/Llama-Guard-3-8B",  # Requires access
                "instance_size": "x1",
                "instance_type": "nvidia-a10g",  # 8B model needs good GPU
                "task": "text-generation",
                "description": "Llama Guard 3 8B Safety Model",
                "requires_access": True
            }
        }

    def check_local_models(self) -> Dict[str, bool]:
        """Check which models exist locally"""
        status = {}
        for name, config in self.model_configs.items():
            local_path = Path(config["local_path"])
            exists = local_path.exists() and local_path.is_dir()
            status[name] = exists
            print(f"{'✓' if exists else '✗'} {name}: {config['local_path']}")
        return status

    def upload_model_to_hub(self, model_name: str, repo_name: Optional[str] = None) -> str:
        """Upload local model to HuggingFace Hub"""
        config = self.model_configs.get(model_name)
        if not config:
            raise ValueError(f"Unknown model: {model_name}")

        local_path = Path(config["local_path"])
        if not local_path.exists():
            raise FileNotFoundError(f"Model not found at {local_path}")

        # Create repo name if not provided
        if not repo_name:
            username = self.api.whoami()["name"]
            repo_name = f"{username}/{model_name}"

        print(f"Uploading {model_name} to {repo_name}...")

        try:
            # Create repository
            self.api.create_repo(
                repo_id=repo_name,
                repo_type="model",
                exist_ok=True,
                private=False  # Set to True for private models
            )

            # Upload model datasets
            self.api.upload_folder(
                folder_path=str(local_path),
                repo_id=repo_name,
                repo_type="model",
                commit_message=f"Upload {model_name}"
            )

            print(f"✓ Model uploaded to https://huggingface.co/{repo_name}")
            return repo_name

        except Exception as e:
            print(f"✗ Error uploading model: {e}")
            raise

    def deploy_model(self, model_name: str, use_hub: bool = True, custom_repo: Optional[str] = None) -> Optional[
        object]:
        """Deploy a model to Inference Endpoints"""

        config = self.model_configs.get(model_name)
        if not config:
            print(f"✗ Unknown model: {model_name}")
            return None

        # Check for special access requirements
        if config.get("requires_access"):
            print(f"⚠️  {model_name} requires special access.")
            print(f"   Visit https://huggingface.co/{config['hub_repo']} to request access.")
            proceed = input("   Proceed anyway? (y/n): ").lower()
            if proceed != 'y':
                return None

        # Determine repository to use
        if custom_repo:
            repository = custom_repo
        elif use_hub:
            repository = config["hub_repo"]
        else:
            # Upload local model first
            print(f"Uploading local model to Hub first...")
            repository = self.upload_model_to_hub(model_name)

        # Generate unique endpoint name
        timestamp = int(time.time())
        endpoint_name = f"{model_name}-{timestamp}".replace("_", "-")[:32]

        print(f"\nDeploying {model_name}...")
        print(f"  Repository: {repository}")
        print(f"  Instance: {config['instance_type']} ({config['instance_size']})")

        try:
            endpoint = create_inference_endpoint(
                name=endpoint_name,
                repository=repository,
                framework="pytorch",
                task=config["task"],
                accelerator="gpu",
                vendor="aws",
                region="us-east-1",
                type="protected",
                instance_size=config["instance_size"],
                instance_type=config["instance_type"],
                # Optional: Add custom environment variables for math models
                env={
                    "MAX_INPUT_LENGTH": "4096",
                    "MAX_TOTAL_TOKENS": "8192",
                    "MAX_BATCH_PREFILL_TOKENS": "4096",
                }
            )

            print(f"✓ Endpoint created: {endpoint.name}")
            print(f"  Status: {endpoint.status}")

            # Option to wait for deployment
            wait = input("\nWait for endpoint to be ready? (y/n): ").lower()
            if wait == 'y':
                print("Waiting (this may take 5-10 minutes)...")
                endpoint.wait()
                print(f"✓ Endpoint ready at: {endpoint.url}")

            return endpoint

        except Exception as e:
            print(f"✗ Deployment failed: {e}")

            if "403" in str(e) or "Forbidden" in str(e):
                print("\nPossible issues:")
                print("1. Token lacks permissions")
                print("2. No payment method on file")
                print("3. Model requires access approval")
                print("4. Insufficient quota for instance type")

            return None

    def deploy_all_models(self, models: Optional[List[str]] = None):
        """Deploy multiple models"""
        if models is None:
            models = list(self.model_configs.keys())

        deployed = []
        failed = []

        for model_name in models:
            print(f"\n{'=' * 50}")
            print(f"Deploying {model_name}...")

            endpoint = self.deploy_model(model_name, use_hub=True)

            if endpoint:
                deployed.append((model_name, endpoint))
            else:
                failed.append(model_name)

            # Add delay between deployments
            if model_name != models[-1]:
                print("\nWaiting 30 seconds before next deployment...")
                time.sleep(30)

        # Summary
        print(f"\n{'=' * 50}")
        print("Deployment Summary:")
        print(f"✓ Successfully deployed: {len(deployed)}")
        for name, ep in deployed:
            print(f"  - {name}: {ep.name}")

        if failed:
            print(f"✗ Failed: {len(failed)}")
            for name in failed:
                print(f"  - {name}")

        return deployed, failed

    def test_endpoint(self, endpoint, prompt: str = "Solve: What is 15 + 27?"):
        """Test a deployed endpoint"""
        try:
            from huggingface_hub import InferenceClient

            client = InferenceClient(model=endpoint.url, token=os.environ.get("HF_TOKEN"))

            response = client.text_generation(
                prompt,
                max_new_tokens=100,
                temperature=0.7,
            )

            print(f"Prompt: {prompt}")
            print(f"Response: {response}")

            return response

        except Exception as e:
            print(f"Error testing endpoint: {e}")
            return None

    def manage_endpoints(self):
        """Interactive endpoint management"""
        while True:
            print(f"\n{'=' * 50}")
            print("Endpoint Management Menu:")
            print("1. List all endpoints")
            print("2. Deploy a single model")
            print("3. Deploy all math models")
            print("4. Test an endpoint")
            print("5. Pause an endpoint")
            print("6. Resume an endpoint")
            print("7. Delete an endpoint")
            print("8. Exit")

            choice = input("\nChoice: ").strip()

            if choice == "1":
                self.list_all_endpoints()

            elif choice == "2":
                print("\nAvailable models:")
                for i, name in enumerate(self.model_configs.keys(), 1):
                    print(f"{i}. {name}: {self.model_configs[name]['description']}")

                model_idx = input("Select model number: ").strip()
                try:
                    model_name = list(self.model_configs.keys())[int(model_idx) - 1]
                    self.deploy_model(model_name)
                except (ValueError, IndexError):
                    print("Invalid selection")

            elif choice == "3":
                # Deploy only math models (not Llama Guard by default)
                math_models = ["deepseek-math-base", "deepseek-math-instruct", "deepseek-math-rl"]
                self.deploy_all_models(math_models)

            elif choice == "4":
                endpoints = list_inference_endpoints()
                if not endpoints:
                    print("No endpoints available")
                    continue

                for i, ep in enumerate(endpoints, 1):
                    print(f"{i}. {ep.name} ({ep.status})")

                ep_idx = input("Select endpoint to test: ").strip()
                try:
                    endpoint = endpoints[int(ep_idx) - 1]
                    prompt = input("Enter prompt (or press Enter for default): ").strip()
                    if not prompt:
                        prompt = "Solve step by step: What is 125 * 8?"
                    self.test_endpoint(endpoint, prompt)
                except (ValueError, IndexError):
                    print("Invalid selection")

            elif choice == "5":  # Pause
                self.pause_resume_endpoint(pause=True)

            elif choice == "6":  # Resume
                self.pause_resume_endpoint(pause=False)

            elif choice == "7":  # Delete
                self.delete_endpoint()

            elif choice == "8":
                break

            else:
                print("Invalid choice")

    def list_all_endpoints(self):
        """List all endpoints with details"""
        endpoints = list_inference_endpoints()
        if not endpoints:
            print("No endpoints found")
            return

        print(f"\nFound {len(endpoints)} endpoint(s):")
        for ep in endpoints:
            print(f"\n- Name: {ep.name}")
            print(f"  Status: {ep.status}")
            print(f"  Model: {ep.repository}")
            if hasattr(ep, 'instance_type'):
                print(f"  Instance: {ep.instance_type}")
            if ep.url:
                print(f"  URL: {ep.url}")

    def pause_resume_endpoint(self, pause: bool = True):
        """Pause or resume an endpoint"""
        endpoints = list_inference_endpoints()
        if not endpoints:
            print("No endpoints found")
            return

        for i, ep in enumerate(endpoints, 1):
            print(f"{i}. {ep.name} ({ep.status})")

        idx = input(f"Select endpoint to {'pause' if pause else 'resume'}: ").strip()
        try:
            endpoint = endpoints[int(idx) - 1]
            if pause:
                endpoint.pause()
                print(f"✓ Paused {endpoint.name}")
            else:
                endpoint.resume()
                print(f"✓ Resumed {endpoint.name}")
                print("  Waiting for it to be ready...")
                endpoint.wait()
                print(f"  Ready at: {endpoint.url}")
        except (ValueError, IndexError):
            print("Invalid selection")
        except Exception as e:
            print(f"Error: {e}")

    def delete_endpoint(self):
        """Delete an endpoint"""
        endpoints = list_inference_endpoints()
        if not endpoints:
            print("No endpoints found")
            return

        for i, ep in enumerate(endpoints, 1):
            print(f"{i}. {ep.name} ({ep.status})")

        idx = input("Select endpoint to delete (or 'all' for all): ").strip()

        if idx.lower() == 'all':
            confirm = input(f"Delete ALL {len(endpoints)} endpoints? (yes/no): ").strip()
            if confirm.lower() == 'yes':
                for ep in endpoints:
                    print(f"Deleting {ep.name}...")
                    ep.delete()
                print("All endpoints deleted")
        else:
            try:
                endpoint = endpoints[int(idx) - 1]
                confirm = input(f"Delete {endpoint.name}? (yes/no): ").strip()
                if confirm.lower() == 'yes':
                    endpoint.delete()
                    print(f"✓ Deleted {endpoint.name}")
            except (ValueError, IndexError):
                print("Invalid selection")


def main():
    """Main entry point"""
    print("=== DeepSeek Math & Llama Guard Model Deployment ===\n")

    # Check for HF token
    if not os.environ.get("HF_TOKEN"):
        print("⚠️  No HF_TOKEN found in environment")
        print("Please set: export HF_TOKEN='your_token_here'")
        token = input("Or enter token now (leave empty to skip): ").strip()
        if token:
            os.environ["HF_TOKEN"] = token
        else:
            print("Continuing without token (limited functionality)")

    deployer = ModelDeployer()

    # Check local models
    print("Checking local models:")
    local_status = deployer.check_local_models()

    # Start interactive management
    deployer.manage_endpoints()


if __name__ == "__main__":
    main()