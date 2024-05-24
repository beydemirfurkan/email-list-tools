import zipfile

def extract_and_merge_zip(zip_file, output_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_info_list = zip_ref.infolist()
        print("Files in the zip archive:")
        for zip_info in zip_info_list:
            print(f"- {zip_info.filename}")

        with open(output_file, 'w') as outfile:
            for zip_info in zip_info_list:
                if zip_info.filename.endswith(".txt"):
                    with zip_ref.open(zip_info) as infile:
                        content = infile.read().decode('utf-8')
                        if content.strip():  
                            outfile.write(content + '\n')
                            print(f"Content from {zip_info.filename}:\n{content}")
                        else:
                            print(f"Content from {zip_info.filename} is empty.")

    print(f"Tüm dosyalar {output_file} dosyasında birleştirildi.")

def main():
    zip_file = "emails.zip"
    output_file = "merged_emails.txt"

    extract_and_merge_zip(zip_file, output_file)

if __name__ == "__main__":
    main()
