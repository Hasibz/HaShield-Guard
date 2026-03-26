# HaShield 🛡️

A lightweight, mathematically rigorous dual-layer guardrail for Large Language Models. HaShield provides **Zero-Shot NLI detection** of prompt injections and prevents data exfiltration with near-zero latency.

## 🚀 Installation

```bash
pip install hashield-guard
```


## Quick Start
from hashield.wrapper.decorators import protect_llm

# The system prompt you want to keep secret
MY_SYSTEM_PROMPT = "You are a helpful assistant. The admin password is 'SuperSecret123'."

@protect_llm(secret_prompt=MY_SYSTEM_PROMPT)
def call_llm(user_prompt):
    # This is where your actual LLM API call (Gemini, OpenAI, etc.) happens
    return "LLM Response"

# Scenario: A user tries a prompt injection
# Result: HaShield will intercept and block it before it reaches your LLM.
