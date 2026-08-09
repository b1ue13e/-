# -*- coding: utf-8 -*-
"""
Unit Tests for CDA Course Datasets, Algorithmic Starters, and Model Verifications
Course: 31-属性数据分析 (Categorical Data Analysis)
"""
import os
import sys
import unittest
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.contingency_tables import StratifiedTable

# Add scripts directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))
from cda_starter import (
    calculate_contingency_2x2_metrics,
    fit_logistic_irls,
    fit_poisson_irls,
    calculate_cmh_stat
)

class TestCDADataAndMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    def test_ucb_dataset_exists_and_valid(self):
        ucb_path = os.path.join(self.data_dir, "ucb_admissions.csv")
        self.assertTrue(os.path.exists(ucb_path), "ucb_admissions.csv missing")
        df = pd.read_csv(ucb_path)
        self.assertEqual(len(df), 24)
        self.assertIn("Dept", df.columns)
        self.assertIn("Freq", df.columns)
        self.assertEqual(df['Freq'].sum(), 4526)

    def test_arthritis_dataset_exists_and_valid(self):
        art_path = os.path.join(self.data_dir, "arthritis.csv")
        self.assertTrue(os.path.exists(art_path), "arthritis.csv missing")
        df = pd.read_csv(art_path, na_filter=False)
        self.assertEqual(len(df), 84, "arthritis dataset must contain full 84 observations")
        self.assertIn("Treatment", df.columns)
        self.assertIn("Improved", df.columns)
        self.assertEqual(set(df['Treatment'].unique()), {'Treated', 'Placebo'})
        self.assertEqual(set(df['Improved'].unique()), {'None', 'Some', 'Marked'})

    def test_crabs_dataset_exists_and_valid(self):
        crabs_path = os.path.join(self.data_dir, "crabs.csv")
        self.assertTrue(os.path.exists(crabs_path), "crabs.csv missing")
        df = pd.read_csv(crabs_path)
        self.assertEqual(len(df), 173, "crabs dataset must contain full 173 observations")
        self.assertIn("Width", df.columns)
        self.assertIn("Weight", df.columns)
        self.assertIn("Satellites", df.columns)
        self.assertTrue((df['Satellites'] >= 0).all())

    def test_from_scratch_2x2_contingency_metrics(self):
        # 2x2 matrix: [[42, 18], [24, 36]]
        mat = np.array([[42, 18], [24, 36]])
        res = calculate_contingency_2x2_metrics(mat)
        
        self.assertAlmostEqual(res["odds_ratio"], 3.5, places=4)
        self.assertAlmostEqual(res["woolf_se"], 0.3858, places=3)
        self.assertAlmostEqual(res["ci_95"][0], 1.6427, places=2)
        self.assertAlmostEqual(res["ci_95"][1], 7.4571, places=2)
        self.assertGreater(res["pearson_chi2"], 8.0)

    def test_from_scratch_logistic_irls_matches_statsmodels(self):
        # Load crabs data and compare fit_logistic_irls vs statsmodels GLM
        crabs_path = os.path.join(self.data_dir, "crabs.csv")
        df = pd.read_csv(crabs_path)
        df['Has_Satellites'] = (df['Satellites'] > 0).astype(float)
        
        # Design matrix X: Intercept + Width
        df['Intercept'] = 1.0
        X = df[['Intercept', 'Width']].values
        y = df['Has_Satellites'].values
        
        # 1. Our from-scratch IRLS solver
        custom_fit = fit_logistic_irls(X, y)
        self.assertTrue(custom_fit["converged"])
        
        # 2. Statsmodels GLM reference
        sm_glm = sm.GLM(y, X, family=sm.families.Binomial()).fit()
        
        # Verify coefficients match statsmodels to 4 decimal places
        np.testing.assert_allclose(custom_fit["beta"], sm_glm.params, rtol=1e-4, atol=1e-4)
        np.testing.assert_allclose(custom_fit["se_beta"], sm_glm.bse, rtol=1e-4, atol=1e-4)
        self.assertAlmostEqual(custom_fit["deviance"], sm_glm.deviance, places=3)

    def test_from_scratch_poisson_irls_and_overdispersion(self):
        crabs_path = os.path.join(self.data_dir, "crabs.csv")
        df = pd.read_csv(crabs_path)
        
        df['Intercept'] = 1.0
        X = df[['Intercept', 'Width']].values
        y = df['Satellites'].values.astype(float)
        
        custom_pois = fit_poisson_irls(X, y)
        self.assertTrue(custom_pois["converged"])
        
        sm_pois = sm.GLM(y, X, family=sm.families.Poisson()).fit()
        
        np.testing.assert_allclose(custom_pois["beta"], sm_pois.params, rtol=1e-4, atol=1e-4)
        self.assertGreater(custom_pois["phi_hat"], 2.0, "Poisson model must detect overdispersion phi > 2.0")

    def test_from_scratch_cmh_stat_matches_statsmodels(self):
        df = pd.read_csv(os.path.join(self.data_dir, "ucb_admissions.csv"))
        tables = []
        for dept in sorted(df['Dept'].unique()):
            sub = df[df['Dept'] == dept].pivot(index='Gender', columns='Admit', values='Freq').fillna(0)
            sub = sub.reindex(index=['Male', 'Female'], columns=['Admitted', 'Rejected'])
            tables.append(sub.values)
            
        tables_arr = np.array(tables) # (K, 2, 2)
        custom_cmh = calculate_cmh_stat(tables_arr)
        
        # Statsmodels StratifiedTable reference
        st = StratifiedTable(tables_arr.transpose(1, 2, 0))
        
        self.assertAlmostEqual(custom_cmh["pooled_mh_or"], st.oddsratio_pooled, places=3)

if __name__ == "__main__":
    unittest.main()
