# HaShield 🛡️

A lightweight, mathematically rigorous dual-layer guardrail for Large Language Models. HaShield provides zero-shot detection of prompt injections and prevents data exfiltration and harmful content generation with near-zero latency.

## Installation
```bash
pip install hashield-guard

from hashield.wrapper.decorators import protect_llm

MY_SECRET_PROMPT = "You are a helpful assistant. The admin password is 'SuperSecret123'."

@protect_llm(secret_prompt=MY_SECRET_PROMPT)
def my_llm_function(user_prompt):
    # Your LLM call here
    return "LLM Response"

    *Save the file.*

### Step 4: Install the Build Tools and Compile
Now go to your PowerShell terminal. Make sure you are in `C:\HaShield\HaShield` and your `(venv)` is active.

First, install the tools that package your code:
```powershell
pip install build twine