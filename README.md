# 🔐 Password Manager (Python)

## 📌 Project Overview  
This project is a **Password Manager built using Python** that allows users to securely store, manage, and retrieve their passwords. It helps users avoid weak or repeated passwords by providing a secure and organized system for credential management.

The application uses encryption techniques to protect sensitive data and ensures that only authorized users can access stored information using a master password.

---

## 🎯 Objective  
- To develop a secure password storage system  
- To prevent password reuse and improve security  
- To enable easy retrieval of stored credentials  
- To generate strong and random passwords  

---

## 🚀 Features  

- 🔒 Secure password storage using AES encryption  
- 🔑 Master password protection with PBKDF2HMAC key derivation  
- ➕ Add new credentials (website, username, password)  
- 🔍 Retrieve saved credentials  
- ⚙️ Generate strong, cryptographically secure random passwords  
- 🗄️ Local SQLite database for organized credential management  

---

## 🛠️ Technologies Used  

- **Python 3** - **Libraries:**
  - `sqlite3` – for local database management  
  - `cryptography` – for Fernet (AES) encryption and key derivation  
  - `secrets` – for secure password generation  
  - `os` & `getpass` – for file handling and secure password input  

---

## 📂 Project Structure  

```text
password_manager.py                                      # Main Python script
requirements.txt                                         # Python dependencies
README.md                                                # Documentation
RAJADITYA_PasswordManager_InternshipReport_USC_UCT.pdf   # Internship Final Report
