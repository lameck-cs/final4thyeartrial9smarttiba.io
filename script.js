/* Smart Tiba Kenya - Medicinal Plant UI Script */

const preview = document.getElementById("preview");
const imageInput = document.getElementById("imageInput");
const cameraBtn = document.getElementById("cameraBtn");
const stopCameraBtn = document.getElementById("stopCameraBtn");
const video = document.getElementById("camera");
const canvas = document.getElementById("canvas");
const identifyBtn = document.getElementById("identifyBtn");

const plantTextSearch = document.getElementById("plantTextSearch");
const searchPlantBtn = document.getElementById("searchPlantBtn");
const diseaseTextSearch = document.getElementById("diseaseTextSearch");
const searchDiseaseBtn = document.getElementById("searchDiseaseBtn");
const loadingIndicator = document.getElementById("loadingIndicator");
const resultsContent = document.getElementById("resultsContent");

let currentFile = null;
let currentStream = null;

function cleanText(str) {
    if (typeof str === 'string') { return str.replace(/\*/g, '').replace(/\#/g, ''); }
    return str || 'N/A';
}

function formatParagraphs(text) {
    if (!text || typeof text !== 'string') return text || 'No data provided.';
    let cleaned = text.replace(/\*/g, '').replace(/\#/g, '');
    let formatted = cleaned.replace(/(?:^|\s)(\d+[\.\)]\s)/g, "<br><br><strong style='color:#f57f17;'>$1</strong>");
    formatted = formatted.replace(/(?:^|\s)(-\s)/g, "<br><br>• ");
    if (formatted.startsWith("<br><br>")) {
        formatted = formatted.substring(8);
    }
    return formatted;
}

function formatList(items) {
    if (Array.isArray(items)) {
        return `<ul style="margin: 5px 0; padding-left: 20px;">
                    ${items.map(i => `<li style="margin-bottom: 3px;">${cleanText(i)}</li>`).join('')}
                </ul>`;
    }
    return formatParagraphs(items); 
}

function showLoading() {
    resultsContent.innerHTML = "";
    loadingIndicator.style.display = "block";
}

function hideLoading() { loadingIndicator.style.display = "none"; }

// --- ULTIMATE PDF GENERATOR FIX (FOR BOTANICAL SCANNER) ---
function downloadPDF(elementId, filename) {
    const element = document.getElementById(elementId);
    const opt = {
      margin:       [0.5, 0.3, 0.5, 0.3], // Top, Right, Bottom, Left margins for breathing room
      filename:     filename.replace(/\s+/g, '_') + '.pdf',
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2, useCORS: true }, 
      jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' },
      pagebreak:    { mode: ['css', 'legacy'] } // 🌟 Forces the PDF to obey the CSS page-break rules below
    };
    html2pdf().set(opt).from(element).save();
}

function searchByPlantName(name) {
    plantTextSearch.value = name;
    searchPlantBtn.click();
}

function renderPlantProfile(data) {
     const imgUrl = data.image_url && !data.image_url.includes("via.placeholder") ? data.image_url : "logo.png";
     const reportName = cleanText(data?.plant_name_english) + "_Botanical_Report";

     // 🌟 NEW: SMART VERNACULAR CLEANER LOGIC
     const swahili = cleanText(data?.local_names?.swahili);
     const kalenjin = cleanText(data?.local_names?.kalenjin);
     const luo = cleanText(data?.local_names?.luo);
     const kisii = cleanText(data?.local_names?.kisii);
     const kikuyu = cleanText(data?.local_names?.kikuyu);

     let localNamesHtml = "";
     const combinedStr = (swahili + kalenjin + luo + kisii + kikuyu).toLowerCase();

     // Check if the AI repeated "not indigenous", "not native", or if it's completely unknown
     if (combinedStr.includes("not indigenous") || combinedStr.includes("not native") || (swahili === "Unknown" && kalenjin === "Unknown")) {
         localNamesHtml = `<span style="color:#d35400; font-style:italic;">🌍 Not indigenous to Kenya (No established local vernacular names).</span>`;
     } else {
         localNamesHtml = `
            <strong>🌍 Local Kenyan Names (Vernacular):</strong><br>
            <span style="color:#555;">
                <b>Swahili:</b> ${swahili} | 
                <b>Kalenjin:</b> ${kalenjin} | 
                <b>Luo:</b> ${luo} | 
                <b>Kisii:</b> ${kisii} | 
                <b>Kikuyu:</b> ${kikuyu}
            </span>
         `;
     }

     let htmlContent = `
        <div style="text-align:right; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.75em; background:#f4f4f4; color:#555; padding:3px 8px; border-radius:10px;">Data Source: ${data.source || "Unknown"}</span>
            <button onclick="downloadPDF('pdf-content', '${reportName}')" style="background:#1565c0; margin:0; padding:8px 15px;">📥 Download PDF Report</button>
        </div>

        <div id="pdf-content" style="background:white; padding:20px; border-radius:8px; border: 1px solid #eee;">
            
            <div style="page-break-inside: avoid; break-inside: avoid; text-align:center; margin-top:10px; margin-bottom:20px;">
                <img src="${imgUrl}" alt="${cleanText(data?.plant_name_english)}" onerror="this.src='logo.png'" style="width:100%; max-width:400px; height:250px; object-fit:cover; border-radius:10px; border: 4px solid #a5d6a7; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            </div>

            <div style="page-break-inside: avoid; break-inside: avoid; border-bottom: 2px solid #a5d6a7; padding-bottom: 10px; margin-bottom: 15px;">
                <h2 style="color:#1b5e20; margin:0;">${cleanText(data?.plant_name_english)}</h2>
                <p style="font-style:italic; color:#2e7d32; margin:0; font-size:1.1em;">${cleanText(data?.scientific_name)}</p>
            </div>

            <div style="page-break-inside: avoid; break-inside: avoid; background:#f1f8e9; padding:10px; border-radius:5px; margin-bottom:15px; font-size:0.9em;">
                ${localNamesHtml}
            </div>

            <div style="page-break-inside: avoid; break-inside: avoid; background:#ffebee; border-left: 5px solid #f44336; padding:10px; margin-bottom:15px; border-radius:4px;">
                <strong style="color:#c62828;">⚠️ Safety & Dosage Warning:</strong>
                <p style="margin:5px 0 0 0; color:#b71c1c; font-size:0.95em;">${cleanText(data?.safety_warning)}</p>
            </div>

            <div style="page-break-inside: avoid; break-inside: avoid; display:flex; gap:10px; flex-wrap:wrap; margin-bottom:15px;">
                <div style="flex:1; min-width:200px; background:#e8f5e9; padding:10px; border-radius:5px; border-top: 3px solid #4caf50;">
                    <strong style="color:#2e7d32;">🌿 Traditional Community Uses</strong>
                    <div style="font-size:0.9em; color:#333; margin-top:5px;">${formatList(data?.medicinal_uses?.traditional || [])}</div>
                </div>
                <div style="flex:1; min-width:200px; background:#e3f2fd; padding:10px; border-radius:5px; border-top: 3px solid #2196f3;">
                    <strong style="color:#1565c0;">🔬 Scientific Backing (Pharmacognosy)</strong>
                    <p style="font-size:0.9em; color:#333; margin-top:5px;">${formatParagraphs(data?.medicinal_uses?.scientific_backing)}</p>
                </div>
            </div>

            <div style="page-break-inside: avoid; break-inside: avoid; margin-bottom:15px;">
                <strong style="color:#555;">🥣 Preparation Method:</strong>
                <div style="font-size:0.95em;">${formatList(data?.preparation_method || [])}</div>
            </div>

            <div style="page-break-inside: avoid; break-inside: avoid; background:#fff8e1; border-left: 5px solid #ffb300; padding:10px; margin-bottom:15px; border-radius:4px;">
                <strong style="color:#f57f17;">💰 Commercial Value (${cleanText(data?.commercial_value?.status)}):</strong>
                <p style="margin:5px 0 0 0; color:#555; font-size:0.95em;">${formatParagraphs(data?.commercial_value?.market_advice)}</p>
            </div>
            
            <p style="text-align:center; font-size:0.8em; color:#aaa; margin-top:20px;">Generated by Smart Tiba Kenya AI System</p>
        </div>

        <div style="text-align:center; margin-top:15px;"><button onclick="location.reload()" style="background:#ddd; color:#555; padding:10px 20px; border-radius:5px; border:none; cursor:pointer;">🔄 New Search</button></div>
    `;
    resultsContent.innerHTML = htmlContent;
}

function renderDiseaseCures(data) {
    const reportName = cleanText(data?.disease) + "_Remedies_Report";

    let htmlContent = `
        <div style="text-align:right; margin-bottom:10px;">
            <button onclick="downloadPDF('pdf-content', '${reportName}')" style="background:#1565c0; padding:8px 15px;">📥 Download PDF Report</button>
        </div>

        <div id="pdf-content" style="background:white; padding:20px; border-radius:8px; border: 1px solid #eee;">
            <div style="page-break-inside: avoid; break-inside: avoid; border-bottom: 2px solid #a5d6a7; padding-bottom: 10px; margin-bottom: 15px;">
                <h2 style="color:#c62828; margin:0;">Suggested Cures for: ${cleanText(data?.disease)}</h2>
                
                ${data.disease_description ? `
                <div style="background:#e3f2fd; padding:12px; border-left:4px solid #2196f3; margin-top:12px; margin-bottom:12px; border-radius:4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <strong style="color:#1565c0; font-size:1.05em;">📖 What is ${cleanText(data?.disease)}?</strong>
                    <p style="margin:5px 0 0 0; color:#333; font-size:0.95em; line-height:1.5;">${cleanText(data.disease_description)}</p>
                </div>` : ''}

                <p style="color:#555; font-size:0.9em; margin-top:5px; font-style:italic;">Ask local ethnobotanists for plant availability. Preparation methods and safety warnings are critical to avoid toxicity.</p>
            </div>
    `;

    if(data?.suggestions) {
        data.suggestions.forEach(s => {
            const imgUrl = s.image_url && !s.image_url.includes("via.placeholder") ? s.image_url : "logo.png";
            
            htmlContent += `
            <div class="suggestion-card" style="page-break-inside: avoid; break-inside: avoid; background:#fff; border-bottom: 2px solid #ddd; padding:15px; margin-bottom:15px; border-radius:5px; display:flex; gap:15px; flex-wrap:wrap;">
                
                <div style="flex:1; min-width: 200px; border-right:2px solid #c62828; padding-right:15px;">
                    <img src="${imgUrl}" alt="${cleanText(s.english_name)}" onerror="this.src='logo.png'" style="width:100%; height:150px; object-fit:cover; border-radius:5px; margin-bottom:10px; border:1px solid #eee;">
                    <h3 style="margin: 0 0 5px 0; color:#1b5e20;">${cleanText(s.english_name)}</h3>
                    <div style="font-size:0.9em; color:#666; font-style:italic; margin-bottom:10px;">Swahili: ${cleanText(s.swahili_name)}</div>
                    <button data-html2canvas-ignore="true" onclick="searchByPlantName('${s.search_query}')" style="background:#558b2f; padding:8px 12px; font-size:0.9em; color:white; border:none; border-radius:4px; cursor:pointer; width:100%;">Analyze Plant Data 🌿</button>
                </div>
                
                <div style="flex:2; min-width: 250px;">
                    <div style="font-size:0.95em; color:#333; margin-bottom:10px;">
                        <strong>Properties:</strong> ${formatParagraphs(s.brief_medicinal_properties)}
                    </div>
                    
                    <div style="background:#e8f5e9; padding:10px; border-radius:4px; margin-bottom:10px; border-left: 4px solid #4caf50;">
                        <strong style="color:#2e7d32;">🥣 Safe Preparation Method:</strong>
                        <div style="font-size:0.9em; margin-top:5px;">${formatList(s.preparation_method || [])}</div>
                    </div>

                    <div style="background:#ffebee; color:#b71c1c; font-size:0.85em; padding:8px; border-radius:3px; border-left: 4px solid #f44336;">
                        <b>⚠️ Toxicity & Safety Warning:</b> ${cleanText(s.safety_warning)}
                    </div>
                </div>
            </div>
            `;
        });
    }
    
    htmlContent += `
            <p style="text-align:center; font-size:0.8em; color:#aaa; margin-top:20px;">Generated by Smart Tiba Kenya AI System</p>
        </div>
        <div style="text-align:center; margin-top:20px;"><button onclick="location.reload()" style="background:#ddd; color:#555; padding:10px 20px; border-radius:5px; border:none; cursor:pointer;">🔄 Clear Search</button></div>
    `;
    resultsContent.innerHTML = htmlContent;
}

searchPlantBtn.addEventListener("click", () => {
    const query = plantTextSearch.value.trim();
    if (!query) { alert("Enter a plant name."); return; }
    
    showLoading();
    fetch("/search_plant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plant_name: query })
    })
    .then(res => res.json())
    .then(data => {
        hideLoading();
        if (data.error) { resultsContent.innerHTML = `<span style="color:red">Error: ${data.error}</span>`; return; }
        renderPlantProfile(data);
    })
    .catch(err => { 
        hideLoading(); 
        resultsContent.innerHTML = `<span style="color:red">Error rendering profile. Check console.</span>`;
        console.error(err);
    });
});

searchDiseaseBtn.addEventListener("click", () => {
    const query = diseaseTextSearch.value.trim();
    if (!query) { alert("Enter a condition."); return; }
    
    showLoading();
    fetch("/search_disease", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ disease_name: query })
    })
    .then(res => res.json())
    .then(data => {
        hideLoading();
        if (data.error) { resultsContent.innerHTML = `<span style="color:red">Error: ${data.error}</span>`; return; }
        renderDiseaseCures(data);
    })
    .catch(err => { 
        hideLoading(); 
        resultsContent.innerHTML = `<span style="color:red">Error rendering cures. Check console.</span>`;
        console.error(err);
    });
});

if(imageInput) {
    imageInput.addEventListener("change", function() {
        if (this.files && this.files[0]) {
            currentFile = this.files[0];
            preview.src = URL.createObjectURL(currentFile);
            preview.style.display = "block";
            if(video) video.style.display = "none";
            stopCamera();
            resultsContent.innerHTML = ""; 
        }
    });
}

function stopCamera() {
    if (currentStream) { currentStream.getTracks().forEach(track => track.stop()); }
    if(video) video.style.display = "none";
    if(stopCameraBtn) stopCameraBtn.style.display = "none";
    if(cameraBtn) cameraBtn.style.display = "block";
}

if(cameraBtn) {
    cameraBtn.addEventListener("click", () => {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                currentStream = stream;
                video.srcObject = stream;
                video.style.display = "block";
                video.play();
                preview.style.display = "none";
                cameraBtn.style.display = "none";
                stopCameraBtn.style.display = "block";

                video.onclick = () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
                    canvas.toBlob(blob => {
                        currentFile = new File([blob], "camera.jpg", { type: "image/jpeg" });
                        preview.src = URL.createObjectURL(currentFile);
                        preview.style.display = "block";
                        stopCamera();
                    }, "image/jpeg", 0.95);
                };
            }).catch(err => alert("Camera error: " + err));
    });
}
if(stopCameraBtn) stopCameraBtn.addEventListener("click", stopCamera);

if(identifyBtn) {
    identifyBtn.addEventListener("click", () => {
        if (!currentFile) { alert("Please upload a plant image."); return; }
        const formData = new FormData();
        formData.append("image", currentFile);
        showLoading();
        fetch("/identify", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            hideLoading();
            if (data.error) { resultsContent.innerHTML = `<span style="color:red">Error: ${data.error}</span>`; return; }
            renderPlantProfile(data);
        }).catch(err => { 
            hideLoading(); 
            resultsContent.innerHTML = `<span style="color:red">Error rendering upload results. Check console.</span>`; 
            console.error(err);
        });
    });
}