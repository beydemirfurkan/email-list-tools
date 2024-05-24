import re
import dns.resolver
import concurrent.futures
from validate_email_address import validate_email

def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, email):
        return False, "Geçersiz email formatı."

    is_valid = validate_email(email)
    if not is_valid:
        return False, "Geçersiz email adresi."

    domain = email.split('@')[1]

    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return False, "MX kaydı bulunamadı."

        dns_records = dns.resolver.resolve(domain, 'A')
        if not dns_records:
            return False, "DNS kaydı bulunamadı."

        return True, "Email adresi geçerli."
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False, "Alan adı bulunamadı."
    except dns.exception.Timeout:
        return False, "DNS sorgusu zaman aşımına uğradı."
    except Exception as e:
        return False, f"Bir hata oluştu: {str(e)}"

def validate_emails(emails):
    valid_emails = []
    invalid_emails = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_email = {executor.submit(is_valid_email, email): email for email in emails}
        for future in concurrent.futures.as_completed(future_to_email):
            email = future_to_email[future]
            try:
                valid, message = future.result()
                if valid:
                    valid_emails.append(email)
                    print(f"{email} geçerli bir email adresidir.")
                else:
                    invalid_emails.append(email)
                    print(f"{email} geçerli bir email adresi değildir. Sebep: {message}")
            except Exception as e:
                invalid_emails.append(email)
                print(f"{email} geçerli bir email adresi değildir. Sebep: {str(e)}")

    return valid_emails, invalid_emails

def read_emails_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def write_emails_to_file(file_path, emails):
    with open(file_path, 'w') as file:
        for email in emails:
            file.write(email + '\n')

def main():
    input_file = "emails.txt"
    valid_emails_file = "valid_emails.txt"
    invalid_emails_file = "invalid_emails.txt"

    emails = read_emails_from_file(input_file)
    valid_emails, invalid_emails = validate_emails(emails)

    write_emails_to_file(valid_emails_file, valid_emails)
    write_emails_to_file(invalid_emails_file, invalid_emails)

    print(f"Geçerli email adresleri {valid_emails_file} dosyasına kaydedildi.")
    print(f"Geçersiz email adresleri {invalid_emails_file} dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
