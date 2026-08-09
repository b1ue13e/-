# -*- coding: utf-8 -*-
"""
CDA Course Visualizer & Intuition Tool
Course: 31-属性数据分析 (Categorical Data Analysis)

Generates visual diagnostic charts for key CDA concepts:
1. Logit link function S-curve & Odds Ratio transformation
2. Poisson vs. Negative Binomial (NB2) probability mass comparison under Overdispersion
3. Complete Separation log-likelihood divergence vs. Firth Penalty
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def plot_logit_and_odds():
    """Plot Logit link function S-curve and Odds Ratio transformation."""
    pi = np.linspace(0.001, 0.999, 500)
    logit_pi = np.log(pi / (1.0 - pi))
    odds = pi / (1.0 - pi)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 1. Logit S-curve
    ax1.plot(logit_pi, pi, 'b-', linewidth=2, label=r'$\pi = \frac{e^\eta}{1 + e^\eta}$')
    ax1.axhline(0.5, color='gray', linestyle='--', alpha=0.7)
    ax1.axvline(0.0, color='gray', linestyle='--', alpha=0.7)
    ax1.set_title("Logit Link Function & Logistic Curve", fontsize=12)
    ax1.set_xlabel(r"Linear Predictor $\eta = X\beta$", fontsize=11)
    ax1.set_ylabel(r"Probability $\pi \in (0, 1)$", fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)
    
    # 2. Odds vs Probability
    ax2.plot(pi, odds, 'r-', linewidth=2, label=r'Odds = $\frac{\pi}{1 - \pi}$')
    ax2.set_title("Odds vs Probability Transformation", fontsize=12)
    ax2.set_xlabel(r"Probability $\pi$", fontsize=11)
    ax2.set_ylabel("Odds", fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=11)
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "logit_odds_intuition.png")
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"[Visualizer] Logit & Odds intuition chart saved to {output_path}")

def plot_overdispersion_comparison():
    """Plot Poisson vs Negative Binomial (NB2) PMF comparison."""
    mu = 5.0
    alpha = 0.5 # Overdispersion parameter
    k = 1.0 / alpha
    
    y = np.arange(0, 20)
    # Poisson PMF
    pmf_pois = stats.poisson.pmf(y, mu)
    
    # Negative Binomial PMF (n=k, p=k/(k+mu))
    p_nb = k / (k + mu)
    pmf_nb = stats.nbinom.pmf(y, k, p_nb)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.35
    ax.bar(y - width/2, pmf_pois, width=width, color='skyblue', label=f'Poisson (mu={mu}, var={mu})')
    ax.bar(y + width/2, pmf_nb, width=width, color='coral', label=f'Neg-Binomial (mu={mu}, var={mu + alpha*mu**2:.1f})')
    
    ax.set_title("Poisson vs. Negative Binomial (Overdispersion)", fontsize=12)
    ax.set_xlabel("Count Outcome Y", fontsize=11)
    ax.set_ylabel("Probability P(Y = y)", fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "overdispersion_comparison.png")
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"[Visualizer] Overdispersion chart saved to {output_path}")

if __name__ == "__main__":
    plot_logit_and_odds()
    plot_overdispersion_comparison()
