import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
from collections import Counter
import pandas as pd
import json

def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), 
                                                      ("Text Files", "*.txt"), 
                                                      ("CSV Files", "*.csv"),
                                                      ("Excel Files", "*.xlsx"),
                                                      ("JSON Files", "*.json")])
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

    else:
        raise ValueError("Unsupported file type")

def analyze_emails(email_list):
    email_counts = Counter()
    invalid_emails = 0
    invalid_reasons = Counter()
    lengths = []
    top_usernames = Counter()
    domain_extensions = Counter()

    for email in email_list:
        email = email.strip()
        if is_valid_email(email):
            domain = email.split('@')[1]
            username = email.split('@')[0]
            extension = domain.split('.')[-1]
            
            email_counts[domain] += 1
            lengths.append(len(email))
            top_usernames[username] += 1
            domain_extensions[extension] += 1
        else:
            invalid_emails += 1
            if '@' not in email:
                invalid_reasons["Missing @"] += 1
            elif email.count('@') > 1:
                invalid_reasons["Multiple @"] += 1
            else:
                invalid_reasons["Invalid format"] += 1

    return {
        'total_emails': len(email_list),
        'invalid_emails': invalid_emails,
        'invalid_reasons': invalid_reasons,
        'email_counts': email_counts,
        'lengths': lengths,
        'top_usernames': top_usernames,
        'domain_extensions': domain_extensions
    }

def display_analysis_results(results):
    output = []
    output.append(f"Total emails: {results['total_emails']}")
    output.append(f"Invalid emails: {results['invalid_emails']}")
    output.append("\nReasons for invalid emails:")
    
    for reason, count in results['invalid_reasons'].items():
        output.append(f"{reason}: {count}")
    
    output.append("\nTop 10 most common domains:")
    for domain, count in results['email_counts'].most_common(10):
        output.append(f"{domain}: {count} occurrences")
    
    output.append(f"\nLongest email length: {max(results['lengths'])}")
    output.append(f"Shortest email length: {min(results['lengths'])}")
    
    output.append("\nTop 10 most common usernames:")
    for username, count in results['top_usernames'].most_common(10):
        output.append(f"{username}: {count} occurrences")
    
    return output

def save_results(results):
    output_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text file", "*.txt"), 
                                                              ("CSV file", "*.csv"), 
                                                              ("Excel file", "*.xlsx")])
    if not output_filename:
        return

    output_data = display_analysis_results(results)

    if output_filename.endswith('.txt'):
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for line in output_data:
                output_file.write(line + '\n')

    elif output_filename.endswith('.csv'):
        df = pd.DataFrame([line.split(": ") for line in output_data if ": " in line], columns=["Metric", "Value"])
        df.to_csv(output_filename, index=False)

    elif output_filename.endswith('.xlsx'):
        df = pd.DataFrame([line.split(": ") for line in output_data if ": " in line], columns=["Metric", "Value"])
        df.to_excel(output_filename, index=False)

    messagebox.showinfo("Result", f"Analysis results saved to {output_filename}.")

def process_emails():
    file_path = entry_file.get()

    if not file_path:
        messagebox.showwarning("Warning", "Please select a file.")
        return

    try:
        email_list = read_file(file_path)
        results = analyze_emails(email_list)
        output_data = display_analysis_results(results)

        preview_text.delete(1.0, tk.END)
        for line in output_data:
            preview_text.insert(tk.END, line + '\n')

        save_results_button.config(state=tk.NORMAL)

    except Exception as e:
        preview_text.delete(1.0, tk.END)
        preview_text.insert(tk.END, f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("Email List Analyzer")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

label_file = tk.Label(frame, text="Select File:")
label_file.grid(row=0, column=0, padx=10, pady=5)
entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=5)
button_file = tk.Button(frame, text="Browse", command=select_file)
button_file.grid(row=0, column=2, padx=10, pady=5)

button_process = tk.Button(frame, text="Analyze Emails", command=process_emails)
button_process.grid(row=1, column=0, columnspan=3, pady=20)

save_results_button = tk.Button(frame, text="Save Results", command=lambda: save_results(results), state=tk.DISABLED)
save_results_button.grid(row=2, column=0, columnspan=3, pady=10)

# Preview area for file content and results
preview_label = tk.Label(frame, text="Results Preview:")
preview_label.grid(row=3, column=0, columnspan=3, pady=5)
preview_text = scrolledtext.ScrolledText(frame, width=80, height=15)
preview_text.grid(row=4, column=0, columnspan=3)

root.mainloop()
