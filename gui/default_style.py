from tkinter import font as tkfont

class AppStyles:
    # Цвета
    PRIMARY_COLOR = "#4a6fa5"
    SECONDARY_COLOR = "#166088"
    BACKGROUND_COLOR = "#f8f9fa"
    TEXT_COLOR = "#333333"
    BUTTON_ACTIVE_COLOR = "#4a7fa5"

    # Шрифты
    @staticmethod
    def title_font():
        return tkfont.Font(family="Helvetica", size=16, weight="bold")

    @staticmethod
    def normal_font():
        return tkfont.Font(family="Helvetica", size=12)

    @staticmethod
    def small_font():
        return tkfont.Font(family="Helvetica", size=10)

    # Стили для виджетов
    @staticmethod
    def button_style():
        return {
            "bg": AppStyles.PRIMARY_COLOR,
            "fg": "white",
            "activebackground": AppStyles.BUTTON_ACTIVE_COLOR,
            "font": AppStyles.normal_font(),
            "borderwidth": 1,
            "relief": "solid",
            "padx": 10,
            "pady": 5
        }

    @staticmethod
    def entry_style():
        return {
            "bg": "white",
            "fg": AppStyles.TEXT_COLOR,
            "font": AppStyles.normal_font(),
            "borderwidth": 1,
            "relief": "solid"
        }

    @staticmethod
    def label_style():
        return {
            "bg": AppStyles.BACKGROUND_COLOR,
            "fg": AppStyles.TEXT_COLOR,
            "font": AppStyles.normal_font()
        }

    @staticmethod
    def frame_style():
        return {
            "bg": AppStyles.BACKGROUND_COLOR,
            "padx": 10,
            "pady": 10
        }

    @staticmethod
    def combobox_style():
        return {
            "fg": AppStyles.TEXT_COLOR,
            "font": AppStyles.normal_font(),
            "borderwidth": 1,
            "relief": "solid"
        }