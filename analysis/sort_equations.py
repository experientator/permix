def optimal_sort(equations, criteria_config, reagent):
    min_max = {}
    for config in criteria_config:
        key = config
        if config == "Масса конкретного реагента":
            key += "_" + reagent

        values = []
        for eq in equations.values():
            val = get_criterion_value(eq, config, reagent)
            if isinstance(val, (int, float)):
                values.append(val)

        if values:
            min_max[key] = {"min": min(values), "max": max(values)}
        else:
            min_max[key] = {"min": 0, "max": 1}

    weights = [0.50, 0.30, 0.20]

    for eq in equations.values():
        total_score = 0
        for i, config in enumerate(criteria_config):
            key = config
            if config == "Масса конкретного реагента":
                key += "_" + reagent

            val = get_criterion_value(eq, config, reagent)
            if isinstance(val, (int, float)) and key in min_max:
                min_v, max_v = min_max[key]["min"], min_max[key]["max"]
                if max_v > min_v:
                    norm_val = 1.0 - (val - min_v) / (max_v - min_v)
                    total_score += weights[i] * norm_val

        eq["score"] = total_score

    return sorted(equations.values(), key=lambda x: x.get("score", 0), reverse=True)

def sort_by_minimum_criteria(equations, criteria_config, reagent):

    def sort_key(eq):
        key = []
        for config in criteria_config:
            value = get_criterion_value(eq, config, reagent)
            key.append(value)
        return key

    return sorted(equations.values(), key=sort_key)

def get_criterion_value(
        equation_data,
        criterion_key,
        specific_reagent = None):
    if criterion_key == "Общая масса":
        return equation_data.get("total_mass_g_final_k")
    elif criterion_key == "Количество прекурсоров":
        return equation_data.get("num_reagents")
    elif criterion_key == "Масса конкретного прекурсора":
        return equation_data.get("masses_g_final_k", {}).get(specific_reagent)
    return None