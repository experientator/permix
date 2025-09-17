def _prepare_and_draw_mass_histogram(self, equations_to_plot, title_suffix = ""):
    target_frame = self.app.mass_histogram_plot_frame
    if not target_frame:
        print("Ошибка: Контейнер для гистограммы не найден")
        return

    if not equations_to_plot:
        self._draw_empty_histogram(target_frame, title_suffix)
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

            mass_val = self._convert_mass_to_float(mass)
            plot_data[salt][i] = mass_val

    salt_order = sorted(all_salts)
    salt_colors = self._get_salt_colors(salt_order)

    title = f"Гистограмма Масс Реагентов {title_suffix}".strip()
    self._draw_histogram(
        target_frame,
        plot_data,
        equation_labels,
        salt_order,
        salt_colors,
        title
    )


def _draw_empty_histogram(self, target_frame, title_suffix):
    self._draw_histogram_generic(
        target_frame,
        "mass_histogram_canvas",
        "mass_histogram_figure",
        {}, [], [], {},
        "", "",
        f"Гистограмма Масс {title_suffix}".strip(),
        single_bar_values=[],
        single_bar_color="lightgray"
    )


def _convert_mass_to_float(self, mass_value):
    if mass_value in [None, "ERROR", "N/A"]:
        return 0.0
    try:
        return float(mass_value)
    except (ValueError, TypeError):
        return 0.0


def _get_salt_colors(self, salts):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    return {salt: colors[i % len(colors)] for i, salt in enumerate(salts)}


def _draw_histogram(self, target_frame, plot_data, equation_labels, salt_order, salt_colors, title):
    self._draw_histogram_generic(
        target_frame=target_frame,
        canvas_attr_name="mass_histogram_canvas",
        figure_attr_name="mass_histogram_figure",
        plot_data=plot_data,
        equation_labels=equation_labels,
        salt_order=salt_order,
        salt_colors=salt_colors,
        x_axis_label="Уравнения",
        y_axis_label="Масса (г)",
        title=title
    )