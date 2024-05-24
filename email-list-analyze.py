import re
from collections import Counter

def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def analyze_emails(input_file):
    with open(input_file, 'r') as file:
        emails = file.readlines()

    email_counts = Counter()
    invalid_emails = 0
    invalid_reasons = Counter()
    lengths = []
    top_usernames = Counter()
    domain_extensions = Counter()

    for email in emails:
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

    most_common_domains = email_counts.most_common(10)

    print("E-posta Analiz Raporu:")
    print("----------------------")
    print(f"Toplam e-posta adresi: {len(emails)}")
    print(f"Geçersiz e-posta adresi: {invalid_emails}")
    print("\nGeçersiz e-posta adreslerinin sebepleri:")
    for reason, count in invalid_reasons.items():
        print(f"{reason}: {count}")

    print("\nEn çok tekrar eden 5 alan adı:")
    for domain, count in most_common_domains:
        print(f"{domain}: {count} kez")

    print("\nEn uzun e-posta adresi uzunluğu:", max(lengths))
    print("En kısa e-posta adresi uzunluğu:", min(lengths))

    print("\nEn çok tekrar eden 5 kullanıcı adı:")
    for username, count in top_usernames.most_common(10):
        print(f"{username}: {count} kez")

def main():
    input_file = "emails.txt"
    analyze_emails(input_file)

if __name__ == "__main__":
    main()
