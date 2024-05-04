import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Global variables
data = {}
attribute_names = []
prefixes = []

def load_file():
    filename = filedialog.askopenfilename()
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)
        parse_file(filename)

def parse_file(filename):
    global data, attribute_names, prefixes
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            attribute_names = lines[0].strip().split()
            data = {line.split()[0]: line.split()[1:] for line in lines[1:]}
            update_filename_list()
            create_attribute_sliders()
            extract_prefixes()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_filename_list():
    filename_combobox['values'] = list(data.keys())
    filename_combobox.current(0)
    update_attributes()

def create_attribute_sliders():
    for widget in attribute_frame.winfo_children():
        widget.destroy()

    attribute_sliders.clear()
    row = 0
    col = 0

    for i, attr in enumerate(attribute_names):  # Include all attributes
        slider = tk.Scale(attribute_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        slider.grid(row=row, column=col, sticky="ew")

        label = tk.Label(attribute_frame, text=attr)
        label.grid(row=row + 1, column=col, sticky="ew")

        attribute_sliders.append(slider)

        row += 2
        if (i % 10 == 0) and (i != 0):  # Switch columns every 10 rows, but not on the first attribute
            col += 1
            row = 0

    attribute_frame.grid_columnconfigure(0, weight=1)
    attribute_frame.grid_columnconfigure(1, weight=1)
    update_attributes()

def update_attributes():
    selected_file = filename_combobox.get()
    if selected_file in data:
        for i, slider in enumerate(attribute_sliders):
            if i < len(data[selected_file]):
                slider.set(float(data[selected_file][i]))

def extract_prefixes():
    global prefixes
    prefixes = sorted(set(filename.split('/')[0] for filename in data.keys()))
    prefix_combobox['values'] = prefixes
    if prefixes:
        prefix_combobox.current(0)

def save_changes():
    new_values = [str(slider.get()) for slider in attribute_sliders]
    selected_file = filename_combobox.get()
    data[selected_file] = new_values

    # Save to file
    with open(file_entry.get(), 'w') as file:
        file.write(' '.join(attribute_names) + '\n')
        for filename, values in data.items():
            file.write(filename + ' ' + ' '.join(values) + '\n')
    messagebox.showinfo("Success", "File saved successfully")

def apply_changes_to_prefix():
    prefix = prefix_combobox.get()
    new_values = [str(slider.get()) for slider in attribute_sliders]

    for filename in data.keys():
        if filename.startswith(prefix):
            data[filename] = new_values

    messagebox.showinfo("Success", f"Changes applied to all files starting with '{prefix}'")

root = tk.Tk()
root.title("Attribute Editor")

file_entry = tk.Entry(root, width=50)
file_entry.pack()

load_button = tk.Button(root, text="Load File", command=load_file)
load_button.pack()

filename_combobox = ttk.Combobox(root, state="readonly", width=47)
filename_combobox.pack()
filename_combobox.bind("<<ComboboxSelected>>", lambda event: update_attributes())

attribute_frame = tk.Frame(root)
attribute_frame.pack(expand=True)

attribute_sliders = []

save_button = tk.Button(root, text="Save Changes", command=save_changes)
save_button.pack()

prefix_label = tk.Label(root, text="Apply changes to prefix:")
prefix_label.pack()

prefix_combobox = ttk.Combobox(root, state="readonly", width=47)
prefix_combobox.pack()

apply_prefix_button = tk.Button(root, text="Apply to Prefix", command=apply_changes_to_prefix)
apply_prefix_button.pack()

root.mainloop()
