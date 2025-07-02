import numpy as np
from scipy.optimize import linprog

# Параметры задачи (примерные данные)
B = 1000  # Общий бюджет
c = np.array([3, 2, 4])  # Важность проблем (n=3)
l = np.array([100, 150, 80, 120])  # Минимальные бюджеты статей (m=4)

# Матрица влияния статей на проблемы (m x n)
A = np.array([
    [0.7, 0.2, 0.4],  # Статья 0
    [0.3, 0.6, 0.5],  # Статья 1
    [0.5, 0.4, 0.8],  # Статья 2
    [0.2, 0.9, 0.1]   # Статья 3
])

# 1. Рассчет весов для статей
weights = A @ c  # Вектор весов размерности m

# 2. Проверка выполнимости ограничений
if sum(l) > B:
    raise ValueError(f"Сумма минимальных бюджетов ({sum(l)}) превышает общий бюджет ({B})")

# 3. Формулировка задачи линейного программирования
# Целевая функция: минимизация отрицательного эффекта (эквивалент максимизации)
c_obj = -weights  # Преобразование для минимизации

# Ограничения:
# Бюджетное ограничение: sum(x) <= B
A_ub = np.ones((1, len(l)))  # Матрица коэффициентов [1, 1, ..., 1]
b_ub = [B]                   # Правая часть ограничения

# Границы переменных: x_j >= l_j
bounds = [(low, None) for low in l]

# 4. Решение задачи
result = linprog(
    c=c_obj,
    A_ub=A_ub,
    b_ub=b_ub,
    bounds=bounds,
    method='highs'  # Эффективный метод для больших задач
)

# 5. Анализ результатов
if not result.success:
    raise RuntimeError(f"Оптимизация не удалась: {result.message}")

optimal_budgets = result.x
total_effect = -result.fun  # Преобразуем обратно к положительному эффекту
used_budget = sum(optimal_budgets)

# 6. Визуализация результатов
print("\nОптимальное распределение бюджета:")
print("---------------------------------")
print(f"Общий бюджет: {B:.1f}")
print(f"Использовано: {used_budget:.1f}")
print(f"Суммарный эффект: {total_effect:.2f}\n")

print("Детали по статьям:")
print("Статья | Мин. бюджет | Выделено | Вес статьи")
for j in range(len(l)):
    print(f"{j:6} | {l[j]:11.1f} | {optimal_budgets[j]:8.1f} | {weights[j]:.2f}")

# Проверка влияния на проблемы
problem_effects = A.T @ optimal_budgets
print("\nВлияние на проблемы:")
print("Проблема | Важность | Полученный эффект")
for i in range(len(c)):
    print(f"{i:7} | {c[i]:8} | {problem_effects[i]:15.2f}"),


def evaluate_solution(optimal_budgets, B, l, c, A, weights):
    # 1. Проверка ограничений
    constraints_ok = True
    if sum(optimal_budgets) > B + 1e-5:
        constraints_ok = False
    if any(optimal_budgets < l - 1e-5):
        constraints_ok = False

    # 2. Расчет эффектов
    total_effect = np.dot(weights, optimal_budgets)
    problem_effects = A.T @ optimal_budgets

    # 3. Метрики эффективности
    efficiency = total_effect / sum(optimal_budgets)
    baseline = np.dot(weights, l)
    improvement = (total_effect - baseline) / baseline if baseline > 0 else 0

    # 4. Метрики справедливости
    min_effect = min(problem_effects)
    rel_effects = problem_effects / c

    # 5. Сравнительные метрики
    uniform_budgets = np.full(len(l), B / len(l))
    uniform_effect = np.dot(weights, uniform_budgets)

    return {
        "constraints_satisfied": constraints_ok,
        "total_effect": total_effect,
        "efficiency_per_unit": efficiency,
        "improvement_vs_baseline": improvement,
        "min_effect": min_effect,
        "min_effect_relative": min(rel_effects),
        "uniform_comparison": total_effect / uniform_effect,
        "problem_coverage": np.mean(rel_effects > 0.5)
    }


# Запуск оценки
metrics = evaluate_solution(optimal_budgets, B, l, c, A, weights)

print(metrics)