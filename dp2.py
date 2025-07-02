import cvxpy as cp
import numpy as np

# Генерация тестовых данных
np.random.seed(42)
n, m = 5, 6  # 5 проблем, 10 статей
B = 1000       # Общий бюджет
c = np.random.randint(1, 6, size=n)  # Важность проблем [1-5]
l = np.random.randint(50, 100, size=m)  # Мин. бюджеты [50-100]
A = np.random.rand(m, n)  # Матрица влияния (0-1)

n = 4  # число проблем
m = 3  # число статей расходов
c = np.array([550, 145, 200, 300])  # частоты упоминаний проблем
B = 1000.0  # общий бюджет
l = np.array([100, 200, 200])  # нижние пороговые ограничения

# Коэффициенты связи (пример)
A = np.array([
    [0.7, 0.3, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.5, 0.5],
    [0.8, 0, 0.2]
]).T

# Проверка выполнимости
assert sum(l) <= B, "Нерешаемо: min бюджеты > общего бюджета"

# 1. Определение переменных
x = cp.Variable(m)  # Бюджеты статей
k = cp.Variable()   # Масштабирующий коэффициент

# 2. Параметры регуляризации
lambda_reg = 0.1    # Коэф. регуляризации
k_min = B / sum(c)  # Минимальное значение k

# 3. Формулировка задачи
objective = cp.Minimize(
    cp.sum_squares(A.T @ x - k * c) +
    lambda_reg * cp.sum_squares(x)
)

constraints = [
    cp.sum(x) == B,
    x >= l,
    k >= k_min
]

problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.ECOS, verbose=False)
# problem.solve()

# 4. Анализ результатов
if problem.status not in ["optimal", "optimal_inaccurate"]:
    raise ValueError(f"Решение не найдено: {problem.status}")

# Расчет эффектов
optimal_x = x.value
optimal_k = k.value
effect = A.T @ optimal_x
desired_effect = optimal_k * c

error = A.T @ optimal_x - optimal_k * c

mse = np.sum([e**2 for e in error])
rmse = np.sqrt(mse)

# 5. Визуализация
print(f"Оптимальное распределение (k = {optimal_k:.2f})")
print("Статья | Выделено | Мин.бюдж | Отклонение")
for j in range(m):
    print(f"{j:6} | {optimal_x[j]:7.1f} | {l[j]:8} | {optimal_x[j] - l[j]:+8.1f}")

print("\nПроблема | Факт.эффект | Желаемый | Отн.отклонение")
for i in range(n):
    dev = effect[i] - desired_effect[i]
    rel_dev = dev / desired_effect[i]
    print(f"{i:7} | {effect[i]:10.1f} | {desired_effect[i]:8.1f} | {rel_dev:+.2%}")

b_eff = B * (c / sum(c))
for i in range(n):
    print(f'budget effect = {b_eff[i]}')

print(f'mse = {mse}')
print(f'rmse = {rmse}')