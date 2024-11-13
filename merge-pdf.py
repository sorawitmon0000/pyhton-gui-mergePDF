import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfWriter
import os

file_list = []

# select PDF
def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if files:
        for file in files:
            if file not in file_list:
                file_list.append(file)
                add_file_to_listbox(file)

# display select pdf
def add_file_to_listbox(file):
    frame = tk.Frame(scrollable_frame)
    frame.pack(fill=tk.X, pady=2, padx=5)

    label = tk.Label(frame, text=os.path.basename(file), anchor="w")
    label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    delete_button = tk.Button(frame, text="❌", command=lambda: remove_file(file, frame))
    delete_button.pack(side=tk.RIGHT, padx=5)

# delete pdf
def remove_file(file, frame):
    file_list.remove(file)
    frame.destroy()

# merge pdf
def merge_pdfs():
    if not file_list:
        messagebox.showwarning("Warning", "No files selected!")
        return
    
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_file:
        try:
            merger = PdfWriter()
            for pdf in file_list:
                merger.append(pdf)
            merger.write(output_file)
            merger.close()
            messagebox.showinfo("Success", "PDFs merged successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# create window
root = tk.Tk()
root.title("PDF Merger")
root.geometry("600x400")

# scroll bar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
scrollbar.pack(side="right", fill="y", pady=5)

# button add file and merge
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Files", command=select_files)
add_button.pack(side=tk.LEFT, padx=5)

merge_button = tk.Button(button_frame, text="Merge PDFs", command=merge_pdfs)
merge_button.pack(side=tk.LEFT, padx=5)

root.mainloop()

