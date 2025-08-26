from tkinter import font as tkfont
import tkinter.ttk as ttk

class AppStyles:
    def __init__(self):
        self.style = ttk.Style()
        self.configure_styles()

    PRIMARY_COLOR = "#4a6fa5"
    SECONDARY_COLOR = "#166088"
    BACKGROUND_COLOR = "#f8f9fa"
    TEXT_COLOR = "#333333"
    BUTTON_ACTIVE_COLOR = "#4a7fa5"
    TITLE_FONT = ("Helvetica", 16, "bold")
    NORMAL_FONT = ("Helvetica", 12)
    SMALL_FONT = ("Helvetica", 10)

    @staticmethod
    def combobox_config():
        return {
            "style": 'TCombobox',
            "font": AppStyles.NORMAL_FONT
        }

    @staticmethod
    def treeview_config():
        return {
            "style": 'Treeview',
        }

    @staticmethod
    def treeview_headings_config():
        return {
        }

    def configure_styles(self):
        self.style.configure('TCombobox',
                   background=AppStyles.BACKGROUND_COLOR,
                   foreground=AppStyles.TEXT_COLOR,
                   fieldbackground=AppStyles.BACKGROUND_COLOR,
                   selectbackground=AppStyles.BACKGROUND_COLOR,
                   selectforeground=AppStyles.TEXT_COLOR,
                   state="readonly",
                   borderwidth=1,
                   relief='solid',
                   font=AppStyles.NORMAL_FONT)

        self.style.configure('Treeview',
                             background=AppStyles.BACKGROUND_COLOR,
                             foreground=AppStyles.TEXT_COLOR,
                             fieldbackground=AppStyles.BACKGROUND_COLOR,
                             borderwidth=1,
                             relief='flat',
                             rowheight=25,
                             font=AppStyles.NORMAL_FONT)

        # Заголовки
        self.style.configure('Treeview.Heading',
                             background=AppStyles.BACKGROUND_COLOR,
                             foreground=AppStyles.TEXT_COLOR,
                             padding=10,
                             borderwidth=1,
                             relief='flat',
                             font=AppStyles.NORMAL_FONT)

    # Стили для виджетов
    @staticmethod
    def button_style():
        return {
            "bg": AppStyles.PRIMARY_COLOR,
            "fg": "white",
            "activebackground": AppStyles.BUTTON_ACTIVE_COLOR,
            "font": AppStyles.NORMAL_FONT,
            "borderwidth": 1,
            "relief": "solid",
            "padx": 10,
            "pady": 5
        }

    @staticmethod
    def checkbutton_style():
        return {
            "bg": AppStyles.PRIMARY_COLOR,
            "fg": "white",
            "activebackground": AppStyles.BUTTON_ACTIVE_COLOR,
            "selectcolor": AppStyles.PRIMARY_COLOR,
            "font": AppStyles.NORMAL_FONT,
            "borderwidth": 1,
            "padx": 10,
            "pady": 5
        }

    @staticmethod
    def entry_style():
        return {
            "bg": "white",
            "fg": AppStyles.TEXT_COLOR,
            "font": AppStyles.NORMAL_FONT,
            "borderwidth": 1,
            "relief": "solid"
        }

    @staticmethod
    def label_style():
        return {
            "bg": AppStyles.BACKGROUND_COLOR,
            "fg": AppStyles.TEXT_COLOR,
            "font": AppStyles.NORMAL_FONT,
            "padx": 10,
            "pady": 10
        }

    @staticmethod
    def labelframe_style():
        return {
            "bg": AppStyles.BACKGROUND_COLOR,
            "fg": AppStyles.TEXT_COLOR,
            "font": AppStyles.NORMAL_FONT,
            "padx": 10,
            "pady": 10
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
            "font": AppStyles.NORMAL_FONT,
            "borderwidth": 1,
            "relief": "solid"
        }
