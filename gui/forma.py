import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from comp_forma_models import CompositionInformation, CompositionStructure, Solvents, Properties

class CompositionStructureForm(tk.LabelFrame):
    fields = ("site", "symbol", "fraction", "valence")

    def __init__(self, master, **kwargs):
        super().__init__(master, text="Composition structure", padx=10, pady=10, **kwargs)
        self.frame = tk.Frame(self)
        self.entries = list(map(self.create_field, enumerate(self.fields)))
        self.frame.pack()

    def create_field(self, field):
        position, text = field
        label = tk.Label(self.frame, text=text)
        entry = tk.Entry(self.frame, width=25)
        label.grid(row=position, column=0, pady=5)
        entry.grid(row=position, column=1, pady=5)
        return entry

    def get_details(self):
        values = [e.get() for e in self.entries]
        try:
            return CompositionStructure(*values)
        except ValueError as e:
            mb.showerror("Ошибка валидации", str(e), parent=self)

class SolventsForm(tk.LabelFrame):
    fields = ("type", "symbol", "fraction")

    def __init__(self, master, **kwargs):
        super().__init__(master, text="Composition structure", padx=10, pady=10, **kwargs)
        self.frame = tk.Frame(self)
        self.entries = list(map(self.create_field, enumerate(self.fields)))
        self.frame.pack()

    def create_field(self, field):
        position, text = field
        label = tk.Label(self.frame, text=text)
        entry = tk.Entry(self.frame, width=25)
        label.grid(row=position, column=0, pady=5)
        entry.grid(row=position, column=1, pady=5)
        return entry

    def get_details(self):
        values = [e.get() for e in self.entries]
        try:
            return Solvents(*values)
        except ValueError as e:
            mb.showerror("Ошибка валидации", str(e), parent=self)

def enter_data():
    accepted = accept_var.get()

    if accepted == "Accepted":
        # User info
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()

        if firstname and lastname:
            title = title_combobox.get()
            age = age_spinbox.get()
            nationality = nationality_combobox.get()

            # Course info
            registration_status = reg_status_var.get()
            numcourses = numcourses_spinbox.get()
            numsemesters = numsemesters_spinbox.get()

            print("First name: ", firstname, "Last name: ", lastname)
            print("Title: ", title, "Age: ", age, "Nationality: ", nationality)
            print("# Courses: ", numcourses, "# Semesters: ", numsemesters)
            print("Registration status", registration_status)
            print("------------------------------------------")
        else:
            tk.messagebox.showwarning(title="Error", message="First name and last name are required.")
    else:
        tk.messagebox.showwarning(title="Error", message="You have not accepted the terms")


window = tk.Tk()
window.title("Permix data uploading")

frame = tk.Frame(window)
frame.pack()

# saving composition information
comp_info_frame = tk.LabelFrame(frame, text="Composition information")
comp_info_frame.grid(row=0, column=0, padx=20, pady=10)

doi = tk.Label(comp_info_frame, text="doi")
doi_entry = tk.Entry(comp_info_frame)
doi.grid(row=0, column=0)
doi_entry.grid(row=1, column=0)

data_type = tk.Label(comp_info_frame, text="data type")
data_box = ttk.Combobox(comp_info_frame, values=["", "experimental", "theoretical", "modelling"])
data_type.grid(row=0, column=1)
data_box.grid(row=1, column=1)

notes = tk.Label(comp_info_frame, text="notes")
notes_entry = tk.Entry(comp_info_frame)
notes.grid(row=0, column=2)
notes_entry.grid(row=1, column=2)

for widget in comp_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Composition structure
comp_frame = tk.LabelFrame(frame, text = "Composition")
comp_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

structure_type = tk.Label(comp_frame, text="structure type")
structure_box = ttk.Combobox(comp_frame, values=["A_site", "B_site", "B_double", "anion"])
structure_type.grid(row=0, column=0)
structure_box.grid(row=1, column=0)

symbol = tk.Label(comp_frame, text="symbol")
symbol_entry = tk.Entry(comp_frame)
symbol.grid(row=0, column=1)
symbol_entry.grid(row=1, column=1)

fraction = tk.Label(comp_frame, text="fraction")
fraction_entry = tk.Entry(comp_frame)
fraction.grid(row=0, column=2)
fraction_entry.grid(row=1, column=2)

valence = tk.Label(comp_frame, text="valence")
valence_entry = tk.Entry(comp_frame)
valence.grid(row=2, column=1)
valence_entry.grid(row=3, column=1)

for widget in comp_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# solvents
solv_frame = tk.LabelFrame(frame, text = "Solvents")
solv_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

symbol = tk.Label(solv_frame, text="symbol")
symbol_entry = tk.Entry(solv_frame)
symbol.grid(row=0, column=0)
symbol_entry.grid(row=1, column=0)

fraction = tk.Label(solv_frame, text="fraction")
fraction_entry = tk.Entry(solv_frame)
fraction.grid(row=0, column=1)
fraction_entry.grid(row=1, column=1)

for widget in solv_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

app = Antisolvent(window)
# antisolv_frame = tk.LabelFrame(frame, text = "Antisolvents")
# antisolv_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)
#
# symbol = tk.Label(antisolv_frame, text="symbol")
# symbol_entry = tk.Entry(antisolv_frame)
# symbol.grid(row=0, column=0)
# symbol_entry.grid(row=1, column=0)
#
# fraction = tk.Label(antisolv_frame, text="fraction")
# fraction_entry = tk.Entry(antisolv_frame)
# fraction.grid(row=0, column=1)
# fraction_entry.grid(row=1, column=1)
#
# for widget in antisolv_frame.winfo_children():
#     widget.grid_configure(padx=10, pady=5)

properties_frame = tk.LabelFrame(frame, text = "Properties")
properties_frame.grid(row=4, column=0, sticky="news", padx=20, pady=10)

bg = tk.Label(properties_frame, text="band gap, eV")
bg_entry = tk.Entry(properties_frame)
bg.grid(row=0, column=0)
bg_entry.grid(row=1, column=0)

pp = tk.Label(properties_frame, text="pce percent")
pp_entry = tk.Entry(properties_frame)
pp.grid(row=0, column=1)
pp_entry.grid(row=1, column=1)

voc = tk.Label(properties_frame, text="voc, V")
voc_entry = tk.Entry(properties_frame)
voc.grid(row=0, column=2)
voc_entry.grid(row=1, column=2)

jsc = tk.Label(properties_frame, text="jsc, mA/cm^2")
jsc_entry = tk.Entry(properties_frame)
jsc.grid(row=2, column=0)
jsc_entry.grid(row=3, column=0)

ff_percent = tk.Label(properties_frame, text="ff percent")
ff_percent_entry = tk.Entry(properties_frame)
ff_percent.grid(row=2, column=1)
ff_percent_entry.grid(row=3, column=1)

stability_notes = tk.Label(properties_frame, text="stability notes")
stability_notes_entry = tk.Entry(properties_frame)
stability_notes.grid(row=2, column=2)
stability_notes_entry.grid(row=3, column=2)

for widget in properties_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button
button = tk.Button(frame, text="Enter data", command=enter_data)
button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

window.mainloop()