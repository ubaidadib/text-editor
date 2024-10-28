import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"AlmdrasaTextEditor - {filepath}")

def save_file():
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"AlmdrasaTextEditor - {filepath}")

def exit_editor():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

def update_status(event=None):
    row, col = txt_edit.index(tk.INSERT).split(".")
    status_bar.config(text=f"Line {row}, Column {col}")

def toggle_word_wrap():
    if txt_edit.cget("wrap") == "none":
        txt_edit.config(wrap="word")
    else:
        txt_edit.config(wrap="none")

window = tk.Tk()
window.title("Almdrasa Text Editor")
window.geometry("800x600")

# Configure rows and columns
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

# Frame for buttons
button_frame = tk.Frame(window)
button_frame.grid(row=0, column=0, sticky="ew")

# Add buttons to the frame
btn_open = tk.Button(button_frame, text="Open", command=open_file)
btn_open.pack(side="left", padx=5, pady=5)

btn_save = tk.Button(button_frame, text="Save As", command=save_file)
btn_save.pack(side="left", padx=5, pady=5)

# Create text area with scrollbar
txt_edit = tk.Text(window, wrap="word", undo=True)
scroll = tk.Scrollbar(window, command=txt_edit.yview)
txt_edit.configure(yscrollcommand=scroll.set)

# Set up status bar
status_bar = tk.Label(window, text="Line 1, Column 0", anchor="w")
status_bar.grid(row=2, column=0, sticky="we")

# Event binding for status update
txt_edit.bind("<KeyRelease>", update_status)

# Menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save As...", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor, accelerator="Ctrl+Q")

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=txt_edit.edit_undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=txt_edit.edit_redo, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=lambda: txt_edit.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: txt_edit.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: txt_edit.event_generate("<<Paste>>"))

# View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_checkbutton(label="Word Wrap", command=toggle_word_wrap)

# Keyboard shortcuts
window.bind("<Control-o>", lambda event: open_file())
window.bind("<Control-s>", lambda event: save_file())
window.bind("<Control-q>", lambda event: exit_editor())

# Arrange widgets in window
txt_edit.grid(row=1, column=0, sticky="nsew")
scroll.grid(row=1, column=1, sticky="ns")

window.mainloop()
