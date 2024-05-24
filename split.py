import os
import zipfile

def split_emails(input_file, emails_per_file):
    with open(input_file, 'r') as file:
        emails = file.readlines()

    total_emails = len(emails)
    num_files = (total_emails + emails_per_file - 1) // emails_per_file

    output_files = []
    for i in range(num_files):
        start_index = i * emails_per_file
        end_index = min(start_index + emails_per_file, total_emails)
        chunk_emails = emails[start_index:end_index]
        output_filename = f"emails_part_{i + 1}.txt"
        with open(output_filename, 'w') as output_file:
            output_file.writelines(chunk_emails)
        output_files.append(output_filename)

    return output_files

def create_zip_file(file_list, output_zip_file):
    with zipfile.ZipFile(output_zip_file, 'w') as zipf:
        for file in file_list:
            zipf.write(file)
            os.remove(file)  

def main():
    input_file = "valid_emails.txt"
    emails_per_file = 50000
    output_zip_file = "split_emails.zip"

    output_files = split_emails(input_file, emails_per_file)

    create_zip_file(output_files, output_zip_file)

    print(f"Toplam {len(output_files)} adet dosya {output_zip_file} dosyasına sıkıştırıldı.")

if __name__ == "__main__":
    main()
