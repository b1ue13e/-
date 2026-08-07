from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ACTIVE_ROOTS = (
    REPO_ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "02-时间序列分析",
    REPO_ROOT / "03-Projects" / "02-时间序列分析",
)

REPLACEMENTS = {
    "02-Knowledge/🧠 学习系统/02-时间序列分析/02-统计基础层/单位根检验": "02-时间序列分析/02-平稳性与相关结构/单位根检验-ADF-KPSS",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/02-统计基础层/自相关函数ACF": "02-时间序列分析/02-平稳性与相关结构/自相关函数ACF",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/02-统计基础层/白噪声": "02-时间序列分析/02-平稳性与相关结构/白噪声",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/ARIMA模型": "02-时间序列分析/03-经典预测模型/ARIMA模型",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/ARMA模型": "02-时间序列分析/03-经典预测模型/ARMA模型",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/SARIMA模型": "02-时间序列分析/03-经典预测模型/SARIMA模型",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/差分运算": "02-时间序列分析/03-经典预测模型/差分运算",
    "02-Knowledge/🧠 学习系统/02-时间序列分析/04-建模与诊断层/协整": "02-时间序列分析/05-多变量与现代扩展/协整",
    "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-05-模型识别与参数估计": "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-06-模型识别与残差诊断",
    "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-06-残差诊断与纯随机性检验": "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-06-模型识别与残差诊断",
    "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-07-SARIMA与季节预测": "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-05-SARIMA与季节预测",
}


def main() -> None:
    changed = 0
    for root in ACTIVE_ROOTS:
        for path in sorted(root.rglob("*.md")):
            if ".tmp" in path.parts or ".reasonix" in path.parts:
                continue
            text = path.read_text(encoding="utf-8-sig")
            original = text
            for old, new in REPLACEMENTS.items():
                text = text.replace(old, new)
            text = text.replace(
                "02-Knowledge/🧠 学习系统/02-时间序列分析/99-历史与兼容入口/🎓 时间序列建模实战路线.md",
                "02-时间序列分析/🗺️ 时间序列分析学习路径.md",
            )
            text = text.replace(
                "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-05-模型识别与参数估计",
                "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-06-模型识别与残差诊断",
            )
            text = text.replace(
                "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-06-残差诊断与纯随机性检验",
                "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-06-模型识别与残差诊断",
            )
            text = text.replace(
                "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-07-SARIMA与季节预测",
                "03-Projects/02-时间序列分析/课后作业/时间序列分析-课后作业-05-SARIMA与季节预测",
            )
            if text != original:
                path.write_text(text, encoding="utf-8")
                changed += 1
                print(path.relative_to(REPO_ROOT))
    print(f"changed_files={changed}")


if __name__ == "__main__":
    main()
