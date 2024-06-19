import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def select_files():
    filetypes = (
        ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"),
        ("All files", "*.*")
    )
    files = filedialog.askopenfilenames(title="Select files", filetypes=filetypes)
    if files:
        for file in files:
            file_list.insert(tk.END, file)

def select_output_directory():
    directory = filedialog.askdirectory(title="Select output directory")
    if directory:
        output_dir.set(directory)

def convert_images():
    from_format = from_var.get()
    to_format = to_var.get()
    output_directory = output_dir.get()

    if not output_directory:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    for file in file_list.get(0, tk.END):
        try:
            img = Image.open(file)
            base_name = os.path.basename(file)
            new_name = os.path.splitext(base_name)[0] + f'.{to_format.lower()}'
            
            if img.mode in ('RGBA', 'LA') and to_format.lower() == 'jpg':
                # Remove alpha channel for JPG conversion
                img = img.convert('RGB')

            img.save(os.path.join(output_directory, new_name), to_format.upper())
        except Exception as e:
            messagebox.showerror("Error", f"Error converting {file}: {e}")
    messagebox.showinfo("Success", "Conversion completed!")

def remove_selected_file():
    selected_files = file_list.curselection()
    for index in reversed(selected_files):
        file_list.delete(index)

# Create the main window
root = tk.Tk()
root.title("Image Converter")

# Create and place widgets
tk.Label(root, text="Select files:").grid(row=0, column=0, padx=10, pady=10)

frame = tk.Frame(root)
frame.grid(row=0, column=1, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_list = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50, height=10, yscrollcommand=scrollbar.set)
file_list.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=file_list.yview)

tk.Button(root, text="Browse...", command=select_files).grid(row=0, column=2, padx=10, pady=10)
tk.Button(root, text="Remove selected", command=remove_selected_file).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="From format:").grid(row=1, column=0, padx=10, pady=10)
from_var = tk.StringVar(value="webp")
from_menu = tk.OptionMenu(root, from_var, "webp", "jpg", "png", "bmp")
from_menu.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="To format:").grid(row=2, column=0, padx=10, pady=10)
to_var = tk.StringVar(value="jpg")
to_menu = tk.OptionMenu(root, to_var, "jpg", "png", "webp", "bmp")
to_menu.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Output directory:").grid(row=3, column=0, padx=10, pady=10)
output_dir = tk.StringVar()
tk.Entry(root, textvariable=output_dir, width=50).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Browse...", command=select_output_directory).grid(row=3, column=2, padx=10, pady=10)

tk.Button(root, text="Convert", command=convert_images).grid(row=4, column=1, padx=10, pady=20)

# Run the main loop
root.mainloop()
