import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk, scrolledtext
from datetime import date

from gui.default_style import AppStyles
from analysis.sort_equations import sort_by_minimum_criteria, optimal_sort
from analysis.histograms import prepare_and_draw_mass_histogram
from gui.language.manager import localization_manager

d = [
("ccv_device1", "Solar Cell", "Солнечный элемент"),
("ccv_device2", "Photodetector", "Фотодетектор)"),
("ccv_device3", "Direct Conversion X-ray Detector", "Детектор рентгеновского излучения прямого преобразования"),
("ccv_device4", "Indirect Conversion X-ray Detector (Scintillator)", "Детектор рентгеновского излучения непрямого преобразования (сцинтилляторы)"),
("ccv_device5", "Light-Emitting Diode (LED)", "Светодиод (LED)"),
("ccv_device6", "Memristor", "Мемристор"),
("ccv_device7", "Laser", "Лазер"),
("ccv_device8", "Field-Effect Transistor (FET)", "Транзистор с полевым эффектом (FET)"),
("ccv_device9", "Thermoelectric Generator", "Термоэлектрический генератор"),

("ccv_dev1_prop1", "Power Conversion Efficiency (PCE) (%)", "Коэффициент полезного действия (КПД) (%)"),
("ccv_dev1_prop2", "Open-Circuit Voltage (V_oc) (V)", "Напряжение холостого хода (V_oc) (В)"),
("ccv_dev1_prop3", "Short-Circuit Current Density (J_sc) (mA/cm²)", "Плотность тока короткого замыкания (J_sc) (мА/см²)"),
("ccv_dev1_prop4", "Fill Factor (FF) (%)", "Фактор заполнения (ФЗ или FF) (%)"),
("ccv_dev1_prop5", "External Quantum Efficiency (EQE) (%)", "Внешняя квантовая эффективность (EQE) (%)"),
("ccv_dev1_prop6", "Operational Stability (h)", "Эксплуатационная стабильность (ч)"),
("ccv_dev1_prop7", "I-V Hysteresis (Hysteresis Index)", "Гистерезис вольт-амперной характеристики (индекс гистерезиса) (безразмерный)"),

("ccv_dev2_prop1", "Responsivity (R) (A/W)", "Отклик (чувствительность) (R) (А/Вт)"),
("ccv_dev2_prop2", "Specific Detectivity (D*) (Jones, cm·Hz¹/²·W⁻¹)", "Удельная обнаружительная способность (D*) (Джонс, см·Гц¹/²·Вт⁻¹)"),
("ccv_dev2_prop3", "External Quantum Efficiency (EQE) (%)", "Внешняя квантовая эффективность (EQE) (%)"),
("ccv_dev2_prop4", "Rise / Fall Time (τ_rise / τ_fall) (s, μs, ns)", "Время нарастания / спада сигнала (τ_rise / τ_fall) (с, мкс, нс)"),
("ccv_dev2_prop5", "Linear Dynamic Range (LDR) (dB)", "Линейный динамический диапазон (LDR) (дБ)"),
("ccv_dev2_prop6", "Noise Equivalent Power (NEP) (W/√Hz)", "Эквивалентная мощность шума (NEP) (Вт/√Гц)"),
("ccv_dev2_prop7", "Spectral Response Range (nm)", "Спектральный диапазон отклика (нм)"),

("ccv_dev3_prop1", "Charge Collection Efficiency (CCE) (%)", "Эффективность сбора заряда (%)"),
("ccv_dev3_prop2", "Sensitivity (μC·Gy⁻¹·cm⁻²)", "Чувствительность (мкКл·Гр⁻¹·см⁻²)"),
("ccv_dev3_prop3", "Limit of Detection (LoD) (nGy_air/s)", "Предел обнаружения (нГр_air/с)"),
("ccv_dev3_prop4", "Mobility-Lifetime Product (μτ) (cm²/V)", "Произведение подвижности и времени жизни носителей заряда (μτ) (см²/В)"),
("ccv_dev3_prop5", "Spatial Resolution (line pairs/mm, lp/mm)", "Пространственное разрешение (пар линий/мм, lp/mm)"),
("ccv_dev3_prop6", "Dark Current (nA/cm²)", "Темновой ток (нА/см²)"),
("ccv_dev3_prop7", "Signal Temporal Stability (Drift) (%/s)", "Временная стабильность сигнала (дрейф) (%/с)"),

("ccv_dev4_prop1", "Light Yield (photons/MeV)", "Световой выход (фотонов/МэВ)"),
("ccv_dev4_prop2", "Limit of Detection (LoD) (nGy_air/s)", "Предел обнаружения (нГр_air/с)"),
("ccv_dev4_prop3", "Spatial Resolution (μm or line pairs/mm, lp/mm)", "Пространственное разрешение (мкм или пар линий/мм, lp/mm)"),
("ccv_dev4_prop4", "Afterglow (% of peak after a given time)", "Послесвечение (% от пика через заданное время)"),
("ccv_dev4_prop5", "Scintillation Decay Time (ns, μs)", "Время затухания сцинтилляции (нс, мкс)"),

("ccv_dev5_prop1", "External Quantum Efficiency (EQE) (%)", "Внешняя квантовая эффективность (EQE) (%"),
("ccv_dev5_prop2", "Luminance (cd/m²)", "Яркость (кд/м²)"),
("ccv_dev5_prop3", "CIE Color Coordinates (x, y)", "Координаты цветности CIE (x, y)"),
("ccv_dev5_prop4", "Full Width at Half Maximum (FWHM) of emission spectrum (nm)", "Полуширина спектра излучения (FWHM) (нм)"),
("ccv_dev5_prop5", "Turn-on Voltage (V)", "Напряжение включения (В)"),
("ccv_dev5_prop6", "Lifetime (LT50 - time until luminance drops to 50% of its initial value) (h)", "Время жизни (LT50 - время до падения яркости до 50% от начальной) (ч)"),
("ccv_dev5_prop7", "Current Efficiency (cd/A)", "Эффективность по току (кд/А)"),

("ccv_dev6_prop1", "On/Off Resistance Ratio (R_off / R_on)", "Соотношение сопротивлений в выключенном и включенном состоянии (R_off / R_on)"),
("ccv_dev6_prop2", "Endurance (number of switching cycles) (cycles)", "Выносливость (количество циклов переключения) (циклы)"),
("ccv_dev6_prop3", "Retention Time (s)", "Время удержания данных (с)"),
("ccv_dev6_prop4", "Switching Speed (s, ns, ps)", "Скорость переключения (с, нс, пс)"),
("ccv_dev6_prop5", "Set/Reset Voltages (V_set / V_reset) (V)", "Напряжения установки/сброса (V_set / V_reset) (В)"),
("ccv_dev6_prop6", "Multilevel Capability (number of distinguishable resistance states) (number of levels)", "Многоуровневость (количество различимых состояний сопротивления) (число уровней)"),

("ccv_dev7_prop1", "Lasing Threshold (μJ/cm² or kW/cm²)", "Порог генерации (мкДж/см² или кВт/см²)"),
("ccv_dev7_prop2", "Quality Factor (Q-factor)", "Добротность (Q-фактор)"),
("ccv_dev7_prop3", "Linewidth of laser emission (nm)", "Ширина линии лазерной генерации (нм)"),
("ccv_dev7_prop4", "Differential Quantum Efficiency (%)", "Дифференциальная квантовая эффективность (%)"),

("ccv_dev8_prop1", "Carrier Mobility (μ) (cm²/V·s)", "Подвижность носителей заряда (μ) (см²/В·с)"),
("ccv_dev8_prop2", "On/Off Current Ratio (I_on / I_off)", "Соотношение токов во включенном и выключенном состоянии (I_on / I_off)"),
("ccv_dev8_prop3", "Threshold Voltage (V_th) (V)", "Пороговое напряжение (V_th) (В)"),
("ccv_dev8_prop4", "Subthreshold Swing (SS) (mV/decade)", "Подпороговый наклон (S) (мВ/декада)"),

("ccv_dev9_prop1", "Thermoelectric Figure of Merit (ZT)", "Термоэлектрическая добротность (ZT)"),
("ccv_dev9_prop2", "Seebeck Coefficient (S) (μV/K)", "Коэффициент Зеебека (S) (мкВ/К)"),
("ccv_dev9_prop3", "Electrical Conductivity (σ) (S/m)", "Электропроводность (σ) (См/м)"),
("ccv_dev9_prop4", "Thermal Conductivity (κ) (W/(m·K))", "Теплопроводность (κ) (Вт/(м·К))"),

]


class UserConfigView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        localization_manager.register_observer(self)

        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.build_ui()
        self.create_template_frame()
        self.dynamic_widgets = []

    def build_ui(self):
        main_frame = tk.Frame(self, **AppStyles.frame_style())
        main_frame.pack(fill="both", expand=True)

        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=10, pady=5)

        first_column_container = tk.Frame(self.paned_window, **AppStyles.frame_style())
        self.paned_window.add(first_column_container, weight=1)

        canvas1 = tk.Canvas(first_column_container, borderwidth=0, highlightthickness=0)
        scrollbar1 = tk.Scrollbar(first_column_container, orient="vertical", command=canvas1.yview)

        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)
        canvas1.configure(yscrollcommand=scrollbar1.set)

        self.first_column = tk.Frame(canvas1, **AppStyles.frame_style())
        canvas_window1 = canvas1.create_window((0, 0), window=self.first_column, anchor="nw")

        self.first_column.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
        canvas1.bind("<Configure>", lambda e: canvas1.itemconfig(canvas_window1, width=e.width))

        def bind_mousewheel1(event):
            canvas1.bind_all("<MouseWheel>", lambda e: canvas1.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        def unbind_mousewheel1(event):
            canvas1.unbind_all("<MouseWheel>")

        self.first_column.bind("<Enter>", bind_mousewheel1)
        self.first_column.bind("<Leave>", unbind_mousewheel1)

        sec_column_container = tk.Frame(self.paned_window, **AppStyles.frame_style())
        self.paned_window.add(sec_column_container, weight=3)

        canvas2 = tk.Canvas(sec_column_container, borderwidth=0, highlightthickness=0)
        scrollbar2 = tk.Scrollbar(sec_column_container, orient="vertical", command=canvas2.yview)

        scrollbar2.pack(side="right", fill="y")
        canvas2.pack(side="left", fill="both", expand=True)
        canvas2.configure(yscrollcommand=scrollbar2.set)

        self.sec_column = tk.Frame(canvas2, **AppStyles.frame_style())
        canvas_window2 = canvas2.create_window((0, 0), window=self.sec_column, anchor="nw")

        self.sec_column.bind("<Configure>", lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))
        canvas2.bind("<Configure>", lambda e: canvas2.itemconfig(canvas_window2, width=e.width))

        def bind_mousewheel2(event):
            canvas2.bind_all("<MouseWheel>", lambda e: canvas2.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        def unbind_mousewheel2(event):
            canvas2.unbind_all("<MouseWheel>")

        self.sec_column.bind("<Enter>", bind_mousewheel2)
        self.sec_column.bind("<Leave>", unbind_mousewheel2)

    def create_template_frame(self):

        info_frame = tk.LabelFrame(self.first_column,
                                   text=localization_manager.tr("ucv_lf1"),
                                   **AppStyles.labelframe_style())
        info_frame.pack(fill='x', pady=5)

        self.results_frame = tk.LabelFrame(self.sec_column,
                                           text=localization_manager.tr("ucv_lf2"),
                                           **AppStyles.labelframe_style())
        self.results_frame.pack(fill='x', pady=5)

        self.console_text = scrolledtext.ScrolledText(
            self.results_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="black",
            fg="white",
            insertbackground="white"
        )

        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.console_text.config(state=tk.DISABLED)
        self.add_text(localization_manager.tr("ucv_cons1"))

        self.summary_frame = tk.Frame(self.results_frame, **AppStyles.frame_style())
        self.summary_frame.columnconfigure(0, weight=3)
        self.summary_frame.columnconfigure(1, weight=1)
        self.summary_frame.columnconfigure(2, weight=3)

        self.summary_label = tk.Label(self.summary_frame,
                                      text=localization_manager.tr("ucv_l1"),
                                      **AppStyles.label_style())
        self.summary_equation_number = tk.Entry(self.summary_frame, **AppStyles.entry_style(), width=5)

        self.summary_button = tk.Button(self.summary_frame,
                                        text=localization_manager.tr("ucv_but1"),
                                        command=self.get_summary, **AppStyles.button_style())

        self.sort_menu_frame = tk.LabelFrame(self.sec_column,
                                             text=localization_manager.tr("ucv_lf3"),
                                             **AppStyles.labelframe_style())

        self.sort_menu_frame.columnconfigure(0, weight=1)
        self.sort_menu_frame.columnconfigure(1, weight=1)
        self.sort_menu_frame.columnconfigure(2, weight=1)
        self.sort_menu_frame.columnconfigure(3, weight=1)

        self.first_level_label = tk.Label(self.sort_menu_frame,
                                          text=localization_manager.tr("ucv_1lvl"),
                                          **AppStyles.label_style())
        self.second_level_label = tk.Label(self.sort_menu_frame,
                                           text=localization_manager.tr("ucv_2lvl"),
                                           **AppStyles.label_style())
        self.third_level_label = tk.Label(self.sort_menu_frame,
                                          text=localization_manager.tr("ucv_3lvl"),
                                          **AppStyles.label_style())

        sort_opt = [localization_manager.tr("ucv_sort1"),
                    localization_manager.tr("ucv_sort2")]
        self.sort_options_label = tk.Label(self.sort_menu_frame,
                                           text=localization_manager.tr("ucv_sort"),
                                           **AppStyles.label_style())

        self.sort_options = ttk.Combobox(self.sort_menu_frame,
                                         **AppStyles.combobox_config(),
                                         values=sort_opt,
                                         state='readonly')

        self.first_criteria_list = [localization_manager.tr("ucv_crit_all"),
                                    localization_manager.tr("ucv_crit_num"),
                                    localization_manager.tr("ucv_crit_mass")]
        self.first_level = ttk.Combobox(self.sort_menu_frame,
                                        **AppStyles.combobox_config(), values=self.first_criteria_list)

        self.second_level = ttk.Combobox(self.sort_menu_frame,
                                         **AppStyles.combobox_config(), state='disabled')

        self.third_level = ttk.Combobox(self.sort_menu_frame,
                                        **AppStyles.combobox_config(), state='disabled')

        self.sort_button = tk.Button(self.sort_menu_frame,
                                     text=localization_manager.tr("ucv_but2"),
                                     command=self.sort_process,
                                     **AppStyles.button_style(),
                                     state='disabled')

        self.mass_reagent = ttk.Combobox(self.sort_menu_frame,
                                         **AppStyles.combobox_config(),
                                         state='readonly',
                                         width=10)
        self.mass_reagent_label = tk.Label(self.sort_menu_frame,
                                           **AppStyles.label_style(),
                                           text=localization_manager.tr("ucv_l2"))

        self.hystogram_frame = tk.Frame(self.sec_column, **AppStyles.frame_style(), width=200)
        self.num_equations_hyst_label = tk.Label(self.sort_menu_frame,
                                                 **AppStyles.label_style(),
                                                 text = localization_manager.tr("ucv_l3"))
        self.num_equations_hyst_entry = tk.Entry(self.sort_menu_frame,
                                                 **AppStyles.entry_style(),
                                                 width = 5)


        self.fav_button = tk.Button(self.first_column,
                                    text=localization_manager.tr("ucv_but3"),
                                    command=self.save_config,
                                    **AppStyles.button_style())

        tk.Label(info_frame,
                 text=localization_manager.tr("ucv_l4"),
                 **AppStyles.label_style()).pack(fill='x', pady=5)
        self.phase_template = ttk.Combobox(info_frame,
                                           values=get_templates_list(),
                                           state="readonly",
                                           **AppStyles.combobox_config())
        self.phase_template.current(0)
        self.phase_template.pack(fill='x', pady=5)

        button_frame = tk.Frame(info_frame)
        button_frame.pack(fill='x', pady=5)

        tk.Button(button_frame,
                  text=localization_manager.tr("ucv_but4"),
                  **AppStyles.button_style(),
                  command=self.open_template_form).pack(side="right", expand=True, fill = 'x', padx=2)

        self.button_entry = tk.Button(button_frame,
                                      text=localization_manager.tr("ucv_but5"),
                                      **AppStyles.button_style(),
                                      command=self.create_sites)
        self.button_entry.pack(side="right", expand=True, fill = 'x', padx=2)

        clear_btn = tk.Button(button_frame,
                              text=localization_manager.tr("ucv_but6"),
                              **AppStyles.button_style(),
                              command=self.reset_form)
        clear_btn.pack(side="right", expand=True, fill = 'x', padx=2)