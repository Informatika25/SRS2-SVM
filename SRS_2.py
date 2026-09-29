import math
import numpy as np
import pandas as pd
from scipy import optimize


# f(x) = exp(x) - 3*x = 0

def f(x):
    return math.exp(x) - 3 * x

def df(x):
    return math.exp(x) - 3


# x = phi(x) (функция для простой итерации)

def phi(x):
    return math.exp(x) / 3.0

def dphi(x):
    return math.exp(x) / 3.0


# 1.ТАБУЛИРОВАНИЕ ФУНКЦИИ

def tabulation(a, b, step):

    print("\n=== ТАБУЛИРОВАНИЕ ФУНКЦИИ ===")
    print(f"{'x':>10} {'f(x)':>15}")
    print("-" * 27)

    x_values = np.arange(a, b + step / 2, step)

    for x in x_values:
        print(f"{x:10.2f} {f(x):15.6f}")



# 2.АВТОМАТИЧЕСКИЙ ПОИСК ИНТЕРВАЛА, НА КОТОРОМ f(a)*f(b)<0

def find_root_interval(a, b, step):

    x_values = np.arange(a, b + step / 2, step)

    intervals = []

    for i in range(len(x_values) - 1):

        x1 = x_values[i]
        x2 = x_values[i + 1]

        if f(x1) * f(x2) < 0:
            intervals.append((x1, x2))

    return intervals


# 3.МЕТОД БИСЕКЦИИ
def bisection_method(a, b, eps):
    iterations = []
    k = 1
    while True:
        c = (a + b) / 2
        fc = f(c)
        error = abs(b - a) / 2
        iterations.append({
            "Итерация": k,
            "Текущее приближение": a,
            "Следующее приближение": c,
            "Ошибка": error,
            "f(x)": fc
        })
        if error < eps:
            return c, k, abs(fc), iterations
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        k += 1


# 4.МЕТОД ХОРД
def chord_method(a, b, eps):
    iterations = []
    x_old = a
    k = 1
    while True:
        fa = f(a)
        fb = f(b)
        x = a - fa * (b - a) / (fb - fa)
        fx = f(x)
        error = abs(x - x_old)
        iterations.append({
            "Итерация": k,
            "Текущее приближение": x_old,
            "Следующее приближение": x,
            "Ошибка": error,
            "f(x)": fx
        })
        if error < eps:
            return x, k, abs(fx), iterations
        if fa * fx < 0:
            b = x
        else:
            a = x
        x_old = x
        k += 1


# 5.МЕТОД НЬЮТОНА
def newton_method(x0, eps):
    iterations = []
    x = x0
    k = 1
    while True:
        x_new = x - f(x) / df(x)
        error = abs(x_new - x)
        iterations.append({
            "Итерация": k,
            "Текущее приближение": x,
            "Следующее приближение": x_new,
            "Ошибка": error,
            "f(x)": f(x_new)
        })
        if error < eps:
            return x_new, k, abs(f(x_new)), iterations
        x = x_new
        k += 1


# 6.МЕТОД ПРОСТОЙ ИТЕРАЦИИ
def simple_iteration(x0, eps):
    iterations = []
    x = x0
    k = 1
    while True:
        x_new = phi(x)
        error = abs(x_new - x)
        iterations.append({
            "Итерация": k,
            "Текущее приближение": x,
            "Следующее приближение": x_new,
            "Ошибка": error,
            "f(x)": f(x_new)
        })
        if error < eps:
            return x_new, k, abs(f(x_new)), iterations
        x = x_new
        k += 1


# ВЫВОД ИТЕРАЦИЙ

def print_iterations(method, iterations, eps, x0=None):

    print("\n" + "=" * 80)

    if x0 is not None:
        print(f"{method}, x0 = {x0}, eps = {eps}")
    else:
        print(f"{method}, eps = {eps}")

    print("=" * 80)

    table = pd.DataFrame(iterations)

    print(
        table.to_string(
            index=False,
            formatters={
                "Текущее приближение": "{:.8f}".format,
                "Следующее приближение": "{:.8f}".format,
                "Ошибка": "{:.8f}".format,
                "f(x)": "{:.15f}".format
            }
        )
    )


# ЧТЕНИЕ РЕЗУЛЬТАТОВ EXCEL ИЗ CSV

def read_excel_results(filename):

    df = pd.read_csv(
        filename,
        sep=";",
        encoding="cp1251"
    )

    df["Точность e"] = (
        df["Точность e"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    df["Найденный корень x*"] = (
        df["Найденный корень x*"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    df["|f(x*)|"] = (
        df["|f(x*)|"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    return df


# ПОИСК РЕЗУЛЬТАТА EXCEL

def get_excel_result(
    excel_df,
    method,
    eps,
    x0=None
):

    condition = (
        (excel_df["Метод"] == method) &
        (excel_df["Точность e"] == eps)
    )

    if x0 is not None:

        condition = condition & (
            excel_df["Начальное приближение"] == f"x0 = {int(x0)}"
        )

    return excel_df[condition].iloc[0]


# ОСНОВНАЯ ПРОГРАММА

def main():

    print("=" * 80)
    print("СРС 2. ЧИСЛЕННЫЕ МЕТОДЫ РЕШЕНИЯ НЕЛИНЕЙНОГО УРАВНЕНИЯ")
    print("=" * 80)

    # Исходный интервал
    a = 0.0
    b = 1.0
    step = 0.1

    eps_list = [1e-3, 1e-5]

    x0_list = [0.0, 1.0]

    # 1.Табулирование
    tabulation(a, b, step)

    # 2.Автоматический поиск интервала
    intervals = find_root_interval(a, b, step)

    print("\n=== ПОИСК ИНТЕРВАЛА, СОДЕРЖАЩЕГО КОРЕНЬ ===")

    for left, right in intervals:

        print(
            f"[{left:.1f}, {right:.1f}]: "
            f"f(a) * f(b) = {f(left) * f(right):.6f}"
        )

    if len(intervals) == 0:

        print("Интервал с корнем не найден.")
        return

    # Для всех численных методов используем исходный интервал [0; 1]
    left, right = a, b

    print(
        f"\nИнтервал для численных методов: "
        f"[{left:.1f}, {right:.1f}]"
    )

    # 10.Проверка сходимости простой итерации
    print("\n=== ПРОВЕРКА УСЛОВИЯ СХОДИМОСТИ ===")

    x_values = np.linspace(a, b, 100)

    derivative_values = [
        abs(dphi(x))
        for x in x_values
    ]

    max_derivative = max(derivative_values)

    print(
        f"max |phi'(x)| = {max_derivative:.6f}"
    )

    if max_derivative < 1:

        print(
            "Условие |phi'(x)| < 1 выполняется."
        )
        print(
            "Метод простой итерации сходится на данном интервале."
        )

    else:

        print(
            "Условие |phi'(x)| < 1 не выполняется."
        )

    excel_df = read_excel_results("results.csv")

    # Итоговые результаты
    results = []

    for eps in eps_list:

        # БИСЕКЦИЯ
        root, iterations, residual, log = bisection_method(
            left, right, eps
        )

        print_iterations(
            "Метод бисекции",
            log,
            eps
        )

        scipy_root = optimize.bisect(
            f,
            left,
            right,
            xtol=eps
        )

        excel_row = get_excel_result(
            excel_df,
            "Бисекция",
            eps
        )

        results.append({
            "Метод": "Бисекция",
            "eps": eps,
            "x0": "-",
            "Корень Python": root,
            "Корень Excel": excel_row["Найденный корень x*"],
            "Итерации Python": iterations,
            "Итерации Excel": excel_row["Число итераций"],
            "SciPy": scipy_root,
            "Невязка Python": residual,
            "Невязка Excel": excel_row["|f(x*)|"]
        })

        # ХОРДЫ
        root, iterations, residual, log = chord_method(
            left, right, eps
        )

        print_iterations(
            "Метод хорд",
            log,
            eps
        )

# SciPy не имеет отдельной функции regula falsi, поэтому используем метод secant как библиотечную проверку корня.
        scipy_root = optimize.root_scalar(
            f,
            x0=left,
            x1=right,
            method="secant",
            xtol=eps
        ).root

        excel_row = get_excel_result(
            excel_df,
            "Хорды",
            eps
        )

        results.append({
            "Метод": "Хорды",
            "eps": eps,
            "x0": "-",
            "Корень Python": root,
            "Корень Excel": excel_row["Найденный корень x*"],
            "Итерации Python": iterations,
            "Итерации Excel": excel_row["Число итераций"],
            "SciPy": scipy_root,
            "Невязка Python": residual,
            "Невязка Excel": excel_row["|f(x*)|"]
        })

        # НЬЮТОН x0 = 0 и x0 = 1
        for x0 in x0_list:

            root, iterations, residual, log = newton_method(
                x0,
                eps
            )

            print_iterations(
                "Метод Ньютона",
                log,
                eps,
                x0
            )

            scipy_root = optimize.newton(
                f,
                x0,
                fprime=df,
                tol=eps
            )

            excel_row = get_excel_result(
                excel_df,
                "Ньютон",
                eps,
                x0
            )

            results.append({
                "Метод": "Ньютон",
                "eps": eps,
                "x0": excel_row["Начальное приближение"],
                "Корень Python": root,
                "Корень Excel": excel_row["Найденный корень x*"],
                "Итерации Python": iterations,
                "Итерации Excel": excel_row["Число итераций"],
                "SciPy": scipy_root,
                "Невязка Python": residual,
                "Невязка Excel": excel_row["|f(x*)|"]
            })

        # ПРОСТАЯ ИТЕРАЦИЯ x0 = 0 и x0 = 1
        for x0 in x0_list:

            root, iterations, residual, log = simple_iteration(
                x0,
                eps
            )

            print_iterations(
                "Метод простой итерации",
                log,
                eps,
                x0
            )

            scipy_root = optimize.fixed_point(
                phi,
                x0,
                xtol=eps,
                method="iteration"
            )

            excel_row = get_excel_result(
                excel_df,
                "Простая итерация",
                eps,
                x0
            )

            results.append({
                "Метод": "Простая итерация",
                "eps": eps,
                "x0": excel_row["Начальное приближение"],
                "Корень Python": root,
                "Корень Excel": excel_row["Найденный корень x*"],
                "Итерации Python": iterations,
                "Итерации Excel": excel_row["Число итераций"],
                "SciPy": scipy_root,
                "Невязка Python": residual,
                "Невязка Excel": excel_row["|f(x*)|"]
            })

    result_df = pd.DataFrame(results)

    print("\n\n")
    print("=" * 120)
    print("ИТОГОВОЕ СРАВНЕНИЕ PYTHON / SCIPY / EXCEL")
    print("=" * 120)

    print(
        result_df.to_string(
            index=False,
            formatters={
                "eps": "{:.0e}".format,
                "Корень Python": "{:.8f}".format,
                "SciPy": "{:.8f}".format,
                "Корень Excel": "{:.8f}".format,
                "Невязка Python": "{:.15f}".format,
                "Невязка Excel": "{:.15f}".format
            }
        )
    )

    print("\n" + "=" * 100)
    print("РАЗНИЦА МЕЖДУ PYTHON И EXCEL")
    print("=" * 100)
    print(
        f"{'Метод':22s} "
        f"{'eps':>8s} "
        f"{'x0':>8s} "
        f"{'Δ корня':>15s} "
        f"{'Δ итераций':>12s} "
        f"{'Δ невязки':>15s}"
    )
    print("-" * 100)

    for _, row in result_df.iterrows():
        diff_root = abs(row["Корень Python"] - row["Корень Excel"])
        diff_iter = int(abs(row["Итерации Python"] - row["Итерации Excel"]))
        diff_res = abs(row["Невязка Python"] - row["Невязка Excel"])

        print(
            f"{row['Метод']:22s} "
            f"{row['eps']:>8.0e} "  
            f"{str(row['x0']):>8s} "
            f"{diff_root:>15.8f} "  
            f"{diff_iter:>12d} "
            f"{diff_res:>15.10f}"
        )


if __name__ == "__main__":
    main()