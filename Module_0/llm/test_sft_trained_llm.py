import requests

API_URL = "https://o1w4a8e7uvlei3kn.us-east-1.aws.endpoints.huggingface.cloud"   # your endpoint URL
HF_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "inputs": "Write an email inviting team for sprint planning meeting.",
    "parameters": {
        "temperature": 0.1,
    }
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json())