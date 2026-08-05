import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Create assets folder if not exists
assets_dir = r"f:\-\02-Knowledge\🧠 学习系统\07-最优化方法\assets"
os.makedirs(assets_dir, exist_ok=True)

# Set scientific white style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12

def plot_condition_number():
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    
    # Z1: k=1 (circle)
    Z1 = X**2 + Y**2
    # Z2: k=10 (ellipse)
    Z2 = X**2 + 10*Y**2
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    ax1.contour(X, Y, Z1, levels=15, cmap='viridis')
    ax1.set_title('Condition Number $\kappa = 1$\n(Circular bowl)')
    ax1.set_aspect('equal')
    
    ax2.contour(X, Y, Z2, levels=15, cmap='viridis')
    ax2.set_title('Condition Number $\kappa = 10$\n(Narrow valley)')
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'condition_number.png'), dpi=150)
    plt.close()

def plot_gd_trajectory():
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + 10*Y**2
    
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.contour(X, Y, Z, levels=20, cmap='viridis', alpha=0.6)
    
    # Simulate GD trajectory (zig-zag)
    # df/dx = 2x, df/dy = 20y
    # step size lr = 0.09
    lr = 0.09
    curr = np.array([-2.5, 2.0])
    path = [curr.copy()]
    for _ in range(15):
        grad = np.array([2*curr[0], 20*curr[1]])
        curr = curr - lr * grad
        path.append(curr.copy())
    
    path = np.array(path)
    ax.plot(path[:,0], path[:,1], 'r.-', label='Gradient Descent', markersize=8)
    ax.set_title('GD on Ill-conditioned Landscape ($\kappa = 10$)\nNotice the zig-zag pattern')
    ax.set_aspect('equal')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'gd_trajectory_condition.png'), dpi=150)
    plt.close()

def plot_sgd_vs_gd():
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.contour(X, Y, Z, levels=10, cmap='Blues', alpha=0.6)
    
    # GD path
    lr = 0.1
    curr = np.array([-2.5, 2.0])
    gd_path = [curr.copy()]
    for _ in range(15):
        grad = np.array([2*curr[0], 2*curr[1]])
        curr = curr - lr * grad
        gd_path.append(curr.copy())
        
    # SGD path (with noise)
    np.random.seed(42)
    curr = np.array([-2.5, 2.0])
    sgd_path = [curr.copy()]
    for _ in range(40):
        # true grad + noise
        grad = np.array([2*curr[0], 2*curr[1]]) + np.random.randn(2)*2.0
        curr = curr - (lr*0.8) * grad
        sgd_path.append(curr.copy())
        
    gd_path = np.array(gd_path)
    sgd_path = np.array(sgd_path)
    
    ax.plot(gd_path[:,0], gd_path[:,1], 'b-', linewidth=2, label='True Gradient Descent')
    ax.plot(sgd_path[:,0], sgd_path[:,1], 'r--', alpha=0.7, label='Stochastic Gradient Descent\n(noisy trajectory)')
    
    ax.set_title('GD vs SGD Trajectory Comparison')
    ax.set_aspect('equal')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'sgd_vs_gd.png'), dpi=150)
    plt.close()

def plot_saddle_point():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2
    
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8)
    
    # Plot saddle point
    ax.scatter([0], [0], [0], color='red', s=100, label='Saddle Point (0,0)')
    
    ax.set_title('Saddle Point: $f(x,y) = x^2 - y^2$')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'saddle_point_3d.png'), dpi=150)
    plt.close()

if __name__ == '__main__':
    plot_condition_number()
    plot_gd_trajectory()
    plot_sgd_vs_gd()
    plot_saddle_point()
    print("Images generated successfully in assets/ directory.")
