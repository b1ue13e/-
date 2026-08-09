# -*- coding: utf-8 -*-
"""
Data Loader and Dictionary for Multivariate Analysis (16-多元统计)
Provides unified interfaces to load authentic empirical datasets:
1. load_swiss_banknotes(): Swiss Banknotes Dataset (Flury & Riedwyl 1988)
2. load_wine_data(): UCI Wine Dataset (178 samples, 13 chemical features, 3 cultivars)
3. load_macro_financial_panel(): 15-year monthly macroeconomic and financial asset return panel
"""
import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_swiss_banknotes() -> pd.DataFrame:
    """
    Load Swiss Banknotes Dataset (Flury & Riedwyl 1988).
    Dimensions: 200 rows x 8 columns.
    Features:
    - Length: Length of bill (mm)
    - Left: Width of left edge (mm)
    - Right: Width of right edge (mm)
    - Bottom: Margin at bottom (mm)
    - Top: Margin at top (mm)
    - Diagonal: Length of diagonal (mm)
    - Status: 'genuine' (100) or 'counterfeit' (100)
    - Is_Counterfeit: 0 (genuine) or 1 (counterfeit)
    """
    path = os.path.join(DATA_DIR, "swiss_banknotes.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    return pd.read_csv(path)


def load_wine_data() -> pd.DataFrame:
    """
    Load UCI Wine Recognition Dataset.
    Dimensions: 178 rows x 14 columns.
    13 continuous physical/chemical features:
    - alcohol, malic_acid, ash, alcalinity_of_ash, magnesium,
      total_phenols, flavanoids, nonflavanoid_phenols, proanthocyanins,
      color_intensity, hue, od280/od315_of_diluted_wines, proline
    Target:
    - Cultivar: 0 (59 samples), 1 (71 samples), 2 (48 samples)
    """
    path = os.path.join(DATA_DIR, "wine_data.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    return pd.read_csv(path)


def load_macro_financial_panel() -> pd.DataFrame:
    """
    Load Macroeconomic and Multi-Asset Financial Monthly Panel Dataset.
    Dimensions: 180 months (15 years) x 17 columns.
    Macro variables (10):
    - GDP_Growth, CPI, PPI, M2_Growth, TSF_Increment, Base_Rate,
      PMI, Trade_Balance, Unemployment_Rate, Industrial_Output
    Asset returns (6):
    - Stock_A_Return, Bond_10Y_Return, Commodity_Return, Gold_Return,
      USD_CNY_Return, Reit_Return
    """
    path = os.path.join(DATA_DIR, "macro_financial_panel.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    return pd.read_csv(path)


if __name__ == "__main__":
    print("=== 1. Swiss Banknotes ===")
    df_bank = load_swiss_banknotes()
    print(df_bank.head(2))
    print("Shape:", df_bank.shape, "Classes:", df_bank['Status'].value_counts().to_dict())

    print("\n=== 2. Wine Data ===")
    df_wine = load_wine_data()
    print(df_wine.head(2))
    print("Shape:", df_wine.shape, "Cultivars:", df_wine['Cultivar'].value_counts().to_dict())

    print("\n=== 3. Macro Financial Panel ===")
    df_macro = load_macro_financial_panel()
    print(df_macro.head(2))
    print("Shape:", df_macro.shape, "Time range:", df_macro['Date'].iloc[0], "to", df_macro['Date'].iloc[-1])
