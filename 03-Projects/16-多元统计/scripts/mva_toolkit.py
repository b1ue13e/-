# -*- coding: utf-8 -*-
"""
Multivariate Analysis (MVA) Core Toolkit
Course: 16-多元统计

Comprehensive scientific and pedagogical toolkit for multivariate statistical analysis:
1. Distance & Distribution Diagnostics:
   - mahalanobis_distance (via Cholesky factorization & condition number checks)
   - mardia_test (multivariate skewness & kurtosis with small-sample corrections)
   - chi_square_qq_plot_data (Q-Q plot diagnostic)
2. Covariance Structure Tests:
   - box_m_test (equality of covariance matrices across groups)
   - bartlett_sphericity_test
   - kmo_test (Kaiser-Meyer-Olkin sampling adequacy)
   - ledoit_wolf_shrinkage (high-dimensional regularization for p > n)
3. Multivariate Hypothesis Testing:
   - hotelling_t2_one_sample (Cholesky-backed T^2 and exact F-transform)
   - hotelling_t2_two_sample (Pooled Cholesky T^2 and exact F-transform)
   - manova_fit (Wilks' Lambda, Pillai, Hotelling-Lawley, Roy's Root)
4. Dimensionality Reduction & Latent Variables:
   - pca_fit (SVD & correlation modes with Whitening transform)
   - varimax_rotation (closed-form iterative orthogonal rotation)
   - factor_analysis_fit (principal factor extraction + rotation)
   - mds_fit (classical metric MDS via double centering)
5. Classification & Clustering:
   - lda_fit (Fisher's LDA via Generalized Eigenvalue Problem eigh(Sb, Sw))
   - qda_fit (Quadratic Discriminant Analysis with Cholesky log-det)
   - gmm_em_fit (GMM EM algorithm with monotonic log-likelihood guarantee)
6. Association & Manifold Geometry:
   - cca_fit (Canonical Correlation Analysis)
   - correspondence_analysis_fit (Dual scaling on contingency tables)
"""

import warnings
import numpy as np
from scipy import stats, linalg


# ==========================================
# Helper: Numerical Safety & Whitening
# ==========================================

def _safe_solve_cov(cov: np.ndarray, B: np.ndarray, reg_factor: float = 1e-6):
    """
    Solve S^{-1} B robustly via Cholesky factorization,
    with condition number checking and automatic ridge regularization.
    cov: shape (p, p)
    B: shape (n_samples, p) or (p, k) or (p,)
    Returns:
    - sol: shape (p, k) where k is second dimension of B
    - cond_number: float
    """
    p = cov.shape[0]
    cond_number = float(np.linalg.cond(cov))
    
    if cond_number > 1e4 or np.isnan(cond_number):
        warnings.warn(
            f"[MVA Warning] Ill-conditioned covariance matrix (cond={cond_number:.2e}). "
            f"Applying ridge regularization lambda={reg_factor:.2e}.",
            RuntimeWarning
        )
        cov = cov + reg_factor * np.trace(cov) / p * np.eye(p)
        cond_number = float(np.linalg.cond(cov))
        
    B_arr = np.atleast_2d(B)
    if B_arr.shape[0] == p:
        target = B_arr
    elif B_arr.shape[1] == p:
        target = B_arr.T
    else:
        target = B_arr
        
    try:
        c, low = linalg.cho_factor(cov, lower=True)
        sol = linalg.cho_solve((c, low), target)
    except linalg.LinAlgError:
        inv_cov = np.linalg.pinv(cov)
        sol = inv_cov @ target
        
    return sol, cond_number


# ==========================================
# 1. Distance & Distribution Diagnostics
# ==========================================

def mahalanobis_distance(x: np.ndarray, mu: np.ndarray, cov: np.ndarray) -> np.ndarray:
    """
    Compute squared Mahalanobis distance D^2 = (x - mu)^T Sigma^{-1} (x - mu).
    Uses Cholesky factorization with condition number checking.
    """
    x = np.atleast_2d(x)
    diff = x - mu
    sol, _ = _safe_solve_cov(cov, diff)
    d2 = np.sum(diff * sol.T, axis=1)
    return d2 if d2.shape[0] > 1 else d2[0]


def mardia_test(X: np.ndarray):
    """
    Mardia's test for multivariate normality (skewness & kurtosis).
    Includes asymptotic Chi-square/Normal tests and small-sample corrections for n < 50.
    """
    n, p = X.shape
    mean = np.mean(X, axis=0)
    S = np.cov(X, rowvar=False, ddof=1)
    diff = X - mean
    
    sol, _ = _safe_solve_cov(S, diff)
    M = diff @ sol
    
    b1_p = np.sum(M ** 3) / (n ** 2)
    df_skew = p * (p + 1) * (p + 2) // 6
    
    k_factor = (p + 1) * (n + 1) * (n + 3) / (n * ((n + 1) * (p + 1) - 6))
    skew_stat = (n * b1_p) / 6.0
    skew_stat_small = (n * k_factor * b1_p) / 6.0
    p_skew = 1.0 - stats.chi2.cdf(skew_stat, df_skew)
    
    b2_p = np.sum(np.diag(M) ** 2) / n
    expected_kurt = p * (p + 2) * (n - 1) / (n + 1)
    var_kurt = 8 * p * (p + 2) / n
    kurt_stat = (b2_p - p * (p + 2)) / np.sqrt(var_kurt)
    p_kurt = 2.0 * (1.0 - stats.norm.cdf(np.abs(kurt_stat)))
    
    return {
        "skewness": float(b1_p),
        "skewness_stat": float(skew_stat),
        "skewness_stat_small_sample": float(skew_stat_small),
        "skewness_p_value": float(p_skew),
        "df_skew": int(df_skew),
        "kurtosis": float(b2_p),
        "expected_kurtosis": float(expected_kurt),
        "kurtosis_stat": float(kurt_stat),
        "kurtosis_p_value": float(p_kurt)
    }


def chi_square_qq_plot_data(X: np.ndarray):
    """
    Generate Chi-Square Q-Q plot theoretical vs empirical quantiles for multivariate normality diagnosis.
    """
    n, p = X.shape
    mean = np.mean(X, axis=0)
    cov = np.cov(X, rowvar=False, ddof=1)
    d2 = mahalanobis_distance(X, mean, cov)
    ordered_d2 = np.sort(d2)
    
    probs = (np.arange(1, n + 1) - 0.5) / n
    theoretical_quantiles = stats.chi2.ppf(probs, df=p)
    
    return {
        "ordered_d2": ordered_d2,
        "theoretical_quantiles": theoretical_quantiles,
        "df": p
    }


# ==========================================
# 2. Covariance Structure Tests
# ==========================================

def box_m_test(X_list: list):
    """
    Box's M test for equality of covariance matrices across g groups.
    """
    g = len(X_list)
    p = X_list[0].shape[1]
    n_k = [x.shape[0] for x in X_list]
    N = sum(n_k)
    
    S_k = [np.cov(x, rowvar=False, ddof=1) for x in X_list]
    S_pooled = sum((n_k[i] - 1) * S_k[i] for i in range(g)) / (N - g)
    
    _, log_det_pooled = np.linalg.slogdet(S_pooled)
    M = (N - g) * log_det_pooled
    
    for i in range(g):
        _, log_det_k = np.linalg.slogdet(S_k[i])
        M -= (n_k[i] - 1) * log_det_k
        
    sum_inv_df = sum(1.0 / (n - 1) for n in n_k)
    c1 = ((2 * p**2 + 3 * p - 1) / (6 * (p + 1) * (g - 1))) * (sum_inv_df - 1.0 / (N - g))
    
    df_M = (g - 1) * p * (p + 1) // 2
    chi2_stat = M * (1.0 - c1)
    p_value = 1.0 - stats.chi2.cdf(chi2_stat, df_M)
    
    return {
        "M_stat": float(M),
        "chi2_stat": float(chi2_stat),
        "df": int(df_M),
        "p_value": float(p_value)
    }


def bartlett_sphericity_test(X: np.ndarray):
    """
    Bartlett's test of sphericity. Tests H0: R = I.
    """
    n, p = X.shape
    R = np.corrcoef(X, rowvar=False)
    _, log_det_R = np.linalg.slogdet(R)
    
    stat = - (n - 1 - (2 * p + 5) / 6.0) * log_det_R
    df = p * (p - 1) // 2
    p_value = 1.0 - stats.chi2.cdf(stat, df)
    return {
        "statistic": float(stat),
        "df": int(df),
        "p_value": float(p_value)
    }


def kmo_test(X: np.ndarray):
    """
    Kaiser-Meyer-Olkin (KMO) Measure of Sampling Adequacy.
    """
    R = np.corrcoef(X, rowvar=False)
    inv_R = np.linalg.pinv(R)
    
    diag_inv = np.diag(inv_R)
    partial_R = - inv_R / np.sqrt(np.outer(diag_inv, diag_inv))
    np.fill_diagonal(partial_R, 1.0)
    
    p = X.shape[1]
    r2_sum = np.sum(R**2) - p
    p2_sum = np.sum(partial_R**2) - p
    
    overall_kmo = r2_sum / (r2_sum + p2_sum + 1e-12)
    return {
        "kmo_overall": float(overall_kmo),
        "factorable": bool(overall_kmo >= 0.6)
    }


def ledoit_wolf_shrinkage(X: np.ndarray):
    """
    Ledoit-Wolf optimal shrinkage estimator for covariance matrix:
    Sigma* = (1 - alpha) * S + alpha * (tr(S)/p) * I
    """
    n, p = X.shape
    X_c = X - np.mean(X, axis=0)
    S = np.cov(X, rowvar=False, ddof=1)
    
    mu = np.trace(S) / p
    target = mu * np.eye(p)
    
    delta_sq = np.sum((S - target) ** 2)
    
    beta_sum = 0.0
    for i in range(n):
        diff_i = np.outer(X_c[i], X_c[i]) - S
        beta_sum += np.sum(diff_i ** 2)
    beta = beta_sum / (n * n)
    
    alpha = np.clip(beta / (delta_sq + 1e-12), 0.0, 1.0)
    shrunk_cov = (1.0 - alpha) * S + alpha * target
    
    return {
        "shrunk_cov": shrunk_cov,
        "sample_cov": S,
        "shrinkage_intensity": float(alpha),
        "target_mu": float(mu)
    }


# ==========================================
# 3. Multivariate Hypothesis Testing
# ==========================================

def hotelling_t2_one_sample(X: np.ndarray, mu_0: np.ndarray):
    """
    One-sample Hotelling's T^2 test backed by Cholesky factorization.
    """
    n, p = X.shape
    if n <= p:
        raise ValueError(f"Sample size n={n} must be greater than dimension p={p}")
    
    x_bar = np.mean(X, axis=0)
    S = np.cov(X, rowvar=False, ddof=1)
    diff = (x_bar - mu_0).reshape(1, -1)
    
    sol, cond_num = _safe_solve_cov(S, diff)
    quad = float(np.sum(diff * sol.T))
    T2 = n * quad
    
    f_stat = ((n - p) / ((n - 1) * p)) * T2
    df1 = p
    df2 = n - p
    p_val = 1.0 - stats.f.cdf(f_stat, df1, df2)
    
    return {
        "T2": float(T2),
        "F_stat": float(f_stat),
        "p_value": float(p_val),
        "df1": int(df1),
        "df2": int(df2),
        "cond_num": cond_num
    }


def hotelling_t2_two_sample(X1: np.ndarray, X2: np.ndarray):
    """
    Two-sample Hotelling's T^2 test assuming equal covariance matrices.
    """
    n1, p1 = X1.shape
    n2, p2 = X2.shape
    if p1 != p2:
        raise ValueError("Dimensions of X1 and X2 must match")
    p = p1
    if (n1 + n2 - p - 1) <= 0:
        raise ValueError(f"Total samples n1+n2={n1+n2} insufficient for dimension p={p}")
    
    x1_bar = np.mean(X1, axis=0)
    x2_bar = np.mean(X2, axis=0)
    
    S1 = np.cov(X1, rowvar=False, ddof=1)
    S2 = np.cov(X2, rowvar=False, ddof=1)
    
    S_pooled = ((n1 - 1) * S1 + (n2 - 1) * S2) / (n1 + n2 - 2)
    diff = (x1_bar - x2_bar).reshape(1, -1)
    
    sol, cond_num = _safe_solve_cov(S_pooled, diff)
    quad = float(np.sum(diff * sol.T))
    
    factor = (n1 * n2) / (n1 + n2)
    T2 = factor * quad
    
    df1 = p
    df2 = n1 + n2 - p - 1
    f_stat = ((df2) / ((n1 + n2 - 2) * p)) * T2
    p_val = 1.0 - stats.f.cdf(f_stat, df1, df2)
    
    return {
        "T2": float(T2),
        "F_stat": float(f_stat),
        "p_value": float(p_val),
        "df1": int(df1),
        "df2": int(df2),
        "cond_num": cond_num
    }


def manova_fit(X: np.ndarray, y: np.ndarray):
    """
    One-Way Multivariate Analysis of Variance (MANOVA).
    """
    classes = np.unique(y)
    g = len(classes)
    N, p = X.shape
    
    overall_mean = np.mean(X, axis=0)
    
    H = np.zeros((p, p))
    E = np.zeros((p, p))
    
    for c in classes:
        Xc = X[y == c]
        nc = Xc.shape[0]
        mc = np.mean(Xc, axis=0)
        
        diff_b = (mc - overall_mean).reshape(-1, 1)
        H += nc * (diff_b @ diff_b.T)
        
        diff_w = Xc - mc
        E += diff_w.T @ diff_w
        
    sol_E, _ = _safe_solve_cov(E, H)
    mat_HE = sol_E.T
    eigvals = np.real(np.linalg.eigvals(mat_HE))
    eigvals = eigvals[eigvals > 0]
    
    wilks_lambda = np.prod(1.0 / (1.0 + eigvals))
    
    df_h = g - 1
    df_e = N - g
    s = np.sqrt(((p**2 * df_h**2 - 4)) / (p**2 + df_h**2 - 5)) if (p**2 + df_h**2 - 5) > 0 else 1.0
    v = (df_e - (p - df_h + 1) / 2.0) * s - (p * df_h - 2) / 2.0
    u = p * df_h
    wilks_F = ((1.0 - wilks_lambda**(1.0/s)) / (wilks_lambda**(1.0/s) + 1e-12)) * (v / u)
    wilks_p = 1.0 - stats.f.cdf(wilks_F, u, v) if v > 0 else 0.0
    
    pillai_trace = np.sum(eigvals / (1.0 + eigvals))
    hotelling_lawley = np.sum(eigvals)
    roys_root = np.max(eigvals) if len(eigvals) > 0 else 0.0
    
    return {
        "wilks_lambda": float(wilks_lambda),
        "wilks_F": float(wilks_F),
        "wilks_p_value": float(wilks_p),
        "pillai_trace": float(pillai_trace),
        "hotelling_lawley": float(hotelling_lawley),
        "roys_largest_root": float(roys_root),
        "H_matrix": H,
        "E_matrix": E
    }


# ==========================================
# 4. Dimensionality Reduction & Latent Variables
# ==========================================

def pca_fit(X: np.ndarray, n_components: int = None, standardize: bool = True):
    """
    Principal Component Analysis (PCA) via SVD with Whitening.
    """
    n, p = X.shape
    if n_components is None:
        n_components = min(n, p)
        
    mean = np.mean(X, axis=0)
    X_centered = X - mean
    
    if standardize:
        std = np.std(X, axis=0, ddof=1)
        std[std == 0] = 1.0
        X_scaled = X_centered / std
    else:
        X_scaled = X_centered
        
    U, s, Vt = np.linalg.svd(X_scaled, full_matrices=False)
    
    eigenvalues = (s ** 2) / (n - 1)
    total_var = np.sum(eigenvalues)
    explained_variance_ratio = eigenvalues / total_var
    
    components = Vt[:n_components]
    transformed = X_scaled @ components.T
    
    whitened = transformed / np.sqrt(eigenvalues[:n_components] * (n - 1) + 1e-12)
    
    return {
        "components": components,
        "explained_variance": eigenvalues[:n_components],
        "explained_variance_ratio": explained_variance_ratio[:n_components],
        "cumulative_variance_ratio": np.cumsum(explained_variance_ratio)[:n_components],
        "transformed": transformed,
        "whitened": whitened,
        "mean": mean
    }


def varimax_rotation(loadings: np.ndarray, max_iter: int = 500, tol: float = 1e-6):
    """
    Kaiser's Varimax Orthogonal Rotation for Factor Loadings.
    """
    p, m = loadings.shape
    if m == 1:
        return loadings, np.eye(1)
        
    R = np.eye(m)
    var = 0
    L = loadings.copy()
    
    for _ in range(max_iter):
        for i in range(m - 1):
            for j in range(i + 1, m):
                x = L[:, i]
                y = L[:, j]
                u = x**2 - y**2
                v = 2 * x * y
                
                A = np.sum(u)
                B = np.sum(v)
                C = np.sum(u**2 - v**2)
                D = 2 * np.sum(u * v)
                
                num = D - 2 * A * B / p
                den = C - (A**2 - B**2) / p
                theta = 0.25 * np.arctan2(num, den)
                
                T = np.array([
                    [np.cos(theta), -np.sin(theta)],
                    [np.sin(theta),  np.cos(theta)]
                ])
                
                L[:, [i, j]] = L[:, [i, j]] @ T
                R[:, [i, j]] = R[:, [i, j]] @ T
                
        new_var = np.sum(p * np.sum(L**4, axis=0) - np.sum(L**2, axis=0)**2) / (p**2)
        if np.abs(new_var - var) < tol:
            break
        var = new_var
        
    return L, R


def factor_analysis_fit(X: np.ndarray, n_factors: int = 2, rotate: bool = True):
    """
    Principal Factor Extraction for Exploratory Factor Analysis.
    """
    n, p = X.shape
    R = np.corrcoef(X, rowvar=False)
    
    inv_R = np.linalg.pinv(R)
    smc = 1.0 - 1.0 / np.diag(inv_R)
    smc = np.clip(smc, 0.1, 0.99)
    
    R_reduced = R.copy()
    np.fill_diagonal(R_reduced, smc)
    
    eigvals, eigvecs = np.linalg.eigh(R_reduced)
    idx = np.argsort(eigvals)[::-1]
    eigvals = np.maximum(eigvals[idx[:n_factors]], 0)
    eigvecs = eigvecs[:, idx[:n_factors]]
    
    loadings = eigvecs * np.sqrt(eigvals)
    
    if rotate and n_factors > 1:
        loadings, rot_mat = varimax_rotation(loadings)
    else:
        rot_mat = np.eye(n_factors)
        
    communalities = np.sum(loadings**2, axis=1)
    uniquenesses = 1.0 - communalities
    
    return {
        "loadings": loadings,
        "communalities": communalities,
        "uniquenesses": uniquenesses,
        "rotation_matrix": rot_mat
    }


def mds_fit(dist_matrix: np.ndarray, n_components: int = 2):
    """
    Classical Multidimensional Scaling (Torgerson Metric MDS).
    """
    n = dist_matrix.shape[0]
    H = np.eye(n) - np.ones((n, n)) / n
    D_sq = dist_matrix ** 2
    B = -0.5 * H @ D_sq @ H
    
    eigvals, eigvecs = np.linalg.eigh(B)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx[:n_components]]
    eigvecs = eigvecs[:, idx[:n_components]]
    
    pos_eigvals = np.maximum(eigvals, 0)
    coords = eigvecs * np.sqrt(pos_eigvals)
    
    stress = np.sum((dist_matrix - np.linalg.norm(coords[:, None] - coords[None, :], axis=2))**2)
    return {
        "coordinates": coords,
        "eigenvalues": eigvals,
        "stress": float(stress)
    }


# ==========================================
# 5. Classification & Clustering
# ==========================================

def lda_fit(X: np.ndarray, y: np.ndarray):
    """
    Multi-Class Fisher's Linear Discriminant Analysis via Generalized Eigenvalue Problem:
    Sb w = lambda Sw w (solved robustly via scipy.linalg.eigh).
    """
    classes = np.unique(y)
    n, p = X.shape
    overall_mean = np.mean(X, axis=0)
    
    Sw = np.zeros((p, p))
    Sb = np.zeros((p, p))
    class_means = {}
    
    for c in classes:
        Xc = X[y == c]
        nc = Xc.shape[0]
        mc = np.mean(Xc, axis=0)
        class_means[c] = mc
        
        diff_w = Xc - mc
        Sw += diff_w.T @ diff_w
        
        diff_b = (mc - overall_mean).reshape(-1, 1)
        Sb += nc * (diff_b @ diff_b.T)
        
    cond_Sw = np.linalg.cond(Sw)
    if cond_Sw > 1e4:
        Sw += 1e-4 * np.trace(Sw) / p * np.eye(p)
        
    eigvals, eigvecs = linalg.eigh(Sb, Sw)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    
    n_components = min(len(classes) - 1, p)
    W = eigvecs[:, :n_components]
    
    for i in range(W.shape[1]):
        norm = np.sqrt(W[:, i].T @ Sw @ W[:, i])
        if norm > 0:
            W[:, i] /= norm
            
    projected = X @ W
    
    return {
        "W": W,
        "eigenvalues": eigvals[:n_components],
        "class_means": class_means,
        "classes": classes,
        "projected": projected
    }


def qda_fit(X: np.ndarray, y: np.ndarray):
    """
    Quadratic Discriminant Analysis (QDA) assuming class-specific covariance matrices.
    """
    classes = np.unique(y)
    n, p = X.shape
    
    priors = {}
    means = {}
    covs = {}
    log_dets = {}
    
    for c in classes:
        Xc = X[y == c]
        nc = Xc.shape[0]
        priors[c] = nc / n
        means[c] = np.mean(Xc, axis=0)
        cov_c = np.cov(Xc, rowvar=False, ddof=1) + 1e-4 * np.eye(p)
        covs[c] = cov_c
        _, log_det = np.linalg.slogdet(cov_c)
        log_dets[c] = log_det
        
    def predict(X_test: np.ndarray):
        X_test = np.atleast_2d(X_test)
        n_test = X_test.shape[0]
        scores = np.zeros((n_test, len(classes)))
        
        for idx, c in enumerate(classes):
            diff = X_test - means[c]
            sol, _ = _safe_solve_cov(covs[c], diff)
            quad = np.sum(diff * sol.T, axis=1)
            scores[:, idx] = -0.5 * log_dets[c] - 0.5 * quad + np.log(priors[c])
            
        pred_idx = np.argmax(scores, axis=1)
        return classes[pred_idx]
        
    return {
        "classes": classes,
        "priors": priors,
        "means": means,
        "covs": covs,
        "predict": predict
    }


def gmm_em_fit(X: np.ndarray, n_components: int = 2, max_iter: int = 100, tol: float = 1e-5, reg_covar: float = 1e-4):
    """
    Gaussian Mixture Model with Expectation-Maximization (EM) Algorithm.
    Monotonic log-likelihood verified at each iteration.
    """
    n, p = X.shape
    np.random.seed(42)
    
    indices = np.random.choice(n, n_components, replace=False)
    means = X[indices].copy()
    covs = np.array([np.cov(X, rowvar=False, ddof=1) + reg_covar * np.eye(p) for _ in range(n_components)])
    weights = np.ones(n_components) / n_components
    
    log_likelihoods = []
    
    for it in range(max_iter):
        densities = np.zeros((n, n_components))
        for k in range(n_components):
            try:
                densities[:, k] = stats.multivariate_normal.pdf(X, mean=means[k], cov=covs[k], allow_singular=True)
            except Exception:
                densities[:, k] = 1e-12
        densities = np.maximum(densities, 1e-12)
        
        weighted_densities = densities * weights
        total_density = np.sum(weighted_densities, axis=1, keepdims=True)
        gamma = weighted_densities / total_density
        
        current_ll = float(np.sum(np.log(total_density)))
        log_likelihoods.append(current_ll)
        
        if it > 0 and (current_ll - log_likelihoods[-2]) < -1e-4:
            warnings.warn(f"[GMM Warning] Monotonicity violated at iteration {it}: {current_ll:.4f} < {log_likelihoods[-2]:.4f}", RuntimeWarning)
            
        if it > 0 and np.abs(current_ll - log_likelihoods[-2]) < tol:
            break
            
        Nk = np.sum(gamma, axis=0) + 1e-10
        weights = Nk / n
        means = (gamma.T @ X) / Nk[:, None]
        
        for k in range(n_components):
            diff = X - means[k]
            covs[k] = (gamma[:, k][:, None] * diff).T @ diff / Nk[k] + reg_covar * np.eye(p)
            
    return {
        "means": means,
        "covariances": covs,
        "weights": weights,
        "responsibilities": gamma,
        "log_likelihoods": log_likelihoods,
        "converged": bool(len(log_likelihoods) < max_iter)
    }


# ==========================================
# 6. Association & Manifold Geometry
# ==========================================

def cca_fit(X: np.ndarray, Y: np.ndarray, n_components: int = None):
    """
    Canonical Correlation Analysis (CCA) between multidimensional variables X and Y.
    """
    n, p = X.shape
    _, q = Y.shape
    
    if n_components is None:
        n_components = min(p, q)
        
    X_c = X - np.mean(X, axis=0)
    Y_c = Y - np.mean(Y, axis=0)
    
    Sxx = (X_c.T @ X_c) / (n - 1) + 1e-6 * np.eye(p)
    Syy = (Y_c.T @ Y_c) / (n - 1) + 1e-6 * np.eye(q)
    Sxy = (X_c.T @ Y_c) / (n - 1)
    
    sol_x, _ = _safe_solve_cov(Sxx, Sxy)
    sol_y, _ = _safe_solve_cov(Syy, Sxy.T)
    
    mat_x = sol_x @ sol_y
    eigvals_x, eigvecs_x = np.linalg.eig(mat_x)
    
    idx = np.argsort(np.real(eigvals_x))[::-1]
    correlations = np.sqrt(np.clip(np.real(eigvals_x[idx]), 0, 1))
    A = np.real(eigvecs_x[:, idx[:n_components]])
    
    B = np.zeros((q, n_components))
    for i in range(n_components):
        if correlations[i] > 1e-6:
            b_vec = sol_y @ A[:, i] / correlations[i]
            B[:, i] = b_vec / (np.sqrt(b_vec.T @ Syy @ b_vec) + 1e-8)
            
    for i in range(n_components):
        a_vec = A[:, i]
        A[:, i] = a_vec / (np.sqrt(a_vec.T @ Sxx @ a_vec) + 1e-8)
        
    u_scores = X_c @ A
    v_scores = Y_c @ B
    
    return {
        "correlations": correlations[:n_components],
        "x_weights": A,
        "y_weights": B,
        "u_scores": u_scores,
        "v_scores": v_scores
    }


def correspondence_analysis_fit(contingency_table: np.ndarray, n_components: int = 2):
    """
    Simple Correspondence Analysis (Dual Scaling SVD).
    """
    N = np.array(contingency_table, dtype=float)
    n = np.sum(N)
    P = N / n
    
    r = np.sum(P, axis=1)
    c = np.sum(P, axis=0)
    
    Dr_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(r, 1e-12)))
    Dc_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(c, 1e-12)))
    
    Z = Dr_inv_sqrt @ (P - np.outer(r, c)) @ Dc_inv_sqrt
    U, s, Vt = np.linalg.svd(Z, full_matrices=False)
    
    total_inertia = np.sum(s ** 2)
    explained_inertia = (s ** 2) / total_inertia
    
    k = min(n_components, len(s))
    F_row = Dr_inv_sqrt @ U[:, :k] * s[:k]
    G_col = Dc_inv_sqrt @ Vt[:k, :].T * s[:k]
    
    return {
        "total_inertia": float(total_inertia),
        "explained_inertia_ratio": explained_inertia[:k],
        "row_principal_coordinates": F_row,
        "col_principal_coordinates": G_col,
        "singular_values": s[:k]
    }
