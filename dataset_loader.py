"""
Dataset Loader for Indian Legal Datasets: ILDC and IL-TUR
Supports Hugging Face Hub loading with graceful offline mode and synthetic benchmark generation.
"""

import os
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_iltur_dataset(task_name: str = "cjpe", split: Optional[str] = None):
    """
    Loads IL-TUR or ILDC dataset from Hugging Face.
    Dataset path: Exploration-Lab/IL-TUR or Exploration-Lab/ILDC
    
    Usage as requested:
      from datasets import load_dataset
      dataset = load_dataset("Exploration-Lab/IL-TUR", "<task_name>", revision="script")
    """
    try:
        from datasets import load_dataset
        logger.info(f"Attempting to load 'Exploration-Lab/IL-TUR' for task '{task_name}'...")
        dataset = load_dataset("Exploration-Lab/IL-TUR", task_name, revision="script")
        if split and split in dataset:
            return dataset[split]
        return dataset
    except Exception as e:
        logger.warning(f"Could not load dataset directly from Hugging Face online: {e}")
        logger.info("Falling back to synthetic benchmark generator for local validation...")
        return generate_mock_legal_dataset()

def generate_mock_legal_dataset(num_samples: int = 100):
    """
    Generates synthetic Indian Court Judgement samples mimicking ILDC / IL-TUR corpus structure.
    Useful for local pipeline testing without downloading gigabytes of text.
    """
    import random
    
    legal_statutes = ["Section 302 IPC", "Article 21 Constitution", "Section 138 NI Act", "Section 482 CrPC", "Order 39 CPC"]
    legal_outcomes = [0, 1] # 0: Dismissed/Acquitted, 1: Allowed/Convicted
    
    mock_data = []
    for i in range(num_samples):
        statute = random.choice(legal_statutes)
        outcome = random.choice(legal_outcomes)
        
        # High-court / Supreme court judgment text structure
        text = (
            f"IN THE SUPREME COURT OF INDIA. PETITIONER: Appellant_{i} VS RESPONDENT: State of India.\n"
            f"JUDGMENT: The present appeal arises out of the final order passed by the High Court under {statute}. "
            f"The prosecution alleged that the accused was involved in unlawful acts contrary to statutory provisions. "
            f"The learned trial judge evaluated the witness testimonies and circumstantial evidence. "
            f"Having considered the arguments of both senior counsels and the precedent set in landmark authorities, "
            f"this court holds that the prosecution {'failed to prove' if outcome==0 else 'established beyond reasonable doubt'} the charges. "
            f"The appeal is hereby {'dismissed with costs' if outcome==0 else 'allowed and conviction upheld'}."
        )
        
        summary = (
            f"Supreme Court ruling on {statute}. Key issue: evidentiary burden and statutory compliance. "
            f"Decision: Appeal {'dismissed' if outcome==0 else 'allowed'}. Counsel arguments evaluated against precedents."
        )
        
        mock_data.append({
            "id": f"legal_doc_{i:04d}",
            "text": text,
            "summary": summary,
            "label": outcome,
            "aspect": statute
        })
        
    return mock_data

if __name__ == "__main__":
    ds = load_iltur_dataset()
    logger.info(f"Loaded dataset sample count: {len(ds)}")
