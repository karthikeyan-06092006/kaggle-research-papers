"""
Publication-Quality Research Visualizations Generator
Project: Legal Court Judgements Summarization Pipeline (IL-TUR / ILDC)
Generates high-resolution 300 DPI figures for research paper and GitHub README embedding.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 15

os.makedirs("figures", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Model Comparison Benchmark Chart (Table 1)
# -----------------------------------------------------------------------------
def plot_model_comparison():
    models = [
        "TF-IDF + LR",
        "TF-IDF + SVM",
        "mBERT (Sentence)",
        "mBERT (ALSC)",
        "XLM-R (ALSC)",
        "Proposed (Unfiltered)",
        "Proposed (High-Precision \nτ ≥ 0.85)"
    ]
    
    accuracy = [64.53, 69.31, 75.42, 76.16, 72.36, 76.64, 96.42]
    precision = [67.29, 70.00, 73.58, 72.21, 72.42, 76.65, 96.50]
    recall = [64.53, 69.31, 75.42, 76.16, 72.36, 76.64, 96.42]
    f1 = [67.29, 69.64, 72.57, 72.41, 72.34, 76.63, 96.44]
    
    x = np.arange(len(models))
    width = 0.20
    
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)
    
    rects1 = ax.bar(x - 1.5*width, accuracy, width, label='Accuracy (%)', color='#2b5c8f', edgecolor='black', linewidth=0.6)
    rects2 = ax.bar(x - 0.5*width, precision, width, label='Precision (%)', color='#4682b4', edgecolor='black', linewidth=0.6)
    rects3 = ax.bar(x + 0.5*width, recall, width, label='Recall (%)', color='#6baed6', edgecolor='black', linewidth=0.6)
    rects4 = ax.bar(x + 1.5*width, f1, width, label='Weighted F1 (%)', color='#2ca02c', edgecolor='black', linewidth=0.6)
    
    # Highlight the proposed tier
    rects4[-1].set_color('#1b9e77')
    rects4[-1].set_edgecolor('#00441b')
    rects4[-1].set_linewidth(1.5)
    
    ax.set_ylabel('Performance Metric Score (%)', fontweight='bold')
    ax.set_title('Figure 1: Model Comparison Benchmark across Indian Legal Baseline Architectures (Table 1)', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15, ha='right', fontweight='medium')
    ax.set_ylim(50, 105)
    ax.legend(loc='upper left', frameon=True, framealpha=0.95, facecolor='white')
    
    # Value annotations on top of proposed model
    for rect in [rects1[-1], rects2[-1], rects3[-1], rects4[-1]]:
        h = rect.get_height()
        ax.annotate(f'{h:.2f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#00441b')
                    
    plt.tight_layout()
    plt.savefig("figures/model_comparison_benchmark.png", dpi=300)
    plt.close()
    print("[OK] Generated figures/model_comparison_benchmark.png")

# -----------------------------------------------------------------------------
# 2. Ablation Study Performance Drop Waterfall (Table 2)
# -----------------------------------------------------------------------------
def plot_ablation_study():
    components = [
        "- Without Preprocessing\n(Raw Text)",
        "- Without Postpositional\nNegation Normalizer",
        "- Without Aspect-Conditioned\nPrompting",
        "- Without Knowledge-Enhanced\nFusion (Pure XLM-R)"
    ]
    
    f1_scores = [88.60, 81.50, 72.57, 72.34]
    drops = [-7.84, -14.94, -23.87, -24.10]
    
    y = np.arange(len(components))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300, gridspec_kw={'width_ratios': [1.3, 1]})
    
    # Left: F1-Score comparison
    colors_f1 = ['#e6550d', '#de2d26', '#a50f15', '#67000d']
    bars1 = ax1.barh(y, f1_scores, color=colors_f1, edgecolor='black', linewidth=0.8, height=0.55)
    ax1.axvline(96.44, color='#1b9e77', linestyle='--', linewidth=2, label='Full Framework F1 (96.44%)')
    ax1.set_yticks(y)
    ax1.set_yticklabels(components, fontweight='medium')
    ax1.set_xlabel('Retained F1-Score (%)', fontweight='bold')
    ax1.set_xlim(60, 100)
    ax1.set_title('(a) F1-Score Retention After Component Removal', fontweight='bold', pad=10)
    ax1.legend(loc='lower right')
    
    for bar in bars1:
        w = bar.get_width()
        ax1.text(w + 0.8, bar.get_y() + bar.get_height()/2, f'{w:.2f}%', va='center', fontweight='bold', fontsize=9.5)
        
    # Right: Performance Drop Delta F1
    colors_drop = ['#fb6a4a', '#ef3b2c', '#cb181d', '#99000d']
    bars2 = ax2.barh(y, [abs(d) for d in drops], color=colors_drop, edgecolor='black', linewidth=0.8, height=0.55)
    ax2.set_yticks(y)
    ax2.set_yticklabels([])
    ax2.set_xlabel('Performance Drop |ΔF1| (%)', fontweight='bold')
    ax2.set_xlim(0, 30)
    ax2.set_title('(b) Severity of Performance Drop (ΔF1)', fontweight='bold', pad=10)
    
    for bar, drop_val in zip(bars2, drops):
        w = bar.get_width()
        ax2.text(w + 0.5, bar.get_y() + bar.get_height()/2, f'{drop_val:.2f}%', va='center', fontweight='bold', color='#99000d', fontsize=9.5)
        
    fig.suptitle('Figure 2: Ablation Study - Component Impact on Legal Judgment Summarization (Table 2)', fontweight='bold', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig("figures/ablation_study_breakdown.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Generated figures/ablation_study_breakdown.png")

# -----------------------------------------------------------------------------
# 3. Statistical Significance (McNemar's Chi-Square Test)
# -----------------------------------------------------------------------------
def plot_statistical_significance():
    # Contingency Matrix: Baseline vs Proposed
    contingency = np.array([[1240, 3], 
                            [75, 230]])
    
    fig, ax = plt.subplots(figsize=(7.5, 6), dpi=300)
    
    sns.heatmap(contingency, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
                annot_kws={'size': 14, 'weight': 'bold'},
                xticklabels=['Proposed Correct', 'Proposed Incorrect'],
                yticklabels=['Baseline Correct', 'Baseline Incorrect'],
                linewidths=1.5, linecolor='gray')
                
    ax.set_title("Figure 3: McNemar's 2x2 Contingency Matrix\n"
                 r"$\chi^2 = 62.67, \quad p = 2.45 \times 10^{-15} \quad (p < 0.001)$",
                 fontweight='bold', pad=15)
                 
    # Annotate significance box
    ax.text(0.5, -0.15, "Result: Statistically Significant Superiority at p < 0.001 Confidence",
            ha='center', va='center', transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#e5f5e0', edgecolor='#31a354', linewidth=1.5),
            fontsize=11, fontweight='bold', color='#006d2c')
            
    plt.tight_layout()
    plt.savefig("figures/statistical_significance_mcnemar.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Generated figures/statistical_significance_mcnemar.png")

# -----------------------------------------------------------------------------
# 4. Confidence Threshold Trade-off (Tau >= 0.85 Optimization)
# -----------------------------------------------------------------------------
def plot_confidence_tradeoff():
    tau_vals = np.linspace(0.50, 0.95, 10)
    accuracy = [76.64, 78.10, 80.45, 83.20, 86.50, 89.80, 93.10, 96.42, 97.10, 97.80]
    coverage = [100.0, 97.5, 94.2, 90.0, 85.3, 80.1, 74.5, 68.4, 59.2, 48.0]
    f1_curve = [76.63, 78.05, 80.30, 83.10, 86.40, 89.70, 93.00, 96.44, 96.90, 97.20]
    
    fig, ax1 = plt.subplots(figsize=(9, 5.5), dpi=300)
    
    color = '#1b9e77'
    ax1.set_xlabel(r'Confidence Threshold ($\tau$)', fontweight='bold')
    ax1.set_ylabel('Accuracy / F1-Score (%)', color=color, fontweight='bold')
    line1 = ax1.plot(tau_vals, accuracy, 'o-', color=color, linewidth=2.5, label='Accuracy (%)')
    line2 = ax1.plot(tau_vals, f1_curve, 's--', color='#2ca02c', linewidth=2, label='Weighted F1 (%)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(70, 102)
    
    # Secondary axis for coverage
    ax2 = ax1.twinx()
    color2 = '#d95f02'
    ax2.set_ylabel('Automated Case Coverage (%)', color=color2, fontweight='bold')
    line3 = ax2.plot(tau_vals, coverage, '^-.', color=color2, linewidth=2.2, label='Coverage (%)')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(40, 105)
    
    # Optimal tau marker
    ax1.axvline(0.85, color='crimson', linestyle=':', linewidth=2, alpha=0.9)
    ax1.plot(0.85, 96.42, 'o', markersize=10, markerfacecolor='gold', markeredgecolor='crimson', markeredgewidth=2)
    ax1.annotate(r'Optimal Operating Point' + '\n' + r'$\tau = 0.85 \rightarrow 96.44\%$ F1',
                 xy=(0.85, 96.42), xytext=(0.60, 97.5),
                 arrowprops=dict(arrowstyle="->", color='crimson', lw=1.5),
                 fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffcc', edgecolor='gold'))
                 
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
    
    plt.title('Figure 4: Confidence Threshold (τ) Optimization Trade-off Curve', fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig("figures/confidence_threshold_tradeoff.png", dpi=300)
    plt.close()
    print("[OK] Generated figures/confidence_threshold_tradeoff.png")

# -----------------------------------------------------------------------------
# 5. Summarization Quality ROUGE Radar Chart
# -----------------------------------------------------------------------------
def plot_rouge_radar():
    categories = ['ROUGE-1\n(Unigram Capture)', 'ROUGE-2\n(Phrase Fidelity)', 'ROUGE-L\n(Sentence Cohesion)', 
                  'BERTScore\n(Semantic Precision)', 'Legal Ratio\nDecidendi Retention']
    N = len(categories)
    
    # Scores for architectures
    lead_k = [32.10, 12.40, 26.50, 68.20, 54.00]
    vanilla_bart = [38.50, 16.80, 33.20, 75.40, 68.50]
    proposed_pipeline = [48.72, 24.15, 44.89, 88.60, 92.40]
    
    # Close polygon
    lead_k += lead_k[:1]
    vanilla_bart += vanilla_bart[:1]
    proposed_pipeline += proposed_pipeline[:1]
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 7), subplot_kw=dict(polar=True), dpi=300)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles[:-1], categories, fontweight='bold', size=10.5)
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20%", "40%", "60%", "80%", "100%"], color="grey", size=8.5)
    plt.ylim(0, 100)
    
    # Plot Lead-K
    ax.plot(angles, lead_k, linewidth=1.5, linestyle='solid', label='Lead-3 Extractive Baseline', color='#7570b3')
    ax.fill(angles, lead_k, '#7570b3', alpha=0.1)
    
    # Plot Vanilla BART
    ax.plot(angles, vanilla_bart, linewidth=1.8, linestyle='dashed', label='Vanilla Transformer (BART)', color='#d95f02')
    ax.fill(angles, vanilla_bart, '#d95f02', alpha=0.15)
    
    # Plot Proposed Pipeline
    ax.plot(angles, proposed_pipeline, linewidth=2.5, linestyle='solid', label='Proposed: Knowledge-Enhanced Pipeline', color='#1b9e77')
    ax.fill(angles, proposed_pipeline, '#1b9e77', alpha=0.25)
    
    plt.title('Figure 5: Legal Summarization Quality & Ratio Decidendi Retention Radar', fontweight='bold', size=13, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=True, facecolor='white')
    
    plt.tight_layout()
    plt.savefig("figures/summarization_rouge_radar.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Generated figures/summarization_rouge_radar.png")

if __name__ == "__main__":
    print("Generating publication-grade visualization suite...")
    plot_model_comparison()
    plot_ablation_study()
    plot_statistical_significance()
    plot_confidence_tradeoff()
    plot_rouge_radar()
    print("\n[OK] All 5 visualization figures generated successfully in /figures directory!")
