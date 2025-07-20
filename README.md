# Scanner Web Interface

Eine einfache Web-Oberfläche zum Scannen von Dokumenten mit Kodak i-Serie Scannern (i2000, i2800, etc.). Das System erstellt automatisch PDF-Dateien aus den gescannten Dokumenten.

## 📋 Voraussetzungen

- **Linux-System** (Ubuntu/Debian empfohlen)
- **Kodak i-Serie Scanner** (i2000, i2800, etc. - angeschlossen und erkannt)
- **Internet-Verbindung** (für die Installation)
- **Administrator-Rechte** (sudo-Zugang)

## 🚀 Installation (Schritt-für-Schritt)

### 1. Scanner vorbereiten
- Kodak i-Serie Scanner (i2000, i2800, etc.) per USB anschließen
- Scanner einschalten und warten bis er bereit ist
- Sicherstellen, dass der Scanner vom System erkannt wird

### 2. Dateien herunterladen
1. Alle Projektdateien in einen Ordner kopieren (z.B. `/home/andy/scanner-web/`)
2. Terminal/Kommandozeile öffnen
3. In den Projektordner wechseln:
   ```bash
   cd /home/andy/scanner-web/
   ```

### 3. Installation starten
Das Installationsskript ausführen:
```bash
chmod +x install.sh
./install.sh
```

Das Skript wird automatisch:
- ✅ Erforderliche Pakete installieren
- ✅ Python-Umgebung einrichten
- ✅ Systemdienst erstellen und starten
- ✅ Berechtigungen setzen

### 4. Installation prüfen
Nach erfolgreicher Installation sollten Sie diese Meldung sehen:
```
Installation complete!
The scanner web interface should be running on http://localhost:5000
```

## 🖥️ Verwendung

### Web-Interface öffnen
1. **Browser öffnen** (Firefox, Chrome, Safari, etc.)
2. **Adresse eingeben**: `http://localhost:5000`
3. Die Scanner-Oberfläche sollte erscheinen

### Dokument scannen
1. **Dokument einlegen**:
   - Dokument(e) in das **Dokumenteneinzugsfach (ADF)** des Scanners einlegen
   - Dokumente mit der **bedruckten Seite nach unten** einlegen
   - Papierführung anpassen

2. **Scan-Einstellungen wählen**:
   - **Auflösung**: 
     - `150 DPI` = Schnell, kleine Dateien (für einfache Dokumente)
     - `300 DPI` = Standard-Qualität (empfohlen)
     - `600 DPI` = Hohe Qualität (für wichtige Dokumente)
     - `1200 DPI` = Sehr hohe Qualität (für Archivierung)
   
   - **Farbmodus**:
     - `Farbe` = Vollfarbig (für bunte Dokumente)
     - `Schwarz/Weiß` = Nur schwarz-weiß (für Textdokumente)
   
   - **Beidseitig scannen**: Haken setzen für Duplex-Scan (beide Seiten)

3. **Scan starten**:
   - Auf **"📄 Scan starten"** klicken
   - Scanner startet automatisch
   - Fortschritt wird angezeigt

4. **PDF erhalten**:
   - Nach dem Scan wird automatisch eine PDF-Datei erstellt
   - Datei wird im Format `scan_2025-07-20_14-30-15.pdf` gespeichert
   - PDF-Dateien werden im Ordner `/mnt/docs` gespeichert

## 📁 Dateispeicherung

- **Temporäre Scan-Dateien**: `/tmp/scans` (werden automatisch gelöscht)
- **Fertige PDF-Dateien**: `/mnt/docs`
- **Dateinamen**: `scan_YYYY-MM-DD_HH-MM-SS.pdf`

## 🔧 Wichtige Befehle

### Service-Status prüfen
```bash
sudo systemctl status scanner-web
```

### Service neu starten
```bash
sudo systemctl restart scanner-web
```

### Service stoppen
```bash
sudo systemctl stop scanner-web
```

### Logs anzeigen (bei Problemen)
```bash
sudo journalctl -u scanner-web -f
```

### Service dauerhaft aktivieren
```bash
sudo systemctl enable scanner-web
```

### Service deaktivieren
```bash
sudo systemctl disable scanner-web
```

## ❗ Häufige Probleme und Lösungen

### Problem: "Seite lädt nicht"
**Lösung**:
1. Service-Status prüfen: `sudo systemctl status scanner-web`
2. Falls nicht aktiv: `sudo systemctl start scanner-web`
3. Browser-Cache leeren und neu laden

### Problem: "Scanner nicht gefunden"
**Lösung**:
1. Scanner-Verbindung prüfen (USB-Kabel)
2. Scanner ein-/ausschalten
3. Service neu starten: `sudo systemctl restart scanner-web`
4. Scanner-Geräte auflisten: `scanimage -L`

### Problem: "Keine Berechtigung"
**Lösung**:
1. Benutzer zur Scanner-Gruppe hinzufügen: `sudo usermod -a -G scanner $USER`
2. Neu anmelden oder System neu starten
3. Ordner-Berechtigungen prüfen: `ls -la /tmp/scans /mnt/docs`

### Problem: "Scan bleibt hängen"
**Lösung**:
1. Dokumenteneinzug prüfen (Papierstau?)
2. Scanner neu starten
3. Service neu starten: `sudo systemctl restart scanner-web`
4. Browser-Seite neu laden

### Problem: "PDF-Erstellung fehlgeschlagen"
**Lösung**:
1. Festplattenspeicher prüfen: `df -h`
2. Schreibrechte prüfen: `ls -la /mnt/docs`
3. Service neu starten: `sudo systemctl restart scanner-web`

## 🛠️ Erweiterte Konfiguration

### Benutzer ändern
Im `install.sh` Skript die Variable `USER="andy"` auf Ihren Benutzernamen ändern.

### Port ändern
In der `run.py` Datei die Zeile `app.run(host="0.0.0.0", port=5000, debug=False)` anpassen.

### Speicherordner ändern
In der `run.py` Datei die Variablen `SCAN_DIR` und `OUTPUT_DIR` anpassen.

## 📞 Support

Bei Problemen:
1. **Logs prüfen**: `sudo journalctl -u scanner-web -f`
2. **Service-Status**: `sudo systemctl status scanner-web`
3. **Scanner testen**: `scanimage -L`

## 🔒 Sicherheitshinweise

- Das Interface läuft standardmäßig auf Port 5000
- Nur lokaler Zugriff (localhost) ist aktiviert
- Für Netzwerkzugriff zusätzliche Sicherheitsmaßnahmen implementieren
- PDF-Dateien werden unverschlüsselt gespeichert

## 📝 Technische Details

- **Sprache**: Python 3 mit Flask
- **Scanner-Interface**: SANE (scanimage)
- **PDF-Erstellung**: img2pdf
- **Service-Management**: systemd
- **Web-Interface**: HTML5 mit responsivem Design

---

**Version**: 1.0  
**Letzte Aktualisierung**: Juli 2025
