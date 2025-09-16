import tkinter as tk
import tkinter.messagebox as mb

def float_test(element, text):
    try:
        element = float(element)
        return element
    except ValueError:
        show_error(title="error", message=f"{text} должны принимать числовое значение")

def fraction_test(data, list, type_name):
    for element in data:
        fraction = float_test(element['fraction'], "Доли")

        if type_name == 'anion':
            list['anions'] += fraction
        else:
            type = element[f'{type_name}']
            list[type] += fraction

    for type, total in list.items():
        if total > 0 and not 0.99 <= total <= 1.01:
            show_error(title="error", message=f"Сумма долей {type} должна быть равна 1")
            raise ValueError

def show_error(title, message):
    mb.showerror(title, message)