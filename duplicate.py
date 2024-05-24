def remove_duplicates(input_file, output_file):
    with open(input_file, 'r') as file:
        emails = file.readlines()

    unique_emails = set()
    duplicate_count = 0

    for email in emails:
        email = email.strip()
        if email in unique_emails:
            duplicate_count += 1
        else:
            unique_emails.add(email)

    with open(output_file, 'w') as file:
        for email in sorted(unique_emails):
            file.write(email + '\n')

    print(f"Toplam {len(unique_emails)} adet tekilleştirilmiş email bulundu.")
    print(f"Toplam {duplicate_count} adet tekrar eden email bulundu.")

def main():
    input_file = "emails.txt"
    output_file = "unique_emails.txt"

    remove_duplicates(input_file, output_file)

if __name__ == "__main__":
    main()
