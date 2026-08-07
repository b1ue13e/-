# -*- coding: utf-8 -*-
"""29-运筹学 作业模型可解性验证（审计证据，B-R2 批次）
覆盖：课后作业 01（第1/3/4题）、课后作业 02（第1/2/4题）、课后作业 03（第1/2题）、阶段作业 01（全模型）
环境：venv ortools 9.15.6755；运行日期见输出时间戳。
"""
import time
from ortools.linear_solver import pywraplp

results = []
def record(name, status, obj, extra=""):
    results.append((name, status, obj, extra))
    print(f"[{name}] status={status} obj={obj} {extra}")

# ---- 课后作业 01 第 3/4 题：max 3x1+2x2 s.t. x1+x2<=4, x1<=2, x2<=3 ----
s = pywraplp.Solver.CreateSolver("GLOP")
x1 = s.NumVar(0, s.infinity(), "x1"); x2 = s.NumVar(0, s.infinity(), "x2")
s.Add(x1 + x2 <= 4); s.Add(x1 <= 2); s.Add(x2 <= 3)
s.Maximize(3*x1 + 2*x2)
st = s.Solve()
record("HW01-3/4 LP", st, s.Objective().Value(), f"x=({x1.solution_value():.4f},{x2.solution_value():.4f}) 期望(2,2) z=10")

# ---- 课后作业 01 第 1 题：资源分配 100h/150kg ----
s = pywraplp.Solver.CreateSolver("GLOP")
x1 = s.NumVar(0, s.infinity(), "A"); x2 = s.NumVar(0, s.infinity(), "B"); x3 = s.NumVar(0, s.infinity(), "C")
s.Add(x1 + x2 + x3 <= 100)        # 机器工时
s.Add(2*x1 + x2 <= 150)           # 原料
s.Maximize(3*x1 + 2*x2 + 1.5*x3)
st = s.Solve()
record("HW01-1 资源分配", st, s.Objective().Value(), f"x=({x1.solution_value():.2f},{x2.solution_value():.2f},{x3.solution_value():.2f})")

# ---- 课后作业 02 第 1 题：对偶 min 3x1+4x2 s.t. x1+x2>=2, x1+2x2>=3 ----
s = pywraplp.Solver.CreateSolver("GLOP")
x1 = s.NumVar(0, s.infinity(), "x1"); x2 = s.NumVar(0, s.infinity(), "x2")
s.Add(x1 + x2 >= 2); s.Add(x1 + 2*x2 >= 3)
s.Minimize(3*x1 + 4*x2)
st = s.Solve()
record("HW02-1 对偶", st, s.Objective().Value(), f"x=({x1.solution_value():.4f},{x2.solution_value():.4f}) 期望(1,1) p*=7")

# ---- 课后作业 02 第 2 题：影子价格 max 3x1+2x2（同上 HW01-3）----
s = pywraplp.Solver.CreateSolver("GLOP")
x1 = s.NumVar(0, s.infinity(), "x1"); x2 = s.NumVar(0, s.infinity(), "x2")
c1 = s.Add(x1 + x2 <= 4); c2 = s.Add(x1 <= 2); c3 = s.Add(x2 <= 3)
s.Maximize(3*x1 + 2*x2)
st = s.Solve()
shadow = [c1.dual_value(), c2.dual_value(), c3.dual_value()]
record("HW02-2 影子价格", st, s.Objective().Value(), f"y=({shadow[0]:.4f},{shadow[1]:.4f},{shadow[2]:.4f}) 期望(2,1,0)")

# ---- 课后作业 02 第 4 题：100% 规则验证 b1: 4->5, b3: 3->2 ----
s = pywraplp.Solver.CreateSolver("GLOP")
x1 = s.NumVar(0, s.infinity(), "x1"); x2 = s.NumVar(0, s.infinity(), "x2")
s.Add(x1 + x2 <= 5); s.Add(x1 <= 2); s.Add(x2 <= 2)   # b1=5, b3=2
s.Maximize(3*x1 + 2*x2)
st = s.Solve()
record("HW02-4 100%规则 b1=5,b3=2", st, s.Objective().Value(), f"x=({x1.solution_value():.4f},{x2.solution_value():.4f})")

# ---- 课后作业 03 第 1 题背包：容量10 (6,8)(5,7)(4,6)(3,4) ----
s = pywraplp.Solver.CreateSolver("SCIP")
w = [6,5,4,3]; v = [8,7,6,4]
xs = [s.IntVar(0, 1, f"x{i}") for i in range(4)]
s.Add(sum(w[i]*xs[i] for i in range(4)) <= 10)
s.Maximize(sum(v[i]*xs[i] for i in range(4)))
st = s.Solve()
record("HW03-1 背包", st, s.Objective().Value(), f"选={[i for i in range(4) if xs[i].solution_value()>0.5]} 期望选A+C z=14")

# ---- 课后作业 03 第 2 题 B&B：max 5x1+4x2 s.t. x1+x2<=5, 10x1+6x2<=45 ----
s = pywraplp.Solver.CreateSolver("SCIP")
x1 = s.IntVar(0, s.infinity(), "x1"); x2 = s.IntVar(0, s.infinity(), "x2")
s.Add(x1 + x2 <= 5); s.Add(10*x1 + 6*x2 <= 45)
s.Maximize(5*x1 + 4*x2)
st = s.Solve()
record("HW03-2 B&B", st, s.Objective().Value(), f"x=({x1.solution_value()},{x2.solution_value()})")

# ---- 阶段作业 01：3产线4产品LP ----
# P1(1,2,0;3,1;8) P2(2,0,1;1,2;10) P3(0,1,2;2,0;6) P4(1,1,1;0,3;12)
s = pywraplp.Solver.CreateSolver("GLOP")
p1 = s.NumVar(0, s.infinity(), "P1"); p2 = s.NumVar(0, s.infinity(), "P2")
p3 = s.NumVar(0, s.infinity(), "P3"); p4 = s.NumVar(0, s.infinity(), "P4")
s.Add(p1 + 2*p2 + p4 <= 120)              # 产线A
s.Add(2*p1 + p3 + p4 <= 120)              # 产线B
s.Add(p2 + 2*p3 + p4 <= 120)              # 产线C
s.Add(3*p1 + p2 + 2*p3 <= 150)            # 原料1
s.Add(p1 + 2*p2 + 3*p4 <= 100)            # 原料2
s.Add(p1 + p2 >= 30)                      # 合同下限
s.Maximize(8*p1 + 10*p2 + 6*p3 + 12*p4)
st = s.Solve()
if st == pywraplp.Solver.OPTIMAL:
    record("S01-1 综合LP", st, s.Objective().Value(),
           f"x=({p1.solution_value():.1f},{p2.solution_value():.1f},{p3.solution_value():.1f},{p4.solution_value():.1f})")
else:
    record("S01-1 综合LP", st, "N/A", "")

print("\n=== 汇总 ===")
for n, st, obj, e in results:
    ok = st == pywraplp.Solver.OPTIMAL
    print(f"{'PASS' if ok else 'FAIL'}  {n}")
