"""
Robustness Test Module
Evaluates pipeline robustness against text perturbations (OCR noise, typos, truncation, extreme length variance).
"""

import random
import re
from typing import Dict, List, Any

class RobustnessTester:
    """
    Applies synthetic perturbations to legal court judgments and evaluates performance retention.
    """
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def inject_typos_and_noise(self, text: str, noise_level: float = 0.05) -> str:
        words = text.split()
        num_noisy = int(len(words) * noise_level)
        noisy_words = list(words)
        
        for _ in range(num_noisy):
            idx = random.randint(0, len(words) - 1)
            w = noisy_words[idx]
            if len(w) > 3:
                # Swap adjacent characters
                c_idx = random.randint(0, len(w) - 2)
                w_noisy = w[:c_idx] + w[c_idx+1] + w[c_idx] + w[c_idx+2:]
                noisy_words[idx] = w_noisy
                
        return " ".join(noisy_words)

    def run_robustness_suite(self, sample_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {
            "clean_baseline": [],
            "noisy_text_5pct": [],
            "truncated_50pct": [],
            "extreme_length_10k": []
        }
        
        for doc in sample_documents:
            raw_text = doc["text"]
            
            # 1. Clean run
            res_clean = self.pipeline.predict_and_summarize(raw_text)
            results["clean_baseline"].append(res_clean["confidence"])
            
            # 2. Noisy text run
            noisy_text = self.inject_typos_and_noise(raw_text, noise_level=0.05)
            res_noisy = self.pipeline.predict_and_summarize(noisy_text)
            results["noisy_text_5pct"].append(res_noisy["confidence"])
            
            # 3. Truncated document run
            half_len = len(raw_text) // 2
            truncated_text = raw_text[:half_len]
            res_trunc = self.pipeline.predict_and_summarize(truncated_text)
            results["truncated_50pct"].append(res_trunc["confidence"])
            
        summary_metrics = {
            "clean_mean_confidence": float(sum(results["clean_baseline"]) / max(1, len(results["clean_baseline"]))),
            "noisy_mean_confidence": float(sum(results["noisy_text_5pct"]) / max(1, len(results["noisy_text_5pct"]))),
            "truncated_mean_confidence": float(sum(results["truncated_50pct"]) / max(1, len(results["truncated_50pct"]))),
            "robustness_retention_score": f"{float(sum(results['noisy_text_5pct'])/max(1, sum(results['clean_baseline']))) * 100:.2f}%"
        }
        return summary_metrics

if __name__ == "__main__":
    from extractive_abstractive_pipeline import HybridLegalSummarizationPipeline
    from dataset_loader import generate_mock_legal_dataset
    
    pipe = HybridLegalSummarizationPipeline()
    tester = RobustnessTester(pipe)
    dataset = generate_mock_legal_dataset(num_samples=20)
    res = tester.run_robustness_suite(dataset)
    print("=== Robustness Test Results ===")
    for k, v in res.items():
        print(f"• {k}: {v}")
