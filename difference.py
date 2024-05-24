import tkinter as tk
from tkinter import filedialog, messagebox

def select_file1():
    file_path = filedialog.askopenfilename()
    entry_file1.delete(0, tk.END)
    entry_file1.insert(0, file_path)

def select_file2():
    file_path = filedialog.askopenfilename()
    entry_file2.delete(0, tk.END)
    entry_file2.insert(0, file_path)

def find_differences():
    file1_path = entry_file1.get()
    file2_path = entry_file2.get()

    if not file1_path or not file2_path:
        messagebox.showwarning("Uyarı", "Lütfen her iki dosyayı da seçin.")
        return

    try:
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            file1_lines = {line.strip() for line in file1 if line.strip()}
            file2_lines = {line.strip() for line in file2 if line.strip()}

        unique_lines_file1 = file1_lines - file2_lines

        if unique_lines_file1:
            output_filename = 'differences.txt'
            with open(output_filename, 'w', encoding='utf-8') as diff_file:
                for line in unique_lines_file1:
                    diff_file.write(line + '\n')
            label_result.config(text=f"Farklar {output_filename} dosyasına yazıldı.")
            messagebox.showinfo("Sonuç", f"{len(unique_lines_file1)} benzersiz satır 1. dosyada bulundu.")
        else:
            label_result.config(text="1. dosya tamamen 2. dosyanın bir alt kümesi.")
            messagebox.showinfo("Sonuç", "1. dosyada 2. dosyadan farklı satır bulunamadı.")

    except Exception as e:
        label_result.config(text=f"Hata: {str(e)}")
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

root = tk.Tk()
root.title("Dosya Farkı Bulucu")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

label_file1 = tk.Label(frame, text="Birinci Dosya:")
label_file1.grid(row=0, column=0, padx=10, pady=5)
entry_file1 = tk.Entry(frame, width=50)
entry_file1.grid(row=0, column=1, padx=10, pady=5)
button_file1 = tk.Button(frame, text="Seç", command=select_file1)
button_file1.grid(row=0, column=2, padx=10, pady=5)

label_file2 = tk.Label(frame, text="İkinci Dosya:")
label_file2.grid(row=1, column=0, padx=10, pady=5)
entry_file2 = tk.Entry(frame, width=50)
entry_file2.grid(row=1, column=1, padx=10, pady=5)
button_file2 = tk.Button(frame, text="Seç", command=select_file2)
button_file2.grid(row=1, column=2, padx=10, pady=5)

button_diff = tk.Button(frame, text="Farkları Bul", command=find_differences)
button_diff.grid(row=2, column=0, columnspan=3, pady=20)

label_result = tk.Label(frame, text="")
label_result.grid(row=3, column=0, columnspan=3)

root.mainloop()
