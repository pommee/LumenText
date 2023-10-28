import tkinter as tk
from frames import text_editor_frame, numbers_frame, bottom_bar_frame, file_listbox, text_area, line_numbers
from functions import *

if __name__ == "__main__":
    display_files_in_directory()
    update_bottom_bar_text()

    root.bind("<Shift_L>", handle_double_shift)
    root.bind("<w>", lambda event: handle_key_event(event, "w"))
    root.bind("<s>", lambda event: handle_key_event(event, "s"))
    root.bind("<e>", lambda event: handle_key_event(event, "e"))
    root.mainloop()