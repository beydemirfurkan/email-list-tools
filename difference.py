import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import json

def select_file1():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), 
                                                      ("Text Files", "*.txt"), 
                                                      ("CSV Files", "*.csv"),
                                                      ("Excel Files", "*.xlsx"),
                                                      ("JSON Files", "*.json"),
                                                      ("TSV Files", "*.tsv")])
    entry_file1.delete(0, tk.END)
    entry_file1.insert(0, file_path)
    display_preview(file_path, preview_text1)

def select_file2():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), 
                                                      ("Text Files", "*.txt"), 
                                                      ("CSV Files", "*.csv"),
                                                      ("Excel Files", "*.xlsx"),
                                                      ("JSON Files", "*.json"),
                                                      ("TSV Files", "*.tsv")])
    entry_file2.delete(0, tk.END)
    entry_file2.insert(0, file_path)
    display_preview(file_path, preview_text2)

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
    """Read different file formats and return the data for comparison or preview"""
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = {line.strip() for line in file if line.strip()}
        return lines if not preview else list(lines)[:5]

    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        return set(df.to_string(index=False).splitlines()) if not preview else df.head().to_string(index=False).splitlines()

    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        return set(df.to_string(index=False).splitlines()) if not preview else df.head().to_string(index=False).splitlines()

    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        # Convert JSON to set of lines (for previewing or comparing)
        lines = {json.dumps(item) for item in json_data} if isinstance(json_data, list) else {json.dumps(json_data)}
        return lines if not preview else list(lines)[:5]

    elif file_path.endswith('.tsv'):
        df = pd.read_csv(file_path, sep='\t')
        return set(df.to_string(index=False).splitlines()) if not preview else df.head().to_string(index=False).splitlines()

    else:
        raise ValueError("Unsupported file type")

def find_differences():
    file1_path = entry_file1.get()
    file2_path = entry_file2.get()

    if not file1_path or not file2_path:
        messagebox.showwarning("Warning", "Please select both files.")
        return

    try:
        file1_lines = read_file(file1_path)
        file2_lines = read_file(file2_path)

        unique_lines_file1 = file1_lines - file2_lines

        if unique_lines_file1:
            output_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("Text file", "*.txt"), 
                                                                      ("CSV file", "*.csv"), 
                                                                      ("Excel file", "*.xlsx")])
            if not output_filename:
                return

            if output_filename.endswith('.txt'):
                with open(output_filename, 'w', encoding='utf-8') as diff_file:
                    for line in unique_lines_file1:
                        diff_file.write(line + '\n')
            elif output_filename.endswith('.csv'):
                df = pd.DataFrame(list(unique_lines_file1), columns=["Unique Lines"])
                df.to_csv(output_filename, index=False)
            elif output_filename.endswith('.xlsx'):
                df = pd.DataFrame(list(unique_lines_file1), columns=["Unique Lines"])
                df.to_excel(output_filename, index=False)
            
            label_result.config(text=f"Differences saved to {output_filename}.")
            messagebox.showinfo("Result", f"{len(unique_lines_file1)} unique lines found in the first file.")
        else:
            label_result.config(text="The first file is a complete subset of the second file.")
            messagebox.showinfo("Result", "No unique lines found in the first file.")

    except Exception as e:
        label_result.config(text=f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("File Difference Finder")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

label_file1 = tk.Label(frame, text="First File:")
label_file1.grid(row=0, column=0, padx=10, pady=5)
entry_file1 = tk.Entry(frame, width=50)
entry_file1.grid(row=0, column=1, padx=10, pady=5)
button_file1 = tk.Button(frame, text="Select", command=select_file1)
button_file1.grid(row=0, column=2, padx=10, pady=5)

label_file2 = tk.Label(frame, text="Second File:")
label_file2.grid(row=1, column=0, padx=10, pady=5)
entry_file2 = tk.Entry(frame, width=50)
entry_file2.grid(row=1, column=1, padx=10, pady=5)
button_file2 = tk.Button(frame, text="Select", command=select_file2)
button_file2.grid(row=1, column=2, padx=10, pady=5)

button_diff = tk.Button(frame, text="Find Differences", command=find_differences)
button_diff.grid(row=2, column=0, columnspan=3, pady=20)

label_result = tk.Label(frame, text="")
label_result.grid(row=3, column=0, columnspan=3)

# Preview areas for file content
preview_label1 = tk.Label(frame, text="File 1 Preview:")
preview_label1.grid(row=4, column=0, columnspan=3, pady=5)
preview_text1 = scrolledtext.ScrolledText(frame, width=80, height=10)
preview_text1.grid(row=5, column=0, columnspan=3)

preview_label2 = tk.Label(frame, text="File 2 Preview:")
preview_label2.grid(row=6, column=0, columnspan=3, pady=5)
preview_text2 = scrolledtext.ScrolledText(frame, width=80, height=10)
preview_text2.grid(row=7, column=0, columnspan=3)

root.mainloop()
