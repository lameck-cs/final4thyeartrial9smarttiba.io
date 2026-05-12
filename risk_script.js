/* Script for Cultivation Guide Page - Smart Tiba Kenya */

const predictBtn = document.getElementById("predictBtn");
const cropInput = document.getElementById("cropInput");
const countyInput = document.getElementById("countyInput");
const resultDiv = document.getElementById("riskResult");
const loadingDiv = document.getElementById("loading");
const chartWrapper = document.querySelector(".chart-wrapper");
const downloadContainer = document.getElementById("downloadContainer");
let myChart = null;

function cleanText(str) {
    if (typeof str === 'string') {
        return str.replace(/\*/g, '').replace(/\#/g, ''); 
    }
    return str || '';
}

function formatParagraphs(text) {
    if (!text || typeof text !== 'string') return text || 'No data provided.';
    let cleaned = text.replace(/\*/g, '').replace(/\#/g, '');
    let formatted = cleaned.replace(/(?:^|\s)(\d+[\.\)]\s)/g, "<br><br><strong style='color:#d35400;'>$1</strong>");
    formatted = formatted.replace(/(?:^|\s)(-\s)/g, "<br><br>• ");
    if (formatted.startsWith("<br><br>")) {
        formatted = formatted.substring(8);
    }
    return formatted;
}

// --- ULTIMATE PDF GENERATOR FIX ---
function downloadRiskPDF() {
    const element = document.getElementById('pdf-risk-content');
    const cropName = cropInput.value.trim() || 'Plant';
    const opt = {
      margin:       [0.5, 0.3, 0.5, 0.3], // Top, Right, Bottom, Left margins for breathing room
      filename:     cropName.replace(/\s+/g, '_') + '_Cultivation_Report.pdf',
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2, useCORS: true }, 
      jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' },
      pagebreak:    { mode: ['css', 'legacy'] } // 🌟 Tells the PDF engine to strictly obey our inline CSS breaks
    };
    html2pdf().set(opt).from(element).save();
}

if(predictBtn) {
    predictBtn.addEventListener("click", () => {
        const crop = cropInput.value.trim();
        const county = countyInput.value.trim();

        if (!crop) { alert("Please enter a plant name!"); return; }

        resultDiv.innerHTML = "";
        chartWrapper.style.display = "none";
        downloadContainer.style.display = "none"; 
        loadingDiv.style.display = "block";

        fetch("/forecast_risk", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ crop_name: crop, county: county })
        })
        .then(res => res.json())
        .then(data => {
            loadingDiv.style.display = "none";

            if (data.error) {
                resultDiv.innerHTML = `<p style="color:red">Error: ${data.error}</p>`;
                return;
            }

            renderChart(data.risks);

            let locationText = data.location ? ` in ${cleanText(data.location)}` : "";
            let html = `<h4 style="color:#1b5e20;">Cultivation Guide for: ${cleanText(data.crop)}${locationText}</h4>`;
            
            data.risks.forEach(risk => {
                let riskColor = risk.probability_score > 70 ? "#2ecc71" : "#f39c12"; 

                // 🌟 MAGIC CSS ADDED HERE: 'page-break-inside: avoid; break-inside: avoid;'
                html += `
                    <div class="disease-card" style="page-break-inside: avoid; break-inside: avoid; background:#f9f9f9; border-left: 5px solid ${riskColor}; padding:15px; margin-bottom:15px; border-radius:5px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                            <strong style="color:#333; font-size:1.1em;">${cleanText(risk.disease_name)}</strong>
                            <span style="background:${riskColor}; color:white; padding:4px 10px; border-radius:15px; font-size:0.85em; font-weight:bold;">
                                Viability: ${risk.probability_score}%
                            </span>
                        </div>
                        
                        <p style="margin:5px 0 10px 0; color:#555; font-style:italic; font-size:0.95em;">
                            "${cleanText(risk.description)}"
                        </p>

                        <p style="margin:5px 0; font-size:0.95em; color:#d35400;">
                            <b>🗓️ Best Planting Season:</b> ${cleanText(risk.risk_months)}
                        </p>

                        <p style="margin:5px 0; font-size:0.9em;"><b>📍 Soil Required:</b> ${cleanText(risk.affected_counties)}</p>
                        <p style="margin:0; font-size:0.9em; color:#555;"><i>☁️ Ecological Conditions: ${cleanText(risk.conditions)}</i></p>
                        
                        <div style="page-break-inside: avoid; break-inside: avoid; margin-top:15px; background:#fff8e1; padding:10px; border-radius:5px; color:#f57f17; font-size:0.9em; border-left: 4px solid #ffb300;">
                            <strong style="color:#f57f17;">💰 Market/Value Addition Advice:</strong> <br>
                            <span style="display:block; margin-top:5px; color:#444;">${formatParagraphs(risk.remedy)}</span>
                        </div>
                    </div>
                `;
            });
            
            html += `<p style="text-align:center; font-size:0.8em; color:#aaa; margin-top:20px;">Generated by Smart Tiba Kenya AI System</p>`;
            resultDiv.innerHTML = html;
            
            downloadContainer.style.display = "block"; 
        })
        .catch(err => {
            loadingDiv.style.display = "none";
            resultDiv.innerHTML = `<p style="color:red">Server Error while rendering. Check console.</p>`;
            console.error(err);
        });
    });
}

function renderChart(risks) {
    const ctx = document.getElementById('riskChart').getContext('2d');
    
    // Add CSS break rule to chart wrapper as well
    chartWrapper.style.display = "block";
    chartWrapper.style.pageBreakInside = "avoid";
    chartWrapper.style.breakInside = "avoid";

    const labels = risks.map(r => cleanText(r.disease_name));
    const dataPoints = risks.map(r => r.probability_score);
    const colors = dataPoints.map(s => s > 70 ? '#2ecc71' : (s > 40 ? '#f39c12' : '#e74c3c'));

    if (myChart) myChart.destroy();

    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ecological Suitability Score (%)',
                data: dataPoints,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });
}