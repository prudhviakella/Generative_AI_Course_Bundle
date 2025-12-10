"""
COMPLETE ML TRAINING PIPELINE DEMONSTRATION
============================================
Full deployment system showing Pretrained → SFT → RL progression
With multiple model family options and comprehensive testing

Author: Training Pipeline Demo
Version: 2.0 (Fixed)
"""

from huggingface_hub import create_inference_endpoint, list_inference_endpoints, InferenceClient, whoami, get_inference_endpoint
import os
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

class ComprehensiveModelFamilies:
    """
    All available model families for demonstrating training progression
    Each family shows: Pretrained → Supervised Fine-Tuning → RL/Optimization
    """

    def __init__(self):
        # ============================================================
        # OPTION 1: GPT-2 Family (Most Reliable)
        # ============================================================
        self.gpt2_family = {
            "name": "GPT-2 Family",
            "description": "Classic models showing progression through different training",
            "models": {
                "base": {
                    "hub_repo": "gpt2",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "124M",
                    "description": "GPT-2 Base - Raw pretrained model",
                    "characteristics": "Basic text generation, no special training"
                },
                "sft": {
                    "hub_repo": "microsoft/DialoGPT-small",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "117M",
                    "description": "DialoGPT - Fine-tuned for conversations",
                    "characteristics": "Trained on dialogue data, better responses"
                },
                "rl": {
                    "hub_repo": "microsoft/DialoGPT-medium",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "345M",
                    "description": "DialoGPT Medium - Larger and more optimized",
                    "characteristics": "Better quality through scaling"
                }
            }
        }

        # ============================================================
        # OPTION 2: Pythia Family (EleutherAI)
        # ============================================================
        self.pythia_family = {
            "name": "Pythia Family",
            "description": "Shows data quality and size progression",
            "models": {
                "base": {
                    "hub_repo": "EleutherAI/pythia-70m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "70M",
                    "description": "Pythia 70M - Smallest base model",
                    "characteristics": "Minimal pretrained model"
                },
                "sft": {
                    "hub_repo": "EleutherAI/pythia-160m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "160M",
                    "description": "Pythia 160M - Larger, better trained",
                    "characteristics": "More parameters, better performance"
                },
                "rl": {
                    "hub_repo": "EleutherAI/pythia-410m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "410M",
                    "description": "Pythia 410M - Best small Pythia model",
                    "characteristics": "Significantly better quality"
                }
            }
        }

        # ============================================================
        # OPTION 3: OPT Family (Meta)
        # ============================================================
        self.opt_family = {
            "name": "OPT Family",
            "description": "Meta's models showing pure scaling effects",
            "models": {
                "base": {
                    "hub_repo": "facebook/opt-125m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "125M",
                    "description": "OPT-125M - Small base model",
                    "characteristics": "Basic pretrained model"
                },
                "sft": {
                    "hub_repo": "facebook/opt-350m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "350M",
                    "description": "OPT-350M - Medium sized",
                    "characteristics": "3x larger, better quality"
                },
                "rl": {
                    "hub_repo": "facebook/opt-1.3b",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "1.3B",
                    "description": "OPT-1.3B - Large model",
                    "characteristics": "10x larger than base"
                }
            }
        }

        # ============================================================
        # OPTION 4: FLAN-T5 Family (Google) - With Fixed Task Type
        # ============================================================
        self.flan_family = {
            "name": "FLAN-T5 Family",
            "description": "Best for showing instruction tuning effects",
            "models": {
                "base": {
                    "hub_repo": "google/flan-t5-small",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "80M",
                    "description": "FLAN-T5 Small - Base instruction model",
                    "characteristics": "Already instruction-tuned"
                },
                "sft": {
                    "hub_repo": "google/flan-t5-base",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "250M",
                    "description": "FLAN-T5 Base - Larger version",
                    "characteristics": "Better instruction following"
                },
                "rl": {
                    "hub_repo": "google/flan-t5-large",
                    "instance_type": "nvidia-l4",
                    "instance_size": "x1",
                    "params": "780M",
                    "description": "FLAN-T5 Large - Best quality",
                    "characteristics": "Production-ready quality"
                }
            }
        }

        # ============================================================
        # OPTION 5: Mixed Best Demonstration
        # ============================================================
        self.mixed_best = {
            "name": "Mixed Best Demo",
            "description": "Different models that best show each stage",
            "models": {
                "base": {
                    "hub_repo": "gpt2",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "124M",
                    "description": "GPT-2 - Pure pretrained, no fine-tuning",
                    "characteristics": "Raw language model"
                },
                "sft": {
                    "hub_repo": "microsoft/DialoGPT-small",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "117M",
                    "description": "DialoGPT - Fine-tuned on conversations",
                    "characteristics": "Specialized for dialogue"
                },
                "rl": {
                    "hub_repo": "google/flan-t5-base",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "250M",
                    "description": "FLAN-T5 - Instruction-optimized",
                    "characteristics": "Best at following instructions"
                }
            }
        }

        # ============================================================
        # OPTION 6: Tiny Models (Fastest Deployment)
        # ============================================================
        self.tiny_models = {
            "name": "Tiny Models",
            "description": "Smallest models for quick testing (deploys in 2 mins)",
            "models": {
                "base": {
                    "hub_repo": "EleutherAI/pythia-70m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "70M",
                    "description": "Pythia 70M - Tiny base model",
                    "characteristics": "Minimal but functional"
                },
                "sft": {
                    "hub_repo": "EleutherAI/pythia-160m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "160M",
                    "description": "Pythia 160M - Small improvement",
                    "characteristics": "2x size, better quality"
                },
                "rl": {
                    "hub_repo": "EleutherAI/pythia-410m",
                    "instance_type": "nvidia-t4",
                    "instance_size": "x1",
                    "params": "410M",
                    "description": "Pythia 410M - Best tiny model",
                    "characteristics": "Good quality despite size"
                }
            }
        }

class MLPipelineDeployment:
    """Main deployment and testing system"""

    def __init__(self):
        self.families = ComprehensiveModelFamilies()
        self.selected_family = None
        self.deployed_endpoints = {}
        self.test_results = {}

    def print_banner(self):
        """Print welcome banner"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                ML TRAINING PIPELINE DEMONSTRATION                 ║
║                                                                   ║
║  See how models improve through training stages:                 ║
║  1. PRETRAINED: Raw language model                              ║
║  2. SUPERVISED FINE-TUNING: Task-specific training              ║
║  3. RL/OPTIMIZATION: Further improvements                        ║
║                                                                   ║
║  Similar to: DeepSeek (base → instruct → RL)                    ║
║             GPT (base → SFT → RLHF)                             ║
║             LLaMA (base → instruct → chat)                      ║
╚══════════════════════════════════════════════════════════════════╝
        """)

    def select_model_family(self) -> bool:
        """Let user select which model family to deploy"""

        print("\n📚 SELECT MODEL FAMILY")
        print("=" * 60)

        families_list = [
            self.families.gpt2_family,
            self.families.pythia_family,
            self.families.opt_family,
            self.families.flan_family,
            self.families.mixed_best,
            self.families.tiny_models
        ]

        for i, family in enumerate(families_list, 1):
            print(f"\n{i}. {family['name']}")
            print(f"   {family['description']}")
            print(f"   Models: {family['models']['base']['params']} → "
                  f"{family['models']['sft']['params']} → "
                  f"{family['models']['rl']['params']}")

            # Cost estimate
            t4_count = sum(1 for m in family['models'].values()
                          if m['instance_type'] == 'nvidia-t4')
            l4_count = sum(1 for m in family['models'].values()
                          if m['instance_type'] == 'nvidia-l4')
            cost = t4_count * 0.60 + l4_count * 0.80
            print(f"   Cost: ~${cost:.2f}/hour")

        print("\n" + "=" * 60)
        print("Recommendations:")
        print("  • For best demonstration: Choose 1 (GPT-2 Family)")
        print("  • For fastest deployment: Choose 6 (Tiny Models)")
        print("  • For instruction tuning: Choose 4 (FLAN-T5)")

        while True:
            choice = input("\nSelect family (1-6): ").strip()

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(families_list):
                    self.selected_family = families_list[idx]
                    print(f"\n✅ Selected: {self.selected_family['name']}")
                    return True
            except:
                pass

            print("❌ Invalid choice. Please enter 1-6")

    def check_and_cleanup_existing(self) -> bool:
        """Check for existing endpoints and offer cleanup"""

        print("\n🔍 Checking existing endpoints...")
        endpoints = list_inference_endpoints()

        if endpoints:
            print(f"Found {len(endpoints)} existing endpoint(s):")

            for ep in endpoints:
                status_emoji = "🟢" if ep.status == "running" else "🟡" if ep.status == "pending" else "🔴"
                print(f"  {status_emoji} {ep.name} ({ep.status})")

            print("\nOptions:")
            print("1. Delete all and start fresh")
            print("2. Keep existing endpoints")

            choice = input("Choice (1/2): ").strip()

            if choice == "1":
                for ep in endpoints:
                    try:
                        print(f"  🗑️ Deleting {ep.name}...")
                        ep.delete()
                    except Exception as e:
                        print(f"  ⚠️ Could not delete {ep.name}: {e}")

                print("✅ Cleanup complete\n")
                return True
            else:
                print("ℹ️ Keeping existing endpoints\n")
                return False
        else:
            print("✅ No existing endpoints\n")
            return True

    def deploy_single_model(self, stage: str, model_config: Dict) -> Optional[object]:
        """Deploy a single model"""

        endpoint_name = f"{stage}-{int(time.time())}"[:32]

        print(f"\n{'='*50}")
        print(f"📦 Deploying {stage.upper()} Model")
        print(f"{'='*50}")
        print(f"Repository: {model_config['hub_repo']}")
        print(f"Size: {model_config['params']}")
        print(f"Instance: {model_config['instance_type']}")
        print(f"Description: {model_config['description']}")
        print(f"Characteristics: {model_config['characteristics']}")

        try:
            print(f"\n⏳ Creating endpoint...")

            # Determine task type based on model
            task = "text-generation"  # Default for most models

            endpoint = create_inference_endpoint(
                name=endpoint_name,
                repository=model_config["hub_repo"],
                framework="pytorch",
                task=task,
                accelerator="gpu",
                vendor="aws",
                region="us-east-1",
                type="protected",
                instance_size=model_config["instance_size"],
                instance_type=model_config["instance_type"]
            )

            print(f"✅ Successfully created!")
            print(f"   Name: {endpoint.name}")
            print(f"   Status: {endpoint.status}")

            return endpoint

        except Exception as e:
            print(f"❌ Deployment failed: {e}")

            # Provide helpful error messages
            if "422" in str(e):
                print("💡 Task type error - model might need different configuration")
            elif "403" in str(e):
                print("💡 Check your HF token permissions and billing")
            elif "quota" in str(e).lower():
                print("💡 GPU quota exceeded - request increase from HuggingFace")

            return None

    def deploy_pipeline(self) -> bool:
        """Deploy the complete pipeline"""

        if not self.selected_family:
            print("❌ No family selected")
            return False

        print(f"\n🚀 DEPLOYING {self.selected_family['name'].upper()}")
        print("=" * 60)

        # Calculate total cost
        total_cost = 0
        for model in self.selected_family['models'].values():
            if model['instance_type'] == 'nvidia-t4':
                total_cost += 0.60
            elif model['instance_type'] == 'nvidia-l4':
                total_cost += 0.80
            elif model['instance_type'] == 'nvidia-a10g':
                total_cost += 1.30

        print(f"Total cost: ${total_cost:.2f}/hour")
        print(f"Models to deploy: 3")

        confirm = input("\nProceed with deployment? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Deployment cancelled")
            return False

        # Deploy each model
        stages = ["base", "sft", "rl"]

        for i, stage in enumerate(stages, 1):
            print(f"\n[Deployment {i}/3]")

            model_config = self.selected_family['models'][stage]
            endpoint = self.deploy_single_model(stage, model_config)

            if endpoint:
                self.deployed_endpoints[stage] = endpoint

                # Wait between deployments
                if stage != "rl":
                    wait_time = 20
                    print(f"\n⏳ Waiting {wait_time}s before next deployment...")
                    for j in range(wait_time, 0, -5):
                        print(f"   {j} seconds...", end='\r')
                        time.sleep(5)
                    print(" " * 30, end='\r')
            else:
                print(f"❌ Failed to deploy {stage}")
                if stage != "rl":
                    cont = input("Continue with remaining models? (y/n): ").strip().lower()
                    if cont not in ['y', 'yes']:
                        break

        # Summary
        print("\n" + "=" * 60)
        print("📊 DEPLOYMENT SUMMARY")
        print("=" * 60)

        if self.deployed_endpoints:
            print(f"✅ Successfully deployed: {len(self.deployed_endpoints)}/3")
            for stage, ep in self.deployed_endpoints.items():
                print(f"   • {stage.upper()}: {ep.name}")
        else:
            print("❌ No models deployed successfully")

        return len(self.deployed_endpoints) > 0

    def wait_for_models(self, timeout: int = 300) -> bool:
        """Wait for all deployed models to be ready"""

        if not self.deployed_endpoints:
            print("No models to wait for")
            return False

        print(f"\n⏳ Waiting for {len(self.deployed_endpoints)} model(s) to initialize...")
        print("   (Usually takes 2-5 minutes)")

        start_time = time.time()
        username = None

        try:
            username = whoami()["name"]
        except:
            print("⚠️ Could not get username for status updates")

        while (time.time() - start_time) < timeout:
            all_ready = True
            status_parts = []

            for stage, endpoint in self.deployed_endpoints.items():
                # Try to refresh status
                if username:
                    try:
                        endpoint = get_inference_endpoint(endpoint.name, namespace=username)
                        self.deployed_endpoints[stage] = endpoint
                    except:
                        pass

                status = endpoint.status if hasattr(endpoint, 'status') else "unknown"

                # Status emoji
                if status == "running":
                    emoji = "🟢"
                elif status == "pending" or status == "initializing":
                    emoji = "🟡"
                    all_ready = False
                elif status == "failed":
                    emoji = "🔴"
                    all_ready = False
                else:
                    emoji = "⚪"
                    all_ready = False

                status_parts.append(f"{stage}:{emoji}")

            # Display status
            elapsed = int(time.time() - start_time)
            status_str = " | ".join(status_parts)
            print(f"\r[{elapsed}s] {status_str}", end="", flush=True)

            if all_ready:
                print("\n✅ All models ready!")
                return True

            # Check for any failures
            failed = [s for s, e in self.deployed_endpoints.items()
                     if hasattr(e, 'status') and e.status == "failed"]
            if failed:
                print(f"\n❌ Failed models: {', '.join(failed)}")
                print("Check logs at: https://ui.endpoints.huggingface.co")
                return False

            time.sleep(10)

        print(f"\n⏱️ Timeout after {timeout} seconds")
        print("Some models may still be initializing. Check: https://ui.endpoints.huggingface.co")
        return False

    def run_tests(self):
        """Run comprehensive tests on deployed models"""

        if not self.deployed_endpoints:
            print("No models to test")
            return

        print("\n" + "=" * 60)
        print("🧪 TESTING MODEL PROGRESSION")
        print("=" * 60)
        print("\nRunning tests to show differences between training stages...\n")

        # Test cases designed to show progression
        test_cases = [
            {
                "name": "Simple Completion",
                "prompt": "The weather today is",
                "explanation": "Basic text completion ability"
            },
            {
                "name": "Question Answering",
                "prompt": "Q: What is the capital of France?\nA:",
                "explanation": "Knowledge and formatting"
            },
            {
                "name": "Instruction Following",
                "prompt": "Write a haiku about summer:",
                "explanation": "Following specific instructions"
            },
            {
                "name": "Math Problem",
                "prompt": "Calculate: 15 + 27 =",
                "explanation": "Basic reasoning"
            },
            {
                "name": "Translation",
                "prompt": "Translate to Spanish: Hello, how are you?",
                "explanation": "Language understanding"
            }
        ]

        for test in test_cases:
            print(f"📝 Test: {test['name']}")
            print(f"   Purpose: {test['explanation']}")
            print(f"   Prompt: \"{test['prompt']}\"")
            print("-" * 50)

            self.test_results[test['name']] = {}

            for stage in ["base", "sft", "rl"]:
                if stage not in self.deployed_endpoints:
                    print(f"   {stage.upper()}: Not deployed")
                    continue

                endpoint = self.deployed_endpoints[stage]

                # Check if ready
                if hasattr(endpoint, 'status') and endpoint.status != "running":
                    print(f"   {stage.upper()}: Not ready (status: {endpoint.status})")
                    continue

                try:
                    client = InferenceClient(
                        model=endpoint.url,
                        token=os.environ.get("HF_TOKEN")
                    )

                    # Generate response
                    response = client.text_generation(
                        test['prompt'],
                        max_new_tokens=50,
                        temperature=0.7,
                        do_sample=True
                    )

                    # Clean response
                    response = response.strip()
                    if len(response) > 150:
                        response = response[:150] + "..."

                    # Store result
                    self.test_results[test['name']][stage] = response

                    # Display with stage label
                    stage_labels = {
                        "base": "PRETRAINED",
                        "sft": "FINE-TUNED",
                        "rl": "OPTIMIZED"
                    }

                    print(f"   {stage_labels[stage]}:")
                    print(f"   → {response}\n")

                except Exception as e:
                    error_msg = str(e)[:100]
                    self.test_results[test['name']][stage] = f"Error: {error_msg}"
                    print(f"   {stage.upper()}: ❌ Error - {error_msg}\n")

            print()  # Extra spacing between tests

    def analyze_results(self):
        """Analyze and explain test results"""

        if not self.test_results:
            print("No test results to analyze")
            return

        print("\n" + "=" * 60)
        print("📊 ANALYSIS & INSIGHTS")
        print("=" * 60)

        print("\n🎯 Key Observations:\n")

        # Analyze each stage
        stages_analysis = {
            "base": {
                "title": "PRETRAINED MODEL",
                "observations": [
                    "May not follow instructions well",
                    "Tends to just continue text naturally",
                    "No understanding of specific task formats",
                    "Raw language modeling capabilities"
                ]
            },
            "sft": {
                "title": "FINE-TUNED MODEL",
                "observations": [
                    "Better at following instructions",
                    "Understands question-answer format",
                    "More coherent responses",
                    "Task-aware generation"
                ]
            },
            "rl": {
                "title": "OPTIMIZED MODEL",
                "observations": [
                    "Best overall quality",
                    "Most reliable responses",
                    "Better reasoning capabilities",
                    "Combines benefits of size/training"
                ]
            }
        }

        for stage, analysis in stages_analysis.items():
            if stage in self.deployed_endpoints:
                print(f"📌 {analysis['title']}:")
                for obs in analysis['observations']:
                    print(f"   • {obs}")
                print()

        print("💡 This progression demonstrates why modern LLMs use:")
        print("   1. Pretraining: Learn language patterns from raw text")
        print("   2. Fine-tuning: Adapt to specific tasks and formats")
        print("   3. RL/RLHF: Optimize for human preferences and quality")
        print("\n   Similar to: GPT → ChatGPT → GPT-4")
        print("               or: LLaMA → Alpaca → Vicuna")
        print("               or: DeepSeek-base → instruct → RL")

    def export_results(self):
        """Export test results to file"""

        if not self.test_results:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pipeline_results_{timestamp}.json"

        export_data = {
            "timestamp": timestamp,
            "family": self.selected_family['name'],
            "models": {
                stage: {
                    "repo": config['hub_repo'],
                    "params": config['params'],
                    "endpoint": self.deployed_endpoints.get(stage, {}).name if stage in self.deployed_endpoints else None
                }
                for stage, config in self.selected_family['models'].items()
            },
            "test_results": self.test_results
        }

        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"\n📄 Results exported to: {filename}")
        except Exception as e:
            print(f"\n⚠️ Could not export results: {e}")

    def cleanup_endpoints(self):
        """Clean up deployed endpoints"""

        if not self.deployed_endpoints:
            print("\n✅ No endpoints to clean up")
            return

        print("\n" + "=" * 60)
        print("🧹 CLEANUP OPTIONS")
        print("=" * 60)

        # Calculate current costs
        total_hourly_cost = 0
        for stage, endpoint in self.deployed_endpoints.items():
            model_config = self.selected_family['models'][stage]
            if model_config['instance_type'] == 'nvidia-t4':
                total_hourly_cost += 0.60
            elif model_config['instance_type'] == 'nvidia-l4':
                total_hourly_cost += 0.80
            elif model_config['instance_type'] == 'nvidia-a10g':
                total_hourly_cost += 1.30

        print(f"Current endpoints: {len(self.deployed_endpoints)}")
        print(f"Hourly cost: ${total_hourly_cost:.2f}")
        print(f"Daily cost: ${total_hourly_cost * 24:.2f}")

        print("\nOptions:")
        print("1. Pause all endpoints (can resume later)")
        print("2. Delete all endpoints (permanent)")
        print("3. Keep running (continue billing)")
        print("4. Delete specific endpoint")

        choice = input("\nChoice (1-4): ").strip()

        if choice == "1":
            # Pause all
            for stage, endpoint in self.deployed_endpoints.items():
                try:
                    print(f"⏸️  Pausing {stage}...")
                    endpoint.pause()
                except Exception as e:
                    print(f"⚠️  Could not pause {stage}: {e}")
            print("✅ All endpoints paused")

        elif choice == "2":
            # Delete all
            confirm = input("⚠️  Delete all endpoints? This is permanent! (type 'yes' to confirm): ").strip()
            if confirm.lower() == "yes":
                for stage, endpoint in self.deployed_endpoints.items():
                    try:
                        print(f"🗑️  Deleting {stage}...")
                        endpoint.delete()
                    except Exception as e:
                        print(f"⚠️  Could not delete {stage}: {e}")
                print("✅ All endpoints deleted")
            else:
                print("❌ Deletion cancelled")

        elif choice == "3":
            # Keep running
            print("ℹ️  Endpoints will continue running")
            print("⚠️  Remember to clean them up when done!")
            print("   Visit: https://ui.endpoints.huggingface.co")

        elif choice == "4":
            # Delete specific
            print("\nWhich endpoint to delete?")
            for i, stage in enumerate(self.deployed_endpoints.keys(), 1):
                print(f"{i}. {stage.upper()}")

            try:
                idx = int(input("Choice: ").strip()) - 1
                stage_to_delete = list(self.deployed_endpoints.keys())[idx]

                confirm = input(f"Delete {stage_to_delete}? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    self.deployed_endpoints[stage_to_delete].delete()
                    print(f"✅ Deleted {stage_to_delete}")
                    del self.deployed_endpoints[stage_to_delete]
            except:
                print("❌ Invalid choice")

class QuickDeploy:
    """Quick deployment option for testing"""

    @staticmethod
    def deploy_minimal_pipeline():
        """Deploy the smallest possible pipeline for quick testing"""

        print("\n🚀 QUICK DEPLOY MODE")
        print("=" * 60)
        print("Deploying minimal pipeline (3 tiny models)")
        print("Perfect for quick testing - deploys in ~2 minutes\n")

        models = [
            ("base", "EleutherAI/pythia-70m", "Pythia 70M - Tiny base"),
            ("sft", "EleutherAI/pythia-160m", "Pythia 160M - Slightly better"),
            ("rl", "EleutherAI/pythia-410m", "Pythia 410M - Best small")
        ]

        deployed = {}

        for stage, repo, desc in models:
            print(f"📦 Deploying {stage.upper()}: {desc}")

            try:
                endpoint = create_inference_endpoint(
                    name=f"quick-{stage}-{int(time.time())}"[:32],
                    repository=repo,
                    framework="pytorch",
                    task="text-generation",
                    accelerator="gpu",
                    vendor="aws",
                    region="us-east-1",
                    type="protected",
                    instance_size="x1",
                    instance_type="nvidia-t4"
                )

                deployed[stage] = endpoint
                print(f"✅ Success: {endpoint.name}\n")

                if stage != "rl":
                    time.sleep(15)

            except Exception as e:
                print(f"❌ Failed: {e}\n")

        return deployed

def main():
    """Main execution function"""

    # Clear screen for better presentation
    os.system('clear' if os.name == 'posix' else 'cls')

    # Check authentication
    print("🔐 Checking authentication...")

    if not os.environ.get("HF_TOKEN"):
        print("\n❌ HF_TOKEN not found in environment!")
        print("\nTo set it:")
        print("  export HF_TOKEN='hf_your_token_here'")
        print("\nGet your token from: https://huggingface.co/settings/tokens")

        token = input("\nEnter token now (or press Enter to exit): ").strip()
        if token:
            os.environ["HF_TOKEN"] = token
        else:
            print("Exiting...")
            return

    # Verify token
    try:
        user_info = whoami()
        print(f"✅ Authenticated as: {user_info['name']}\n")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("Please check your token and try again")
        return

    # Main menu
    pipeline = MLPipelineDeployment()
    pipeline.print_banner()

    print("\n📋 DEPLOYMENT OPTIONS")
    print("=" * 60)
    print("1. Full Pipeline Deployment (Choose model family)")
    print("2. Quick Deploy (Tiny models, 2 minutes)")
    print("3. Check existing endpoints")
    print("4. Exit")

    choice = input("\nChoice (1-4): ").strip()

    if choice == "1":
        # Full deployment
        pipeline.check_and_cleanup_existing()

        if pipeline.select_model_family():
            if pipeline.deploy_pipeline():
                if pipeline.wait_for_models():
                    pipeline.run_tests()
                    pipeline.analyze_results()
                    pipeline.export_results()
                else:
                    print("\n⚠️ Models not ready. You can:")
                    print("1. Check status at: https://ui.endpoints.huggingface.co")
                    print("2. Run tests manually once ready")

                pipeline.cleanup_endpoints()
            else:
                print("\n❌ Deployment failed")

    elif choice == "2":
        # Quick deploy
        deployed = QuickDeploy.deploy_minimal_pipeline()

        if deployed:
            print(f"\n✅ Deployed {len(deployed)} models")
            print("⏳ Wait 2-3 minutes for initialization")
            print("📍 Monitor at: https://ui.endpoints.huggingface.co")

            cleanup = input("\n🧹 Delete all when done? (y/n): ").strip().lower()
            if cleanup in ['y', 'yes']:
                for ep in deployed.values():
                    ep.delete()
                print("✅ All deleted")

    elif choice == "3":
        # Check existing
        endpoints = list_inference_endpoints()

        if endpoints:
            print(f"\n📊 Found {len(endpoints)} endpoint(s):\n")

            for ep in endpoints:
                status_emoji = "🟢" if ep.status == "running" else "🟡" if ep.status == "pending" else "🔴"
                print(f"{status_emoji} {ep.name}")
                print(f"   Model: {ep.repository}")
                print(f"   Status: {ep.status}")
                if hasattr(ep, 'url') and ep.url:
                    print(f"   URL: {ep.url}")
                print()

            action = input("Delete all? (y/n): ").strip().lower()
            if action in ['y', 'yes']:
                for ep in endpoints:
                    try:
                        ep.delete()
                        print(f"🗑️ Deleted {ep.name}")
                    except:
                        pass
        else:
            print("\n✅ No endpoints found")

    print("\n👋 Thanks for using the ML Pipeline Demo!")
    print("📚 Learn more about training pipelines:")
    print("   • Pretraining: https://arxiv.org/abs/2005.14165")
    print("   • Fine-tuning: https://arxiv.org/abs/2109.01652")
    print("   • RLHF: https://arxiv.org/abs/2203.02155")

if __name__ == "__main__":
    main()