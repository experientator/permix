import tkinter.messagebox as mb
from gui.language.manager import localization_manager

def float_test(element, text):
    try:
        element = float(element)
        return element
    except ValueError:
        er1 = localization_manager.tr("act_err1")
        show_error(title="error", message=f"{text} {er1}")

def fraction_test(data, list, type_name):
    for element in data:
        fraction = float_test(element['fraction'], localization_manager.tr("act_err2"))

        if type_name == 'anion':
            list['anions'] += fraction
        else:
            type = element[f'{type_name}']
            list[type] += fraction

    for type, total in list.items():
        if total > 0 and not 0.99 <= total <= 1.01:
            er1 = localization_manager.tr("act_err3")
            er2 = localization_manager.tr("act_err4")
            show_error(message=f"{er1} {type} {er2}")
            raise ValueError

def show_error(message):
    mb.showerror(localization_manager.tr("error_title"), message)