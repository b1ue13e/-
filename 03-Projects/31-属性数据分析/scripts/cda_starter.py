# -*- coding: utf-8 -*-
"""
CDA Course Starter Module & Algorithmic Foundations
Course: 31-属性数据分析 (Categorical Data Analysis)

This module provides from-scratch implementations of fundamental CDA algorithms:
1. Contingency Table Metrics (Chi2, Deviance G2, Odds Ratio, Woolf SE, 95% CI)
2. Iteratively Reweighted Least Squares (IRLS) Binary Logistic Regression Solver
3. Poisson GLM IRLS Solver & Overdispersion Diagnostic (Pearson phi)
4. Cochran-Mantel-Haenszel (CMH) Stratified Test & Pooled Odds Ratio
"""
import numpy as np
import scipy.stats as stats

def calculate_contingency_2x2_metrics(mat):
    """
    Calculate fundamental metrics for a 2x2 contingency table.
    mat: 2x2 numpy array [[a, b], [c, d]]
    Returns dict containing:
      - odds_ratio: (a*d) / (b*c)
      - ln_or: ln(odds_ratio)
      - woolf_se: sqrt(1/a + 1/b + 1/c + 1/d)
      - ci_95: (exp(ln_or - 1.96*se), exp(ln_or + 1.96*se))
      - pearson_chi2: sum((O - E)^2 / E)
      - deviance_g2: 2 * sum(O * ln(O / E))
      - p_value_chi2: p-value of Pearson Chi2 (dof=1)
    """
    mat = np.asarray(mat, dtype=float)
    if mat.shape != (2, 2):
        raise ValueError("Input matrix must be 2x2.")
    
    a, b = mat[0, 0], mat[0, 1]
    c, d = mat[1, 0], mat[1, 1]
    
    n = np.sum(mat)
    row_sums = np.sum(mat, axis=1)
    col_sums = np.sum(mat, axis=0)
    expected = np.outer(row_sums, col_sums) / n
    
    # 1. Odds Ratio & Woolf SE
    or_val = (a * d) / (b * c)
    ln_or = np.log(or_val)
    woolf_se = np.sqrt(1.0/a + 1.0/b + 1.0/c + 1.0/d)
    ci_lower = np.exp(ln_or - 1.96 * woolf_se)
    ci_upper = np.exp(ln_or + 1.96 * woolf_se)
    
    # 2. Pearson Chi2
    pearson_chi2 = np.sum((mat - expected)**2 / expected)
    p_val_chi2 = 1.0 - stats.chi2.cdf(pearson_chi2, df=1)
    
    # 3. Deviance G2 (Likelihood Ratio Chi2)
    with np.errstate(divide='ignore', invalid='ignore'):
        terms = np.where(mat > 0, mat * np.log(mat / expected), 0.0)
    deviance_g2 = 2.0 * np.sum(terms)
    
    return {
        "odds_ratio": float(or_val),
        "ln_or": float(ln_or),
        "woolf_se": float(woolf_se),
        "ci_95": (float(ci_lower), float(ci_upper)),
        "pearson_chi2": float(pearson_chi2),
        "deviance_g2": float(deviance_g2),
        "p_value_chi2": float(p_val_chi2)
    }

def fit_logistic_irls(X, y, max_iter=30, tol=1e-8):
    """
    Fit Binary Logistic Regression using from-scratch Iteratively Reweighted Least Squares (IRLS / Fisher Scoring).
    
    Model: P(Y=1|X) = pi = 1 / (1 + exp(-X @ beta))
    Update: beta^{(t+1)} = (X^T W X)^{-1} X^T W z
            where W = diag(pi * (1 - pi)), z = eta + (y - pi) / (pi * (1 - pi))
            
    X: ndarray of shape (N, P)
    y: ndarray of shape (N,) with 0 or 1
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, p = X.shape
    
    beta = np.zeros(p)
    converged = False
    
    for it in range(max_iter):
        eta = X @ beta
        eta_bounded = np.clip(eta, -30.0, 30.0)
        pi = 1.0 / (1.0 + np.exp(-eta_bounded))
        
        w = pi * (1.0 - pi)
        w = np.maximum(w, 1e-10)
        
        W = np.diag(w)
        z = eta + (y - pi) / w
        
        XtWX = X.T @ W @ X
        try:
            cov_mat = np.linalg.inv(XtWX)
        except np.linalg.LinAlgError:
            cov_mat = np.linalg.pinv(XtWX)
            
        beta_new = cov_mat @ (X.T @ W @ z)
        
        diff = np.max(np.abs(beta_new - beta))
        beta = beta_new
        
        if diff < tol:
            converged = True
            break
            
    eta_final = np.clip(X @ beta, -30.0, 30.0)
    pi_final = 1.0 / (1.0 + np.exp(-eta_final))
    
    eps = 1e-12
    ll = np.sum(y * np.log(pi_final + eps) + (1.0 - y) * np.log(1.0 - pi_final + eps))
    deviance = -2.0 * ll
    se_beta = np.sqrt(np.diag(cov_mat))
    
    return {
        "beta": beta,
        "cov_matrix": cov_mat,
        "se_beta": se_beta,
        "log_likelihood": float(ll),
        "deviance": float(deviance),
        "iterations": it + 1,
        "converged": converged
    }

def fit_poisson_irls(X, y, exposure=None, max_iter=30, tol=1e-8):
    """
    Fit Poisson Rate Regression via from-scratch IRLS.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, p = X.shape
    
    if exposure is None:
        log_t = np.zeros(n)
    else:
        log_t = np.log(np.asarray(exposure, dtype=float))
        
    beta = np.zeros(p)
    converged = False
    
    for it in range(max_iter):
        eta = log_t + X @ beta
        eta_bounded = np.clip(eta, -30.0, 30.0)
        mu = np.exp(eta_bounded)
        mu = np.maximum(mu, 1e-10)
        
        W = np.diag(mu)
        z = (eta - log_t) + (y - mu) / mu
        
        XtWX = X.T @ W @ X
        try:
            cov_mat = np.linalg.inv(XtWX)
        except np.linalg.LinAlgError:
            cov_mat = np.linalg.pinv(XtWX)
            
        beta_new = cov_mat @ (X.T @ (y - mu)) + beta
        diff = np.max(np.abs(beta_new - beta))
        beta = beta_new
        
        if diff < tol:
            converged = True
            break
            
    eta_final = np.clip(log_t + X @ beta, -30.0, 30.0)
    mu_final = np.exp(eta_final)
    
    pearson_chi2 = np.sum((y - mu_final)**2 / mu_final)
    df_resid = n - p
    phi_hat = pearson_chi2 / df_resid if df_resid > 0 else np.nan
    
    with np.errstate(divide='ignore', invalid='ignore'):
        dev_terms = np.where(y > 0, y * np.log(y / mu_final) - (y - mu_final), mu_final)
    deviance = 2.0 * np.sum(dev_terms)
    
    return {
        "beta": beta,
        "cov_matrix": cov_mat,
        "se_beta": np.sqrt(np.diag(cov_mat)),
        "deviance": float(deviance),
        "pearson_chi2": float(pearson_chi2),
        "phi_hat": float(phi_hat),
        "iterations": it + 1,
        "converged": converged
    }

def calculate_cmh_stat(tables_k):
    """
    Calculate Cochran-Mantel-Haenszel (CMH) Test Statistic & Pooled MH Odds Ratio across K strata.
    tables_k: numpy array of shape (K, 2, 2)
    """
    tables_k = np.asarray(tables_k, dtype=float)
    K = tables_k.shape[0]
    
    num_mh = 0.0
    den_mh = 0.0
    
    sum_a = 0.0
    sum_exp_a = 0.0
    var_a = 0.0
    
    for k in range(K):
        mat = tables_k[k]
        a, b = mat[0, 0], mat[0, 1]
        c, d = mat[1, 0], mat[1, 1]
        n_k = a + b + c + d
        
        r1 = a + b
        r2 = c + d
        c1 = a + c
        c2 = b + d
        
        num_mh += (a * d) / n_k
        den_mh += (b * c) / n_k
        
        exp_a = (r1 * c1) / n_k
        v_a = (r1 * r2 * c1 * c2) / (n_k**2 * (n_k - 1.0)) if n_k > 1 else 0.0
        
        sum_a += a
        sum_exp_a += exp_a
        var_a += v_a
        
    mh_or = num_mh / den_mh if den_mh > 0 else np.nan
    cmh_stat = (abs(sum_a - sum_exp_a) - 0.5)**2 / var_a if var_a > 0 else 0.0
    p_value = 1.0 - stats.chi2.cdf(cmh_stat, df=1)
    
    return {
        "pooled_mh_or": float(mh_or),
        "cmh_stat": float(cmh_stat),
        "p_value": float(p_value)
    }
