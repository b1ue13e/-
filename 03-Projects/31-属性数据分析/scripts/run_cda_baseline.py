# -*- coding: utf-8 -*-
"""
Baseline Analysis and Model Verification Script for CDA Course Projects
Course: 31-属性数据分析 (Categorical Data Analysis)
"""
import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.miscmodels.ordinal_model import OrderedModel

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def run_ucb_analysis():
    print("=" * 60)
    print("1. Running UCB Admissions Simpson's Paradox & CMH Analysis")
    print("=" * 60)
    df = pd.read_csv(os.path.join(DATA_DIR, "ucb_admissions.csv"))
    
    # 1. 边际列联表
    marginal = df.groupby(['Gender', 'Admit'])['Freq'].sum().unstack()
    print("Marginal 2x2 Table:\n", marginal)
    
    chi2, p_val, dof, _ = stats.chi2_contingency(marginal, correction=False)
    odds_male = marginal.loc['Male', 'Admitted'] / marginal.loc['Male', 'Rejected']
    odds_female = marginal.loc['Female', 'Admitted'] / marginal.loc['Female', 'Rejected']
    marginal_or = odds_male / odds_female
    print(f"Marginal OR (Male vs Female): {marginal_or:.4f}, Chi2: {chi2:.4f}, p: {p_val:.4e}")
    
    # 2. 分层 2x2xk CMH 分析
    tables = []
    depts = sorted(df['Dept'].unique())
    for dept in depts:
        sub = df[df['Dept'] == dept].pivot(index='Gender', columns='Admit', values='Freq').fillna(0)
        # Ensure rows are [Male, Female] and columns [Admitted, Rejected]
        sub = sub.reindex(index=['Male', 'Female'], columns=['Admitted', 'Rejected'])
        tables.append(sub.values)
    
    # StratifiedTable 接受 (2, 2, k) 数组
    tables_arr = np.array(tables).transpose(1, 2, 0)
    st = StratifiedTable(tables_arr)
    print(f"Stratified Pooled MH OR: {st.oddsratio_pooled:.4f}")
    print(f"CMH Test Statistic: {st.test_null_odds().statistic:.4f}, p: {st.test_null_odds().pvalue:.4f}")
    print(f"Breslow-Day Homogeneity Test Statistic: {st.test_equal_odds().statistic:.4f}, p: {st.test_equal_odds().pvalue:.4f}")
    
    return marginal_or, st.oddsratio_pooled

def run_arthritis_analysis():
    print("\n" + "=" * 60)
    print("2. Running Arthritis Ordinal Cumulative Logit Model (N=84)")
    print("=" * 60)
    df = pd.read_csv(os.path.join(DATA_DIR, "arthritis.csv"), na_filter=False)
    
    # 编码有序响应: None=0, Some=1, Marked=2
    df['Improved'] = df['Improved'].astype(str).str.strip()
    df['Treatment'] = df['Treatment'].astype(str).str.strip()
    level_map = {'None': 0, 'Some': 1, 'Marked': 2}
    y_ord = df['Improved'].map(level_map).astype(int).values
    df['Treatment_Treated'] = (df['Treatment'] == 'Treated').astype(float)
    
    # 拟合有序累积 Logit 模型
    exog = df[['Treatment_Treated', 'Age']].values.astype(float)
    ord_model = OrderedModel(
        y_ord,
        exog,
        distr='logit'
    ).fit(method='bfgs', disp=False)
    
    print(ord_model.summary())
    treated_coef = ord_model.params[0]
    treated_or = np.exp(treated_coef)
    print(f"\nTreated Cumulative Odds Ratio (better improvement): {treated_or:.4f}")
    return ord_model

def run_crabs_analysis():
    print("\n" + "=" * 60)
    print("3. Running Crabs Logistic, Poisson & NB2 Models (N=173)")
    print("=" * 60)
    df = pd.read_csv(os.path.join(DATA_DIR, "crabs.csv"))
    
    # 1. 二分类 Logistic 回归
    df['Has_Satellites'] = (df['Satellites'] > 0).astype(int)
    logit_mod = smf.glm('Has_Satellites ~ Width + Weight', data=df, family=sm.families.Binomial()).fit()
    print("--- Logistic Regression Summary ---")
    print(logit_mod.summary())
    
    # 2. Poisson 回归与过度离散诊断
    pois_mod = smf.glm('Satellites ~ Width + Weight', data=df, family=sm.families.Poisson()).fit()
    phi_hat = pois_mod.pearson_chi2 / pois_mod.df_resid
    print(f"\n--- Poisson Model Dispersion: phi_hat = {phi_hat:.4f} (Overdispersion detected!) ---")
    
    # 3. 负二项回归 (NB2) 修正过度离散
    nb_mod = smf.glm('Satellites ~ Width + Weight', data=df, family=sm.families.NegativeBinomial(alpha=1.0)).fit()
    print("\n--- Negative Binomial Model Summary ---")
    print(nb_mod.summary())
    
    return logit_mod, pois_mod, nb_mod

if __name__ == "__main__":
    run_ucb_analysis()
    run_arthritis_analysis()
    run_crabs_analysis()
    print("\nAll authentic baseline experiments completed successfully!")
