import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import json

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), 
                                                      ("Text Files", "*.txt"), 
                                                      ("CSV Files", "*.csv"),
                                                      ("Excel Files", "*.xlsx"),
                                                      ("JSON Files", "*.json"),
                                                      ("TSV Files", "*.tsv")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)
    display_preview(file_path, preview_text)

def display_preview(file_path, preview_widget):
    """Display the first few lines of the file in a scrolled text box"""
    try:
        data = read_file(file_path, preview=True)
        preview_widget.delete(1.0, tk.END)  # Clear previous text
        for line in data:
            preview_widget.insert(tk.END, line + '\n')
    except Exception as e:
        preview_widget.delete(1.0, tk.END)
        preview_widget.insert(tk.END, f"Error reading file: {str(e)}")

def read_file(file_path, preview=False):
    """Read different file formats and return the data for processing or preview"""
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
        return lines if not preview else lines[:5]

    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        return df.iloc[:, 0].tolist() if not preview else df.head().iloc[:, 0].tolist()

    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        return df.iloc[:, 0].tolist() if not preview else df.head().iloc[:, 0].tolist()

    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data if not preview else list(json_data)[:5]

    elif file_path.endswith('.tsv'):
        df = pd.read_csv(file_path, sep='\t')
        return df.iloc[:, 0].tolist() if not preview else df.head().iloc[:, 0].tolist()

    else:
        raise ValueError("Unsupported file type")

def remove_duplicates(input_data):
    """Remove duplicate entries from the list"""
    unique_items = set()
    duplicate_count = 0
    for item in input_data:
        if item in unique_items:
            duplicate_count += 1
        else:
            unique_items.add(item)
    return unique_items, duplicate_count

def process_duplicates():
    file_path = entry_file.get()

    if not file_path:
        messagebox.showwarning("Warning", "Please select a file.")
        return

    try:
        file_data = read_file(file_path)
        unique_data, duplicate_count = remove_duplicates(file_data)

        output_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                       filetypes=[("Text file", "*.txt"), 
                                                                  ("CSV file", "*.csv"), 
                                                                  ("Excel file", "*.xlsx")])
        if not output_filename:
            return

        if output_filename.endswith('.txt'):
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                for item in sorted(unique_data):
                    output_file.write(item + '\n')

        elif output_filename.endswith('.csv'):
            df = pd.DataFrame(sorted(unique_data), columns=["Unique Data"])
            df.to_csv(output_filename, index=False)

        elif output_filename.endswith('.xlsx'):
            df = pd.DataFrame(sorted(unique_data), columns=["Unique Data"])
            df.to_excel(output_filename, index=False)

        label_result.config(text=f"Processed {len(unique_data)} unique entries. Found {duplicate_count} duplicates.")
        messagebox.showinfo("Result", f"Duplicates removed. {len(unique_data)} unique entries saved to {output_filename}.")

    except Exception as e:
        label_result.config(text=f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("Duplicate Remover")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

label_file = tk.Label(frame, text="Select File:")
label_file.grid(row=0, column=0, padx=10, pady=5)
entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=5)
button_file = tk.Button(frame, text="Browse", command=select_file)
button_file.grid(row=0, column=2, padx=10, pady=5)

button_process = tk.Button(frame, text="Remove Duplicates", command=process_duplicates)
button_process.grid(row=1, column=0, columnspan=3, pady=20)

label_result = tk.Label(frame, text="")
label_result.grid(row=2, column=0, columnspan=3)

# Preview area for file content
preview_label = tk.Label(frame, text="File Preview:")
preview_label.grid(row=3, column=0, columnspan=3, pady=5)
preview_text = scrolledtext.ScrolledText(frame, width=80, height=10)
preview_text.grid(row=4, column=0, columnspan=3)

root.mainloop()
