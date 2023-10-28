from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

from frames import *
from main import *

current_directory = os.getcwd() 
current_file = None
current_mode = "file"
bottom_text_label = None
current_selection = 0

def handle_double_shift(event):
    global shift_last_press, current_mode
    if event.time - shift_last_press < 250:
        if current_mode == "text":
            current_mode = "file"
            text_area.pack_forget()
            file_listbox.pack(fill=tk.BOTH, expand=True)
            update_bottom_bar_text()
        elif current_mode == "file":
            current_mode = "text"
            file_listbox.delete(0, tk.END)
            text_area.pack(fill=tk.BOTH, expand=True)
    shift_last_press = event.time

def handle_key_event(event, key):
    global current_selection
    if current_mode == "file":
        if key == "w" and current_selection > 0:
            current_selection -= 1
        elif key == "s" and current_selection < file_listbox.size() - 1:
            current_selection += 1
        elif key == "e":
            selected_file = file_listbox.get(current_selection)
            read_file_content(selected_file)

        if key in ["w", "s"]:
            file_listbox.select_clear(0, tk.END)
            file_listbox.select_set(current_selection)
            file_listbox.activate(current_selection)

def display_files_in_directory():
    file_listbox.delete(0, tk.END)
    for file in os.listdir(current_directory):
        file_listbox.insert(tk.END, file)

def read_file_content(filename):
    global current_directory, current_file
    file_path = os.path.join(current_directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            content = file.read()
            current_file = os.path.basename(file.name)

            # syntax-highlighting
            Percolator(text_area).insertfilter(ColorDelegator())
            
            text_area.delete('1.0', tk.END)
            file_listbox.forget()
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert(tk.END, content)
            line_numbers.pack(side=tk.LEFT, fill=tk.Y)
            update_line_numbers()
            update_bottom_bar_text()
    elif os.path.isdir(file_path):
        current_directory = file_path
        display_files_in_directory()
    else:
        print(f"File {filename} not found in the current directory.")

def update_line_numbers():
    line_numbers.config(state='normal')
    line_numbers.delete('1.0', tk.END)
    _, yview = text_area.yview()
    lines = text_area.get('1.0', 'end').count('\n') + 1
    num_digits = len(str(lines))

    for i in range(1, lines + 1):
        line_numbers.insert(tk.END, str(i) + '\n')
    line_numbers.config(width=num_digits + 1, state='disabled')
    text_area.yview_moveto(yview)

def update_bottom_bar_text():
    global bottom_text_label
    text = {
        "file": current_file,
        "mode": current_mode
    }
    label_text = ""
    for key, value in text.items():
        label_text += f"{key}: {value}  *  "
    if bottom_text_label:
        bottom_text_label.config(text=label_text[:-3])
    else:
        bottom_text_label = tk.Label(bottom_bar_frame, text=label_text[:-3], fg="white", bg="black", anchor='w')
        bottom_text_label.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)