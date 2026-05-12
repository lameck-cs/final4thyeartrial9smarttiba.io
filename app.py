print("\n--- SMART TIBA KENYA: SECURE PRO-ENGINE WITH OMNI-MODEL FALLBACK ---")

import os
import json
import sqlite3
import requests 
import urllib.parse 
import time  
from flask import Flask, request, jsonify, send_from_directory, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv 

# Load the hidden .env file
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "smart-tiba-kenya-super-secret-key") 
CORS(app)

# --- MULTI-KEY ROTATION SYSTEM (SECURE) ---
api_keys_string = os.environ.get("GEMINI_API_KEYS", "")
API_KEYS = [key.strip() for key in api_keys_string.split(",") if key.strip()]

if not API_KEYS:
    print("❌ CRITICAL SECURITY WARNING: No API keys found in .env file or environment variables!")
    API_KEYS = ["MISSING_KEY"]

current_key_index = 0
client = genai.Client(api_key=API_KEYS[current_key_index])

DB_NAME = "smart_tiba.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- AUTO-INITIALIZE NEW TABLES ---
def init_dynamic_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cultivation_cache (
            query_key TEXT PRIMARY KEY,
            forecast_json TEXT NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_dynamic_tables() 

# --- AUTHENTICATION ROUTES ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if existing_user:
        conn.close()
        return jsonify({"error": "Email already registered"}), 400

    password_hash = generate_password_hash(password)
    try:
        conn.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                     (username, email, password_hash))
        conn.commit()
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"message": "Login successful", "username": user['username']}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear() 
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/current_user', methods=['GET'])
def current_user():
    if 'user_id' in session:
        return jsonify({"logged_in": True, "username": session.get('username')})
    return jsonify({"logged_in": False})


# --- BULLETPROOF HELPER: Wikipedia REST API ---
def get_wiki_image(plant_name, scientific_name=None):
    search_terms = []
    
    if scientific_name and scientific_name.lower() != "unknown":
        clean_sci_name = " ".join(scientific_name.split()[:2])
        search_terms.append(clean_sci_name)
        
    if plant_name:
        search_terms.append(plant_name)

    # 1. Try Wikipedia First
    for term in search_terms:
        try:
            formatted_term = urllib.parse.quote(term.strip().replace(" ", "_"))
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_term}"
            headers = {'User-Agent': 'SmartTibaKenyaApp/1.0'}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "originalimage" in data and "source" in data["originalimage"]:
                    return data["originalimage"]["source"]
                elif "thumbnail" in data and "source" in data["thumbnail"]:
                    return data["thumbnail"]["source"]
        except Exception:
            pass 
            
    # 2. 🌟 NEW FIX: Safe, permanent Unsplash generic plant placeholder (NO CATS!)
    return "https://images.unsplash.com/photo-1497250681554-18398b1e428c?auto=format&fit=crop&w=600&q=80"

# --- GEMINI API HANDLER WITH OMNI-MODEL FALLBACK & STRICT=FALSE FIX ---
def get_gemini_response(prompt, image_bytes=None, mime_type="image/jpeg"):
    global current_key_index, client
    
    if API_KEYS[0] == "MISSING_KEY":
        print("❌ Error: API Keys are missing. Check your Render Environment Variables or .env file.")
        return None

    # --- UPDATED: Only using active, supported models ---
    models = [
        "gemini-2.5-flash", 
        "gemini-2.0-flash"
    ]
    
    for model_name in models:
        attempts = 0
        while attempts < len(API_KEYS):
            try:
                print(f"🤖 [API CALL] Contacting {model_name} (Using Key index {current_key_index})")
                if image_bytes:
                    res = client.models.generate_content(model=model_name, contents=[prompt, types.Part.from_bytes(data=image_bytes, mime_type=mime_type)])
                else:
                    res = client.models.generate_content(model=model_name, contents=[prompt])
                
                print(f"✅ [SUCCESS] Data received from {model_name}")
                
                return json.loads(res.text.replace("```json", "").replace("```", "").strip(), strict=False)
                
            except Exception as e:
                error_msg = str(e).lower()
                
                if "quota" in error_msg or "429" in error_msg or "exhausted" in error_msg or "403" in error_msg or "leaked" in error_msg or "permission" in error_msg:
                    print(f"🔄 [KEY REJECTED/EMPTY] Shifting to backup API Key...")
                    current_key_index = (current_key_index + 1) % len(API_KEYS)
                    client = genai.Client(api_key=API_KEYS[current_key_index])
                    attempts += 1
                    continue
                
                elif "503" in error_msg or "unavailable" in error_msg or "high demand" in error_msg:
                    print(f"⏳ [SERVER BUSY] {model_name} is overwhelmed. Waiting 2 seconds...")
                    time.sleep(2) 
                    attempts += 1
                    continue
                
                else:
                    print(f"⚠️ [MODEL FAILED] {model_name} failed with: {e}. Trying next model...")
                    break 
                    
    print("❌ [FATAL] All AI models and all API Keys failed.")
    return None

# --- DATABASE CACHE LOGIC ---
def query_disease_db(disease_name):
    conn = get_db_connection()
    row = conn.execute('SELECT suggestions_json FROM disease_cache WHERE disease_query = ?', (disease_name.lower(),)).fetchone()
    conn.close()
    return json.loads(row['suggestions_json']) if row else None

def save_disease_to_db(disease_name, suggestions):
    conn = get_db_connection()
    conn.execute('INSERT OR REPLACE INTO disease_cache (disease_query, suggestions_json) VALUES (?, ?)', (disease_name.lower(), json.dumps(suggestions)))
    conn.commit()
    conn.close()

def query_forecast_db(crop, county):
    query_key = f"{crop}_{county}".lower()
    conn = get_db_connection()
    row = conn.execute('SELECT forecast_json FROM cultivation_cache WHERE query_key = ?', (query_key,)).fetchone()
    conn.close()
    return json.loads(row['forecast_json']) if row else None

def save_forecast_to_db(crop, county, forecast_data):
    query_key = f"{crop}_{county}".lower()
    conn = get_db_connection()
    conn.execute('INSERT OR REPLACE INTO cultivation_cache (query_key, forecast_json) VALUES (?, ?)', (query_key, json.dumps(forecast_data)))
    conn.commit()
    conn.close()

def query_db_by_image_analysis(analysis_data):
    sci_name = analysis_data.get("scientific_name")
    eng_name = analysis_data.get("plant_name_english")
    conn = get_db_connection()
    plant = conn.execute('''
        SELECT * FROM plants 
        WHERE (scientific_name = ? AND scientific_name != 'Unknown') 
           OR (plant_name_english = ? AND plant_name_english != 'Unknown')
    ''', (sci_name, eng_name)).fetchone()
    conn.close()
    if plant: return db_row_to_api_response(plant)
    return None

def save_plant_to_db(api_data):
    eng_name = api_data.get("plant_name_english")
    sci_name = api_data.get("scientific_name", "Unknown")
    if not eng_name or eng_name == "Unknown": return 
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT OR REPLACE INTO plants (
                plant_name_english, scientific_name, vernacularSwahili, vernacularKalenjin, vernacularLuo, vernacularKisii, vernacularKikuyu,
                usesTraditional, usesScientific, preparationMethod, safetyWarning, commercialStatus, commercialMarketAdvice
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            eng_name, sci_name, api_data.get("local_names", {}).get("swahili"),
            api_data.get("local_names", {}).get("kalenjin"), api_data.get("local_names", {}).get("luo"),
            api_data.get("local_names", {}).get("kisii"), api_data.get("local_names", {}).get("kikuyu"),
            json.dumps(api_data.get("medicinal_uses", {}).get("traditional")), api_data.get("medicinal_uses", {}).get("scientific_backing"),
            json.dumps(api_data.get("preparation_method")), api_data.get("safety_warning"),
            api_data.get("commercial_value", {}).get("status"), api_data.get("commercial_value", {}).get("market_advice")
        ))
        conn.commit()
    except Exception as e:
        print(f"DB Save Error: {e}")
    finally:
        conn.close()

def db_row_to_api_response(row):
    eng_name = row['plant_name_english']
    sci_name = row['scientific_name']
    return {
        "plant_name_english": eng_name,
        "scientific_name": sci_name,
        "image_url": get_wiki_image(eng_name, sci_name),
        "local_names": {
            "swahili": row['vernacularSwahili'] or "Unknown",
            "kalenjin": row['vernacularKalenjin'] or "Unknown",
            "luo": row['vernacularLuo'] or "Unknown",
            "kisii": row['vernacularKisii'] or "Unknown",
            "kikuyu": row['vernacularKikuyu'] or "Unknown"
        },
        "medicinal_uses": {
            "traditional": json.loads(row['usesTraditional']) if row['usesTraditional'] else [],
            "scientific_backing": row['usesScientific']
        },
        "preparation_method": json.loads(row['preparationMethod']) if row['preparationMethod'] else [],
        "safety_warning": row['safetyWarning'],
        "commercial_value": {
            "status": row['commercialStatus'],
            "market_advice": row['commercialMarketAdvice']
        },
        "source": "Local Database (Smart Tiba Kenya Cache)"
    }


# --- PROMPTS ---
BOTANICAL_ANALYSIS_PROMPT = """
        You are an elite expert in Kenyan Ethnobotany and Linguistics. Analyze this plant/weed. Identify it and provide its medicinal properties.
        CRITICAL VERNACULAR RULES:
        1. For local_names, provide ONLY the botanical name used in that culture.
        2. DO NOT use family titles or kinship terms.
        3. If a common Swahili name is used locally, use that rather than inventing a word.
        4. DO NOT use markdown formatting (** or #).
        OUTPUT ONLY RAW JSON:
        {
            "plant_name_english": "Name", "scientific_name": "Scientific Name",
            "local_names": {"swahili": "...", "kalenjin": "...", "luo": "...", "kisii": "...", "kikuyu": "..."},
            "medicinal_uses": {"traditional": ["Use 1"], "scientific_backing": "..."},
            "preparation_method": ["Step 1"], "safety_warning": "...",
            "commercial_value": {"status": "Value", "market_advice": "..."}
        }
        """

CULTIVATION_PROMPT = """
    You are an Agricultural Economist and Botanist in Kenya. DO NOT use markdown like asterisks (**). Keep text plain.
    Provide a cultivation and commercialization guide for '{crop_name}' in {county} County, Kenya.
    OUTPUT ONLY RAW JSON.
    {{
        "crop": "{crop_name}", "location": "{county}",
        "risks": [{{
            "disease_name": "Ecological Suitability", "probability_score": 90, "description": "Suitability explanation",
            "risk_months": "Best planting season", "affected_counties": "Required Soil Type",
            "conditions": "Water/Sun requirements", "remedy": "Market advice/Value addition."
        }}]
    }}
    """

# --- API ROUTES ---
@app.route("/identify", methods=["POST"])
def identify_image():
    if "user_id" not in session: return jsonify({"error": "Unauthorized"}), 401
    if "image" not in request.files: return jsonify({"error": "No image uploaded"}), 400
    try:
        image_bytes = request.files["image"].read()
        mime_type = request.files["image"].content_type or "image/jpeg"
        
        id_prompt = "Identify this Kenyan plant. OUTPUT RAW JSON: {'plant_name_english': '...', 'scientific_name': '...'}. Keep text plain, no asterisks."
        analysis = get_gemini_response(id_prompt, image_bytes, mime_type)
        if analysis:
            db_result = query_db_by_image_analysis(analysis)
            if db_result: return jsonify(db_result)

        full_analysis = get_gemini_response(BOTANICAL_ANALYSIS_PROMPT, image_bytes, mime_type)
        if not full_analysis: return jsonify({"error": "System Busy or Quota Exceeded. Please try again in 1 minute."}), 503
        
        save_plant_to_db(full_analysis)
        full_analysis["source"] = "Google Gemini AI (Real-time Analysis)"
        full_analysis["image_url"] = get_wiki_image(full_analysis.get("plant_name_english", ""), full_analysis.get("scientific_name", ""))
        
        return jsonify(full_analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/search_plant", methods=["POST"])
def search_plant():
    if "user_id" not in session: return jsonify({"error": "Unauthorized"}), 401
    plant_name = request.json.get("plant_name", "").strip()
    
    conn = get_db_connection()
    search_pattern = f'%{plant_name}%'
    row = conn.execute('''
        SELECT * FROM plants 
        WHERE plant_name_english LIKE ? 
        OR scientific_name LIKE ?
        OR vernacularSwahili LIKE ?
        OR vernacularKalenjin LIKE ?
        OR vernacularLuo LIKE ?
        OR vernacularKisii LIKE ?
        OR vernacularKikuyu LIKE ?
    ''', (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)).fetchone()
    conn.close()
    
    if row: return jsonify(db_row_to_api_response(row))

    print(f"🔍 [DATABASE MISS] Plant not found locally. Asking Gemini...")
    text_prompt = f"The user is searching for the plant named '{plant_name}'.\n\n" + BOTANICAL_ANALYSIS_PROMPT
    data = get_gemini_response(text_prompt)
    
    if data and data.get("plant_name_english") and data.get("plant_name_english") != "Unknown":
        save_plant_to_db(data)
        data["source"] = "Google Gemini AI (Text Query)"
        data["image_url"] = get_wiki_image(data.get("plant_name_english", ""), data.get("scientific_name", ""))
        return jsonify(data)
        
    return jsonify({"error": "Plant not found or AI limits exceeded. Try again later."}), 404


@app.route("/search_disease", methods=["POST"])
def search_disease():
    if "user_id" not in session: return jsonify({"error": "Unauthorized"}), 401
    disease_name = request.json.get("disease_name", "").strip()
    
    cached_data = query_disease_db(disease_name)
    if cached_data:
        is_obsolete = isinstance(cached_data, list) or "disease_description" not in cached_data
        
        if is_obsolete:
            print(f"🔄 [CACHE FIX] Upgrading data for '{disease_name}' to include Medical Descriptions...")
        else:
            cures_list = cached_data.get("cures", [])
            is_missing_scientific = any("scientific_name" not in s for s in cures_list)
            
            if not is_missing_scientific:
                print(f"⚡ [DATABASE HIT] Found fresh saved cures for: '{disease_name}'")
                for s in cures_list:
                    if "image_url" not in s or s["image_url"] == "logo.png":
                        s["image_url"] = get_wiki_image(s["english_name"], s.get("scientific_name"))
                
                return jsonify({
                    "disease": disease_name, 
                    "disease_description": cached_data.get("disease_description"),
                    "suggestions": cures_list, 
                    "source": "Local Database"
                })

    print(f"🔍 [DATABASE MISS] Fetching medical definition and cures for '{disease_name}' via Gemini...")
    
    prompt = f"""
    You are an expert medical professional, Kenyan ethnobotanist, and toxicologist. 
    First, provide a brief, clear medical definition/description of '{disease_name}'.
    Then, suggest reliable medicinal plants commonly used in Kenya to treat or control it.
    DO NOT use markdown asterisks (**). Keep text plain.
    CRITICAL RULE: Herbal medicine can be deadly if prepared incorrectly. You MUST include precise preparation methods and explicitly state what NOT to do to avoid poisoning.
    OUTPUT ONLY RAW JSON in this exact format:
    {{
        "disease_description": "Brief medical definition of the disease goes here...",
        "cures": [
            {{
                "english_name": "Garlic", 
                "scientific_name": "Allium sativum",
                "swahili_name": "Kitunguu Saumu",
                "brief_medicinal_properties": "Biochemical compound Allicin proven to reduce systolic blood pressure.",
                "preparation_method": ["Crush 1-2 cloves and let sit for 10 mins.", "Consume raw with water.", "DO NOT boil."],
                "safety_warning": "Safe but can thin blood; consult doctor if taking medication."
            }}
        ]
    }}
    """
    response_data = get_gemini_response(prompt)
    if not response_data or "cures" not in response_data: 
        return jsonify({"error": "Quota exceeded or system busy. Please try again in 1 minute."}), 503
    
    description = response_data.get("disease_description", "No description available.")
    suggestions = response_data.get("cures", [])
    
    for s in suggestions: 
        s["search_query"] = s["english_name"]
        s["image_url"] = get_wiki_image(s["english_name"], s.get("scientific_name"))
        
    save_disease_to_db(disease_name, response_data)
    
    return jsonify({
        "disease": disease_name, 
        "disease_description": description, 
        "suggestions": suggestions, 
        "source": "Google Gemini AI"
    })

@app.route("/forecast_risk", methods=["POST"])
def cultivate():
    if "user_id" not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    crop = data.get("crop_name", "").strip()
    county = data.get("county", "").strip()

    cached_forecast = query_forecast_db(crop, county)
    if cached_forecast:
        print(f"⚡ [DATABASE HIT] Found cached forecast for {crop} in {county}")
        return jsonify(cached_forecast)

    print(f"🔍 [DATABASE MISS] Fetching ecological forecast for {crop} in {county} via Gemini...")
    prediction = get_gemini_response(CULTIVATION_PROMPT.format(crop_name=crop, county=county))
    if not prediction: 
        return jsonify({"error": "Quota Exceeded. Please try again later."}), 500

    save_forecast_to_db(crop, county, prediction)
    return jsonify(prediction)

# --- CHATBOT API ROUTE ---
@app.route("/api/chat", methods=["POST"])
def chat():
    if "user_id" not in session: return jsonify({"error": "Unauthorized"}), 401
    user_msg = request.json.get("message", "").strip()
    
    prompt = f"""
    You are the official Customer Support and Ethnobotany Assistant for 'Smart Tiba Kenya'. 
    The user is asking: "{user_msg}"
    Provide a polite, concise, and helpful response. If they ask about ethnobotany, give them a brief fact.
    Do not use markdown like asterisks (**). 
    OUTPUT ONLY RAW JSON: {{"reply": "your text response here"}}
    """
    
    data = get_gemini_response(prompt)
    if data and "reply" in data:
        return jsonify({"reply": data["reply"]})
        
    return jsonify({"reply": "I'm sorry, all our AI agents are currently busy or our daily quota has been reached! Please email lameck.cs16@gmail.com or call +254 725 713 859 for 24/7 assistance."})

# --- SECURE PAGE SERVING ---
@app.route('/')
def serve_index(): 
    if 'user_id' not in session:
        return redirect('/login.html')
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    protected_pages = ['index.html', 'diagnosis.html', 'risk.html', 'support.html']
    if path in protected_pages and 'user_id' not in session:
        return redirect('/login.html')
    return send_from_directory('.', path)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)