import os
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter import TclError

from frames import background_color, file_listbox, text_area, line_numbers, highlight_color, tk, bottom_bar_frame, \
    font_family, font_size

cd = ColorDelegator()

# Override background color, white by default
cd.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': background_color}
cd.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': background_color}
cd.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': background_color}
cd.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': background_color}
cd.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': background_color}

current_directory = os.getcwd()
current_file = None
current_mode = "file"
bottom_text_label = None
current_selection = 0
shift_last_press = 0


def handle_double_shift(event):
    global shift_last_press, current_mode
    if event.time - shift_last_press < 250:
        if current_mode == "text":
            current_mode = "file"
            hide_text_area()
            show_file_listbox()
            display_files_in_directory()
            update_bottom_bar_text()
    shift_last_press = event.time


def handle_key_event(event, key):
    global current_selection, current_mode, current_directory
    if current_mode == "file":
        if key == "w" and current_selection > 0:
            current_selection -= 1
        elif key == "s" and current_selection < file_listbox.size() - 1:
            current_selection += 1
        elif key == "e":
            selected_file = file_listbox.get(current_selection)
            read_file_content(selected_file)
        elif key == "q" and current_directory != os.path.expanduser("~"):
            current_directory = os.path.dirname(current_directory)
            display_files_in_directory()

        if key in ["w", "s"]:
            file_listbox.select_clear(0, tk.END)
            file_listbox.select_set(current_selection)
            file_listbox.activate(current_selection)


def display_files_in_directory():
    global current_selection
    file_listbox.delete(0, tk.END)
    current_selection = 0
    for file in os.listdir(current_directory):
        if os.path.isdir(file):
            file_listbox.insert(tk.END, u'\N{FOLDER} ' + file)
        else:
            file_listbox.insert(tk.END, u'\N{PAGE FACING UP} ' + file)
    file_listbox.selection_set(0)


def save_file():
    global current_directory, current_file
    if current_file:
        file_path = os.path.join(current_directory, current_file)
        with open(file_path, 'w', encoding='utf-8') as file:
            content = text_area.get('1.0', tk.END)
            file.write(content)
    else:
        print("No file is currently open. Save operation aborted.")


def read_file_content(filename):
    global current_mode
    if '\N{FOLDER}' in filename or '/..' in filename:
        filename = filename.split('\N{FOLDER}')[1].split('/..')[0].replace(" ", "")
    elif '\N{PAGE FACING UP}' in filename:
        current_mode = "text"
        filename = filename.split('\N{PAGE FACING UP}')[1].replace(" ", "")
    global current_directory, current_file
    file_path = os.path.join(current_directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            content = file.read()
            current_file = os.path.basename(file.name)

            hide_file_listbox()
            show_text_area()

            try:
                Percolator(text_area).insertfilter(cd)
            except TclError:
                # TODO: Initialized once, once more not needed.
                #       Maybe do this outside on the first run?
                print("Error")

            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, content)
            show_line_numbers()
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
    lines = text_area.get('1.0', 'end').count('\n')
    num_digits = len(str(lines))

    for i in range(1, lines + 1):
        line_numbers.insert(tk.END, str(i) + '\n')
    line_numbers.config(width=num_digits + 1, state='disabled')
    text_area.yview_moveto(yview)


def update_bottom_bar_text():
    global bottom_text_label
    text = {
        "mode": current_mode,
        "file": current_file
    }
    label_text = ""
    for key, value in text.items():
        label_text += f"{key}: {value}  *  "
    if bottom_text_label:
        bottom_text_label.config(text=label_text[:-3])
    else:
        bottom_text_label = tk.Label(bottom_bar_frame, text=label_text[:-3], fg="white", bg="black", anchor='w')
        show_bottom_text_label()


def highlight_current_line(event):
    text_area.tag_remove("highlight", "1.0", "end")
    current_line_num = text_area.index("insert").split(".")[0]
    current_cursor_pos = f"{current_line_num}.0"
    text_area.tag_add("highlight", current_cursor_pos, current_cursor_pos + " lineend")
    text_area.tag_config("highlight", background=highlight_color)


def adjust_font_size(event):
    current_font_size = text_area.cget("font")
    current_font_size = current_font_size.split()[-1]
    current_font_size = int(current_font_size)
    updated_font_size = current_font_size

    if event.keysym == "plus":
        updated_font_size = current_font_size + 1
    elif event.keysym == "minus":
        updated_font_size = max(1, current_font_size - 1)

    font_settings = (font_family, updated_font_size)
    text_area.config(font=font_settings)
    line_numbers.config(font=font_settings)


def hide_text_area():
    text_area.pack_forget()


def show_text_area():
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.focus_set()
    text_area.see('1.0')


def hide_file_listbox():
    file_listbox.pack_forget()


def show_file_listbox():
    file_listbox.pack(fill=tk.BOTH, expand=True)
    file_listbox.focus_set()


def hide_bottom_text_label():
    bottom_text_label.pack_forget()


def show_bottom_text_label():
    bottom_text_label.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)


def hide_line_numbers():
    line_numbers.pack_forget()


def show_line_numbers():
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)
