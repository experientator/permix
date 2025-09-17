from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

def prepare_and_draw_mass_histogram(equations_to_plot, target_frame, title_suffix = ""):
    if not target_frame:
        print("Ошибка: Контейнер для гистограммы не найден")
        return

    if not equations_to_plot:
        _draw_empty_histogram(target_frame, title_suffix)
        return

    plot_data = {}
    equation_labels = []
    all_salts = set()

    for i, eq_data in enumerate(equations_to_plot):
        eq_num = eq_data.get('eq_key_numeric', i + 1)
        equation_labels.append(f"Eq.{eq_num}")

        masses = eq_data.get("masses_g_final_k", {})
        for salt, mass in masses.items():
            all_salts.add(salt)
            if salt not in plot_data:
                plot_data[salt] = [0.0] * len(equations_to_plot)

            mass_val = _convert_mass_to_float(mass)
            plot_data[salt][i] = mass_val

    salt_order = sorted(all_salts)
    salt_colors = _get_salt_colors(salt_order)

    title = f"Гистограмма Масс Реагентов {title_suffix}".strip()
    _draw_histogram(
        target_frame,
        plot_data,
        equation_labels,
        salt_order,
        salt_colors,
        title
    )


def _draw_empty_histogram(target_frame, title_suffix):
    for widget in target_frame.winfo_children():
        widget.destroy()
    tk.Label(target_frame, text=f"Нет данных для гистограммы {title_suffix}").pack(padx=5, pady=5)


def _convert_mass_to_float(mass_value):
    if mass_value in [None, "ERROR", "N/A"]:
        return 0.0
    try:
        return float(mass_value)
    except (ValueError, TypeError):
        return 0.0


def _get_salt_colors(salts):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    return {salt: colors[i % len(colors)] for i, salt in enumerate(salts)}


def _draw_histogram(target_frame, plot_data, equation_labels, salt_order, salt_colors, title):
    _draw_histogram_generic(
        target_frame=target_frame,
        plot_data=plot_data,
        equation_labels=equation_labels,
        salt_order=salt_order,
        salt_colors=salt_colors,
        x_axis_label="Уравнения",
        y_axis_label="Масса (г)",
        title=title
    )


def _draw_histogram_generic(
        target_frame,
        plot_data,
        equation_labels,
        salt_order,
        salt_colors,
        x_axis_label,
        y_axis_label,
        title,
        single_bar_values=None,
        single_bar_color="cornflowerblue"
):
    # Очищаем целевой фрейм
    for widget in target_frame.winfo_children():
        widget.destroy()

    # Проверяем наличие данных для построения
    has_data = False
    if single_bar_values is not None:
        has_data = any(v is not None and v > 1e-9 for v in single_bar_values)
    else:
        has_data = any(
            any(v > 1e-9 for v in values)
            for values in plot_data.values()
        )

    if not has_data:
        tk.Label(target_frame, text="Нет данных для гистограммы.").pack(padx=5, pady=5)
        return

    try:
        # Создаем фигуру
        fig, ax = plt.subplots(figsize=(8, 4))

        num_equations = len(equation_labels)
        bar_width = 0.6 if num_equations <= 5 else 0.8

        if single_bar_values is not None:
            # Простая гистограмма с одним столбцом на уравнение
            values = [v if v is not None else 0.0 for v in single_bar_values]
            ax.bar(equation_labels, values, color=single_bar_color, width=bar_width)
        else:
            # Сложенная гистограмма
            bottoms = [0] * num_equations
            for salt in salt_order:
                values = plot_data.get(salt, [0.0] * num_equations)
                ax.bar(
                    equation_labels,
                    values,
                    bottom=bottoms,
                    label=salt,
                    color=salt_colors.get(salt, "grey"),
                    width=bar_width
                )
                bottoms = [b + v for b, v in zip(bottoms, values)]

            # Добавляем легенду если есть данные
            if salt_order:
                ax.legend(title="Прекурсоры", bbox_to_anchor=(1.05, 1), loc='upper left')

        # Настраиваем внешний вид
        ax.set_ylabel(y_axis_label)
        ax.set_xlabel(x_axis_label)
        ax.set_title(title)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Поворачиваем подписи если много уравнений
        if num_equations > 5:
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        # Создаем canvas и отображаем
        canvas = FigureCanvasTkAgg(fig, master=target_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    except Exception as e:
        print(f"Ошибка при построении гистограммы: {e}")
        tk.Label(target_frame, text="Ошибка построения", fg="red").pack(padx=5, pady=5)