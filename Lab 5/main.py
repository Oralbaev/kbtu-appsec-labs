from getpass import getpass

from encryption import encrypt_file, decrypt_file
from password import hash_password, verify_password


def show_menu():
    print("\n=== Cryptography App ===")
    print("1. Encrypt file")
    print("2. Decrypt file")
    print("3. Hash password")
    print("4. Verify password")
    print("0. Exit")


def main():
    while True:
        show_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            filename = input("Enter file name: ")
            encrypt_file(filename)

        elif choice == "2":
            filename = input("Enter encrypted file name: ")
            decrypt_file(filename)

        elif choice == "3":
            password = getpass("Enter password: ")
            hash_password(password)

        elif choice == "4":
            password = getpass("Enter password to verify: ")
            verify_password(password)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()