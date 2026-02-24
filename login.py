import sqlite3
from database import create_connection

# Register new user
def register():
    conn = create_connection()
    cursor = conn.cursor()

    username = input("Enter new username: ")
    password = input("Enter new password: ")
    role = input("Enter role (admin/user): ")

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        print("✅ Registration successful!")
    except:
        print("❌ Username already exists!")

    conn.close()


# Login function
def login():
    conn = create_connection()
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Welcome {username}! Role: {user[3]}")
        return user
    else:
        print("❌ Invalid username or password!")
        return None