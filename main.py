from frames import root, text_area
from functions import display_files_in_directory, update_bottom_bar_text, handle_double_shift, handle_key_event, save_file, highlight_current_line, adjust_font_size

if __name__ == "__main__":
    display_files_in_directory()
    update_bottom_bar_text()

    root.bind("<Shift_L>", handle_double_shift)
    root.bind("<w>", lambda event: handle_key_event(event, "w"))
    root.bind("<s>", lambda event: handle_key_event(event, "s"))
    root.bind("<e>", lambda event: handle_key_event(event, "e"))
    root.bind("<q>", lambda event: handle_key_event(event, "q"))
    root.bind("<Control-s>", lambda event: save_file())
    text_area.bind("<KeyRelease>", highlight_current_line)
    root.bind("<Control-plus>", adjust_font_size)
    root.bind("<Control-minus>", adjust_font_size)

    root.iconbitmap('./resources/l-solid.ico')
    root.mainloop()

