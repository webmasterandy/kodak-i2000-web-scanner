from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import subprocess
import os
import datetime
import threading
import time
import img2pdf

app = Flask(__name__)

SCAN_DIR = "/tmp/scans"
OUTPUT_DIR = "/mnt/docs"

if not os.path.exists(SCAN_DIR):
    os.makedirs(SCAN_DIR)

scan_status = {
    "running": False,
    "message": "Bereit zum Scannen",
    "last_pdf": None,
    "progress": 0
}

HTML = '''
<!doctype html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scanner Web Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
            font-size: 1.1em;
        }
        
        input[type="number"], select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 1.1em;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        input[type="number"]:focus, select:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 15px;
            cursor: pointer;
        }
        
        .checkbox-group label {
            margin-bottom: 0;
            cursor: pointer;
            user-select: none;
        }
        
        .scan-button {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .scan-button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .scan-button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .status-section {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .status-text {
            color: #555;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e1e5e9;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        .scanner-icon {
            text-align: center;
            font-size: 4em;
            margin-bottom: 20px;
            color: #667eea;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .scanning {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="scanner-icon {% if running %}scanning{% endif %}">🖨️</div>
        <h1>Dokument Scanner</h1>
        
        <form method="POST" id="scanForm">
            <div class="form-group">
                <label for="resolution">Auflösung (DPI):</label>
                <select name="resolution" id="resolution" required>
                    <option value="150">150 DPI (schnell, klein)</option>
                    <option value="300">300 DPI (standard)</option>
                    <option value="600">600 DPI (hoch, groß)</option>
                    <option value="1200">1200 DPI (sehr hoch)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="color_mode">Farbmodus:</label>
                <select name="color_mode" id="color_mode" required>
                    <option value="Color">Farbe</option>
                    <option value="Lineart">Schwarz/Weiß</option>
                </select>
            </div>
            
            <div class="checkbox-group">
                <input type="checkbox" name="duplex" id="duplex">
                <label for="duplex">Beidseitig scannen (Duplex)</label>
            </div>
            
            <button type="submit" class="scan-button" {% if running %}disabled{% endif %}>
                {% if running %}
                    🔄 Scan läuft...
                {% else %}
                    📄 Scan starten
                {% endif %}
            </button>
        </form>
        
        <div class="status-section">
            <div class="status-text">Status: {{status}}</div>
            {% if running %}
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{progress}}%"></div>
            </div>
            {% endif %}
            {% if pdf %}
            <div style="margin-top: 15px; color: #28a745; font-weight: 600;">
                📑 PDF erstellt: {{pdf}}
            </div>
            {% endif %}
        </div>
    </div>
    
    {% if running %}
    <script>
        setTimeout(function() {
            window.location.reload();
        }, 3000);
    </script>
    {% endif %}
    
    <script>
        // Einstellungen beim Laden der Seite wiederherstellen
        document.addEventListener('DOMContentLoaded', function() {
            // Gespeicherte Werte laden
            const savedResolution = localStorage.getItem('scanner_resolution') || '300';
            const savedColorMode = localStorage.getItem('scanner_color_mode') || 'Color';
            const savedDuplex = localStorage.getItem('scanner_duplex') === 'true';
            
            // Werte in Formular setzen
            document.getElementById('resolution').value = savedResolution;
            document.getElementById('color_mode').value = savedColorMode;
            document.getElementById('duplex').checked = savedDuplex;
        });
        
        // Einstellungen beim Absenden speichern
        document.getElementById('scanForm').addEventListener('submit', function() {
            localStorage.setItem('scanner_resolution', document.getElementById('resolution').value);
            localStorage.setItem('scanner_color_mode', document.getElementById('color_mode').value);
            localStorage.setItem('scanner_duplex', document.getElementById('duplex').checked);
        });
    </script>
</body>
</html>
'''

def scan_job(resolution, duplex, color_mode):
    scan_status["running"] = True
    scan_status["message"] = "Scanner wird vorbereitet..."
    scan_status["progress"] = 10
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Source korrekt basierend auf duplex Einstellung
    if duplex:
        source = "ADF Duplex"
    else:
        source = "ADF Front"  # Explizit nur Vorderseite für Simplex
    
    scan_status["message"] = f"Scanne mit {resolution} DPI ({'duplex' if duplex else 'simplex'}, {color_mode.lower()})..."
    scan_status["progress"] = 30
    
    # Batch-Scan für mehrere Seiten
    batch_pattern = os.path.join(SCAN_DIR, "out_%d.tiff")
    
    # Scan-Befehl mit batch für mehrere Seiten
    cmd = [
        "scanimage",
        "--device-name", "kds_i2000:i2000",
        "--source", source,
        "--mode", color_mode,
        "--resolution", str(resolution),
        "--format", "tiff",
        "--batch=" + batch_pattern,
        "--batch-start", "1",
        "--batch-increment", "1"
    ]
    
    try:
        scan_status["progress"] = 50
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if proc.returncode != 0:
            scan_status["message"] = f"Scan fehlgeschlagen: {proc.stderr}"
            scan_status["running"] = False
            scan_status["progress"] = 0
            return
            
        scan_status["progress"] = 70
        
    except subprocess.TimeoutExpired:
        scan_status["message"] = "Scan-Timeout erreicht"
        scan_status["running"] = False
        scan_status["progress"] = 0
        return
    except Exception as e:
        scan_status["message"] = f"Scan-Fehler: {str(e)}"
        scan_status["running"] = False
        scan_status["progress"] = 0
        return

    # Alle gescannten TIFF-Dateien finden
    tiff_files = []
    i = 1
    while True:
        tiff_file = os.path.join(SCAN_DIR, f"out_{i}.tiff")
        if os.path.exists(tiff_file):
            tiff_files.append(tiff_file)
            i += 1
        else:
            break
    
    if not tiff_files:
        scan_status["message"] = "Keine Seiten gescannt - Prüfen Sie das Dokumenteneinzugsfach"
        scan_status["running"] = False
        scan_status["progress"] = 0
        return

    # PDF erzeugen aus allen TIFF-Dateien
    scan_status["message"] = f"Erstelle PDF aus {len(tiff_files)} Seite(n)..."
    scan_status["progress"] = 85
    pdf_path = os.path.join(OUTPUT_DIR, f"scan_{timestamp}.pdf")
    
    try:
        with open(pdf_path, "wb") as f_pdf:
            f_pdf.write(img2pdf.convert(tiff_files))
    except Exception as e:
        scan_status["message"] = f"PDF-Erstellung fehlgeschlagen: {str(e)}"
        scan_status["running"] = False
        scan_status["progress"] = 0
        return

    # Alle temporären TIFF-Dateien löschen
    for tiff_file in tiff_files:
        try:
            os.remove(tiff_file)
        except:
            pass

    scan_status["message"] = f"✅ Scan erfolgreich abgeschlossen! {len(tiff_files)} Seite(n) verarbeitet."
    scan_status["last_pdf"] = os.path.basename(pdf_path)
    scan_status["running"] = False
    scan_status["progress"] = 100


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if scan_status["running"]:
            return redirect(url_for("index"))

        try:
            resolution = int(request.form.get("resolution", 300))
        except:
            resolution = 300
            
        duplex = "duplex" in request.form
        color_mode = request.form.get("color_mode", "Color")
        
        # Validiere color_mode (ohne Gray)
        if color_mode not in ["Color", "Lineart"]:
            color_mode = "Color"

        # Scan im Thread starten
        threading.Thread(target=scan_job, args=(resolution, duplex, color_mode)).start()
        return redirect(url_for("index"))

    return render_template_string(HTML,
                                  status=scan_status["message"],
                                  pdf=scan_status["last_pdf"],
                                  running=scan_status["running"],
                                  progress=scan_status["progress"])


@app.route("/pdf/<filename>")
def serve_pdf(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
