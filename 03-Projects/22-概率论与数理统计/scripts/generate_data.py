import os
import numpy as np
import pandas as pd

np.random.seed(42)
n = 1000

# 模拟真实世界中具有右偏、厚尾特征的服务器响应延迟/金融赔付数据
request_volume = np.random.uniform(10, 500, size=n)
server_load = np.random.beta(2, 5, size=n) * 100 # 负载百分比
system_tier = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2], size=n) # 核心层级
is_peak_hour = (np.random.rand(n) < 0.35).astype(int)

# 真实潜在生成机制 (混合分布与右偏厚尾)
log_base_latency = (
    1.5 
    + 0.002 * request_volume 
    + 0.015 * server_load 
    - 0.2 * system_tier 
    + 0.4 * is_peak_hour
)

base_noise = np.random.gamma(shape=3.0, scale=0.5, size=n)
heavy_tail_shock = np.random.pareto(a=2.5, size=n) * (np.random.rand(n) < 0.12) * 15.0

latency_ms = np.exp(log_base_latency) + base_noise * 5.0 + heavy_tail_shock

df = pd.DataFrame({
    "sample_id": np.arange(1, n + 1),
    "latency_ms": np.round(latency_ms, 2),
    "request_volume": np.round(request_volume, 1),
    "server_load": np.round(server_load, 2),
    "system_tier": system_tier,
    "is_peak_hour": is_peak_hour
})

out_dir = os.path.join(os.getcwd(), "data")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "financial_loss_or_delay_data.csv")
df.to_csv(out_path, index=False)
print(f"Generated dataset with {len(df)} records at {out_path}. Latency summary:")
print(df["latency_ms"].describe())
