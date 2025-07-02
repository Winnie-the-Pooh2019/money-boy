import numpy as np
import pandas as pd
from scipy.optimize import minimize

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Sample data (you can replace with your own)
A = np.array([
    [1.0, 0.5, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.5, 1.0],
    [1.0, 0.1, 0.2]
])
v = np.array([550, 145, 200, 300])
B = 1000.0
L = np.array([100, 200, 200])
w = np.array([0.4, 0.3, 0.3])

# Derived targets
y = (v / v.sum()) * B


def pareto_front(A, y, B, L, w, num_points=10):
    m = A.shape[1]
    results = []

    # Objective components
    def f1(x):  # coverage error (L2)
        return np.sum((A @ x - y) ** 2)

    def f2(x):  # deviation from priority
        return np.sum((x - w * B) ** 2)

    # constraints and bounds
    cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - B}
    bounds = [(L[j], None) for j in range(m)]

    for alpha in np.linspace(0, 1, num_points):
        # Scalarized objective
        def obj(x):
            return alpha * f1(x) + (1 - alpha) * f2(x)

        x0 = np.full(m, B / m)
        res = minimize(obj, x0, bounds=bounds, constraints=cons, method='SLSQP')
        if res.success:
            x_opt = res.x
            results.append({
                'alpha': alpha,
                'f1_coverage_error': f1(x_opt),
                'f2_priority_dev': f2(x_opt),
                'x_values': x_opt
            })

    return pd.DataFrame(results)


# Compute Pareto front
df_pareto = pareto_front(A, y, B, L, w, num_points=10)

# Display results
print(df_pareto)
