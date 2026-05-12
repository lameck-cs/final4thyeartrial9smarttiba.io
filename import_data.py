import csv
import sqlite3
import json
import os

DB_NAME = "smart_tiba.db"

def import_mitishamba_data(csv_filepath):
    if not os.path.exists(csv_filepath):
        print(f"❌ Error: Could not find the file '{csv_filepath}'. Please make sure it is in the same folder.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # CHANGED TO 'utf-8-sig' to automatically remove invisible Windows BOM characters!
        with open(csv_filepath, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            print(f"📊 Found Columns: {reader.fieldnames}") # This will help us see if Excel messed up the commas
            
            success_count = 0
            error_count = 0
            
            print(f"⏳ Reading data from {csv_filepath}...")
            
            for row in reader:
                try:
                    # Extract the English Name first (it's our unique identifier)
                    eng_name = row.get('English Name', '').strip()
                    
                    if not eng_name:
                        continue 
                        
                    sci_name = row.get('Scientific Name', 'Unknown').strip()
                    swa = row.get('Swahili', 'Unknown').strip()
                    kal = row.get('Kalenjin', 'Unknown').strip()
                    luo = row.get('Luo', 'Unknown').strip()
                    kis = row.get('Kisii', 'Unknown').strip()
                    kik = row.get('Kikuyu', 'Unknown').strip()
                    
                    raw_trad = row.get('Traditional Uses', '').strip()
                    trad_list = [item.strip() for item in raw_trad.split('|')] if raw_trad else []
                    
                    sci_back = row.get('Scientific Backing', '').strip()
                    
                    raw_prep = row.get('Preparation', '').strip()
                    prep_list = [item.strip() for item in raw_prep.split('|')] if raw_prep else []
                    
                    safety = row.get('Safety Warning', '').strip()
                    comm_stat = row.get('Commercial Status', 'Unknown').strip()
                    comm_adv = row.get('Market Advice', '').strip()

                    # Insert into the database
                    cursor.execute('''
                        INSERT OR REPLACE INTO plants (
                            plant_name_english, scientific_name, vernacularSwahili, vernacularKalenjin, vernacularLuo, vernacularKisii, vernacularKikuyu,
                            usesTraditional, usesScientific, preparationMethod, safetyWarning, commercialStatus, commercialMarketAdvice
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        eng_name, sci_name, swa, kal, luo, kis, kik,
                        json.dumps(trad_list), sci_back, json.dumps(prep_list), safety, comm_stat, comm_adv
                    ))
                    success_count += 1
                except Exception as row_e:
                    print(f"⚠️ Error importing row '{eng_name}': {row_e}")
                    error_count += 1

        conn.commit()
        print(f"\n✅ SUCCESS! Added or Updated {success_count} plants in the Smart Tiba Kenya database.")
        if error_count > 0:
            print(f"⚠️ {error_count} plants failed to import.")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("\n🌿 SMART TIBA KENYA: MITISHAMBA BULK IMPORTER 🌿")
    print("Make sure your CSV file has the correct column headers.")
    csv_file = input("Enter the exact name of your CSV file (e.g., plants.csv): ")
    import_mitishamba_data(csv_file)