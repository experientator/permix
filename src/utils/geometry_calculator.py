import math
import tkinter.messagebox as mb
from src.utils.database_utils import (get_ionic_radius, get_template_site_types,
                                      get_template_site_valences, get_dimensionality)
from src.utils.chemistry_utils import separate_cations_by_site

DEFAULT_CN_A = 12
DEFAULT_CN_B = 6
DEFAULT_CN_X = 6

SPECIAL_CN_RULES = {
    4: { # Для фазы A2BX3 (id=4)
        "b_site": {
            "Cu": 4,
            "Ag": 4
        }
    },
    5: { # Для фазы A3B2X5 (id=5)
        "b_site": {
            "Cu": 4,
            "Ag": 4
        }
    },
    6: { # Для фазы ABX2 (id=6)
        "b_site": {
            "Cu": 4,
            "Ag": 4
        }
    }
}

def show_error(message):
    mb.showerror(title="error", message=message)


def calculate_effective_radius(components, site_name, template_id, default_charge=None):
    total_fraction = 0.0
    weighted_radius_sum = 0
    missing_radius_for_significant_component = False

    for comp_data in components:
        name = comp_data.get("symbol")
        fraction = float(comp_data.get("fraction"))

        # Берем валентность из данных компонента
        charge = int(comp_data.get("valence", default_charge))

        # --- НОВАЯ ЛОГИКА ОПРЕДЕЛЕНИЯ КЧ ---
        cn_for_ion = None
        # 1. Проверяем словарь исключений
        if template_id in SPECIAL_CN_RULES:
            if site_name in SPECIAL_CN_RULES[template_id]:
                if name in SPECIAL_CN_RULES[template_id][site_name]:
                    cn_for_ion = SPECIAL_CN_RULES[template_id][site_name][name]

        # 2. Если исключения нет, используем правило по умолчанию
        if cn_for_ion is None:
            if site_name in ["a_site", "spacer"]:
                cn_for_ion = DEFAULT_CN_A
            elif site_name in ["b_site", "b_double"]:
                cn_for_ion = DEFAULT_CN_B
            else:  # Для анионов
                cn_for_ion = DEFAULT_CN_X
        # --- КОНЕЦ НОВОЙ ЛОГИКИ ---

        radius_comp = get_ionic_radius(name, charge, cn_for_ion)

        if radius_comp is None:
            # Эта ошибка теперь будет содержать правильное КЧ
            show_error(
                f"Не найден ионный радиус для компонента {name} с зарядом {charge} и коорд. числом {cn_for_ion}. Проверьте базу данных.")
            missing_radius_for_significant_component = True
            break
        else:
            radius_comp = float(radius_comp)
            weighted_radius_sum += fraction * radius_comp

    if missing_radius_for_significant_component:
        return None

    return weighted_radius_sum


def _calculate_goldschmidt_factor(rA, rB, rX):
    """Рассчитывает фактор толерантности Гольдшмидта t = (rA + rX) / (sqrt(2) * (rB + rX))."""
    denominator = (rB + rX) * math.sqrt(2)
    try:
        t_factor = (rA + rX) / denominator
        return t_factor
    except Exception as e:
        show_error(
            f"GEOM_CALC: _calculate_goldschmidt_factor: Ошибка при расчете t: {e}"
        )
        return None


def _calculate_octahedral_factor(rB, rX):
    """Рассчитывает октаэдрический фактор μ = rB / rX."""
    try:
        mu_factor = rB / rX
        return mu_factor
    except Exception as e:
        show_error(
            f"GEOM_CALC: _calculate_octahedral_factor: Ошибка при расчете μ: {e}"
        )
        return None


def get_effective_geometry_radius(cations_by_site, site_name, template_id):
    components_list = cations_by_site[site_name]
    """
    Просто передает данные в calculate_effective_radius, который теперь выполняет всю логику.
    """
    components_list = cations_by_site[site_name]

    r_eff = calculate_effective_radius(
        components_list, site_name=site_name, template_id=template_id
    )

    if r_eff is None:
        show_error(
            f"GEOM_CALC: Не удалось рассчитать эффективный радиус для сайта {site_name}."
        )
    return r_eff

def calculate_geometry_factors(cation_config, anion_config, template_id):

    results = {
        "t": None,
        "mu": None,
        "mu_prime": None,
        "mu_double_prime": None,
    }

    error_message = None
    dimensionality = get_dimensionality(template_id)

    # --- 1. Расчет эффективного радиуса аниона rX ---
    rX_eff = calculate_effective_radius(anion_config, site_name='anion', template_id=template_id, default_charge=1)

    # --- 2. Определение ключевых сайтов из шаблона ---
    # будет true or false
    a_site_config, spacer_config, b_site_config, b_double_config = get_template_site_types(template_id)

    cations_by_site = separate_cations_by_site(cation_config)

    # --- 3. Расчет эффективных радиусов катионов ---
    rA_eff = None
    rB_eff = None  # Для B-сайта
    rB_double_eff = None  # Для B'' в двойных
    rB_overall_avg_for_t = None  # Средний B для расчета t в двойных

    # Радиус A нужен для фактора Гольдшмидта (t)

    if a_site_config or spacer_config:
        if spacer_config:
            site_name = "spacer"
        if a_site_config:
            site_name = "a_site"
        rA_eff = get_effective_geometry_radius(cations_by_site, site_name, template_id)

    # B-сайты (обычный или двойной)
    is_double_perovskite_structure = b_site_config and b_double_config

    if is_double_perovskite_structure:
        # B' сайт
        if b_site_config:
            site_name = "b_site"
            rB_eff = get_effective_geometry_radius(cations_by_site, site_name, template_id)
        # B'' сайт
        if b_double_config:
            site_name = "b_double"
            rB_double_eff = get_effective_geometry_radius(cations_by_site, site_name, template_id)

        if rB_eff and rB_double_eff:
            rB_overall_avg_for_t = (rB_eff + rB_double_eff) / 2.0
        elif rB_eff is None and rB_double_eff is None:
            error_message = (
                error_message or ""
            ) + "Не удалось рассчитать радиусы для B' и B'' сайтов. "
        elif rB_eff is None:
            error_message = (
                error_message or ""
            ) + "Не удалось рассчитать радиус для B'-сайта. "
        elif rB_double_eff is None:
            error_message = (
                error_message or ""
            ) + "Не удалось рассчитать радиус для B''-сайта. "

    elif b_site_config:  # Обычный B-сайт
        site_name = "b_site"
        rB_eff = get_effective_geometry_radius(cations_by_site, site_name, template_id)

    else:  # Если B-сайта нет (например, для некоторых 0D или специфических шаблонов)
        show_error(
            "GEOM_CALC: B-сайт не найден в конфигурации или шаблоне. Факторы μ не будут рассчитаны."
        )
        # error_message не устанавливаем, так как это может быть нормальным для некоторых структур

    # --- 4. Расчет геометрических факторов ---
    if dimensionality == 3:
        if is_double_perovskite_structure:  # Двойной 3D перовскит (A2B'B''X6)
            if rA_eff and rB_overall_avg_for_t and rX_eff:
                results["t"] = _calculate_goldschmidt_factor(
                    rA_eff, rB_overall_avg_for_t, rX_eff
                )
            # μ' и μ'' рассчитываются независимо
            if rB_eff and rX_eff:
                results["mu_prime"] = _calculate_octahedral_factor(rB_eff, rX_eff)
            if rB_double_eff and rX_eff:
                results["mu_double_prime"] = _calculate_octahedral_factor(
                    rB_double_eff, rX_eff
                )
        else:  # Обычный 3D перовскит (ABX3)
            if rA_eff and rB_eff and rX_eff:
                results["t"] = _calculate_goldschmidt_factor(rA_eff, rB_eff, rX_eff)
            if rB_eff and rX_eff:
                results["mu"] = _calculate_octahedral_factor(rB_eff, rX_eff)

    elif dimensionality == 2:  # Слоистый 2D
        results["t"] = "N/A"  # Фактор Гольдшмидта обычно не применим
        # μ для B-сайта, если он есть
        if rB_eff and rX_eff:
            results["mu"] = _calculate_octahedral_factor(rB_eff, rX_eff)
        # Для 2D двойных перовскитов логика может быть сложнее, пока не реализовано

    elif dimensionality == 1 or dimensionality == 0:  # 1D или 0D структуры
        results["t"] = "N/A"
        # μ для B-сайта, если он есть
        if rB_eff and rX_eff:  # Для обычного B
            results["mu"] = _calculate_octahedral_factor(rB_eff, rX_eff)
        # Для 0D двойных (например, A4B'B''X12 или димеров)
        elif is_double_perovskite_structure:
            if rB_eff and rX_eff:
                results["mu_prime"] = _calculate_octahedral_factor(rB_eff, rX_eff)
            if rB_double_eff and rX_eff:
                results["mu_double_prime"] = _calculate_octahedral_factor(
                    rB_double_eff, rX_eff
                )
    # Добавляем сообщение об ошибке в результаты, если оно есть
    if error_message:
        show_error(f"GEOM_CALC: Завершено с ошибками: {results['error']}")

    return results