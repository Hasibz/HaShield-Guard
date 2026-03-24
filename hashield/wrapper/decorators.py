from functools import wraps
from hashield.core.zero_shot import HaShieldCore

# Initialize the global engine instance with our newly tuned thresholds
guard = HaShieldCore(input_threshold=0.65, output_threshold=0.70)

def protect_llm(secret_prompt=""):
    """
    A decorator that wraps around an LLM API call.
    It automatically scans the input before sending, and the output before returning.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(prompt, *args, **kwargs):
            
            # --- 1. INPUT LAYER (Pre-flight check) ---
            input_scan = guard.scan_input(prompt)
            if input_scan["status"] == "BLOCKED":
                print(f"[HaShield Blocked Input] {input_scan['reason']} (Score: {input_scan['score']})")
                return "HaShield Alert: Malicious prompt injection blocked."
            
            # --- 2. EXECUTE THE LLM ---
            # If the input is safe, we actually run the developer's function
            llm_response = func(prompt, *args, **kwargs)
            
            # --- 3. OUTPUT LAYER (Post-flight check) ---
            if secret_prompt:
                output_scan = guard.scan_output(llm_response, secret_prompt)
                if output_scan["status"] == "BLOCKED":
                    print(f"[HaShield Blocked Output] {output_scan['reason']} (Score: {output_scan['score']})")
                    return "HaShield Alert: Data exfiltration prevented."
            
            return llm_response
        return wrapper
    return decorator