import sqlite3
import json

def view_database():
    try:
        conn = sqlite3.connect('smart_tiba.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        print("\n" + "="*60)
        print("🌿 SAVED PLANTS IN DATABASE (smart_tiba.db)")
        print("="*60)
        
        plants = cursor.execute('SELECT id, plant_name_english, scientific_name FROM plants').fetchall()
        
        if not plants:
            print("No plants saved yet.")
        else:
            for p in plants:
                print(f"ID: {p['id']:<3} | Normal Name: {p['plant_name_english']:<20} | Scientific: {p['scientific_name']}")

        print("\n" + "="*60)
        print("🩺 SAVED DISEASES IN CACHE")
        print("="*60)
        
        diseases = cursor.execute('SELECT disease_query FROM disease_cache').fetchall()
        
        if not diseases:
            print("No diseases saved yet.")
        else:
            for d in diseases:
                print(f"Disease Query: '{d['disease_query']}'")

        print("\n" + "="*60)
        
    except sqlite3.OperationalError:
        print("❌ Database not found. Make sure you have run 'python init_db.py' first.")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    view_database()