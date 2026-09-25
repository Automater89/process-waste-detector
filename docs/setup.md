# Setup Guide

## Prerequisites

- Azure subscription with access to Azure OpenAI
- Python 3.10+
- VS Code (recommended)
- GitHub account

## Azure Resources Needed

| Resource | Tier | Notes |
|---|---|---|
| Azure OpenAI | Standard S0 | Deploy `gpt-4o` |

This project requires only Azure OpenAI — no Search or Storage needed.

## Provision Azure OpenAI

1. Go to [portal.azure.com](https://portal.azure.com)
2. Search "Azure OpenAI" and create a new resource
3. Region: East US 2 (best model availability)
4. Once deployed, go to Azure OpenAI Studio > Deployments
5. Deploy `gpt-4o`, name the deployment `gpt-4o`
6. Copy the endpoint and key from Keys and Endpoint

## Local Setup

```bash
git clone https://github.com/Automater89/process-waste-detector.git
cd process-waste-detector
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your Azure OpenAI endpoint and key to .env
```

## Verify Setup

```bash
python src/utils/config.py
```

Expected output:
```
[OK] All environment variables loaded.
  OpenAI endpoint: https://your-resource.openai.azure.com/
```

## Cost Notes

- Azure OpenAI GPT-4o: charged per token
- A single process analysis uses approximately 500-800 tokens total (input + output)
- At standard pricing, cost per analysis is well under $0.01
- No persistent services to leave running — costs only accrue when you run the tool
