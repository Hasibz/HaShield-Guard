from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
import re
from .vector_math import calculate_cosine_similarity

class HaShieldCore:
    def __init__(self, input_threshold: float = 0.65, output_threshold: float = 0.70): 
        print("[HaShield] Booting Enterprise Mathematical Engines...")
        
        self.model = SentenceTransformer('all-mpnet-base-v2')
        
        self.intent_classifier = pipeline(
            "zero-shot-classification", 
            model="typeform/distilbert-base-uncased-mnli",
            device=-1  
        )
        
        self.input_threshold = input_threshold
        self.output_threshold = output_threshold
        
        # We now have two distinct threat categories
        self.injection_labels = ["system override", "ignore previous instructions", "malicious roleplay"]
        self.safety_labels = ["illegal instructions", "drug synthesis", "harmful content", "violence or weapons"]
            
        print(f"[HaShield] Engine Ready. Input Threshold: {self.input_threshold} | Output Threshold: {self.output_threshold}\n")

    def _analyze_intent(self, text: str, labels: list, threshold: float, threat_type: str) -> dict:
        """Helper function to run the NLI math efficiently."""
        # Truncate text to avoid crashing the model on massive outputs
        truncated_text = text[:1500] 
        
        result = self.intent_classifier(
            truncated_text, 
            candidate_labels=labels + ["benign", "safe conversation", "educational"],
            multi_label=False
        )
        
        highest_score = 0.0
        for label, score in zip(result['labels'], result['scores']):
            if label in labels and score > highest_score:
                highest_score = score

        if highest_score >= threshold:
            return {"status": "BLOCKED", "score": round(float(highest_score), 3), "reason": f"AUP Violation: Detected {threat_type}."}
        
        return {"status": "SAFE"}

    def scan_input(self, prompt: str) -> dict:
        """Dual-scan for both Injections and Safety Violations."""
        
        # 1. Check for Prompt Injections
        injection_check = self._analyze_intent(prompt, self.injection_labels, self.input_threshold, "Prompt Injection")
        if injection_check["status"] == "BLOCKED":
            return injection_check
            
        # 2. Check for Harmful Intent (Safety)
        safety_check = self._analyze_intent(prompt, self.safety_labels, self.input_threshold, "Harmful Request")
        if safety_check["status"] == "BLOCKED":
            return safety_check
        
        return {"status": "SAFE", "score": 0.0, "prompt": prompt}

    def scan_output(self, llm_response: str, protected_system_prompt: str) -> dict:
        """Tri-scan for API Keys, Data Leaks, and Harmful Generation."""
        
        # 1. Hardcoded API Key Check
        if re.search(r"(sk-[a-zA-Z0-9]{32,})", llm_response):
            return {"status": "BLOCKED", "score": 1.0, "reason": "Data Exfiltration: API Key detected."}

        # 2. Data Exfiltration Check (Cosine Similarity)
        response_vector = self.model.encode(llm_response)
        system_vector = self.model.encode(protected_system_prompt)
        leak_score = calculate_cosine_similarity(response_vector, system_vector)
        
        if leak_score >= self.output_threshold:
            return {"status": "BLOCKED", "score": round(float(leak_score), 3), "reason": "Data Exfiltration: Matches protected instructions."}
            
        # 3. Trust & Safety Check (Did the LLM generate a recipe for something illegal?)
        # We use a slightly higher threshold (0.75) for output to reduce false positives on educational answers
        safety_check = self._analyze_intent(llm_response, self.safety_labels, 0.75, "Harmful/Illegal Output Generation")
        if safety_check["status"] == "BLOCKED":
            return safety_check
        
        return {"status": "SAFE", "score": round(float(leak_score), 3), "response": llm_response}
    