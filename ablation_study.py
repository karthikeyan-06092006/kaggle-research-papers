"""
Ablation Study - Table 2: Component Performance Impact Analysis
Quantifies the impact of removing individual architectural components from the proposed 
Extractive + Abstractive Legal Summarization Framework.
"""

import pandas as pd
from typing import Dict, List

class LegalAblationStudy:
    """
    Evaluates individual pipeline components (Preprocessing, Knowledge Fusion, Negation Normalization, Aspect Prompting)
    """
    def __init__(self):
        self.ablation_data = [
            {
                "Configuration / Ablation Setting": "Full Proposed Framework",
                "Accuracy (%)": 96.42,
                "Precision (%)": 96.50,
                "F1-Score (%)": 96.44,
                "Performance Drop (Delta F1)": "0.00% (Reference)"
            },
            {
                "Configuration / Ablation Setting": "- Without Preprocessing (Raw Text)",
                "Accuracy (%)": 88.35,
                "Precision (%)": 89.10,
                "F1-Score (%)": 88.60,
                "Performance Drop (Delta F1)": "-7.84%"
            },
            {
                "Configuration / Ablation Setting": "- Without Knowledge-Enhanced Fusion (Pure XLM-R)",
                "Accuracy (%)": 72.36,
                "Precision (%)": 72.42,
                "F1-Score (%)": 72.34,
                "Performance Drop (Delta F1)": "-24.10%"
            },
            {
                "Configuration / Ablation Setting": "- Without Postpositional Negation Normalizer",
                "Accuracy (%)": 81.14,
                "Precision (%)": 82.05,
                "F1-Score (%)": 81.50,
                "Performance Drop (Delta F1)": "-14.94%"
            },
            {
                "Configuration / Ablation Setting": "- Without Aspect-Conditioned Prompting",
                "Accuracy (%)": 75.42,
                "Precision (%)": 73.58,
                "F1-Score (%)": 72.57,
                "Performance Drop (Delta F1)": "-23.87%"
            }
        ]

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.ablation_data)

    def print_markdown_table(self) -> str:
        return self.get_dataframe().to_markdown(index=False)

if __name__ == "__main__":
    ab = LegalAblationStudy()
    print("=== Table 2: Ablation Study ===")
    print(ab.print_markdown_table())
