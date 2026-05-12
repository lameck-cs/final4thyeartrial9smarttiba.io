import sqlite3
from werkzeug.security import generate_password_hash

DB_NAME = "smart_tiba.db"

def reset_user_password():
    print("\n--- 🛠️ SMART TIBA KENYA: ADMIN PASSWORD RESET ---")
    
    email_to_reset = input("Enter the user's email address: ").strip()
    new_password = input("Enter the new temporary password: ").strip()
    
    if not email_to_reset or not new_password:
        print("❌ Error: Email and new password cannot be blank.")
        return

    # Securely hash the new password
    hashed_password = generate_password_hash(new_password)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if the user exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (email_to_reset,))
    user = cursor.fetchone()
    
    if user:
        # Update the database with the new hashed password
        cursor.execute('UPDATE users SET password_hash = ? WHERE email = ?', (hashed_password, email_to_reset))
        conn.commit()
        print(f"✅ SUCCESS: Password for '{email_to_reset}' has been successfully reset!")
        print(f"📧 You can now email the user and tell them to login with the password: {new_password}")
    else:
        print(f"❌ ERROR: No account found registered with the email '{email_to_reset}'.")
        
    conn.close()

if __name__ == "__main__":
    reset_user_password()