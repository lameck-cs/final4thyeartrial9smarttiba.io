import sqlite3
import json

def init_db():
    try:
        conn = sqlite3.connect('smart_tiba.db')
        cursor = conn.cursor()
        
        # 1. Create the plants table 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_name_english TEXT NOT NULL UNIQUE,
                scientific_name TEXT,
                vernacularSwahili TEXT,
                vernacularKalenjin TEXT,
                vernacularLuo TEXT,
                vernacularKisii TEXT,
                vernacularKikuyu TEXT,
                usesTraditional TEXT, 
                usesScientific TEXT,
                preparationMethod TEXT, 
                safetyWarning TEXT,
                commercialStatus TEXT,
                commercialMarketAdvice TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Disease Suggestions Cache Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disease_cache (
                disease_query TEXT PRIMARY KEY,
                suggestions_json TEXT NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scientific_name ON plants (scientific_name)')

        # 3. NEW: Secure Users Table for Authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # SEED DATA: Common Kenyan Plants
        seed_plants = [
            {
                "eng": "Neem Tree", "sci": "Azadirachta indica",
                "swa": "Mwarobaini", "kal": "Mwarobaini", "luo": "Mwarobaini", "kis": "Mwarobaini", "kik": "Mwarobaini",
                "trad": ["Treating malaria and fevers.", "Curing skin diseases.", "Stomach aches."],
                "sci_back": "Contains azadirachtin; proven anti-malarial and antibacterial properties.",
                "prep": ["Boil 5-10 fresh leaves in 2 cups of water for 15 minutes.", "Drink half a cup twice a day."],
                "safe": "DO NOT give to children under 12 or pregnant women.",
                "comm_stat": "High Value", "comm_adv": "Extract neem oil or sell dried leaves for herbal teas."
            },
            {
                "eng": "Blackjack", "sci": "Bidens pilosa",
                "swa": "Kichoma Mguu", "kal": "Kipkoleit", "luo": "Onyiego", "kis": "Enyaboke", "kik": "Muceege",
                "trad": ["Treating fresh wounds.", "Curing stomach ulcers.", "Managing blood pressure."],
                "sci_back": "Rich in flavonoids; acts as a natural antibiotic.",
                "prep": ["Crush fresh leaves into a paste for wounds.", "Boil leaves for 10 mins for ulcers."],
                "safe": "Generally safe. Wash thoroughly to remove pesticides.",
                "comm_stat": "Untapped", "comm_adv": "Dry and package as a detoxifying herbal tea."
            },
            {
                "eng": "Stinging Nettle", "sci": "Urtica dioica",
                "swa": "Thabai", "kal": "Siwot", "luo": "Kayo", "kis": "Enyabikira", "kik": "Hatha",
                "trad": ["Treating arthritis and joint pain.", "Boosting blood count (anemia).", "Managing prostate issues in men."],
                "sci_back": "Contains high levels of iron, Vitamin C, and histamine. Extracts inhibit inflammatory pathways.",
                "prep": ["Wear gloves to harvest.", "Boil leaves for 10 minutes to neutralize the sting.", "Drink the broth or eat as a vegetable (Mukimo)."],
                "safe": "CRITICAL: Do not eat raw, the sting causes severe allergic reactions. Safe once boiled or dried.",
                "comm_stat": "High Value", "comm_adv": "Dry the leaves and grind into a powder. Sells at a premium as a health supplement for smoothies and teas."
            },
            {
                "eng": "Aloe Vera", "sci": "Aloe barbadensis",
                "swa": "Shubiri", "kal": "Tugumin", "luo": "Ogaka", "kis": "Enyarwanda", "kik": "Kiluma",
                "trad": ["Healing burns and skin rashes.", "Treating severe constipation.", "Poultry medicine (added to chicken water)."],
                "sci_back": "The gel contains acemannan which accelerates tissue repair. The latex contains aloin, a powerful laxative.",
                "prep": ["Slice the leaf open and scoop out the clear gel for skin application.", "For internal use, wash away the yellow sap (latex) thoroughly before blending."],
                "safe": "DO NOT consume the yellow latex just under the skin in large amounts; it causes severe cramping and diarrhea. Avoid internal use if pregnant.",
                "comm_stat": "High Value", "comm_adv": "Extract and stabilize the clear gel to sell to cosmetic companies, or sell whole mature leaves in urban markets."
            },
            {
                "eng": "Moringa", "sci": "Moringa oleifera",
                "swa": "Mlonge", "kal": "Moringa", "luo": "Moringa", "kis": "Moringa", "kik": "Moringa",
                "trad": ["General immunity booster.", "Increasing breast milk production.", "Managing diabetes and blood sugar."],
                "sci_back": "Exceptionally rich in vitamins, minerals, and antioxidants like quercetin and chlorogenic acid which stabilize blood sugar.",
                "prep": ["Dry leaves in the shade (not direct sun) to preserve vitamins.", "Grind into a powder and add 1 teaspoon to porridge, hot water, or food."],
                "safe": "Leaves are highly safe. Avoid eating the root bark, which contains toxic alkaloids.",
                "comm_stat": "High Value", "comm_adv": "Highly commercial. Sell dried leaf powder as a superfood supplement. Press seeds for high-value Ben oil."
            }
        ]

        for p in seed_plants:
            cursor.execute('''
                INSERT OR IGNORE INTO plants (
                    plant_name_english, scientific_name, vernacularSwahili, vernacularKalenjin, vernacularLuo, vernacularKisii, vernacularKikuyu,
                    usesTraditional, usesScientific, preparationMethod, safetyWarning, commercialStatus, commercialMarketAdvice
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                p["eng"], p["sci"], p["swa"], p["kal"], p["luo"], p["kis"], p["kik"],
                json.dumps(p["trad"]), p["sci_back"], json.dumps(p["prep"]), p["safe"], p["comm_stat"], p["comm_adv"]
            ))

        conn.commit()
        print("✅ Database 'smart_tiba.db' initialized! Security tables ready.")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()