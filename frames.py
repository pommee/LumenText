import tkinter as tk

background_color = "#212121"
foreground_color = "#f0f0f0"
highlight_color = "#313131"
font_settings = ("Consolas", 12)

# Create Tkinter Window
root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{screen_width // 2}x{screen_height - 100}+0+0")

# Frames
text_editor_frame = tk.Frame(root)
numbers_frame = tk.Frame(root)
bottom_bar_frame = tk.Frame(root, bg="black", height=30)

# Initialize Widgets
file_listbox = tk.Listbox(
    text_editor_frame,
    selectmode=tk.SINGLE,
    background=background_color,
    foreground=foreground_color,
    font=("Consolas", 20)
)
text_area = tk.Text(
    text_editor_frame,
    background=background_color,
    foreground=foreground_color,
    insertbackground=foreground_color,
    font=font_settings,
    borderwidth=0,
    wrap='none'
)
line_numbers = tk.Text(
    numbers_frame,
    padx=5,
    takefocus=0,
    border=0,
    background=background_color,
    foreground=foreground_color,
    state='disabled',
    font=font_settings
)

# Pack Widgets
bottom_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)
numbers_frame.pack(side=tk.LEFT, fill=tk.Y)
text_editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
file_listbox.pack(fill=tk.BOTH, expand=True)
