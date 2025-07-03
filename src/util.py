import psycopg2
from psycopg2 import sql
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import cvxpy as cp

# Параметры подключения к БД
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "money",
    "user": "ivan",
    "password": "password"
}


def get_problem_data():
    """Извлекает данные о проблемах и возвращает вектор кортежей (name, frequency)"""
    try:
        # Подключаемся к БД
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # SQL-запрос для выборки данных
        query = sql.SQL("""
                        SELECT name, frequency
                        FROM problem_item
                        ORDER BY id
                        """)

        cursor.execute(query)
        rows = cursor.fetchall()

        # Формируем вектор кортежей
        problem_vector = [(row[0], row[1]) for row in rows]

        return problem_vector

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return []


def get_problem_data_by_report():
    """
    Извлекает данные о проблемах, сгруппированные по отчетам.
    Возвращает словарь: {report_id: [(problem_name, frequency), ...]}
    """
    try:
        # Подключаемся к БД
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # SQL-запрос для выборки данных с группировкой по отчетам
        query = sql.SQL("""
                        SELECT p.report_id,
                               p.name,
                               p.frequency
                        FROM problem_item p
                        ORDER BY p.report_id, p.id
                        """)

        cursor.execute(query)
        rows = cursor.fetchall()

        # Группируем данные по report_id
        report_data = {}
        for report_id, name, frequency in rows:
            if report_id not in report_data:
                report_data[report_id] = []
            report_data[report_id].append((name, frequency))

        return report_data

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return {}


def get_problem_data_as_list():
    """
    Извлекает данные о проблемах, сгруппированные по отчетам.
    Возвращает список кортежей: [(report_id, [(name, frequency), ...])]
    """
    report_dict = get_problem_data_by_report()
    return list(report_dict.items())


def get_budget_items():
    """Извлекает статьи бюджета и возвращает вектор кортежей (name, min_budget)"""
    try:
        # Подключаемся к БД
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # SQL-запрос для выборки данных
        query = sql.SQL("""
                        SELECT name, min_sum
                        FROM item
                        ORDER BY id
                        """)

        cursor.execute(query)
        rows = cursor.fetchall()

        # Формируем вектор кортежей
        budget_vector = [(row[0], float(row[1])) for row in rows]

        return budget_vector

    except Exception as e:
        print(f"Ошибка при получении статей бюджета: {e}")
        return []


def get_influence_matrix():
    """Извлекает матрицу влияния: строки - статьи бюджета, столбцы - проблемы"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)

        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

        # Запрос для получения данных с именами
        query = """
                        SELECT bi.name AS budget_item,
                               pi.name AS problem_item,
                               pbl.efficiency
                        FROM problem_budget_link pbl
                                 JOIN item bi ON bi.id = pbl.budget_item_id
                                 JOIN problem_item pi ON pi.id = pbl.problem_item_id
                        ORDER BY bi.id, pi.id
                        """

        # Читаем данные в DataFrame
        df = pd.read_sql(query, engine)

        # Если данных нет, возвращаем пустые структуры
        if df.empty:
            return pd.DataFrame(), [], []

        # Создаем матрицу влияния (pivot table)
        matrix = df.pivot(
            index='budget_item',
            columns='problem_item',
            values='efficiency'
        ).fillna(0)  # Заменяем пропуски на 0

        # Получаем списки названий
        budget_items = matrix.index.tolist()
        problem_items = matrix.columns.tolist()

        return matrix, budget_items, problem_items

    except Exception as e:
        print(f"Ошибка при получении матрицы влияния: {e}")
        return pd.DataFrame(), [], []
    finally:
        if conn:
            conn.close()


def get_influence_matrix_as_array():
    """Возвращает матрицу в виде numpy array + списки названий"""
    matrix_df, budget_items, problem_items = get_influence_matrix()

    if matrix_df.empty:
        return np.array([]), [], []

    return matrix_df.to_numpy(), budget_items, problem_items


def get_influence_matrix_by_report():
    """
    Извлекает матрицы влияния, сгруппированные по отчетам.
    Возвращает словарь: {report_id: (matrix_df, budget_items, problem_items)}
    """
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

        # Запрос для получения данных с указанием отчета
        query = """
                SELECT pi.report_id, \
                       bi.name AS budget_item, \
                       pi.name AS problem_item, \
                       pbl.efficiency
                FROM problem_budget_link pbl
                         JOIN item bi ON bi.id = pbl.budget_item_id
                         JOIN problem_item pi ON pi.id = pbl.problem_item_id
                ORDER BY pi.report_id, bi.id, pi.id \
                """

        # Читаем все данные
        df = pd.read_sql(query, engine)

        if df.empty:
            return {}

        # Группируем по отчетам
        result = {}
        for report_id, group_df in df.groupby('report_id'):
            # Создаем матрицу влияния для отчета
            matrix = group_df.pivot(
                index='budget_item',
                columns='problem_item',
                values='efficiency'
            ).fillna(0)

            # Получаем списки названий
            budget_items = matrix.index.tolist()
            problem_items = matrix.columns.tolist()

            result[report_id] = (matrix, budget_items, problem_items)

        return result

    except Exception as e:
        print(f"Ошибка при получении матрицы влияния: {e}")
        return {}


def get_influence_matrix_for_report(report_id):
    """
    Извлекает матрицу влияния для конкретного отчета
    Возвращает (matrix_df, budget_items, problem_items)
    """
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

        # Запрос для конкретного отчета
        query = """
                SELECT bi.name AS budget_item, \
                       pi.name AS problem_item, \
                       pbl.efficiency
                FROM problem_budget_link pbl
                         JOIN item bi ON bi.id = pbl.budget_item_id
                         JOIN problem_item pi ON pi.id = pbl.problem_item_id
                WHERE pi.report_id = %(report_id)s
                ORDER BY bi.id, pi.id \
                """

        # Читаем данные
        df = pd.read_sql(query, engine, params={"report_id": report_id})

        if df.empty:
            return pd.DataFrame(), [], []

        # Создаем матрицу
        matrix = df.pivot(
            index='budget_item',
            columns='problem_item',
            values='efficiency'
        ).fillna(0)

        return matrix, matrix.index.tolist(), matrix.columns.tolist()

    except Exception as e:
        print(f"Ошибка при получении матрицы для отчета {report_id}: {e}")
        return pd.DataFrame(), [], []


def distribute_budget(c, B, L, A, mu=0.0):
    """
    Распределяет бюджетные средства на основе частоты упоминаний проблем и нижних пороговых ограничений.

    Параметры:
    n (int): число проблем
    m (int): число статей расходов
    w (np.array): веса статей
    c (np.array): частоты упоминаний проблем
    B (float): общий бюджет
    L (np.array): нижние пороговые ограничения для статей расходов
    a (np.array): матрица коэффициентов связи между проблемами и статьями расходов

    Возвращает:
    np.array: оптимальное распределение бюджета по статьям расходов
    """
    n = len(c)
    m = len(L)

    # Переменные для оптимизации
    x = cp.Variable(m, nonneg=True)
    l = L / sum(L)

    # y = c / c.sum()
    y = c / c.sum() * B

    # Целевая функция
    I = A @ x - y
    # I = A @ x * B - y

    loss = cp.sum_squares(I)
    reg_loss = cp.sum_squares(x)

    # objective = cp.Minimize(loss)
    objective = cp.Minimize(loss + mu * reg_loss)

    # Ограничения
    constraints = [
        cp.sum(x) == B,
        x >= L,
    ]
    # Задача оптимизации
    problem = cp.Problem(objective, constraints)

    # Решение задачи
    problem.solve(solver=cp.OSQP)
    # problem.solve(verbose=True)

    # Проверка статуса решения
    if problem.status in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        x_v = x.value
        e = A @ x_v - y

        mae = np.mean(np.abs(e))
        mse = np.mean(e ** 2)
        rmse = np.sqrt(np.mean(e ** 2))

        return x_v, mae, mse, rmse
    else:
        return None
    
    
def dp_budget_allocation(c, B, L, A, K=100):
    """
    Приближение L2‑задачи через DP с дискретизацией:
      x_j = k_j * δ,  δ = B/K,  sum k_j = K.

    Возвращает вектор x длины m.
    """
    n, m = A.shape
    # 1) Целевые абсолютные расходы по проблемам
    y = (c / c.sum()) * B
    # 2) Распределяем эти расходы по статьям
    y_art = A.T @ y   # в идеале x_j ~ y_art[j]

    d = B / K
    # минимум гранул на j-ю статью
    kmin = np.ceil(L/d).astype(int)

    # DP таблица
    dp = np.full((m+1, K+1), np.inf)
    dp[0,0] = 0
    # back‑pointer
    parent = np.zeros((m+1, K+1), int)

    for j in range(1, m+1):
        for k in range(K+1):
            for q in range(kmin[j-1], k+1):
                prev = dp[j-1, k-q]
                cost = (q*d - y_art[j-1])**2
                val = prev + cost
                if val < dp[j, k]:
                    dp[j, k] = val
                    parent[j, k] = q

    # восстанавливаем k_j
    k = K
    ks = np.zeros(m, int)
    for j in range(m, 0, -1):
        q = parent[j, k]
        ks[j-1] = q
        k -= q

    # финальное распределение
    x = ks * d

    e = A @ x - y

    mae = np.mean(np.abs(e))
    mse = np.mean(e ** 2)
    rmse = np.sqrt(np.mean(e ** 2))

    return x, mae, mse, rmse


# def perform_foundation_distribution(B, problem_report_id, distro_func=dp_budget_allocation, *distro_args):
#     matrix, budget_labels, problem_labels = get_influence_matrix_for_report(problem_report_id)
#
#     problems_by_rep = get_problem_data_by_report()[problem_report_id]
#     budget_items = get_budget_items()
#
#     print(f'problems_by_report = {problems_by_rep}')
#
#     A = matrix.to_numpy().T
#     L = np.array([B / len(A[0]) / 5] * len(A[0]))
#     c = np.array([p[1] for p in problems_by_rep])
#
#     result, mae, mse, rmse = distro_func(c, B, L, A, *distro_args)
#
#     print(f'распределение методом дин программирования = {result}')
#     print(f'B sum = {np.sum(result)}')
#     print(f"Средняя абсолютная ошибка (mae): {mae / B:.2f}")
#     print(f"Среднеквадратичная ошибка (mse): {mse:.4f}")
#     print(f"Среднеквадратичная ошибка (rmse): {rmse:.2f}")




# if __name__ == "__main__":
#     # Получаем данные
#     problems_by_report = get_problem_data_by_report()
#
#     # Выводим результат
#     for report_id, problems in problems_by_report.items():
#         print(f"\nОтчет #{report_id}:")
#         for i, (name, freq) in enumerate(problems, 1):
#             print(f"  {i}. {name} (частота: {freq})")
#
#     # Или в виде списка кортежей
#     problems_list = get_problem_data_as_list()
#     print(f'problems_list = {problems_list[0][1]}')
#     print("\nДанные в виде списка кортежей:")
#     for report_id, problems in problems_list:
#         print(f"Отчет {report_id}: {len(problems)} проблем")
#
#     budget_items = get_budget_items()
#
#     # Выводим результат
#     print(f"Получено {len(budget_items)} статей бюджета:")
#     for i, (name, min_budget) in enumerate(budget_items, 1):
#         print(f"{i}. {name} (мин. бюджет: {min_budget:,.2f} руб.)")
#
#     # Пример использования вектора
#     print("\nВектор кортежей:")
#     print(budget_items)
#
#     # Получаем все матрицы по отчетам
#     all_matrices = get_influence_matrix_by_report()
#
#     # Выводим информацию по каждому отчету
#     for report_id, (matrix, budget_items, problem_items) in all_matrices.items():
#         print(f"\nОтчет #{report_id}")
#         print(f"Статьи бюджета: {budget_items}")
#         print(f"Проблемы: {problem_items}")
#         print("Матрица влияния:")
#         print(matrix)
#         matrix.to_csv(f"influence_matrix_report_{report_id}.csv")
#
#     # Получаем матрицу для конкретного отчета
#     report_id = 2
#     matrix, budget_items, problem_items = get_influence_matrix_for_report(report_id)
#
#     # if not matrix.empty:
#     print(f"\nМатрица для отчета #{report_id} ({len(problem_items)} проблем):")
#     print(matrix.head())
#
#     # Использование в оптимизации
#     A = matrix.to_numpy().T  # Транспонируем для модели (проблемы x статьи)
#     print(f"Размерность матрицы для оптимизации: {A.shape}")
#
#     c = np.array([p[1] for p in problems_list[1][1]])
#     B = 10**6
#     a = A
#     L = np.array([B / len(a[0]) / 5] * len(a[0]))
#
#     res, d_mae, d_mse, d_rmse = dp_budget_allocation(c, B, L, A, K=100)
#     v = c / sum(c)
#     print(f'распределение методом дин программирования = {res}')
#     print(f'B sum = {np.sum(res)}')
#     print(f"Средняя абсолютная ошибка (mae): {d_mae / B:.2f}")
#     print(f"Среднеквадратичная ошибка (mse): {d_mse:.4f}")
#     print(f"Среднеквадратичная ошибка (rmse): {d_rmse:.2f}")
#
#     result, mae, mse, rmse = distribute_budget(c, B, L, a)
#
#     if result is not None:
#         print("Оптимальное распределение бюджета:")
#         # result *= B
#         for j in range(len(result)):
#             print(f"Статья расходов {j + 1}: {result[j]:.2f}")
#
#         # Вычисление ошибки
#         print(f"Среднеквадратичная ошибка (mae): {mae / B:.2f}")
#         print(f"Среднеквадратичная ошибка (mse): {mse:.4f}")
#         print(f"Среднеквадратичная ошибка (rmse): {rmse:.2f}")
#     else:
#         print("Задача не имеет оптимального решения.")