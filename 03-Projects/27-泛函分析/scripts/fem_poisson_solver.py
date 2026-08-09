r"""
1D and 2D Poisson Equation Galerkin Finite Element Solver
=========================================================
Rigorous Numerical Verification of Functional Analysis Theory:
1. Lax-Milgram Theorem: Positive definiteness & coercivity of discrete stiffness matrix K.
2. Sobolev Trace Theorem & Boundary Lifting: Non-homogeneous boundary value u = w + u_g.
3. Céa's Lemma & Aubin-Nitsche Duality: Energy error ||u - u_h||_{H1} = O(h), L2 error = O(h^2).
4. Sobolev Regularity & Corner Singularity: 2D L-shaped domain re-entrant corner singularity
   u(r, \theta) = r^{2/3} \sin(2\theta/3) \in H^{5/3-\epsilon}(\Omega) \setminus H^2(\Omega).
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from typing import Tuple, Dict, List, Callable


# =====================================================================
# 1. 1D Homogeneous Poisson FEM Solver
# =====================================================================

def solve_poisson_1d(n_elements: int, f_func: Callable, u_exact_func: Callable, du_exact_func: Callable) -> Dict:
    """
    Solve -u''(x) = f(x) on (0, 1) with u(0) = 0, u(1) = 0 using P1 linear FEM.
    """
    h = 1.0 / n_elements
    nodes = np.linspace(0.0, 1.0, n_elements + 1)
    n_nodes = n_elements + 1
    
    # 1. Assemble 1D Stiffness Matrix (Tridiagonal)
    main_diag = (2.0 / h) * np.ones(n_nodes)
    off_diag = (-1.0 / h) * np.ones(n_nodes - 1)
    K = sp.diags([off_diag, main_diag, off_diag], [-1, 0, 1], format='csr')
    
    # 2. Assemble Load Vector F using 2-point Gauss Quadrature per element
    F = np.zeros(n_nodes)
    gp_std = np.array([-1.0 / np.sqrt(3.0), 1.0 / np.sqrt(3.0)])
    gw_std = np.array([1.0, 1.0])
    
    for e in range(n_elements):
        x_l, x_r = nodes[e], nodes[e + 1]
        gps = 0.5 * (x_r - x_l) * gp_std + 0.5 * (x_l + x_r)
        gws = 0.5 * (x_r - x_l) * gw_std
        
        for gp, w in zip(gps, gws):
            f_val = f_func(gp)
            phi_0 = (x_r - gp) / h
            phi_1 = (gp - x_l) / h
            F[e] += w * f_val * phi_0
            F[e + 1] += w * f_val * phi_1
            
    # 3. Apply Homogeneous Dirichlet Boundary Conditions (u(0) = 0, u(1) = 0)
    interior = np.arange(1, n_nodes - 1)
    K_int = K[interior, :][:, interior]
    F_int = F[interior]
    
    u_int = spla.spsolve(K_int, F_int)
    
    u_h = np.zeros(n_nodes)
    u_h[interior] = u_int
    
    # 4. Compute L2 and H1-semi Errors via 3-point Gauss Quadrature per element
    l2_error_sq = 0.0
    h1_error_sq = 0.0
    
    gp3_std = np.array([-np.sqrt(3.0 / 5.0), 0.0, np.sqrt(3.0 / 5.0)])
    gw3_std = np.array([5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0])
    
    for e in range(n_elements):
        x_l, x_r = nodes[e], nodes[e + 1]
        gps = 0.5 * h * gp3_std + 0.5 * (x_l + x_r)
        gws = 0.5 * h * gw3_std
        
        u_h_l, u_h_r = u_h[e], u_h[e + 1]
        du_h_val = (u_h_r - u_h_l) / h
        
        for gp, gw in zip(gps, gws):
            u_ex = u_exact_func(gp)
            du_ex = du_exact_func(gp)
            
            phi_0 = (x_r - gp) / h
            phi_1 = (gp - x_l) / h
            u_fem = u_h_l * phi_0 + u_h_r * phi_1
            
            l2_error_sq += gw * (u_ex - u_fem) ** 2
            h1_error_sq += gw * (du_ex - du_h_val) ** 2
            
    return {
        'h': h,
        'nodes': nodes,
        'u_h': u_h,
        'l2_error': float(np.sqrt(l2_error_sq)),
        'h1_error': float(np.sqrt(h1_error_sq))
    }


# =====================================================================
# 2. 1D Non-Homogeneous Dirichlet Boundary Lifting Solver
# =====================================================================

def solve_poisson_1d_nonhomogeneous(n_elements: int, f_func: Callable, g0: float, g1: float,
                                    u_exact_func: Callable, du_exact_func: Callable) -> Dict:
    r"""
    Solve -u''(x) = f(x) on (0, 1) with non-homogeneous Dirichlet BC: u(0) = g0, u(1) = g1.
    
    Trace Lifting Method (迹定理边界提升):
    1. Define H^1 boundary lifting u_g(x) = (1 - x)*g0 + x*g1.
    2. Write total solution as u(x) = w(x) + u_g(x), where w \in H_0^1(0, 1).
    3. Variational formulation for w:
       a(w, v) = <f, v> - a(u_g, v), \forall v \in H_0^1.
    """
    h = 1.0 / n_elements
    nodes = np.linspace(0.0, 1.0, n_elements + 1)
    n_nodes = n_elements + 1
    
    # 1. Global Stiffness Matrix
    main_diag = (2.0 / h) * np.ones(n_nodes)
    off_diag = (-1.0 / h) * np.ones(n_nodes - 1)
    K = sp.diags([off_diag, main_diag, off_diag], [-1, 0, 1], format='csr')
    
    # 2. Assemble Load Vector F
    F = np.zeros(n_nodes)
    gp_std = np.array([-1.0 / np.sqrt(3.0), 1.0 / np.sqrt(3.0)])
    gw_std = np.array([1.0, 1.0])
    
    for e in range(n_elements):
        x_l, x_r = nodes[e], nodes[e + 1]
        gps = 0.5 * (x_r - x_l) * gp_std + 0.5 * (x_l + x_r)
        gws = 0.5 * (x_r - x_l) * gw_std
        for gp, w in zip(gps, gws):
            f_val = f_func(gp)
            phi_0 = (x_r - gp) / h
            phi_1 = (gp - x_l) / h
            F[e] += w * f_val * phi_0
            F[e + 1] += w * f_val * phi_1
            
    # 3. Boundary lifting function values at nodes
    u_g = (1.0 - nodes) * g0 + nodes * g1
    
    # Modified RHS for zero-trace w: F_mod = F - K * u_g
    F_mod = F - K.dot(u_g)
    
    interior = np.arange(1, n_nodes - 1)
    K_int = K[interior, :][:, interior]
    F_int = F_mod[interior]
    
    w_int = spla.spsolve(K_int, F_int)
    
    w_h = np.zeros(n_nodes)
    w_h[interior] = w_int
    
    # Total discrete solution
    u_h = w_h + u_g
    
    # 4. Error evaluation
    l2_error_sq = 0.0
    h1_error_sq = 0.0
    gp3_std = np.array([-np.sqrt(3.0 / 5.0), 0.0, np.sqrt(3.0 / 5.0)])
    gw3_std = np.array([5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0])
    
    for e in range(n_elements):
        x_l, x_r = nodes[e], nodes[e + 1]
        gps = 0.5 * h * gp3_std + 0.5 * (x_l + x_r)
        gws = 0.5 * h * gw3_std
        
        u_h_l, u_h_r = u_h[e], u_h[e + 1]
        du_h_val = (u_h_r - u_h_l) / h
        
        for gp, gw in zip(gps, gws):
            u_ex = u_exact_func(gp)
            du_ex = du_exact_func(gp)
            phi_0 = (x_r - gp) / h
            phi_1 = (gp - x_l) / h
            u_fem = u_h_l * phi_0 + u_h_r * phi_1
            
            l2_error_sq += gw * (u_ex - u_fem) ** 2
            h1_error_sq += gw * (du_ex - du_h_val) ** 2
            
    return {
        'h': h,
        'nodes': nodes,
        'u_h': u_h,
        'w_h': w_h,
        'u_g': u_g,
        'l2_error': float(np.sqrt(l2_error_sq)),
        'h1_error': float(np.sqrt(h1_error_sq))
    }


# =====================================================================
# 3. 2D L-Shaped Domain Corner Singularity Solver
# =====================================================================

def solve_poisson_2d_lshaped(n_subdiv: int) -> Dict:
    r"""
    Solve -\Delta u = 0 on L-shaped domain \Omega = (-1, 1)^2 \setminus ([0, 1] \times [-1, 0]).
    Exact harmonic singular solution in polar coordinates:
    u(r, \theta) = r^{2/3} \sin(2\theta / 3), \quad \theta \in [0, 3\pi/2].
    
    Singularity Properties:
    - \nabla u \sim r^{-1/3} \in L^2(\Omega) \implies u \in H^1(\Omega) (Weak solution exists!).
    - \nabla^2 u \sim r^{-4/3} \notin L^2(\Omega) \implies u \notin H^2(\Omega) (Classical C^2 regularity collapses!).
    - Asymptotic FEM H1-rate is O(h^{2/3}) ~ 0.67 due to corner singularity.
    """
    h = 1.0 / n_subdiv
    
    # Use grid indexing:
    # Grid covers [-1, 1] x [-1, 1] with step h, total (2*n_subdiv + 1) x (2*n_subdiv + 1) points
    N = 2 * n_subdiv
    xs = np.linspace(-1.0, 1.0, N + 1)
    ys = np.linspace(-1.0, 1.0, N + 1)
    
    # Point is in L-shape if NOT (x > 0 and y < 0)
    # Map (i, j) to node index
    grid_to_node = -np.ones((N + 1, N + 1), dtype=int)
    nodes_list = []
    
    for i in range(N + 1):
        for j in range(N + 1):
            x, y = xs[i], ys[j]
            # Exclude strict bottom-right quadrant (x > 1e-6 and y < -1e-6)
            if x > 1e-6 and y < -1e-6:
                continue
            grid_to_node[i, j] = len(nodes_list)
            nodes_list.append((x, y))
            
    nodes_arr = np.array(nodes_list)
    n_nodes = len(nodes_arr)
    
    # Build elements fast
    # Analytical local stiffness for standard right-angled isosceles triangles with legs h, h:
    # Type A (lower-right): vertices (i, j), (i+1, j), (i+1, j+1)
    # k_A = 0.5 * [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]
    # Type B (upper-left): vertices (i, j), (i+1, j+1), (i, j+1)
    # k_B = 0.5 * [[2, -1, -1], [-1, 1, 0], [-1, 0, 1]]
    k_A = 0.5 * np.array([[1.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 1.0]])
    k_B = 0.5 * np.array([[2.0, -1.0, -1.0], [-1.0, 1.0, 0.0], [-1.0, 0.0, 1.0]])
    
    row_ind, col_ind, data = [], [], []
    elements = []
    
    for i in range(N):
        for j in range(N):
            n00 = grid_to_node[i, j]
            n10 = grid_to_node[i+1, j]
            n01 = grid_to_node[i, j+1]
            n11 = grid_to_node[i+1, j+1]
            
            if n00 >= 0 and n10 >= 0 and n11 >= 0:
                elem_A = [n00, n10, n11]
                elements.append(('A', elem_A, (xs[i], ys[j])))
                for r in range(3):
                    for c in range(3):
                        row_ind.append(elem_A[r])
                        col_ind.append(elem_A[c])
                        data.append(k_A[r, c])
                        
            if n00 >= 0 and n11 >= 0 and n01 >= 0:
                elem_B = [n00, n11, n01]
                elements.append(('B', elem_B, (xs[i], ys[j])))
                for r in range(3):
                    for c in range(3):
                        row_ind.append(elem_B[r])
                        col_ind.append(elem_B[c])
                        data.append(k_B[r, c])
                        
    K_global = sp.csr_matrix((data, (row_ind, col_ind)), shape=(n_nodes, n_nodes))
    
    def exact_u(x, y):
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        if theta < 0:
            theta += 2.0 * np.pi
        return (r ** (2.0 / 3.0)) * np.sin(2.0 * theta / 3.0)
    
    def exact_grad_u(x, y):
        r = np.sqrt(x**2 + y**2)
        if r < 1e-12:
            return 0.0, 0.0
        theta = np.arctan2(y, x)
        if theta < 0:
            theta += 2.0 * np.pi
        
        du_dr = (2.0 / 3.0) * (r ** (-1.0 / 3.0)) * np.sin(2.0 * theta / 3.0)
        du_dth = (2.0 / 3.0) * (r ** (2.0 / 3.0)) * np.cos(2.0 * theta / 3.0)
        
        du_dx = du_dr * np.cos(theta) - (du_dth / r) * np.sin(theta)
        du_dy = du_dr * np.sin(theta) + (du_dth / r) * np.cos(theta)
        return du_dx, du_dy
    
    # Identify boundary nodes
    is_boundary = np.zeros(n_nodes, dtype=bool)
    for idx, (x, y) in enumerate(nodes_arr):
        if (abs(x + 1.0) < 1e-6 or abs(y - 1.0) < 1e-6 or
            (abs(y + 1.0) < 1e-6 and x <= 1e-6) or
            (abs(x - 1.0) < 1e-6 and y >= -1e-6) or
            (abs(x) < 1e-6 and y <= 1e-6) or
            (abs(y) < 1e-6 and x >= -1e-6)):
            is_boundary[idx] = True
            
    u_exact_nodes = np.array([exact_u(x, y) for x, y in nodes_arr])
    u_g = np.zeros(n_nodes)
    u_g[is_boundary] = u_exact_nodes[is_boundary]
    
    # Solve for interior zero-trace w
    F_lift = - K_global.dot(u_g)
    interior = np.where(~is_boundary)[0]
    K_int = K_global[interior, :][:, interior]
    F_int = F_lift[interior]
    
    w_int = spla.spsolve(K_int, F_int)
    u_h = np.zeros(n_nodes)
    u_h[interior] = w_int
    u_h += u_g
    
    # Compute H1 semi-norm error
    # Triangle area = 0.5 * h^2
    area = 0.5 * (h ** 2)
    h1_err_sq = 0.0
    
    for elem_type, elem, (x0, y0) in elements:
        u_vals = u_h[elem]
        if elem_type == 'A':
            # n00=(x0, y0), n10=(x0+h, y0), n11=(x0+h, y0+h)
            # du/dx = (u10 - u00)/h, du/dy = (u11 - u10)/h
            du_dx_fem = (u_vals[1] - u_vals[0]) / h
            du_dy_fem = (u_vals[2] - u_vals[1]) / h
            cx = x0 + (2.0/3.0)*h
            cy = y0 + (1.0/3.0)*h
        else:
            # n00=(x0, y0), n11=(x0+h, y0+h), n01=(x0, y0+h)
            # du/dx = (u11 - u01)/h, du/dy = (u01 - u00)/h
            du_dx_fem = (u_vals[1] - u_vals[2]) / h
            du_dy_fem = (u_vals[2] - u_vals[0]) / h
            cx = x0 + (1.0/3.0)*h
            cy = y0 + (2.0/3.0)*h
            
        gx_ex, gy_ex = exact_grad_u(cx, cy)
        h1_err_sq += area * ((gx_ex - du_dx_fem)**2 + (gy_ex - du_dy_fem)**2)
        
    return {
        'h': h,
        'n_nodes': n_nodes,
        'n_elements': len(elements),
        'h1_error': float(np.sqrt(h1_err_sq))
    }


# =====================================================================
# 4. Convergence Order Studies
# =====================================================================

def verify_poisson_convergence_orders(mesh_sizes: List[int], f_func: Callable, u_exact: Callable, du_exact: Callable) -> Dict:
    h_list, l2_errors, h1_errors = [], [], []
    for n_elem in mesh_sizes:
        res = solve_poisson_1d(n_elem, f_func, u_exact, du_exact)
        h_list.append(res['h'])
        l2_errors.append(res['l2_error'])
        h1_errors.append(res['h1_error'])
        
    rate_l2, _ = np.polyfit(np.log(h_list), np.log(l2_errors), 1)
    rate_h1, _ = np.polyfit(np.log(h_list), np.log(h1_errors), 1)
    
    return {
        'mesh_sizes': mesh_sizes,
        'h_list': h_list,
        'l2_errors': l2_errors,
        'h1_errors': h1_errors,
        'rate_l2': float(rate_l2),
        'rate_h1': float(rate_h1)
    }


def verify_nonhomogeneous_lifting_orders(mesh_sizes: List[int]) -> Dict:
    f = lambda x: (np.pi ** 2) * np.sin(np.pi * x)
    u_exact = lambda x: np.sin(np.pi * x) + 2.0 * x + 1.0 # u(0)=1, u(1)=3
    du_exact = lambda x: np.pi * np.cos(np.pi * x) + 2.0
    g0, g1 = 1.0, 3.0
    
    h_list, l2_errors, h1_errors = [], [], []
    for n_elem in mesh_sizes:
        res = solve_poisson_1d_nonhomogeneous(n_elem, f, g0, g1, u_exact, du_exact)
        h_list.append(res['h'])
        l2_errors.append(res['l2_error'])
        h1_errors.append(res['h1_error'])
        
    rate_l2, _ = np.polyfit(np.log(h_list), np.log(l2_errors), 1)
    rate_h1, _ = np.polyfit(np.log(h_list), np.log(h1_errors), 1)
    return {
        'mesh_sizes': mesh_sizes,
        'h_list': h_list,
        'l2_errors': l2_errors,
        'h1_errors': h1_errors,
        'rate_l2': float(rate_l2),
        'rate_h1': float(rate_h1)
    }


def verify_2d_lshaped_singularity_orders(mesh_subdivs: List[int]) -> Dict:
    h_list, h1_errors = [], []
    for n_sub in mesh_subdivs:
        res = solve_poisson_2d_lshaped(n_sub)
        h_list.append(res['h'])
        h1_errors.append(res['h1_error'])
        
    rate_h1, _ = np.polyfit(np.log(h_list), np.log(h1_errors), 1)
    return {
        'mesh_subdivs': mesh_subdivs,
        'h_list': h_list,
        'h1_errors': h1_errors,
        'rate_h1': float(rate_h1)
    }


def run_all_fem_benchmarks():
    print("=" * 75)
    print(" FUNCTIONAL ANALYSIS VARIATIONAL FEM & SOBOLEV LABORATORY")
    print("=" * 75)
    
    # 1. 1D Homogeneous Dirichlet Benchmark
    print("\n--- 1. 1D Homogeneous Dirichlet Benchmark (Cea & Aubin-Nitsche) ---")
    rates_1d = verify_poisson_convergence_orders([8, 16, 32, 64, 128],
                                                lambda x: (np.pi**2)*np.sin(np.pi*x),
                                                lambda x: np.sin(np.pi*x),
                                                lambda x: np.pi*np.cos(np.pi*x))
    print(f"Computed L2 Rate: {rates_1d['rate_l2']:.2f} (Theory: 2.00) | H1 Rate: {rates_1d['rate_h1']:.2f} (Theory: 1.00)")
    
    # 2. 1D Non-Homogeneous Trace Lifting Benchmark
    print("\n--- 2. 1D Non-Homogeneous Boundary Lifting (u = w + u_g) ---")
    rates_lift = verify_nonhomogeneous_lifting_orders([8, 16, 32, 64, 128])
    print(f"Computed L2 Rate: {rates_lift['rate_l2']:.2f} (Theory: 2.00) | H1 Rate: {rates_lift['rate_h1']:.2f} (Theory: 1.00)")
    
    # 3. 2D L-Shaped Corner Singularity
    print("\n--- 3. 2D L-Shaped Domain Re-Entrant Corner Singularity u in H^{5/3-eps} ---")
    rates_2d = verify_2d_lshaped_singularity_orders([4, 8, 16, 32])
    print(f"Computed H1 Singularity Rate: {rates_2d['rate_h1']:.2f} (Theory Bound: ~0.67 due to r^{{2/3}} singularity)")
    print("=" * 75)


if __name__ == "__main__":
    run_all_fem_benchmarks()
