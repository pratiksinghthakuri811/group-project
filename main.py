from database import create_users_table
from login import login, register

create_users_table()

while True:
    print("\n=== Football Management System ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        register()
    elif choice == "2":
        user = login()
        if user:
            print("Access granted.")
            break
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")