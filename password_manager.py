import sqlite3
import secrets
import string
import base64
import os
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- Configuration & Setup ---
DB_NAME = "vault.db"
SALT_FILE = "salt.key"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )"""
    )
    conn.commit()
    return conn

# --- Encryption & Security ---
def generate_key(master_password: str, salt: bytes) -> bytes:
    """Derives a secure cryptographic key from the master password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def setup_master_password():
    """Sets up the master password for the first time."""
    print("--- First Time Setup ---")
    master_password = getpass.getpass("Create a Master Password: ")
    confirm_password = getpass.getpass("Confirm Master Password: ")
    
    if master_password != confirm_password:
        print("Passwords do not match. Please try again.")
        exit()
        
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    
    return generate_key(master_password, salt)

def authenticate():
    """Authenticates the user and retrieves the encryption key."""
    if not os.path.exists(SALT_FILE):
        return setup_master_password()
    
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
        
    master_password = getpass.getpass("Enter Master Password: ")
    return generate_key(master_password, salt)

# --- Core Features ---
def generate_strong_password(length=16):
    """Generates a cryptographically strong random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def add_password(fernet, conn):
    """Encrypts and adds a new account to the database."""
    website = input("Enter Website/App name: ")
    username = input("Enter Username/Email: ")
    
    choice = input("Do you want to (1) Auto-generate a password or (2) Enter manually? [1/2]: ")
    if choice == '1':
        password = generate_strong_password()
        print(f"Generated Password: {password}")
    else:
        password = getpass.getpass("Enter Password: ")
        
    encrypted_pwd = fernet.encrypt(password.encode()).decode()
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (website, username, password) VALUES (?, ?, ?)", 
                   (website, username, encrypted_pwd))
    conn.commit()
    print(f"\n[+] Credentials for {website} saved securely!")

def retrieve_password(fernet, conn):
    """Retrieves and decrypts a password from the database."""
    website = input("Enter the Website/App name to retrieve: ")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM accounts WHERE website = ?", (website,))
    results = cursor.fetchall()
    
    if not results:
        print(f"\n[-] No accounts found for {website}.")
        return
        
    print(f"\n--- Results for {website} ---")
    for row in results:
        username = row[0]
        encrypted_pwd = row[1]
        try:
            decrypted_pwd = fernet.decrypt(encrypted_pwd.encode()).decode()
            print(f"Username: {username}\nPassword: {decrypted_pwd}\n{'-'*20}")
        except Exception:
            print("[-] Error decrypting password. Invalid Master Password.")

# --- Main Interface ---
def main():
    print("Welcome to the Secure Python Password Manager\n")
    key = authenticate()
    fernet = Fernet(key)
    conn = get_db_connection()
    
    while True:
        print("\n=== Main Menu ===")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Generate a strong password (without saving)")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            add_password(fernet, conn)
        elif choice == '2':
            retrieve_password(fernet, conn)
        elif choice == '3':
            length = int(input("Enter desired password length (default 16): ") or 16)
            print(f"\n[+] Generated Password: {generate_strong_password(length)}")
        elif choice == '4':
            print("Locking vault and exiting. Goodbye!")
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()