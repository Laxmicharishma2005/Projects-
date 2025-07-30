import os

USER_FILE = "users.txt"

def register_user():
    print("🔐 Register New User")
    username = input("Enter username: ")
    password = input("Enter password: ")

    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password}\n")
    print("✅ Registration successful!\n")


def login_user():
    print("🔑 Login")
    username = input("Username: ")
    password = input("Password: ")

    if not os.path.exists(USER_FILE):
        print("❌ No users registered yet.")
        return None

    with open(USER_FILE, "r") as f:
        for line in f:
            stored_user, stored_pass = line.strip().split(",")
            if username == stored_user and password == stored_pass:
                print("✅ Login successful!\n")
                return username

    print("❌ Invalid username or password.\n")
    return None


def logout_user(username):
    print(f"👋 {username}, you have been logged out. See you next time!\n")
