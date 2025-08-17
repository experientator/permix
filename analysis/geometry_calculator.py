import logging
import math
from decimal import (
    Decimal,
    InvalidOperation,
)  # Добавил ROUND_HALF_UP для единообразия, если понадобится
from typing import Any, Dict, List, Optional, Union

from src.app.data_processing import db_manager  # Обновленный импорт

logger = logging.getLogger(__name__)

# Координационные числа по умолчанию для расчетов
DEFAULT_CN_A = 12
DEFAULT_CN_B = 6
DEFAULT_CN_X = 6  # Обычно для аниона в октаэдре с B, или в кубооктаэдре с A
# Порог для проверки деления на ноль и незначительных значений
ZERO_THRESHOLD = Decimal("1e-9")


def _get_radius(symbol: str, charge: int, cn: int) -> Optional[Decimal]:
    """
    Внутренняя функция-обертка для получения радиуса из db_manager
    и преобразования его в Decimal.
    """
    radius_float = db_manager.get_ionic_radius(symbol, charge, cn)
    if radius_float is None:
        # db_manager.get_ionic_radius уже должен логировать отсутствие или null
        return None
    try:
        # Используем строку для точности преобразования float -> Decimal
        radius_decimal = Decimal(str(radius_float))
        # Проверка, что радиус положительный
        if radius_decimal <= ZERO_THRESHOLD:
            logger.warning(
                f"GEOM_CALC: Радиус для {symbol} (заряд {charge}, CN {cn}) равен или меньше нуля ({radius_decimal}). Возвращается None."
            )
            return None
        return radius_decimal
    except InvalidOperation:
        logger.error(
            f"GEOM_CALC: Не удалось преобразовать радиус {radius_float} для {symbol} в Decimal."
        )
        return None


def calculate_effective_radius(
    components: List[Dict[str, Any]],
    charge: int,
    cn: int,
    fraction_key: str = "fraction_on_site",  # Ключ для доли компонента
) -> Optional[Decimal]:
    """
    Рассчитывает эффективный ионный радиус для смешанного сайта (например, A или X).
    Использует линейную комбинацию радиусов компонентов r_eff = sum(x_i * r_i).

    Args:
        components: Список словарей компонентов на сайте. Каждый словарь
                    должен содержать 'symbol' и ключ с долей (fraction_key).
        charge: Целевой заряд ионов на этом сайте (для получения индивидуальных радиусов).
        cn: Целевое координационное число (для получения индивидуальных радиусов).
        fraction_key: Ключ в словаре component, указывающий на долю.
                      Для катионов это "fraction_on_site", для анионов "fraction".

    Returns:
        Усредненный радиус как Decimal, или None если радиус для любого
        значимого компонента не найден или сумма долей некорректна.
    """
    if not components:
        logger.warning(
            "GEOM_CALC: calculate_effective_radius: Получен пустой список компонентов."
        )
        return None

    total_fraction = Decimal("0.0")
    weighted_radius_sum = Decimal("0.0")
    missing_radius_for_significant_component = False

    for comp_data in components:
        symbol = comp_data.get("symbol")
        fraction_val = comp_data.get(fraction_key)

        if not symbol:
            logger.warning(
                "GEOM_CALC: calculate_effective_radius: Пропущен компонент без символа."
            )
            continue

        try:
            # Доля может быть уже Decimal или строкой (например, из JSON избранного)
            if isinstance(fraction_val, Decimal):
                fraction = fraction_val
            elif fraction_val is not None:
                fraction = Decimal(str(fraction_val))
            else:  # fraction_val is None
                fraction = Decimal("0.0")

            if (
                fraction < ZERO_THRESHOLD
            ):  # Пропускаем компоненты с нулевой или незначительной долей
                continue
        except (InvalidOperation, TypeError) as e:
            logger.warning(
                f"GEOM_CALC: calculate_effective_radius: Некорректная доля '{fraction_val}' для {symbol}. Ошибка: {e}. Пропуск компонента."
            )
            continue  # Пропускаем этот компонент

        total_fraction += fraction
        radius_comp = _get_radius(symbol, charge, cn)

        if radius_comp is None:
            logger.warning(
                f"GEOM_CALC: calculate_effective_radius: Не найден радиус для компонента {symbol} (заряд {charge}, CN {cn}) с долей {fraction}. "
                "Расчет эффективного радиуса невозможен."
            )
            missing_radius_for_significant_component = True
            break  # Если для значимого компонента нет радиуса, дальше считать нет смысла
        else:
            weighted_radius_sum += fraction * radius_comp

    if missing_radius_for_significant_component:
        return None

    # Проверка суммы долей (должна быть близка к 1.0 для корректного расчета)
    # Допуск 0.01 (1%)
    if abs(total_fraction - Decimal("1.0")) > Decimal("0.01"):
        logger.warning(
            f"GEOM_CALC: calculate_effective_radius: Сумма долей ({total_fraction:.4f}) для расчета эффективного радиуса "
            f"существенно отличается от 1.0. Результат может быть неточным."
        )
        # Можно решить, возвращать ли None или результат "как есть".
        # Если сумма долей 0, то делить нельзя.
        if total_fraction <= ZERO_THRESHOLD:
            logger.error(
                "GEOM_CALC: Сумма долей равна нулю, невозможно рассчитать эффективный радиус."
            )
            return None
    elif (
        total_fraction <= ZERO_THRESHOLD
    ):  # Если сумма долей 0, но прошла проверку выше (маловероятно)
        logger.warning(
            "GEOM_CALC: calculate_effective_radius: Общая доля компонентов равна нулю. Невозможно рассчитать радиус."
        )
        return None

    # Нормализация не требуется, если мы используем r_eff = sum(x_i * r_i),
    # и сумма x_i предполагается равной 1. Если она не равна 1, это проблема входных данных.
    # Однако, если мы все же хотим получить результат, можно раскомментировать нормализацию:
    # effective_radius = weighted_radius_sum / total_fraction
    # Но лучше, чтобы данные были корректны на входе.
    # Сейчас мы просто возвращаем сумму произведений долей на радиусы.
    effective_radius = weighted_radius_sum
    return effective_radius


def _calculate_goldschmidt_factor(
    rA: Decimal, rB: Decimal, rX: Decimal
) -> Optional[Decimal]:
    """Рассчитывает фактор толерантности Гольдшмидта t = (rA + rX) / (sqrt(2) * (rB + rX))."""
    denominator_sum = rB + rX
    if abs(denominator_sum) < ZERO_THRESHOLD:
        logger.error(
            "GEOM_CALC: _calculate_goldschmidt_factor: Сумма (rB + rX) близка к нулю. Делитель будет нулевым."
        )
        return None

    denominator = denominator_sum * Decimal(str(math.sqrt(2)))
    if abs(denominator) < ZERO_THRESHOLD:  # Дополнительная проверка на всякий случай
        logger.error(
            "GEOM_CALC: _calculate_goldschmidt_factor: Делитель (rB + rX) * sqrt(2) близок к нулю. Невозможно рассчитать t."
        )
        return None
    try:
        t_factor = (rA + rX) / denominator
        return t_factor  # Округление будет в вызывающей функции или при форматировании
    except (
        Exception
    ) as e:  # Ловим возможные ошибки деления, хотя проверки выше должны их предотвратить
        logger.error(
            f"GEOM_CALC: _calculate_goldschmidt_factor: Ошибка при расчете t: {e}"
        )
        return None


def _calculate_octahedral_factor(rB: Decimal, rX: Decimal) -> Optional[Decimal]:
    """Рассчитывает октаэдрический фактор μ = rB / rX."""
    if abs(rX) < ZERO_THRESHOLD:
        logger.error(
            "GEOM_CALC: _calculate_octahedral_factor: Радиус аниона rX близок к нулю. Невозможно рассчитать μ."
        )
        return None
    try:
        mu_factor = rB / rX
        return mu_factor  # Округление в вызывающей функции или при форматировании
    except Exception as e:
        logger.error(
            f"GEOM_CALC: _calculate_octahedral_factor: Ошибка при расчете μ: {e}"
        )
        return None


def calculate_geometry_factors(
    cation_config: Dict[str, List[Dict[str, Any]]],
    anion_config: Dict[str, Any],
    template_data: Dict[str, Any],
) -> Dict[str, Union[Decimal, str, None]]:
    """
    Рассчитывает геометрические факторы (t, μ) для заданного состава и шаблона.

    Args:
        cation_config: Словарь конфигурации катионов (ключ - имя сайта).
                       Доли катионов ("fraction_on_site") должны быть Decimal.
        anion_config: Словарь конфигурации анионов.
                      Доли анионов ("fraction") должны быть Decimal.
        template_data: Словарь данных для выбранного шаблона.

    Returns:
        Словарь с рассчитанными факторами.
        Значения могут быть Decimal, строкой "N/A" (неприменимо) или None (ошибка расчета).
        Пример: {'t': Decimal('0.912'), 'mu': Decimal('0.541')}
                 {'t': "N/A", 'mu': Decimal('0.600')}
                 {'t': None, 'mu': None, 'mu_prime': None, 'mu_double_prime': None, 'error': "Сообщение об ошибке"}
    """
    results: Dict[str, Union[Decimal, str, None]] = {
        "t": None,
        "mu": None,
        "mu_prime": None,
        "mu_double_prime": None,
    }
    # Сообщение об ошибке, если что-то пойдет не так
    error_message: Optional[str] = None

    if not template_data or not cation_config or not anion_config:
        logger.error(
            "GEOM_CALC: calculate_geometry_factors: Отсутствуют входные данные (конфиг или шаблон)."
        )
        results["error"] = "Отсутствуют входные данные для расчета геом. факторов."
        return results  # Не можем продолжать

    dimensionality = template_data.get("dimensionality")
    sites_info_from_template = template_data.get("sites", {})
    anion_mix_list = anion_config.get("anion_mix", [])

    # --- 1. Расчет эффективного радиуса аниона rX ---
    # Предполагается, что anion_mix_list содержит доли как Decimal
    rX_eff = calculate_effective_radius(
        anion_mix_list, charge=-1, cn=DEFAULT_CN_X, fraction_key="fraction"
    )
    if rX_eff is None:
        error_message = "Не удалось рассчитать эффективный радиус аниона rX."
        logger.error(f"GEOM_CALC: {error_message}")
        results["error"] = error_message
        return results  # Критическая ошибка, без rX ничего не посчитать

    # --- 2. Определение ключевых сайтов из шаблона ---
    # (используем .lower() для большей гибкости к регистру ключей в JSON)
    a_site_key_config = next(
        (k for k in sites_info_from_template if k.lower().startswith("a_site")), None
    )
    spacer_site_key_config = next(
        (k for k in sites_info_from_template if k.lower().startswith("spacer")), None
    )
    # Для B-сайтов ищем более точные совпадения
    b_site_key_config = next(
        (k for k in sites_info_from_template if k.lower() == "b_site"), None
    )
    b_prime_key_config = next(
        (k for k in sites_info_from_template if k.lower().startswith("b_prime")), None
    )
    b_double_prime_key_config = next(
        (k for k in sites_info_from_template if k.lower().startswith("b_double_prime")),
        None,
    )

    # --- 3. Расчет эффективных радиусов катионов ---
    rA_eff: Optional[Decimal] = None
    rB_eff: Optional[Decimal] = None  # Для обычного B-сайта
    rB_prime_eff: Optional[Decimal] = None  # Для B' в двойных
    rB_double_prime_eff: Optional[Decimal] = None  # Для B'' в двойных
    rB_overall_avg_for_t: Optional[Decimal] = None  # Средний B для расчета t в двойных

    # A-сайт (или Spacer-сайт, если A-сайта нет но есть спейсер)
    # Радиус A нужен для фактора Гольдшмидта (t)
    actual_a_site_key_for_radius = a_site_key_config or spacer_site_key_config

    if actual_a_site_key_for_radius and actual_a_site_key_for_radius in cation_config:
        a_components_list = cation_config[actual_a_site_key_for_radius]
        # Берем первый разрешенный заряд для A-сайта из шаблона
        a_charge = sites_info_from_template[actual_a_site_key_for_radius].get(
            "allowed_valences", [0]
        )[0]
        if a_charge > 0:
            rA_eff = calculate_effective_radius(
                a_components_list, charge=a_charge, cn=DEFAULT_CN_A
            )
            if rA_eff is None:
                logger.warning(
                    f"GEOM_CALC: Не удалось рассчитать rA для сайта {actual_a_site_key_for_radius}. Фактор 't' может быть не рассчитан."
                )
        else:
            logger.warning(
                f"GEOM_CALC: Некорректный или отсутствующий заряд для A-сайта {actual_a_site_key_for_radius} в шаблоне."
            )
    elif dimensionality == 3:  # Если 3D, а A-катиона нет в конфиге или шаблоне
        logger.warning(
            "GEOM_CALC: Для 3D структуры не найден A-сайт в конфигурации или шаблоне. Фактор 't' не будет рассчитан."
        )

    # B-сайты (обычный или двойной)
    is_double_perovskite_structure = b_prime_key_config and b_double_prime_key_config

    if is_double_perovskite_structure:
        # B' сайт
        if b_prime_key_config in cation_config:
            bp_components = cation_config[b_prime_key_config]
            bp_charge = sites_info_from_template[b_prime_key_config].get(
                "allowed_valences", [0]
            )[0]
            if bp_charge > 0:
                rB_prime_eff = calculate_effective_radius(
                    bp_components, charge=bp_charge, cn=DEFAULT_CN_B
                )
            else:
                logger.warning(
                    f"GEOM_CALC: Некорректный заряд для B'-сайта {b_prime_key_config}."
                )
        # B'' сайт
        if b_double_prime_key_config in cation_config:
            bdp_components = cation_config[b_double_prime_key_config]
            bdp_charge = sites_info_from_template[b_double_prime_key_config].get(
                "allowed_valences", [0]
            )[0]
            if bdp_charge > 0:
                rB_double_prime_eff = calculate_effective_radius(
                    bdp_components, charge=bdp_charge, cn=DEFAULT_CN_B
                )
            else:
                logger.warning(
                    f"GEOM_CALC: Некорректный заряд для B''-сайта {b_double_prime_key_config}."
                )

        if rB_prime_eff and rB_double_prime_eff:
            rB_overall_avg_for_t = (rB_prime_eff + rB_double_prime_eff) / Decimal("2.0")
        elif rB_prime_eff is None and rB_double_prime_eff is None:
            error_message = (
                error_message or ""
            ) + "Не удалось рассчитать радиусы для B' и B'' сайтов. "
        elif rB_prime_eff is None:
            error_message = (
                error_message or ""
            ) + "Не удалось рассчитать радиус для B'-сайта. "
        elif rB_double_prime_eff is None:
            error_message = (
                error_message or ""
            ) + "Не удалось рассчитать радиус для B''-сайта. "

    elif b_site_key_config and b_site_key_config in cation_config:  # Обычный B-сайт
        b_components_list = cation_config[b_site_key_config]
        b_charge = sites_info_from_template[b_site_key_config].get(
            "allowed_valences", [0]
        )[0]
        if b_charge > 0:
            rB_eff = calculate_effective_radius(
                b_components_list, charge=b_charge, cn=DEFAULT_CN_B
            )
            if rB_eff is None:
                error_message = (
                    error_message or ""
                ) + f"Не удалось рассчитать rB для сайта {b_site_key_config}. "
        else:
            logger.warning(
                f"GEOM_CALC: Некорректный заряд для B-сайта {b_site_key_config}."
            )
            error_message = (
                error_message or ""
            ) + f"Некорректный заряд для B-сайта {b_site_key_config}. "
    else:  # Если B-сайта нет (например, для некоторых 0D или специфических шаблонов)
        logger.info(
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
            if rB_prime_eff and rX_eff:
                results["mu_prime"] = _calculate_octahedral_factor(rB_prime_eff, rX_eff)
            if rB_double_prime_eff and rX_eff:
                results["mu_double_prime"] = _calculate_octahedral_factor(
                    rB_double_prime_eff, rX_eff
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
            if rB_prime_eff and rX_eff:
                results["mu_prime"] = _calculate_octahedral_factor(rB_prime_eff, rX_eff)
            if rB_double_prime_eff and rX_eff:
                results["mu_double_prime"] = _calculate_octahedral_factor(
                    rB_double_prime_eff, rX_eff
                )
    else:  # Неизвестная или не указанная размерность
        logger.warning(
            f"GEOM_CALC: Неизвестная или не указанная размерность ({dimensionality}). Геометрические факторы не рассчитаны."
        )
        error_message = (
            error_message or ""
        ) + f"Неизвестная размерность ({dimensionality}). "

    # Добавляем сообщение об ошибке в результаты, если оно есть
    if error_message:
        results["error"] = error_message.strip()
        logger.error(f"GEOM_CALC: Завершено с ошибками: {results['error']}")

    # Очищаем результаты от ключей, которые остались None (кроме 'error')
    final_results = {k: v for k, v in results.items() if v is not None or k == "error"}
    if (
        not any(k in final_results for k in ["t", "mu", "mu_prime", "mu_double_prime"])
        and "error" not in final_results
    ):
        final_results["error"] = "Не удалось рассчитать ни один геометрический фактор."

    logger.info(f"GEOM_CALC: Рассчитанные геометрические факторы: {final_results}")
    return final_results