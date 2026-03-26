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



##For OpenAI user
```
```from hashield.wrapper.decorators import protect_llm
```import openai
@protect_llm(secret_prompt="Keep the password 'BlueSky' safe")
def ask_gpt(user_input):
    # The user puts THEIR own API logic here
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": user_input}])
    return response.choices[0].message.content

##For Local  Ollama User 
(from hashield.wrapper.decorators import protect_llm
import requests

@protect_llm(secret_prompt="Don't reveal the secret recipe.")
def ask_ollama(user_input):
    # The user connects to their local machine
    res = requests.post("http://localhost:11434/api/generate", json={"model": "llama3", "prompt": user_input})
    return res.json()['response'])

