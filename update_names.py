import sqlite3

def fix_vernacular_errors():
    conn = sqlite3.connect('smart_tiba.db')
    cursor = conn.cursor()

    # List of corrections: (Correct Word, Incorrect Word)
    corrections = [
        ("Nyanyat", "Kamati"),
        ("Nyanyat", "Kamet")
    ]

    print("--- 🛠️ Starting Database Correction ---")
    
    for correct, wrong in corrections:
        cursor.execute('''
            UPDATE plants 
            SET vernacularKalenjin = ? 
            WHERE vernacularKalenjin = ?
        ''', (correct, wrong))
        
        if cursor.rowcount > 0:
            print(f"✅ Fixed: Replaced '{wrong}' with '{correct}' in Kalenjin column.")
        else:
            print(f"ℹ️ No instances of '{wrong}' found to fix.")

    conn.commit()
    conn.close()
    print("--- 🏁 Correction Complete ---")

if __name__ == "__main__":
    fix_vernacular_errors()