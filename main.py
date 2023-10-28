import tkinter as tk
import os
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
import re

background_color = "#313131"
foreground_color = "#f0f0f0"

shift_last_press, current_mode, current_selection = 0, "text_editor", 0
current_directory, font_settings = os.getcwd(), ("Consolas", 12)

root = tk.Tk()
text_editor_frame = tk.Frame(root)
numbers_frame = tk.Frame(root)
file_listbox = tk.Listbox(text_editor_frame, selectmode=tk.SINGLE, background=background_color, foreground=foreground_color)
text_area = tk.Text(text_editor_frame, background=background_color, foreground=foreground_color, insertbackground=foreground_color, font=font_settings)
line_numbers = tk.Text(numbers_frame, padx=5, takefocus=0, border=0, background=background_color, foreground=foreground_color, state='disabled', font=font_settings)
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()


def display_files_in_directory():
    file_listbox.delete(0, tk.END)
    for file in os.listdir(current_directory):
        file_listbox.insert(tk.END, file)

def handle_double_shift(event):
    global shift_last_press, current_mode
    if event.time - shift_last_press < 250:
        if current_mode == "text_editor":
            current_mode = "file_editor"
            text_area.pack_forget()
            display_files_in_directory()
        elif current_mode == "file_editor":
            current_mode = "text_editor"
            file_listbox.delete(0, tk.END)
            text_area.pack(fill=tk.BOTH, expand=True)
    shift_last_press = event.time

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

def handle_key_event(event, key):
    global current_selection
    if current_mode == "file_editor":
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

def read_file_content(filename):
    global current_directory
    file_path = os.path.join(current_directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            content = file.read()

            # syntax-highlighting
            Percolator(text_area).insertfilter(ColorDelegator())
            
            text_area.delete('1.0', tk.END)
            file_listbox.forget()
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert(tk.END, content)
            line_numbers.pack(side=tk.LEFT, fill=tk.Y)
            update_line_numbers()
    elif os.path.isdir(file_path):
        current_directory = file_path
        display_files_in_directory()
    else:
        print(f"File {filename} not found in the current directory.")

def create_window():
    root.geometry(f"{screen_width // 2}x{screen_height - 100}+0+0")
    root.title("File Editor")
    numbers_frame.pack(side=tk.LEFT, fill=tk.Y)
    text_editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    file_listbox.pack(fill=tk.BOTH, expand=True)
    text_area.pack_forget()

    root.bind("<Shift_L>", handle_double_shift)
    root.bind("<w>", lambda event: handle_key_event(event, "w"))
    root.bind("<s>", lambda event: handle_key_event(event, "s"))
    root.bind("<e>", lambda event: handle_key_event(event, "e"))
    root.mainloop()

create_window()
