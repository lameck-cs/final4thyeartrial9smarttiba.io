import sqlite3
import json

DB_NAME = "smart_tiba.db"

plants_data = [
    # --- INDIGENOUS & HIGH-VALUE TREES/SHRUBS ---
    {
        "English Name": "African Cherry", "Scientific Name": "Prunus africana", "Swahili": "Mueri", "Kalenjin": "Tenduet", "Luo": "Mueri", "Kisii": "Omotamayu", "Kikuyu": "Muiri",
        "Traditional Uses": "Treats prostate gland enlargement | Relieves chest pain | Manages malaria",
        "Scientific Backing": "Contains phytosterols and pentacyclic triterpenoids proven to reduce prostate inflammation.",
        "Preparation": "Boil the bark for 20 minutes | Drink one cup daily | Do not exceed recommended dosage.",
        "Safety Warning": "High doses can cause stomach upset. Must be sustainably harvested to avoid killing the tree.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Harvesting the bark is highly lucrative for pharmaceutical export (treating benign prostatic hyperplasia). Plant on a large scale."
    },
    {
        "English Name": "Sausage Tree", "Scientific Name": "Kigelia africana", "Swahili": "Mvungunya", "Kalenjin": "Ratinuet", "Luo": "Yago", "Kisii": "Omosabibu", "Kikuyu": "Muratina",
        "Traditional Uses": "Treats skin fungal infections | Manages syphilis | Applied to wounds and ulcers",
        "Scientific Backing": "Rich in iridoids and naphthoquinones showing strong antibacterial and antifungal activity.",
        "Preparation": "Roast the fruit before applying as a poultice | Boil bark for internal use.",
        "Safety Warning": "Raw fruit is highly poisonous and can cause severe mouth blistering. Must be cooked.",
        "Commercial Status": "Moderate",
        "Market Advice": "High potential in the cosmetic industry for skin creams and ointments targeting acne and psoriasis."
    },
    {
        "English Name": "East African Greenheart", "Scientific Name": "Warburgia ugandensis", "Swahili": "Muthiga", "Kalenjin": "Sokotwek", "Luo": "Apacha", "Kisii": "Omosokonoi", "Kikuyu": "Muthiga",
        "Traditional Uses": "Relieves toothaches | Treats common cold and malaria | Manages stomach ulcers",
        "Scientific Backing": "Possesses potent antimicrobial and antifungal drimane sesquiterpenes.",
        "Preparation": "Chew leaves for toothaches | Boil bark and roots for malaria tea | Use sparingly.",
        "Safety Warning": "Extremely potent and spicy. Can cause vomiting in large doses. Not for pregnant women.",
        "Commercial Status": "High",
        "Market Advice": "Excellent commercial potential for natural toothpastes and organic antimicrobial throat lozenges."
    },
    {
        "English Name": "White's Ginger", "Scientific Name": "Mondia whitei", "Swahili": "Mukombero", "Kalenjin": "Kumukombero", "Luo": "Okombere", "Kisii": "Omokombero", "Kikuyu": "Mukombero",
        "Traditional Uses": "Boosts male fertility and libido | Stimulates appetite | Relieves stress and depression",
        "Scientific Backing": "Contains zinc, iron, and bio-active saponins proven to increase testosterone and improve sperm motility.",
        "Preparation": "Chew the fresh or dried roots directly | Boil roots to make a potent tea.",
        "Safety Warning": "Generally very safe. Can cause mild insomnia if taken in massive doses late at night.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Highly endangered in the wild. Cultivating this is a guaranteed cash crop for energy drinks and supplements."
    },
    {
        "English Name": "Croton", "Scientific Name": "Croton megalocarpus", "Swahili": "Musine", "Kalenjin": "Masineitet", "Luo": "Kanya-nya", "Kisii": "Omosene", "Kikuyu": "Mukinduri",
        "Traditional Uses": "Treats severe stomach aches | Bark used for deworming poultry | Poultice for swelling",
        "Scientific Backing": "Seeds contain highly potent croton oil which is a drastic purgative and antimicrobial.",
        "Preparation": "Boil the bark for a stomach remedy | Crush seeds for topical joint application.",
        "Safety Warning": "Seeds are highly toxic if swallowed raw. Internal use of seed oil must be strictly avoided.",
        "Commercial Status": "High",
        "Market Advice": "The seeds are currently highly valued for biofuel/biodiesel production and organic poultry feed."
    },
    {
        "English Name": "African Pepper Bark", "Scientific Name": "Zanthoxylum gilletii", "Swahili": "Mungu", "Kalenjin": "Sagawoita", "Luo": "Rungu", "Kisii": "Omoikomo", "Kikuyu": "Mũcagwe",
        "Traditional Uses": "Cures persistent coughs and tuberculosis | Relieves toothaches | Manages rheumatism",
        "Scientific Backing": "Rich in alkaloids (chelerythrine) and amides that numb pain and kill oral bacteria.",
        "Preparation": "Chew the bark directly for toothaches | Boil bark into a spicy tea for coughs.",
        "Safety Warning": "Creates a strong tingling/numbing sensation in the mouth. Do not give to young children.",
        "Commercial Status": "Moderate",
        "Market Advice": "Excellent potential for processing into organic throat lozenges and dental care products."
    },
    {
        "English Name": "Baobab", "Scientific Name": "Adansonia digitata", "Swahili": "Mbuyu", "Kalenjin": "Mbuyu", "Luo": "Mbuyu", "Kisii": "Mbuyu", "Kikuyu": "Mbuyu",
        "Traditional Uses": "Treats stomach aches and diarrhea | Boosts immunity | Leaves used for fever",
        "Scientific Backing": "Fruit pulp is exceptionally high in Vitamin C, antioxidants, and prebiotic fiber.",
        "Preparation": "Mix fruit powder with water | Boil leaves for malaria/fever tea.",
        "Safety Warning": "Extremely safe. Highly nutritious.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Harvest and process the fruit pulp into superfood powders for export. Extract baobab oil for premium cosmetics."
    },
    {
        "English Name": "Tamarind", "Scientific Name": "Tamarindus indica", "Swahili": "Mkwaju", "Kalenjin": "Mkwaju", "Luo": "Chwaa", "Kisii": "Mkwaju", "Kikuyu": "Mkwaju",
        "Traditional Uses": "Relieves constipation | Lowers fevers | Leaves applied to joint pain",
        "Scientific Backing": "Contains tartaric acid, malic acid, and potassium which act as a gentle, natural laxative.",
        "Preparation": "Soak fruit pulp in warm water and drink | Crush leaves and apply to swollen joints.",
        "Safety Warning": "Safe. The high acidity can irritate stomach ulcers if consumed in massive quantities.",
        "Commercial Status": "High",
        "Market Advice": "Process into juices, sauces, and natural laxative supplements."
    },
    
    # --- COMMON WEEDS & HERBS ---
    {
        "English Name": "Blackjack", "Scientific Name": "Bidens pilosa", "Swahili": "Kichoma Mguu", "Kalenjin": "Kipkoleit", "Luo": "Onyiego", "Kisii": "Enyaboke", "Kikuyu": "Muceege",
        "Traditional Uses": "Treats fresh wounds | Cures stomach ulcers | Manages blood pressure",
        "Scientific Backing": "Rich in flavonoids and polyacetylenes; acts as a natural antibiotic and anti-inflammatory.",
        "Preparation": "Crush fresh leaves into a paste for wounds | Boil leaves for 10 mins for ulcers.",
        "Safety Warning": "Generally safe. Wash thoroughly to remove dust and potential pesticides.",
        "Commercial Status": "Untapped",
        "Market Advice": "Dry and package as a detoxifying herbal tea."
    },
    {
        "English Name": "Stinging Nettle", "Scientific Name": "Urtica dioica", "Swahili": "Thabai", "Kalenjin": "Siwot", "Luo": "Kayo", "Kisii": "Enyabikira", "Kikuyu": "Hatha",
        "Traditional Uses": "Treats arthritis and joint pain | Boosts blood count (anemia) | Manages prostate issues",
        "Scientific Backing": "Contains high levels of iron, Vitamin C, and histamine. Extracts inhibit inflammatory pathways.",
        "Preparation": "Wear gloves to harvest | Boil leaves for 10 minutes to neutralize the sting | Drink the broth.",
        "Safety Warning": "CRITICAL: Do not eat raw, the sting causes severe allergic reactions. Safe once boiled or dried.",
        "Commercial Status": "High Value",
        "Market Advice": "Dry the leaves and grind into a powder. Sells at a premium as a health supplement."
    },
    {
        "English Name": "Lion's Ear", "Scientific Name": "Leonotis leonurus", "Swahili": "Mnyanyasi", "Kalenjin": "Chepkurkuriet", "Luo": "Onyasi", "Kisii": "Omonyanyasi", "Kikuyu": "Mucatha",
        "Traditional Uses": "Relieves asthma and bronchitis | Manages skin rashes | Treats jaundice",
        "Scientific Backing": "Contains leonurine which has mild psychoactive and strong antispasmodic effects.",
        "Preparation": "Smoke dried leaves for asthma (traditional) | Boil leaves for tea | Apply crushed leaves to rashes.",
        "Safety Warning": "Smoking can cause dizziness. Pregnant women should avoid internal use.",
        "Commercial Status": "Untapped",
        "Market Advice": "Can be packaged as a calming herbal tea or processed into natural respiratory syrups."
    },
    {
        "English Name": "African Pennywort", "Scientific Name": "Centella asiatica", "Swahili": "Mnamu", "Kalenjin": "Chepkemkem", "Luo": "Ondong'", "Kisii": "Omokemkem", "Kikuyu": "Mũkengeria",
        "Traditional Uses": "Enhances memory and brain function | Speeds up wound healing | Manages arthritis",
        "Scientific Backing": "Rich in triterpenoid saponins (asiaticoside) proven to boost collagen production.",
        "Preparation": "Eat fresh leaves in salads | Blend into a green juice | Apply crushed leaves to wounds.",
        "Safety Warning": "Very safe. However, ensure it is harvested from clean water sources to avoid liver flukes.",
        "Commercial Status": "High",
        "Market Advice": "Highly sought after globally for nootropic (brain-boosting) supplements and anti-aging skincare serums."
    },
    {
        "English Name": "African Wormwood", "Scientific Name": "Artemisia afra", "Swahili": "Fivi", "Kalenjin": "Kipsinaita", "Luo": "Lel", "Kisii": "Omofivi", "Kikuyu": "Ageria",
        "Traditional Uses": "Treats severe malaria | Clears respiratory infections and asthma | Relieves intestinal worms",
        "Scientific Backing": "Contains artemisinin and volatile oils with proven anti-parasitic and broad-spectrum antimicrobial properties.",
        "Preparation": "Boil leaves and inhale steam for asthma | Steep leaves in hot water for 10 mins for malaria tea.",
        "Safety Warning": "Do not boil directly for tea (steep only) to preserve volatile oils. Toxic to pregnant women.",
        "Commercial Status": "High",
        "Market Advice": "Massive global demand for artemisinin extraction for anti-malarial drugs."
    },
    {
        "English Name": "Sodom Apple", "Scientific Name": "Solanum incanum", "Swahili": "Mtunguja", "Kalenjin": "Sosiot", "Luo": "Ochok", "Kisii": "Omotunguja", "Kikuyu": "Mutongu",
        "Traditional Uses": "Relieves toothaches (using fruit juice) | Treats ringworm | Manages asthma",
        "Scientific Backing": "Contains steroidal glycoalkaloids like solasodine which are precursors for steroid drug synthesis.",
        "Preparation": "Squeeze fruit juice directly onto the aching tooth | Apply sap to ringworm | DO NOT ingest.",
        "Safety Warning": "Highly toxic if swallowed. The yellow fruit can cause severe poisoning and death.",
        "Commercial Status": "Industrial Only",
        "Market Advice": "Cultivate strictly for sale to pharmaceutical companies that extract solasodine."
    },
    {
        "English Name": "Devil's Horsewhip", "Scientific Name": "Achyranthes aspera", "Swahili": "Mshika-nguo", "Kalenjin": "Chepkunyuk", "Luo": "Onyiego", "Kisii": "Enyaboke", "Kikuyu": "Mũrũrũca",
        "Traditional Uses": "Expels kidney stones | Relieves asthma | Stops bleeding from deep cuts",
        "Scientific Backing": "Rich in oleanolic acid and saponins which act as powerful diuretics to flush the kidneys.",
        "Preparation": "Crush leaves and apply to wounds to clot blood | Boil roots for a kidney-flushing tea.",
        "Safety Warning": "Strong diuretic; causes frequent urination. Drink plenty of water to avoid dehydration.",
        "Commercial Status": "Untapped",
        "Market Advice": "Can be commercialized as an organic diuretic tea for kidney and urinary tract health."
    },
    {
        "English Name": "Pigweed", "Scientific Name": "Amaranthus hybridus", "Swahili": "Mchicha", "Kalenjin": "Mchicha", "Luo": "Ododo", "Kisii": "Emboga", "Kikuyu": "Terere",
        "Traditional Uses": "Treats severe anemia | Boosts immunity | Relieves stomach ulcers",
        "Scientific Backing": "Exceptionally high in iron, calcium, and Vitamin C. Very low in oxalates when cooked.",
        "Preparation": "Boil the leaves as a vegetable | Drink the broth to boost blood count.",
        "Safety Warning": "Safe to eat. Do not harvest near roadsides as it absorbs heavy metals from car exhaust.",
        "Commercial Status": "High",
        "Market Advice": "Sell fresh in urban markets as a premium indigenous health vegetable."
    },
    {
        "English Name": "Wandering Jew", "Scientific Name": "Commelina benghalensis", "Swahili": "Mukengeria", "Kalenjin": "Kiplekwet", "Luo": "Odielo", "Kisii": "Omokengeria", "Kikuyu": "Mukengeria",
        "Traditional Uses": "Soothes burns and skin rashes | Treats eye infections | Relieves sore throats",
        "Scientific Backing": "The mucilage (sap) contains potent anti-inflammatory and cooling properties.",
        "Preparation": "Crush leaves and apply the sap directly to burns or rashes | Squeeze sap into eyes for conjunctivitis.",
        "Safety Warning": "Generally safe. Ensure the plant is washed thoroughly if applying to the eyes.",
        "Commercial Status": "Low",
        "Market Advice": "Can be utilized in organic skin-soothing salves and burn ointments."
    },
    {
        "English Name": "Lantana", "Scientific Name": "Lantana camara", "Swahili": "Mshomoro", "Kalenjin": "Chepkiyeny", "Luo": "Nyabend-winy", "Kisii": "Omonya", "Kikuyu": "Mubau",
        "Traditional Uses": "Treats respiratory infections | Heals fresh cuts | Relieves joint pain",
        "Scientific Backing": "Leaves contain lantanine and essential oils with strong antimicrobial and wound-healing effects.",
        "Preparation": "Crush leaves and apply to cuts | Boil leaves and inhale steam for chest congestion.",
        "Safety Warning": "The berries are highly toxic, especially to children, causing liver damage. ONLY use the leaves externally or via steam.",
        "Commercial Status": "Low",
        "Market Advice": "Extract essential oils for use in organic insect repellents and antiseptic creams."
    },
    
    # --- COMMON CROPS & FRUIT TREES (Used Medicinally) ---
    {
        "English Name": "Guava", "Scientific Name": "Psidium guajava", "Swahili": "Mpera", "Kalenjin": "Mpera", "Luo": "Mapera", "Kisii": "Eripera", "Kikuyu": "Mubera",
        "Traditional Uses": "Cures severe diarrhea and amoeba | Relieves toothaches | Manages diabetes",
        "Scientific Backing": "Leaves are incredibly rich in quercetin and tannins, acting as a potent anti-diarrheal and antimicrobial.",
        "Preparation": "Boil 5-7 young leaves in water for 15 mins and drink | Chew fresh young leaves for toothaches.",
        "Safety Warning": "Safe. Drinking too much concentrated leaf tea can cause severe constipation.",
        "Commercial Status": "High",
        "Market Advice": "Dry and package guava leaves as an organic anti-diarrheal and blood-sugar control tea."
    },
    {
        "English Name": "Mango", "Scientific Name": "Mangifera indica", "Swahili": "Mwembe", "Kalenjin": "Mwembe", "Luo": "Maembe", "Kisii": "Omwembe", "Kikuyu": "Mwembe",
        "Traditional Uses": "Lowers blood pressure | Cures malaria | Treats bleeding gums",
        "Scientific Backing": "Leaves contain mangiferin, a potent antioxidant that lowers blood pressure and blood sugar.",
        "Preparation": "Boil young, reddish mango leaves to make a tea | Use the bark as a chewing stick for gums.",
        "Safety Warning": "Safe. The sap from the fruit stem can cause contact dermatitis (skin rash) in sensitive people.",
        "Commercial Status": "High",
        "Market Advice": "Mango leaf tea is gaining massive global popularity for diabetes management."
    },
    {
        "English Name": "Avocado", "Scientific Name": "Persea americana", "Swahili": "Mparachichi", "Kalenjin": "Mparachichi", "Luo": "Avocado", "Kisii": "Omoparadichi", "Kikuyu": "Ikorobia",
        "Traditional Uses": "Dissolves kidney stones | Lowers cholesterol | Manages hypertension",
        "Scientific Backing": "The seed (pit) contains high levels of antioxidants, soluble fiber, and potassium to regulate blood pressure.",
        "Preparation": "Grate the avocado pit, dry it, and boil 1 teaspoon in water to make tea | Boil the leaves for coughs.",
        "Safety Warning": "Avocado leaves and pits contain persin, which is mildly toxic to animals (dogs/horses) but generally safe for humans in small, tea-sized doses.",
        "Commercial Status": "Moderate",
        "Market Advice": "Avocado seed powder is a trending superfood additive."
    },
    {
        "English Name": "Papaya", "Scientific Name": "Carica papaya", "Swahili": "Mpapai", "Kalenjin": "Mpapai", "Luo": "Papai", "Kisii": "Omopapai", "Kikuyu": "Mubabai",
        "Traditional Uses": "Cures Dengue fever and Malaria | Expels intestinal worms | Heals stomach ulcers",
        "Scientific Backing": "Leaves contain carpaine which increases blood platelet count. Seeds contain caricin, a potent anthelmintic (dewormer).",
        "Preparation": "Crush fresh leaves and squeeze the raw juice to cure Dengue | Chew a teaspoon of dried seeds to expel worms.",
        "Safety Warning": "Papaya seeds act as a natural contraceptive in men if taken daily. Pregnant women must strictly avoid unripe papaya and leaf juice as it causes miscarriage.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Papaya leaf extract is the primary pharmaceutical treatment globally for increasing blood platelets during Dengue fever."
    },
    {
        "English Name": "Lemon Grass", "Scientific Name": "Cymbopogon citratus", "Swahili": "Mchaichai", "Kalenjin": "Mchaichai", "Luo": "Mchaichai", "Kisii": "Mchaichai", "Kikuyu": "Mucaicai",
        "Traditional Uses": "Relieves stress and anxiety | Treats common cold and fevers | Repels mosquitoes",
        "Scientific Backing": "Contains citral, a potent anti-inflammatory and calming agent. Also a proven insect repellent.",
        "Preparation": "Boil fresh or dried leaves to make a fragrant tea | Crush leaves and rub on skin to prevent mosquito bites.",
        "Safety Warning": "Very safe. Avoid drinking massive amounts if pregnant.",
        "Commercial Status": "High",
        "Market Advice": "Sell as dried herbal tea, or extract the essential oil for use in natural mosquito repellents and aromatherapy."
    },
    {
        "English Name": "Castor Oil Plant", "Scientific Name": "Ricinus communis", "Swahili": "Mbarika", "Kalenjin": "Maniot", "Luo": "Odagwa", "Kisii": "Omobarika", "Kikuyu": "Mubariki",
        "Traditional Uses": "Relieves severe constipation | Treats arthritis and joint pain | Hair growth stimulant",
        "Scientific Backing": "Contains ricinoleic acid which is a powerful laxative and anti-inflammatory agent.",
        "Preparation": "Apply oil topically to joints | Use 1 teaspoon internally for constipation | Apply oil to scalp.",
        "Safety Warning": "The raw seeds contain Ricin, one of the most toxic substances on earth. ONLY use processed, heat-treated oil.",
        "Commercial Status": "High",
        "Market Advice": "Cultivate purely for commercial oil pressing. The cosmetic and industrial market for castor oil is massive."
    },
    {
        "English Name": "Sweet Potato", "Scientific Name": "Ipomoea batatas", "Swahili": "Kiazi Tamu", "Kalenjin": "Kiazi", "Luo": "Rabuor", "Kisii": "Ekiabeta", "Kikuyu": "Ngwaci",
        "Traditional Uses": "Treats severe dengue fever | Boosts platelet count | Heals burns",
        "Scientific Backing": "Leaves are incredibly rich in Vitamin B, iron, and antioxidants. Proven to raise blood platelets similar to Papaya leaves.",
        "Preparation": "Boil the leaves and drink the broth to recover from severe fevers | Crush leaves to apply to minor burns.",
        "Safety Warning": "Safe and highly nutritious.",
        "Commercial Status": "High",
        "Market Advice": "Sweet potato leaves (Matembele) are a highly profitable, fast-growing indigenous vegetable."
    },
    
    # --- CLASSIC MEDICINALS (Spices, Herbs, Succulents) ---
    {
        "English Name": "Neem Tree", "Scientific Name": "Azadirachta indica", "Swahili": "Mwarobaini", "Kalenjin": "Mwarobaini", "Luo": "Mwarobaini", "Kisii": "Mwarobaini", "Kikuyu": "Mwarobaini",
        "Traditional Uses": "Treating malaria and fevers | Curing skin diseases | Stomach aches",
        "Scientific Backing": "Contains azadirachtin; proven anti-malarial and antibacterial properties.",
        "Preparation": "Boil 5-10 fresh leaves in 2 cups of water for 15 minutes | Drink half a cup twice a day.",
        "Safety Warning": "DO NOT give to children under 12 or pregnant women. Neem oil is toxic if swallowed.",
        "Commercial Status": "High Value",
        "Market Advice": "Extract neem oil for organic agriculture pesticides, or sell dried leaves for herbal teas."
    },
    {
        "English Name": "Aloe Vera", "Scientific Name": "Aloe barbadensis", "Swahili": "Shubiri", "Kalenjin": "Tugumin", "Luo": "Ogaka", "Kisii": "Enyarwanda", "Kikuyu": "Kiluma",
        "Traditional Uses": "Healing burns and skin rashes | Treating severe constipation | Poultry medicine",
        "Scientific Backing": "The gel contains acemannan which accelerates tissue repair. The latex contains aloin, a powerful laxative.",
        "Preparation": "Slice the leaf open and scoop out the clear gel for skin application | Wash away the yellow sap before blending.",
        "Safety Warning": "DO NOT consume the yellow latex just under the skin in large amounts; it causes severe cramping and diarrhea.",
        "Commercial Status": "High Value",
        "Market Advice": "Extract and stabilize the clear gel to sell to cosmetic companies."
    },
    {
        "English Name": "Moringa", "Scientific Name": "Moringa oleifera", "Swahili": "Mlonge", "Kalenjin": "Moringa", "Luo": "Moringa", "Kisii": "Moringa", "Kikuyu": "Moringa",
        "Traditional Uses": "General immunity booster | Increasing breast milk production | Managing diabetes",
        "Scientific Backing": "Exceptionally rich in vitamins, minerals, and antioxidants like quercetin which stabilize blood sugar.",
        "Preparation": "Dry leaves in the shade to preserve vitamins | Grind into a powder and add 1 teaspoon to food.",
        "Safety Warning": "Leaves are highly safe. Avoid eating the root bark, which contains toxic alkaloids.",
        "Commercial Status": "High Value",
        "Market Advice": "Highly commercial. Sell dried leaf powder as a superfood supplement. Press seeds for Ben oil."
    },
    {
        "English Name": "Ginger", "Scientific Name": "Zingiber officinale", "Swahili": "Tangawizi", "Kalenjin": "Tangawizi", "Luo": "Tangawizi", "Kisii": "Tangawizi", "Kikuyu": "Tangawizi",
        "Traditional Uses": "Relieves severe nausea | Cures colds and flu | Treats joint pain (arthritis)",
        "Scientific Backing": "Contains gingerol, a substance with powerful anti-inflammatory and antioxidant properties.",
        "Preparation": "Crush fresh rhizome and boil for 10 minutes to make a potent tea.",
        "Safety Warning": "Safe. Mild blood thinner; be cautious if taking pharmaceutical blood thinners.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Very high local and export demand. Process into dried powder for higher profit margins."
    },
    {
        "English Name": "Garlic", "Scientific Name": "Allium sativum", "Swahili": "Kitunguu Saumu", "Kalenjin": "Kitunguu Saumu", "Luo": "Kitunguu Saumu", "Kisii": "Kitunguu Saumu", "Kikuyu": "Gitunguu Saumu",
        "Traditional Uses": "Lowers blood pressure | Cures bacterial and fungal infections | Clears chest congestion",
        "Scientific Backing": "Contains Allicin, a proven broad-spectrum antibiotic and vasodilator.",
        "Preparation": "Crush 2 cloves, let sit for 10 minutes to activate the Allicin, then swallow raw with water. Do not boil.",
        "Safety Warning": "Can cause heartburn on an empty stomach. Acts as a natural blood thinner.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Always in high demand. Cultivate for the culinary and natural supplement market."
    },
    {
        "English Name": "Turmeric", "Scientific Name": "Curcuma longa", "Swahili": "Manjano", "Kalenjin": "Manjano", "Luo": "Manjano", "Kisii": "Manjano", "Kikuyu": "Manjano",
        "Traditional Uses": "Cures stomach ulcers | Relieves arthritis | Heals internal wounds",
        "Scientific Backing": "Contains Curcumin, one of the most powerful natural anti-inflammatory compounds known to science.",
        "Preparation": "Boil 1 teaspoon of powder in milk or water. MUST be consumed with a pinch of black pepper to absorb into the body.",
        "Safety Warning": "Very safe. Can mildly stain teeth and skin yellow.",
        "Commercial Status": "Extremely High",
        "Market Advice": "The global health market for organic Turmeric is booming. Highly profitable cash crop."
    },
    {
        "English Name": "Rosemary", "Scientific Name": "Rosmarinus officinalis", "Swahili": "Mrozimari", "Kalenjin": "Rosemary", "Luo": "Rosemary", "Kisii": "Rosemary", "Kikuyu": "Rosemary",
        "Traditional Uses": "Improves memory and focus | Stimulates hair growth | Relieves muscle pain",
        "Scientific Backing": "Contains carnosic acid which protects the brain from neurodegeneration. Oil increases scalp blood circulation.",
        "Preparation": "Boil leaves to make a memory-boosting tea | Steep leaves in olive oil for 2 weeks to make hair growth oil.",
        "Safety Warning": "Safe in culinary amounts. Avoid massive doses if pregnant.",
        "Commercial Status": "High",
        "Market Advice": "Extract essential oil for the booming natural hair-care market (alopecia treatments)."
    },
    {
        "English Name": "Peppermint", "Scientific Name": "Mentha piperita", "Swahili": "Mnanaa", "Kalenjin": "Mint", "Luo": "Mint", "Kisii": "Mint", "Kikuyu": "Mint",
        "Traditional Uses": "Relieves irritable bowel syndrome (IBS) | Cures tension headaches | Clears blocked sinuses",
        "Scientific Backing": "Menthol acts as a natural muscle relaxant for the digestive tract and a potent decongestant.",
        "Preparation": "Steep leaves in hot water for 5 minutes for digestion | Rub crushed leaves on the temples for a headache.",
        "Safety Warning": "Safe. Avoid giving strong mint tea to infants as it can cause breathing issues.",
        "Commercial Status": "High",
        "Market Advice": "Sell fresh to supermarkets or extract menthol oil for pharmaceuticals and cosmetics."
    },
    
    # --- AFRICAN SPECIFIC HERBS & TREES ---
    {
        "English Name": "Spider Plant", "Scientific Name": "Cleome gynandra", "Swahili": "Sagaa", "Kalenjin": "Saget", "Luo": "Dek", "Kisii": "Chinsaga", "Kikuyu": "Thageti",
        "Traditional Uses": "Replenishes blood for pregnant/nursing mothers | Boosts eyesight | Cures severe constipation",
        "Scientific Backing": "Exceptionally high in iron, calcium, and Vitamin A. Proven to combat clinical anemia.",
        "Preparation": "Boil the leaves, drain the bitter water, and fry with milk or tomatoes.",
        "Safety Warning": "Extremely safe and healthy. The bitter taste is normal and indicates high phytonutrient content.",
        "Commercial Status": "High",
        "Market Advice": "Sell fresh in urban markets as a premium indigenous health vegetable."
    },
    {
        "English Name": "African Cabbage", "Scientific Name": "Brassica carinata", "Swahili": "Kanzira", "Kalenjin": "Kandhira", "Luo": "Kandhira", "Kisii": "Chinkandhira", "Kikuyu": "Kanyira",
        "Traditional Uses": "Treats stomach ulcers | Boosts immune system | Prevents scurvy",
        "Scientific Backing": "Rich in glucosinolates which have potent anti-cancer and ulcer-healing properties.",
        "Preparation": "Cook lightly as a vegetable. Do not overboil as it destroys the ulcer-healing vitamins.",
        "Safety Warning": "Safe. Individuals with thyroid issues should cook it thoroughly to reduce goitrogens.",
        "Commercial Status": "High",
        "Market Advice": "Highly commercial indigenous vegetable. Easy to grow in dry areas and fetches high market prices."
    },
    {
        "English Name": "Eucalyptus", "Scientific Name": "Eucalyptus globulus", "Swahili": "Mkaratusi", "Kalenjin": "Kiplengwet", "Luo": "Bao", "Kisii": "Omooringi", "Kikuyu": "Mubau",
        "Traditional Uses": "Cures severe chest congestion and bronchitis | Relieves muscle pain | Disinfects wounds",
        "Scientific Backing": "Contains eucalyptol (1,8-cineole), a powerful mucolytic (thins mucus) and antibacterial agent.",
        "Preparation": "Boil leaves and deeply inhale the steam under a towel | Crush leaves and bind over wounds.",
        "Safety Warning": "Highly toxic if swallowed. The essential oil MUST NOT be ingested under any circumstances.",
        "Commercial Status": "High",
        "Market Advice": "Harvest leaves for essential oil distillation used in cough syrups, rubs (like Vicks), and timber."
    },
    {
        "English Name": "Pomegranate", "Scientific Name": "Punica granatum", "Swahili": "Mkomamanga", "Kalenjin": "Mkomamanga", "Luo": "Mkomamanga", "Kisii": "Mkomamanga", "Kikuyu": "Mkomamanga",
        "Traditional Uses": "Cures severe diarrhea and amoeba | Eliminates tapeworms | Boosts heart health",
        "Scientific Backing": "The fruit rind and bark contain pelletierine alkaloids that paralyze intestinal worms.",
        "Preparation": "Boil the dried fruit rind (skin) for 20 minutes to make an anti-parasitic tea.",
        "Safety Warning": "The root bark is highly toxic in large doses. Only use the fruit rind for internal medicine.",
        "Commercial Status": "High",
        "Market Advice": "Cultivate for the high-value fruit market, and dry the rinds for the herbal supplement market."
    },
    {
        "English Name": "African Olive", "Scientific Name": "Olea europaea subsp. cuspidata", "Swahili": "Mtaa", "Kalenjin": "Emityot", "Luo": "Kang'o", "Kisii": "Omolea", "Kikuyu": "Mutamaiyu",
        "Traditional Uses": "Treats high blood pressure | Relieves eye infections | Deworming agent",
        "Scientific Backing": "Contains oleuropein which is a proven vasodilator and powerful antioxidant.",
        "Preparation": "Steep leaves in hot water for 15 mins to make tea | Use leaf extract as eye drops (only if sterilized).",
        "Safety Warning": "Generally safe but can lower blood pressure significantly if taken with pharmaceutical hypertension drugs.",
        "Commercial Status": "Moderate",
        "Market Advice": "Sell dried leaves to herbal tea manufacturers targeting cardiovascular health."
    },
    {
        "English Name": "Cypress", "Scientific Name": "Cupressus lusitanica", "Swahili": "Msindano", "Kalenjin": "Cypress", "Luo": "Cypress", "Kisii": "Msindano", "Kikuyu": "Mwerere",
        "Traditional Uses": "Relieves severe coughs | Shrinks hemorrhoids | Stops minor bleeding",
        "Scientific Backing": "The essential oil acts as a powerful astringent (shrinks tissues) and antispasmodic.",
        "Preparation": "Boil leaves and inhale steam for coughs | Apply cooled tea directly to hemorrhoids.",
        "Safety Warning": "Do not ingest the essential oil. Safe for topical use and steam inhalation.",
        "Commercial Status": "High",
        "Market Advice": "Primarily a timber crop, but the branches can be distilled for high-value aromatherapy oils."
    },
    {
        "English Name": "Cape Gooseberry", "Scientific Name": "Physalis peruviana", "Swahili": "Nathi", "Kalenjin": "Chesare", "Luo": "Nathi", "Kisii": "Chinchabera", "Kikuyu": "Nathi",
        "Traditional Uses": "Boosts immune system | Treats asthma | Clears urinary tract infections",
        "Scientific Backing": "Incredibly rich in Vitamin C, Vitamin A, and withanolides which reduce systemic inflammation.",
        "Preparation": "Eat the ripe yellow fruits raw | Boil the leaves for a mild diuretic tea.",
        "Safety Warning": "The UNRIPE green fruits and the plant leaves are poisonous. Only eat the fully orange/yellow fruit.",
        "Commercial Status": "High",
        "Market Advice": "High-value cash crop for supermarkets, bakeries, and jam manufacturers."
    },
    {
        "English Name": "Mexican Marigold", "Scientific Name": "Tagetes minuta", "Swahili": "Muvumbasi", "Kalenjin": "Chepbisit", "Luo": "Nyanjaga", "Kisii": "Omovumbasi", "Kikuyu": "Mubangi",
        "Traditional Uses": "Kills stomach worms | Repels mosquitoes and ticks | Treats gastritis",
        "Scientific Backing": "Contains thiophenes which are highly toxic to nematodes (worms) and insects.",
        "Preparation": "Boil a small amount of leaves for deworming tea | Crush and rub on skin as an insect repellent.",
        "Safety Warning": "Very strong and potentially toxic to the liver in large doses. Use sparingly.",
        "Commercial Status": "Moderate",
        "Market Advice": "Excellent for extracting organic, bio-degradable agricultural pesticides (nematicides)."
    },
    {
        "English Name": "Passion Fruit", "Scientific Name": "Passiflora edulis", "Swahili": "Matunda ya Pasheni", "Kalenjin": "Pasheni", "Luo": "Pasheni", "Kisii": "Epasheni", "Kikuyu": "Matunda",
        "Traditional Uses": "Cures insomnia | Relieves severe anxiety | Lowers blood pressure",
        "Scientific Backing": "The LEAVES contain harman alkaloids which act as a powerful natural sedative and mild tranquilizer.",
        "Preparation": "Boil 2-3 fresh passion fruit leaves to make a calming tea before bed.",
        "Safety Warning": "Safe. May cause drowsiness; do not drink the leaf tea before driving.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Cultivate for the juice market, and package the dried leaves as organic sleep-aid teas."
    },
    {
        "English Name": "Pumpkin", "Scientific Name": "Cucurbita pepo", "Swahili": "Malenge", "Kalenjin": "Malenge", "Luo": "Budho", "Kisii": "Erimenya", "Kikuyu": "Mungu",
        "Traditional Uses": "Treats enlarged prostate | Expels tapeworms | Boosts male fertility",
        "Scientific Backing": "The SEEDS contain high levels of zinc and cucurbitacin, which paralyze worms and shrink prostate tissue.",
        "Preparation": "Dry and roast the seeds, then eat them daily as a snack | Grind seeds and mix with water to expel worms.",
        "Safety Warning": "Extremely safe and highly nutritious.",
        "Commercial Status": "High",
        "Market Advice": "Do not throw away the seeds! Pumpkin seed oil and roasted seeds are premium health products."
    },
    {
        "English Name": "Hibiscus", "Scientific Name": "Hibiscus sabdariffa", "Swahili": "Rosela", "Kalenjin": "Rosela", "Luo": "Rosela", "Kisii": "Rosela", "Kikuyu": "Rosela",
        "Traditional Uses": "Lowers extreme high blood pressure | Reduces cholesterol | Mild laxative",
        "Scientific Backing": "Rich in anthocyanins and acts as a natural ACE inhibitor (similar to pharmaceutical blood pressure drugs).",
        "Preparation": "Steep the dried red calyces (flowers) in hot or cold water to make a tart, red tea.",
        "Safety Warning": "Can cause a drastic drop in blood pressure. Do not mix with prescription blood pressure medication without consulting a doctor.",
        "Commercial Status": "High",
        "Market Advice": "Package as a premium cardiovascular health tea. Huge export market demand."
    },
    {
        "English Name": "Coriander", "Scientific Name": "Coriandrum sativum", "Swahili": "Dania", "Kalenjin": "Dania", "Luo": "Dania", "Kisii": "Dania", "Kikuyu": "Dania",
        "Traditional Uses": "Removes heavy metals from the body | Cures food poisoning | Relieves bloating",
        "Scientific Backing": "Contains dodecenal, which is proven to be twice as effective as common antibiotics at killing Salmonella.",
        "Preparation": "Blend fresh leaves into a juice for detoxing | Boil seeds to relieve stomach gas.",
        "Safety Warning": "Very safe. Some people have a genetic trait that makes it taste like soap.",
        "Commercial Status": "High",
        "Market Advice": "Essential fast-growing cash crop for urban culinary and detox markets."
    },
    {
        "English Name": "Cinnamon", "Scientific Name": "Cinnamomum verum", "Swahili": "Mdalasini", "Kalenjin": "Mdalasini", "Luo": "Mdalasini", "Kisii": "Mdalasini", "Kikuyu": "Mdalasini",
        "Traditional Uses": "Reverses insulin resistance (Diabetes) | Fights fungal infections | Stops diarrhea",
        "Scientific Backing": "Contains cinnamaldehyde, which dramatically lowers fasting blood sugar and mimics insulin.",
        "Preparation": "Boil the bark sticks to make a sweet tea, or add half a teaspoon of powder to food/drinks daily.",
        "Safety Warning": "Safe. However, cheaper 'Cassia' cinnamon contains coumarin which damages the liver in large doses. True 'Ceylon' cinnamon is safe.",
        "Commercial Status": "Extremely High",
        "Market Advice": "High-value spice crop. Cultivate true Ceylon cinnamon for premium health markets."
    },
    {
        "English Name": "Clove", "Scientific Name": "Syzygium aromaticum", "Swahili": "Karafuu", "Kalenjin": "Karafuu", "Luo": "Karafuu", "Kisii": "Karafuu", "Kikuyu": "Karafuu",
        "Traditional Uses": "Instantly kills toothache pain | Cures stomach ulcers | Fights cholera and food poisoning",
        "Scientific Backing": "Contains Eugenol, a chemical so effective at numbing pain and killing bacteria that it is still used by modern dentists.",
        "Preparation": "Place a whole clove directly against the aching tooth | Boil 3-4 cloves in water for a stomach-healing tea.",
        "Safety Warning": "Clove essential oil is highly concentrated and toxic to the liver if swallowed. Only use the whole dried buds for internal use.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Highly lucrative coastal cash crop. Global demand for dental and culinary applications."
    },
    {
        "English Name": "Jambolan Plum", "Scientific Name": "Syzygium cumini", "Swahili": "Mzambarao", "Kalenjin": "Mzambarao", "Luo": "Mzambarao", "Kisii": "Mzambarao", "Kikuyu": "Mzambarao",
        "Traditional Uses": "Cures severe diabetes | Treats chronic diarrhea | Heals mouth ulcers",
        "Scientific Backing": "The SEEDS contain jamboline, which physically prevents the conversion of starch into sugar in the digestive tract.",
        "Preparation": "Dry the seeds, grind them into a fine powder, and consume 1 teaspoon daily with water.",
        "Safety Warning": "Can cause a severe drop in blood sugar (hypoglycemia) if taken alongside pharmaceutical diabetes drugs.",
        "Commercial Status": "High",
        "Market Advice": "Do not just sell the fruit! The dried seeds are a highly valuable commodity for organic diabetes management."
    },
    {
        "English Name": "Arrowroot", "Scientific Name": "Maranta arundinacea", "Swahili": "Nduma", "Kalenjin": "Nduma", "Luo": "Nduma", "Kisii": "Nduma", "Kikuyu": "Nduma",
        "Traditional Uses": "Cures diarrhea in infants | Soothes stomach acid | Boosts infant weight gain",
        "Scientific Backing": "The starch is exceptionally easy to digest, completely gluten-free, and acts as a soothing demulcent for the gut.",
        "Preparation": "Boil the tuber and eat, or extract the pure white starch powder and mix with milk/water for infants.",
        "Safety Warning": "Extremely safe and highly nutritious for sensitive stomachs.",
        "Commercial Status": "High",
        "Market Advice": "Process into refined arrowroot powder to sell as a premium, gluten-free thickening agent and baby food."
    },
    {
        "English Name": "Waterleaf", "Scientific Name": "Talinum fruticosum", "Swahili": "Mchicha Maji", "Kalenjin": "Mchicha", "Luo": "Mchicha", "Kisii": "Mchicha", "Kikuyu": "Mchicha",
        "Traditional Uses": "Softens tumors | Treats measles | Enhances brain function in children",
        "Scientific Backing": "Rich in Omega-3 fatty acids, Vitamin C, and acts as a mild natural diuretic.",
        "Preparation": "Cook lightly as a vegetable, or crush fresh leaves to apply to external swellings.",
        "Safety Warning": "Contains oxalates; individuals prone to kidney stones should blanch it in hot water before eating.",
        "Commercial Status": "Moderate",
        "Market Advice": "A highly resilient, drought-resistant vegetable ideal for urban kitchen gardens."
    },
    {
        "English Name": "Dandelion", "Scientific Name": "Taraxacum officinale", "Swahili": "Mrehani", "Kalenjin": "Mrehani", "Luo": "Mrehani", "Kisii": "Mrehani", "Kikuyu": "Mrehani",
        "Traditional Uses": "Detoxifies the liver | Cures jaundice | Dissolves gallstones",
        "Scientific Backing": "The roots contain taraxacin, which stimulates bile production and flushes liver toxins.",
        "Preparation": "Boil the roasted roots to make a coffee substitute | Eat the fresh leaves in salads as a strong diuretic.",
        "Safety Warning": "Avoid if you have blocked bile ducts or severe gallstones without consulting a doctor.",
        "Commercial Status": "High",
        "Market Advice": "Considered a weed locally, but the dried roots fetch premium prices as organic liver-detox teas globally."
    },
    {
        "English Name": "Cassava", "Scientific Name": "Manihot esculenta", "Swahili": "Mhogo", "Kalenjin": "Mhogo", "Luo": "Muogo", "Kisii": "Omoogo", "Kikuyu": "Mwanga",
        "Traditional Uses": "Cures ringworm | Treats prostate cancer (traditional belief) | Relieves arthritis",
        "Scientific Backing": "Leaves are rich in Vitamin K and bone-building minerals. Contains Vitamin B17 (amygdalin).",
        "Preparation": "Pound raw leaves and apply to ringworm | Boil leaves extensively before eating to destroy cyanide.",
        "Safety Warning": "Raw cassava roots and leaves contain lethal amounts of cyanide. MUST be thoroughly boiled or fermented before consumption.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Process into cassava flour for gluten-free baking markets. A vital national food security crop."
    },
    {
        "English Name": "Purslane", "Scientific Name": "Portulaca oleracea", "Swahili": "Glisto", "Kalenjin": "Glisto", "Luo": "Glisto", "Kisii": "Glisto", "Kikuyu": "Glisto",
        "Traditional Uses": "Cures scurvy | Treats heart palpitations | Relieves muscle spasms",
        "Scientific Backing": "Contains the highest amount of heart-healthy Omega-3 fatty acids of ANY land plant.",
        "Preparation": "Eat raw in salads or lightly sautéed as a vegetable.",
        "Safety Warning": "Contains oxalic acid. Not recommended in massive doses for people with kidney stone history.",
        "Commercial Status": "Moderate",
        "Market Advice": "Often destroyed as a weed, but holds massive potential as an Omega-3 vegan superfood."
    },
    {
        "English Name": "Thyme", "Scientific Name": "Thymus vulgaris", "Swahili": "Zatari", "Kalenjin": "Zatari", "Luo": "Zatari", "Kisii": "Zatari", "Kikuyu": "Zatari",
        "Traditional Uses": "Cures whooping cough | Treats acne | Kills intestinal hookworms",
        "Scientific Backing": "Contains Thymol, an incredibly powerful biocide that kills bacteria, fungi, and parasites on contact.",
        "Preparation": "Boil into a strong tea for coughs | Steep in alcohol/witch hazel to create an acne-clearing face wash.",
        "Safety Warning": "Safe as an herb. The pure essential oil is toxic if swallowed and burns the skin if undiluted.",
        "Commercial Status": "High",
        "Market Advice": "Extract thymol for use in organic mouthwashes and natural acne medications."
    },
    {
        "English Name": "Toothbrush Tree", "Scientific Name": "Salvadora persica", "Swahili": "Mswaki", "Kalenjin": "Sokot", "Luo": "Athi", "Kisii": "Omosaki", "Kikuyu": "Mswaki",
        "Traditional Uses": "Prevents tooth decay | Cures bleeding gums | Relieves stomach aches",
        "Scientific Backing": "Twigs contain natural fluorides, silica, and antimicrobial sulfur compounds that clean teeth better than standard toothbrushes.",
        "Preparation": "Cut a small twig, peel the bark at the tip, and chew until it forms bristles. Brush teeth daily.",
        "Safety Warning": "Extremely safe. Highly recommended for daily oral hygiene.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Massive potential for commercializing organic chewing sticks (Miswak) for export to the Middle East and health food stores."
    },
    {
        "English Name": "African Blue Basil", "Scientific Name": "Ocimum kilimandscharicum", "Swahili": "Kivumbasi", "Kalenjin": "Mwongya", "Luo": "Bwar", "Kisii": "Omovumbasi", "Kikuyu": "Mukandu",
        "Traditional Uses": "Clears nasal congestion | Repels mosquitoes | Treats measles in children",
        "Scientific Backing": "Leaves contain extremely high levels of camphor and eugenol, acting as a potent decongestant and natural insecticide.",
        "Preparation": "Boil leaves and inhale the vapor for colds | Burn dried leaves to smoke out mosquitoes.",
        "Safety Warning": "Safe for steam inhalation and external use. Do not ingest large amounts of the essential oil.",
        "Commercial Status": "High",
        "Market Advice": "Extract camphor essential oils for making organic chest rubs and natural bug sprays."
    },
    {
        "English Name": "Peanut Butter Cassia", "Scientific Name": "Senna didymobotrya", "Swahili": "Mwena", "Kalenjin": "Senetwet", "Luo": "Ohingla", "Kisii": "Omobeno", "Kikuyu": "Mwena",
        "Traditional Uses": "Treats fungal skin infections | Cures ringworm | Drastic purgative for stomach cleansing",
        "Scientific Backing": "Contains anthraquinones with potent antifungal and purgative (laxative) properties.",
        "Preparation": "Crush leaves and rub the sap directly onto ringworm | Boil roots for a strong stomach cleanse.",
        "Safety Warning": "Highly toxic in large doses. Internal use causes severe diarrhea and cramping. Best used only externally for skin fungi.",
        "Commercial Status": "Low",
        "Market Advice": "Can be harvested to extract organic antifungal agents for veterinary and agricultural use."
    },
    {
        "English Name": "Natal Plum", "Scientific Name": "Carissa spinarum", "Swahili": "Mtanda mboo", "Kalenjin": "Leldet", "Luo": "Ochuoga", "Kisii": "Omochuoga", "Kikuyu": "Mukawa",
        "Traditional Uses": "Treats malaria | Relieves chest pains | Roots used to treat gonorrhea",
        "Scientific Backing": "Root bark contains carissin and powerful cardiac glycosides that fight bacterial infections.",
        "Preparation": "Boil root bark for 15 minutes to make a medicinal decoction | Eat the ripe dark-purple fruits for vitamins.",
        "Safety Warning": "The roots are highly potent and can affect the heart. ONLY the ripe fruit is completely safe to eat.",
        "Commercial Status": "Moderate",
        "Market Advice": "The delicious, nutrient-rich fruits can be commercialized into indigenous jams and juices."
    },
    {
        "English Name": "Red Hot Poker Tree", "Scientific Name": "Erythrina abyssinica", "Swahili": "Muhuti", "Kalenjin": "Kogoiyot", "Luo": "Oremo", "Kisii": "Omorembe", "Kikuyu": "Muhuti",
        "Traditional Uses": "Treats trachoma | Relieves joint pain | Bark used for syphilis",
        "Scientific Backing": "Bark contains erythrinaline alkaloids which have strong antibacterial and anti-inflammatory properties.",
        "Preparation": "Pound bark and apply as a poultice on swollen joints | Boil roots for a medicinal wash.",
        "Safety Warning": "The bright red seeds are highly toxic. Do not ingest seeds under any circumstances.",
        "Commercial Status": "Low",
        "Market Advice": "Primarily valued as a beautiful ornamental landscaping tree that also fixes nitrogen in the soil."
    },
    {
        "English Name": "Cape Fig", "Scientific Name": "Ficus sur", "Swahili": "Mkuyu", "Kalenjin": "Mokoywet", "Luo": "Ng'owo", "Kisii": "Omokuyu", "Kikuyu": "Mukuyu",
        "Traditional Uses": "Boosts breast milk production | Treats sore throats | Heals stomach ulcers",
        "Scientific Backing": "The milky latex contains proteolytic enzymes and antibacterial compounds that heal mucosal linings.",
        "Preparation": "Boil the bark and drink the broth for ulcers | Eat the fresh figs to boost nutrition.",
        "Safety Warning": "Very safe. The figs are highly nutritious but may contain harmless pollinating wasps.",
        "Commercial Status": "Moderate",
        "Market Advice": "A vital agroforestry tree. The fruits can be dried and sold as organic health snacks."
    },
    {
        "English Name": "Quinine Tree", "Scientific Name": "Rauvolfia caffra", "Swahili": "Msesewe", "Kalenjin": "Rerendet", "Luo": "Oseno", "Kisii": "Omosesewe", "Kikuyu": "Mwerere",
        "Traditional Uses": "Cures severe malaria | Acts as a tranquilizer for mental illness | Relieves muscle cramps",
        "Scientific Backing": "Contains reserpine, an alkaloid proven to lower blood pressure and act as a powerful antipsychotic and sedative.",
        "Preparation": "Boil bark to make a very bitter tea for malaria | Administered by traditional healers for severe anxiety.",
        "Safety Warning": "Highly potent. Can cause a dangerous drop in blood pressure and severe drowsiness. Must be dosed carefully.",
        "Commercial Status": "Industrial Only",
        "Market Advice": "Bark is harvested for pharmaceutical extraction of reserpine (used in modern blood pressure medications)."
    },
    {
        "English Name": "African Tulip Tree", "Scientific Name": "Spathodea campanulata", "Swahili": "Kifabakari", "Kalenjin": "Nandi flame", "Luo": "Nandi flame", "Kisii": "Omonandi", "Kikuyu": "Mugirigiri",
        "Traditional Uses": "Treats skin rashes | Relieves severe stomach aches | Flower nectar used for eye infections",
        "Scientific Backing": "Bark and leaves contain iridoid glycosides which have strong antimicrobial and anti-inflammatory effects.",
        "Preparation": "Boil bark for stomach ache decoctions | Crush leaves to apply directly on skin rashes.",
        "Safety Warning": "Generally safe. Do not consume massive quantities of the bark broth.",
        "Commercial Status": "Low",
        "Market Advice": "Highly popular as an ornamental shade tree due to its brilliant red flowers."
    },
    {
        "English Name": "Bitter Leaf", "Scientific Name": "Vernonia amygdalina", "Swahili": "Tughutu", "Kalenjin": "Tughutu", "Luo": "Olusia", "Kisii": "Omoikonge", "Kikuyu": "Mucatha",
        "Traditional Uses": "Treats severe malaria | Lowers high blood sugar (Diabetes) | Cures stomach worms",
        "Scientific Backing": "Contains vernonioside and sesquiterpene lactones which are incredibly potent anti-malarial and anti-diabetic compounds.",
        "Preparation": "Wash the leaves thoroughly to reduce bitterness, then boil to make a tea, or eat them directly as a vegetable.",
        "Safety Warning": "Safe to eat but incredibly bitter. Pregnant women should avoid eating raw bitter leaf in high amounts.",
        "Commercial Status": "High",
        "Market Advice": "Very high demand in urban markets for West/Central African diaspora and local diabetes management."
    },
    {
        "English Name": "Desert Date", "Scientific Name": "Balanites aegyptiaca", "Swahili": "Mjunju", "Kalenjin": "Tuyunwo", "Luo": "Othoo", "Kisii": "Omojunju", "Kikuyu": "Mjunju",
        "Traditional Uses": "Kills bilharzia snails | Treats stomach aches | Oil used for skin diseases",
        "Scientific Backing": "Roots and bark contain powerful saponins that are lethal to the snails carrying schistosomiasis (bilharzia).",
        "Preparation": "Soak crushed roots in ponds to kill bilharzia snails | Press seeds to extract valuable healing oil.",
        "Safety Warning": "Safe. The fruit is edible, but eating too much raw fruit acts as a strong laxative.",
        "Commercial Status": "High",
        "Market Advice": "The seed oil is highly prized in the cosmetic industry, and the tree is vital for dryland afforestation."
    },

    # --- COMMON VEGETABLES & HERBS ---
    {
        "English Name": "Bitter Melon", "Scientific Name": "Momordica charantia", "Swahili": "Karela", "Kalenjin": "Karela", "Luo": "Nyanya-ruoth", "Kisii": "Karela", "Kikuyu": "Karela",
        "Traditional Uses": "Reverses type 2 diabetes | Clears skin infections | Expels stomach worms",
        "Scientific Backing": "Contains charantin and polypeptide-p, which physically mimic insulin and lower blood sugar.",
        "Preparation": "Blend the raw fruit to make a bitter green juice, or cook the fruit and leaves into a stew.",
        "Safety Warning": "Can cause a dangerous drop in blood sugar if combined with pharmaceutical diabetes drugs. Avoid if pregnant.",
        "Commercial Status": "High",
        "Market Advice": "Highly profitable cash crop. Package dried bitter melon as an organic diabetes tea."
    },
    {
        "English Name": "Spiny Amaranth", "Scientific Name": "Amaranthus spinosus", "Swahili": "Mchicha Miiba", "Kalenjin": "Keluet", "Luo": "Ododo", "Kisii": "Emboga", "Kikuyu": "Terere",
        "Traditional Uses": "Treats severe anemia | Relieves painful menstruation | Acts as a natural diuretic",
        "Scientific Backing": "Incredibly high in iron, folic acid, and calcium. Promotes rapid red blood cell production.",
        "Preparation": "Boil the young, thornless leaves and eat as a vegetable. Drink the broth for anemia.",
        "Safety Warning": "The plant has sharp spines. Contains oxalates; boil thoroughly and discard the first water if prone to kidney stones.",
        "Commercial Status": "Moderate",
        "Market Advice": "A highly resilient indigenous vegetable that grows well in poor soils."
    },
    {
        "English Name": "Velvet Leaf", "Scientific Name": "Cissampelos pareira", "Swahili": "Kishiki cha buga", "Kalenjin": "Kinyalil", "Luo": "Owang'", "Kisii": "Omowang'", "Kikuyu": "Mukururuka",
        "Traditional Uses": "Cures severe stomach cramps | Prevents miscarriages | Relieves malaria fever",
        "Scientific Backing": "Contains highly active bisbenzylisoquinoline alkaloids which are powerful muscle relaxants and antispasmodics.",
        "Preparation": "Boil the roots and leaves to make a bitter tea | Drink half a cup to stop stomach cramping instantly.",
        "Safety Warning": "Very potent muscle relaxant. Do not overdose. Must be administered carefully if pregnant.",
        "Commercial Status": "Untapped",
        "Market Advice": "High potential for processing into natural, organic anti-cramping and anti-diarrheal supplements."
    },
    {
        "English Name": "Wild Asparagus", "Scientific Name": "Asparagus racemosus", "Swahili": "Mwinamila", "Kalenjin": "Mwinamila", "Luo": "Mwinamila", "Kisii": "Mwinamila", "Kikuyu": "Mwinamila",
        "Traditional Uses": "Boosts female fertility | Increases breast milk production | Relieves stomach ulcers",
        "Scientific Backing": "Contains steroidal saponins (shatavarins) that act as a powerful female hormone regulator (phytoestrogen).",
        "Preparation": "Boil the fleshy tubers (roots) in milk or water to make a soothing, sweet tonic.",
        "Safety Warning": "Safe and highly nutritious. Acts as a mild diuretic.",
        "Commercial Status": "High",
        "Market Advice": "Globally marketed under the name 'Shatavari' as a premium female reproductive health supplement."
    },
    {
        "English Name": "Finger Euphorbia", "Scientific Name": "Euphorbia tirucalli", "Swahili": "Kanya", "Kalenjin": "Okondek", "Luo": "Ojuok", "Kisii": "Omokanya", "Kikuyu": "Kariaria",
        "Traditional Uses": "Treats severe bone fractures | Removes warts and corns | Acts as a natural fence",
        "Scientific Backing": "The white latex contains highly caustic diterpenes that physically burn off skin growths.",
        "Preparation": "Apply a tiny drop of the white sap directly onto a wart. Avoid healthy skin. Used externally to set broken bones.",
        "Safety Warning": "EXTREMELY TOXIC TO EYES. The sap can cause permanent blindness. Never ingest.",
        "Commercial Status": "Low",
        "Market Advice": "Primarily used as a live fence that protects crops from livestock due to its toxicity."
    },
    
    # --- FRUITS & CULINARY MEDICINES ---
    {
        "English Name": "Lemon", "Scientific Name": "Citrus limon", "Swahili": "Mlimau", "Kalenjin": "Mlimau", "Luo": "Mlimau", "Kisii": "Omolimau", "Kikuyu": "Mũrimau",
        "Traditional Uses": "Cures severe colds and flu | Aids digestion | Flushes kidney stones",
        "Scientific Backing": "High in Vitamin C, citric acid, and d-limonene, which boost immunity and dissolve calcium kidney stones.",
        "Preparation": "Squeeze fresh juice into warm water with honey | Boil the leaves and rind for a potent flu tea.",
        "Safety Warning": "Pure juice can erode tooth enamel. Always dilute with water.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Process into immune-boosting syrups, or extract the peel oil for cleaning products and cosmetics."
    },
    {
        "English Name": "Sweet Orange", "Scientific Name": "Citrus sinensis", "Swahili": "Mchungwa", "Kalenjin": "Mchungwa", "Luo": "Mchungwa", "Kisii": "Omochungwa", "Kikuyu": "Mũcungwa",
        "Traditional Uses": "Reduces high blood pressure | Boosts skin health | Relieves constipation",
        "Scientific Backing": "Rich in hesperidin and Vitamin C which strengthen blood vessels and improve heart health.",
        "Preparation": "Eat the fruit for fiber | Boil the dried peels to make a tea that stimulates digestion.",
        "Safety Warning": "Safe and highly nutritious.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Orange peel powder is a highly requested ingredient in organic skincare routines and teas."
    },
    {
        "English Name": "Onion", "Scientific Name": "Allium cepa", "Swahili": "Kitunguu", "Kalenjin": "Kitunguu", "Luo": "Kitunguu", "Kisii": "Egetunguu", "Kikuyu": "Gĩtunguu",
        "Traditional Uses": "Treats persistent coughs | Clears ear infections | Relieves asthma",
        "Scientific Backing": "Contains high levels of quercetin and sulfur compounds that thin mucus and reduce airway inflammation.",
        "Preparation": "Boil raw onion with honey for cough syrup | Drop 1 drop of warm onion juice into infected ears.",
        "Safety Warning": "Safe. Raw onion can cause heartburn in people with acid reflux.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Essential food crop. Extract onion oil for organic hair growth serums (currently trending globally)."
    },
    {
        "English Name": "Citronella", "Scientific Name": "Cymbopogon nardus", "Swahili": "Mchaichai (Feki)", "Kalenjin": "Mchaichai", "Luo": "Mchaichai", "Kisii": "Mchaichai", "Kikuyu": "Mucaicai",
        "Traditional Uses": "Repels mosquitoes and insects | Relieves muscle spasms | Cleans wounds",
        "Scientific Backing": "Contains citronellal and geraniol, which are universally recognized, highly effective natural insect repellents.",
        "Preparation": "Crush leaves and rub on exposed skin | Plant around the house to ward off mosquitoes | Do not drink (too harsh).",
        "Safety Warning": "Not for internal use. External application of pure essential oil may irritate sensitive skin.",
        "Commercial Status": "High",
        "Market Advice": "Massive global market for distilling Citronella essential oil for organic bug sprays and candles."
    },
    {
        "English Name": "Wild Olive", "Scientific Name": "Olea africana", "Swahili": "Mutamaiyu", "Kalenjin": "Emityot", "Luo": "Kang'o", "Kisii": "Omolea", "Kikuyu": "Mutamaiyu",
        "Traditional Uses": "Treats hypertension | Fights bacterial infections | Bark used for tapeworms",
        "Scientific Backing": "Contains oleuropein and hydroxytyrosol, highly potent antioxidants that lower blood pressure.",
        "Preparation": "Boil a small handful of leaves to make a bitter olive-leaf tea.",
        "Safety Warning": "Safe. Can cause hypotension (low blood pressure) if mixed with medical blood pressure drugs.",
        "Commercial Status": "Moderate",
        "Market Advice": "Sell the dried leaves to wellness brands for use in cardiovascular health supplements."
    },
    
    # --- RARE AND SPECIALIZED PLANTS ---
    {
        "English Name": "Cape Mahogany", "Scientific Name": "Trichilia emetica", "Swahili": "Mti maji", "Kalenjin": "Koruet", "Luo": "Okwe", "Kisii": "Omokwe", "Kikuyu": "Mururi",
        "Traditional Uses": "Heals severe skin burns | Treats eczema | Root decoction for stomach ache",
        "Scientific Backing": "The seed oil (Mafura butter) is rich in essential fatty acids (palmitic, stearic) and limonoids, deeply nourishing the skin.",
        "Preparation": "Boil the seeds to extract Mafura butter and apply directly to skin | Boil roots for a stomach wash.",
        "Safety Warning": "The seed coat can be toxic if ingested raw. The oil is strictly for external use.",
        "Commercial Status": "High",
        "Market Advice": "Mafura butter is a highly sought-after premium ingredient in the global organic cosmetics market."
    },
    {
        "English Name": "Waterberry", "Scientific Name": "Syzygium guineense", "Swahili": "Mzambarau mwitu", "Kalenjin": "Lamaiywet", "Luo": "Lemba", "Kisii": "Omolomba", "Kikuyu": "Mukowe",
        "Traditional Uses": "Cures severe diarrhea | Treats dysentery | Bark used for wound healing",
        "Scientific Backing": "Bark and leaves are extremely rich in tannins, which act as powerful astringents to stop bleeding and diarrhea.",
        "Preparation": "Boil the bark for 20 minutes to make a dark red, astringent tea | Apply crushed leaves to cuts.",
        "Safety Warning": "Safe. The fruits are edible and delicious. Avoid massive doses of bark tea to prevent severe constipation.",
        "Commercial Status": "Moderate",
        "Market Advice": "A highly resilient agroforestry tree. The fruits can be sold fresh in local markets."
    },
    {
        "English Name": "Elgon Teak", "Scientific Name": "Olea welwitschii", "Swahili": "Mutamaiyu", "Kalenjin": "Loliondo", "Luo": "Lolut", "Kisii": "Omotamaiyu", "Kikuyu": "Mutamaiyu",
        "Traditional Uses": "Treats malaria | Relieves joint pain | General painkiller",
        "Scientific Backing": "Contains seciridoid glycosides which have strong antimalarial and analgesic properties.",
        "Preparation": "Boil leaves and bark for 15 minutes to create a potent antimalarial tea.",
        "Safety Warning": "Do not consume during pregnancy. Use standard dosages to avoid liver strain.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Primarily valued for its highly durable, termite-resistant timber. Plant heavily for agroforestry wealth."
    },
    {
        "English Name": "African Pokeweed", "Scientific Name": "Phytolacca dodecandra", "Swahili": "Icheje", "Kalenjin": "Icheje", "Luo": "Icheje", "Kisii": "Icheje", "Kikuyu": "Icheje",
        "Traditional Uses": "Kills bilharzia snails | Used as natural soap | Drastic purgative",
        "Scientific Backing": "Berries contain incredibly high concentrations of saponins that foam like soap and are highly toxic to aquatic snails.",
        "Preparation": "Crush berries and throw into ponds to kill snails | Use crushed berries to wash clothes.",
        "Safety Warning": "HIGHLY TOXIC if swallowed raw. The berries cause severe poisoning in humans and livestock. External/agricultural use only.",
        "Commercial Status": "Low",
        "Market Advice": "Can be utilized by governments or NGOs for natural, eco-friendly bilharzia control in lakes."
    },
    {
        "English Name": "Mexican Sunflower", "Scientific Name": "Tithonia diversifolia", "Swahili": "Maua", "Kalenjin": "Maua", "Luo": "Maua", "Kisii": "Maua", "Kikuyu": "Maua",
        "Traditional Uses": "Treats liver diseases | Acts as a powerful organic fertilizer | Treats bruises",
        "Scientific Backing": "Contains tagitinin and other sesquiterpene lactones which reduce inflammation. Highly rich in nitrogen and phosphorus.",
        "Preparation": "Crush leaves to apply to bruises | Chop the plant and bury it in the soil as green manure.",
        "Safety Warning": "Do not ingest in large quantities. Mainly valued as an agricultural aid rather than internal medicine.",
        "Commercial Status": "Moderate",
        "Market Advice": "Essential for organic farmers. Use it to make highly potent liquid green manure for zero-cost fertilizer."
    },
    
    # --- MORE COMMON CROPS ---
    {
        "English Name": "Java Plum", "Scientific Name": "Ziziphus mauritiana", "Swahili": "Mkunazi", "Kalenjin": "Ngoiywet", "Luo": "Ngo", "Kisii": "Omongo", "Kikuyu": "Mukunazi",
        "Traditional Uses": "Relieves severe stomach ulcers | Treats diarrhea | Boosts immune system",
        "Scientific Backing": "Fruit is rich in Vitamin C. Bark contains mucilage and tannins that soothe and heal the stomach lining.",
        "Preparation": "Boil the root bark for a stomach-healing decoction | Eat the fruit raw.",
        "Safety Warning": "Very safe. Highly nutritious fruit for dry, arid regions.",
        "Commercial Status": "Moderate",
        "Market Advice": "Thrives in dry, ASAL regions. Process the fruits into organic jams and dried snacks."
    },
    {
        "English Name": "Wild Celery", "Scientific Name": "Apium graveolens", "Swahili": "Seleri", "Kalenjin": "Seleri", "Luo": "Seleri", "Kisii": "Seleri", "Kikuyu": "Seleri",
        "Traditional Uses": "Lowers high blood pressure | Relieves gout and joint pain | Acts as a natural diuretic",
        "Scientific Backing": "Contains 3-n-butylphthalide (3nB) which relaxes the smooth muscles in blood vessels, lowering pressure.",
        "Preparation": "Eat raw in salads, blend into a green juice, or boil seeds for a diuretic tea.",
        "Safety Warning": "Safe. Mild diuretic, so drink plenty of water. Can cause mild allergic skin reactions in sunlight for some people.",
        "Commercial Status": "High",
        "Market Advice": "High-demand urban crop. Grow organically for juice bars and health enthusiasts."
    },
    {
        "English Name": "Ginseng", "Scientific Name": "Panax ginseng", "Swahili": "Ginseng", "Kalenjin": "Ginseng", "Luo": "Ginseng", "Kisii": "Ginseng", "Kikuyu": "Ginseng",
        "Traditional Uses": "Boosts physical energy and stamina | Enhances immunity | Lowers blood sugar",
        "Scientific Backing": "Contains ginsenosides, which act as powerful adaptogens, helping the body resist physical and chemical stress.",
        "Preparation": "Slice the root and steep in hot water for a potent energy tea, or chew a small slice of raw root.",
        "Safety Warning": "Can cause insomnia and jitteriness if taken in high doses. Do not mix with pharmaceutical blood thinners.",
        "Commercial Status": "Extremely High",
        "Market Advice": "A highly lucrative export crop if you have the right climate. Sells at premium prices in international health markets."
    },
    {
        "English Name": "Fennel", "Scientific Name": "Foeniculum vulgare", "Swahili": "Shamari", "Kalenjin": "Shamari", "Luo": "Shamari", "Kisii": "Shamari", "Kikuyu": "Shamari",
        "Traditional Uses": "Relieves baby colic and gas | Aids digestion | Increases breast milk production",
        "Scientific Backing": "Contains anethole, a phytoestrogen that reduces intestinal spasms and mimics estrogen to boost milk supply.",
        "Preparation": "Chew half a teaspoon of seeds after meals | Boil seeds in water for a soothing stomach tea.",
        "Safety Warning": "Very safe. A popular, gentle remedy for infants with colic.",
        "Commercial Status": "High",
        "Market Advice": "Process into gripe water alternatives or sell dried seeds as an organic digestive spice."
    },
    {
        "English Name": "Basil", "Scientific Name": "Ocimum basilicum", "Swahili": "Mrehani", "Kalenjin": "Mrehani", "Luo": "Mrehani", "Kisii": "Mrehani", "Kikuyu": "Mrehani",
        "Traditional Uses": "Relieves anxiety and stress | Cures tension headaches | Aids digestion",
        "Scientific Backing": "Contains eugenol, linalool, and citronellol which lower cortisol levels and reduce inflammation.",
        "Preparation": "Blend fresh leaves into pesto, or steep dried leaves for a calming tea.",
        "Safety Warning": "Extremely safe culinary herb. Essential oil should not be ingested.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Essential fast-growing herb for restaurants, supermarkets, and essential oil extraction."
    },
    {
        "English Name": "Catnip", "Scientific Name": "Nepeta cataria", "Swahili": "Catnip", "Kalenjin": "Catnip", "Luo": "Catnip", "Kisii": "Catnip", "Kikuyu": "Catnip",
        "Traditional Uses": "Cures insomnia | Relieves severe stomach cramps | Induces sweating to break fevers",
        "Scientific Backing": "Contains nepetalactone, which acts as a mild sedative in humans (and a strong stimulant in cats).",
        "Preparation": "Steep dried leaves in hot water for 10 minutes to make a potent sleep-inducing tea.",
        "Safety Warning": "Safe. Will make you very drowsy. Do not operate machinery after drinking a strong brew.",
        "Commercial Status": "Moderate",
        "Market Advice": "Can be packaged as a premium organic sleep-aid tea, or sold as a recreational product for pet cats."
    },
    {
        "English Name": "Borage", "Scientific Name": "Borago officinalis", "Swahili": "Borage", "Kalenjin": "Borage", "Luo": "Borage", "Kisii": "Borage", "Kikuyu": "Borage",
        "Traditional Uses": "Relieves Rheumatoid arthritis | Treats eczema and skin inflammation | Lifts mood",
        "Scientific Backing": "The seeds contain the highest known plant source of gamma-linolenic acid (GLA), a crucial anti-inflammatory fat.",
        "Preparation": "Eat fresh leaves in salads | Extract oil from the seeds for internal or topical use.",
        "Safety Warning": "The leaves contain trace pyrrolizidine alkaloids which can harm the liver in massive doses. Seed oil is safe.",
        "Commercial Status": "High",
        "Market Advice": "Borage seed oil is an incredibly valuable cosmetic and supplement ingredient globally."
    },
    {
        "English Name": "Cumin", "Scientific Name": "Cuminum cyminum", "Swahili": "Bizari", "Kalenjin": "Bizari", "Luo": "Bizari", "Kisii": "Bizari", "Kikuyu": "Bizari",
        "Traditional Uses": "Treats food poisoning | Aids severe digestion issues | Promotes weight loss",
        "Scientific Backing": "Rich in thymol and other essential oils that stimulate salivary glands and kill food-borne bacteria.",
        "Preparation": "Boil 1 teaspoon of seeds in water to make a stomach-soothing tea | Use extensively in cooking.",
        "Safety Warning": "Extremely safe culinary spice. May mildly lower blood sugar.",
        "Commercial Status": "High",
        "Market Advice": "A staple spice in local markets. Easy to grow and dry for long-term storage."
    },
    {
        "English Name": "Oregano", "Scientific Name": "Origanum vulgare", "Swahili": "Oregano", "Kalenjin": "Oregano", "Luo": "Oregano", "Kisii": "Oregano", "Kikuyu": "Oregano",
        "Traditional Uses": "Cures respiratory infections | Kills candida and fungal infections | Preserves food",
        "Scientific Backing": "Contains massive amounts of carvacrol, which is proven to be as effective as some pharmaceutical antibiotics.",
        "Preparation": "Boil fresh leaves for a potent antibacterial tea | Extract the essential oil for skin infections.",
        "Safety Warning": "Oregano essential oil is incredibly strong and will burn the skin if not diluted in olive/coconut oil.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Oil of Oregano is a highly profitable global commodity used as a natural, broad-spectrum antibiotic."
    },
    {
        "English Name": "Anise", "Scientific Name": "Pimpinella anisum", "Swahili": "Anise", "Kalenjin": "Anise", "Luo": "Anise", "Kisii": "Anise", "Kikuyu": "Anise",
        "Traditional Uses": "Treats severe menstrual cramps | Relieves asthma and coughs | Acts as a mild laxative",
        "Scientific Backing": "Contains anethole, a phytoestrogen that relieves muscle spasms and thins respiratory mucus.",
        "Preparation": "Chew the seeds directly | Boil crushed seeds for 10 minutes to make a sweet, licorice-flavored tea.",
        "Safety Warning": "Safe. In extreme, concentrated doses (anise oil), it can be toxic. Stick to using the seeds.",
        "Commercial Status": "Moderate",
        "Market Advice": "Valued for flavoring in bakeries, confectioneries, and organic health teas."
    },
    {
        "English Name": "Cardamom", "Scientific Name": "Elettaria cardamomum", "Swahili": "Iliki", "Kalenjin": "Iliki", "Luo": "Iliki", "Kisii": "Iliki", "Kikuyu": "Iliki",
        "Traditional Uses": "Cures bad breath and gum disease | Lowers blood pressure | Heals stomach ulcers",
        "Scientific Backing": "Contains potent antimicrobial compounds that eliminate oral bacteria and protect the stomach lining.",
        "Preparation": "Chew the pods whole after a meal | Crush the inner seeds and boil in tea/coffee.",
        "Safety Warning": "Extremely safe culinary spice.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Known as the 'Queen of Spices', cardamom is one of the most expensive and profitable spices to cultivate."
    },
    
    # --- RURAL EDIBLE AND MEDICINAL WEEDS ---
    {
        "English Name": "Gallant Soldier", "Scientific Name": "Galinsoga parviflora", "Swahili": "Msekeseke", "Kalenjin": "Msekeseke", "Luo": "Msekeseke", "Kisii": "Msekeseke", "Kikuyu": "Kang'ei",
        "Traditional Uses": "Coagulates blood (stops bleeding) | Treats nettle stings | High-nutrition survival food",
        "Scientific Backing": "Rich in flavonoids and Vitamin C. Its sap acts as a natural astringent and anti-inflammatory.",
        "Preparation": "Crush leaves and rub onto stinging nettle burns | Apply to fresh cuts | Boil young leaves as spinach.",
        "Safety Warning": "Safe. Often dismissed as a weed but is a highly nutritious wild vegetable.",
        "Commercial Status": "Low",
        "Market Advice": "Encourage cultivation as a zero-cost, high-nutrition indigenous vegetable for food security."
    },
    {
        "English Name": "Black Nightshade", "Scientific Name": "Solanum nigrum", "Swahili": "Mnavu", "Kalenjin": "Isoiyot", "Luo": "Osuga", "Kisii": "Rinagu", "Kikuyu": "Managu",
        "Traditional Uses": "Boosts blood count | Treats stomach ulcers | Relieves persistent fevers",
        "Scientific Backing": "Contains exceptionally high levels of iron, riboflavin, and Vitamin C. Mild alkaloid content acts as an analgesic.",
        "Preparation": "Boil leaves thoroughly in water or milk to remove bitterness and eat as a premium vegetable.",
        "Safety Warning": "The UNRIPE green berries are toxic. Only eat the fully ripe black/purple berries or the properly cooked leaves.",
        "Commercial Status": "High",
        "Market Advice": "One of the most popular and commercially viable indigenous vegetables in Kenya today. Massive urban demand."
    },
    {
        "English Name": "Cowpea", "Scientific Name": "Vigna unguiculata", "Swahili": "Kunde", "Kalenjin": "Kunde", "Luo": "Boo", "Kisii": "Egesare", "Kikuyu": "Kunde",
        "Traditional Uses": "Treats severe malnutrition and anemia | Promotes bowel movement | Relieves heart issues",
        "Scientific Backing": "Leaves are incredibly high in iron and folic acid. The beans contain high soluble fiber to lower cholesterol.",
        "Preparation": "Lightly boil the leaves and eat as a vegetable | Cook the beans thoroughly.",
        "Safety Warning": "Very safe. Eating raw or undercooked beans can cause severe gas and bloating.",
        "Commercial Status": "Extremely High",
        "Market Advice": "A highly profitable, drought-resistant dual-crop (you can sell both the leaves and the beans)."
    },
    {
        "English Name": "Slender Amaranth", "Scientific Name": "Amaranthus viridis", "Swahili": "Mchicha", "Kalenjin": "Mchicha", "Luo": "Ododo", "Kisii": "Emboga", "Kikuyu": "Terere",
        "Traditional Uses": "Treats acute anemia | Boosts immunity | Aids recovery from severe illness",
        "Scientific Backing": "Contains high levels of essential amino acids, calcium, iron, and vitamins. Acts as a rapid nutritional booster.",
        "Preparation": "Boil the leaves as a vegetable. The water used to boil it is drunk as a blood-boosting tonic.",
        "Safety Warning": "Safe. Avoid harvesting near heavily polluted areas or major highways as it absorbs heavy metals.",
        "Commercial Status": "High",
        "Market Advice": "Sell fresh in urban markets. Easy to grow in almost any soil condition."
    },
    {
        "English Name": "Jute Mallow", "Scientific Name": "Corchorus olitorius", "Swahili": "Mrenda", "Kalenjin": "Mrenda", "Luo": "Apoth", "Kisii": "Mrenda", "Kikuyu": "Mrenda",
        "Traditional Uses": "Relieves severe constipation | Heals stomach ulcers | Strengthens bones",
        "Scientific Backing": "The mucilage (slime) coats and protects the stomach lining. Exceptionally rich in calcium and Vitamin E.",
        "Preparation": "Chop finely and boil with a pinch of baking soda (magadi) to create a highly nutritious, slippery stew.",
        "Safety Warning": "Very safe and highly recommended for pregnant women and people with sensitive stomachs.",
        "Commercial Status": "High",
        "Market Advice": "Massive demand in urban and rural markets alike. Very fast growing cash-crop."
    },
    {
        "English Name": "Sisal", "Scientific Name": "Agave sisalana", "Swahili": "Mkonge", "Kalenjin": "Mkonge", "Luo": "Mkonge", "Kisii": "Mkonge", "Kikuyu": "Mkonge",
        "Traditional Uses": "Treats severe skin fungal infections | Acts as a drastic laxative | Cleans wounds",
        "Scientific Backing": "The sap contains powerful steroidal saponins that are highly antifungal and antibacterial.",
        "Preparation": "Apply the sap carefully to fungal infections | Roast the heart of the plant to eat in times of extreme famine.",
        "Safety Warning": "The sap is highly irritating to healthy skin and eyes. Avoid internal use as it is a harsh purgative.",
        "Commercial Status": "Industrial Only",
        "Market Advice": "Primarily grown commercially for highly durable natural fibers used in ropes, mats, and dartboards."
    },
    {
        "English Name": "Napier Grass", "Scientific Name": "Pennisetum purpureum", "Swahili": "Nyasi ya Ndovu", "Kalenjin": "Nyasi", "Luo": "Nyasi", "Kisii": "Nyasi", "Kikuyu": "Nyasi",
        "Traditional Uses": "Controls soil erosion | Used in traditional rituals for pest control | Animal fodder",
        "Scientific Backing": "Acts as a 'push-pull' trap crop. It naturally attracts stem-borer moths away from maize and kills their larvae.",
        "Preparation": "Plant as a border around maize fields to protect crops from pests.",
        "Safety Warning": "The leaf edges are very sharp and can cause paper-cuts to the skin. Safe for livestock.",
        "Commercial Status": "High",
        "Market Advice": "Essential agricultural crop. Grow to sell as premium livestock fodder (zero-grazing dairy farming)."
    },
    {
        "English Name": "Luffa", "Scientific Name": "Luffa aegyptiaca", "Swahili": "Dodoki", "Kalenjin": "Dodoki", "Luo": "Dodoki", "Kisii": "Dodoki", "Kikuyu": "Dodoki",
        "Traditional Uses": "Treats jaundice | Acts as a natural body scrub for skin conditions | Edible vegetable",
        "Scientific Backing": "The young fruit is highly nutritious. The mature dried fruit fiber aggressively exfoliates dead skin cells, promoting healing.",
        "Preparation": "Cook young fruits like zucchini | Allow mature fruits to dry completely on the vine, peel, and use as a bath sponge.",
        "Safety Warning": "Safe. Ensure the dried sponges are kept clean to prevent bacterial growth in the bathroom.",
        "Commercial Status": "Moderate",
        "Market Advice": "Cultivate the mature vines to harvest and sell organic, eco-friendly bath sponges (loofahs)."
    },
    {
        "English Name": "Macadamia", "Scientific Name": "Macadamia integrifolia", "Swahili": "Makadamia", "Kalenjin": "Makadamia", "Luo": "Makadamia", "Kisii": "Makadamia", "Kikuyu": "Makadamia",
        "Traditional Uses": "Lowers extreme cholesterol | Promotes heart health | Oil used for dry skin",
        "Scientific Backing": "Nuts are incredibly rich in monounsaturated fats (oleic acid) and palmitoleic acid, which repair the skin and lower bad LDL cholesterol.",
        "Preparation": "Crack the hard shell and eat the raw/roasted nuts | Press the nuts to extract premium cosmetic oil.",
        "Safety Warning": "Extremely toxic to dogs (causes paralysis). Completely safe and highly nutritious for humans.",
        "Commercial Status": "Extremely High",
        "Market Advice": "One of the most expensive and profitable nuts in the world. Extract the oil for the premium cosmetic market."
    },
    {
        "English Name": "Pyrethrum", "Scientific Name": "Chrysanthemum cinerariifolium", "Swahili": "Pireto", "Kalenjin": "Pireto", "Luo": "Pireto", "Kisii": "Pireto", "Kikuyu": "Pireto",
        "Traditional Uses": "Kills mosquitoes | Treats head lice | Organic crop pesticide",
        "Scientific Backing": "The flowers contain pyrethrins, one of the most powerful, naturally occurring, biodegradable neurotoxins for insects.",
        "Preparation": "Dry the white flowers, grind into a powder, and mix with water to spray on crops, or burn to kill mosquitoes.",
        "Safety Warning": "Highly toxic to insects and fish. Very low toxicity to humans and mammals. Wear a mask when grinding the powder.",
        "Commercial Status": "Extremely High",
        "Market Advice": "Kenya is one of the world's top producers. Cultivate strictly to sell to natural pesticide manufacturers."
    },
    {
        "English Name": "Taro", "Scientific Name": "Colocasia esculenta", "Swahili": "Nduma", "Kalenjin": "Nduma", "Luo": "Nduma", "Kisii": "Nduma", "Kikuyu": "Nduma",
        "Traditional Uses": "Cures severe stomach acidity | Manages diabetes | Provides sustained energy",
        "Scientific Backing": "The corm (tuber) is rich in complex carbohydrates and dietary fiber that stabilize blood sugar.",
        "Preparation": "Boil or roast the tuber thoroughly before eating. Leaves can be cooked extensively as a vegetable.",
        "Safety Warning": "Raw Taro contains calcium oxalate crystals which act like microscopic glass shards in the throat. MUST be cooked thoroughly.",
        "Commercial Status": "High",
        "Market Advice": "A staple, high-value food security crop. Highly sought after for healthy breakfasts in urban areas."
    }
]
def inject_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    count = 0
    print("⏳ Injecting massive Mitishamba payload directly into database...")
    
    for row in plants_data:
        trad_list = [item.strip() for item in row['Traditional Uses'].split('|')]
        prep_list = [item.strip() for item in row['Preparation'].split('|')]
        
        cursor.execute('''
            INSERT OR REPLACE INTO plants (
                plant_name_english, scientific_name, vernacularSwahili, vernacularKalenjin, vernacularLuo, vernacularKisii, vernacularKikuyu,
                usesTraditional, usesScientific, preparationMethod, safetyWarning, commercialStatus, commercialMarketAdvice
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['English Name'], row['Scientific Name'], row['Swahili'], row['Kalenjin'], row['Luo'], row['Kisii'], row['Kikuyu'],
            json.dumps(trad_list), row['Scientific Backing'], json.dumps(prep_list), row['Safety Warning'], row['Commercial Status'], row['Market Advice']
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"✅ SUCCESS! {count} highly valuable medicinal plants injected perfectly.")

if __name__ == "__main__":
    inject_data()