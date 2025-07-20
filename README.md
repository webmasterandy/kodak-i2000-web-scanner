# Kodak i2000 Scanner Web Interface

## Übersicht

Dieses Projekt besteht aus zwei Hauptkomponenten:

1. **Kodak Alaris i2000 Scanner Treiber** - Ermöglicht die Kommunikation mit dem Scanner
2. **Web-Interface** - Einfache Benutzeroberfläche zum Scannen von Dokumenten über den Browser

## Systemanforderungen

- Linux-Betriebssystem (getestet mit Ubuntu, Debian)
- Python 3.6 oder höher
- Scanner Kodak Alaris i2400/i2600/i2800 Serie
- Benutzer mit sudo-Rechten
- Internetzugang für die Installation von Abhängigkeiten

## Installation

### 1. Treiberinstallation

Die Treiber für den Kodak Scanner müssen zuerst installiert werden, bevor das Web-Interface funktionieren kann.

#### 1.1 Entpacken der Treiber

```bash
cd /pfad/zu/scanner/treiber
tar -xvzf Kodak_i2000_Linux_Driver.tar.gz
# oder falls als ZIP-Datei
unzip Kodak_i2000_Linux_Driver.zip
cd Kodak_i2000_Linux_Driver
```

#### 1.2 Vorbereitung

Stellen Sie sicher, dass der Scanner **ausgeschaltet** oder **nicht angeschlossen** ist, bevor Sie mit der Installation beginnen.

#### 1.3 Treiberinstallation

Die Treiberinstallation erfolgt mit folgendem Befehl:

```bash
sudo ./setup
```

Während der Installation werden Sie durch mehrere Schritte geführt:

1. Akzeptieren der Lizenzvereinbarung (geben Sie "Y" ein)
2. Bestätigung der Installation von Abhängigkeiten (falls erforderlich)
   - QT v3.x (für die TWAIN-Benutzeroberfläche)
   - Mono und Mono-WinForms (für die TWAIN-Benutzeroberfläche)
   - SANE-Treiber (für SANE-kompatible Anwendungen)
3. Abschließen der Installation

Der Installationsprozess installiert folgende Komponenten in der richtigen Reihenfolge:
- libudev0 (falls erforderlich)
- OpenUSB
- TWAIN Data Source Manager
- Kodak Scanner-Treiberpakete

#### 1.4 Treiberüberprüfung

Nach der Installation können Sie überprüfen, ob die Treiber korrekt installiert wurden:

```bash
# Überprüfung des SANE-Treibers
scanimage -L

# Sollte etwas wie folgendes anzeigen:
# device 'kds_i2000:i2000' is a Kodak i2400 Scanner
```

### 2. Web-Interface Installation

Nachdem die Treiber erfolgreich installiert wurden, können Sie das Web-Interface einrichten:

```bash
cd /pfad/zu/scanner/webinterface
sudo ./install.sh
```

Die Installation:
1. Erstellt eine Python-Umgebung
2. Installiert die notwendigen Python-Abhängigkeiten (Flask, img2pdf)
3. Richtet einen systemd-Service ein, der das Web-Interface automatisch startet

## Verwendung

### Web-Interface

Nach erfolgreicher Installation ist das Web-Interface unter folgender Adresse erreichbar:

```
http://localhost:5000
```

Falls Sie von einem anderen Gerät aus darauf zugreifen möchten, ersetzen Sie "localhost" durch die IP-Adresse des Computers.

Das Interface bietet folgende Funktionen:
- **Auflösung (DPI)**: Wählen Sie zwischen 150, 300, 600 oder 1200 DPI
- **Farbmodus**: Farbe oder Schwarz/Weiß
- **Beidseitig scannen**: Aktivieren Sie diese Option für Duplex-Scans

Nach dem Scannen wird automatisch eine PDF-Datei erstellt und im Ordner `/mnt/docs` gespeichert.

### Servicemanagement

Der Webservice kann über folgende Befehle verwaltet werden:

```bash
# Status überprüfen
sudo systemctl status scanner-web

# Service neustarten
sudo systemctl restart scanner-web

# Service stoppen
sudo systemctl stop scanner-web

# Logs anzeigen
sudo journalctl -u scanner-web -f
```

## Fehlerbehebung

### Scanner wird nicht erkannt

1. Stellen Sie sicher, dass der Scanner eingeschaltet und korrekt angeschlossen ist
2. Überprüfen Sie die USB-Verbindung
3. Überprüfen Sie, ob der Benutzer in der "scanner"-Gruppe ist:
   ```bash
   sudo usermod -a -G scanner $USER
   # Abmelden und wieder anmelden, damit die Änderungen wirksam werden
   ```
4. Überprüfen Sie, ob die Scanner-Treiber korrekt installiert sind:
   ```bash
   scanimage -L
   ```

### Web-Interface ist nicht erreichbar

1. Überprüfen Sie, ob der Service läuft:
   ```bash
   sudo systemctl status scanner-web
   ```
2. Überprüfen Sie die Firewall-Einstellungen, um sicherzustellen, dass Port 5000 freigegeben ist
3. Überprüfen Sie die Logs auf Fehler:
   ```bash
   sudo journalctl -u scanner-web -f
   ```

### Fehlgeschlagene Scans

1. Stellen Sie sicher, dass Papier korrekt ins Dokumenteneinzugsfach eingelegt ist
2. Überprüfen Sie, ob der Ausgabeordner `/mnt/docs` existiert und Schreibrechte hat
3. Überprüfen Sie die Logs des Web-Interfaces

## Zusätzliche Hinweise

- Die gescannten Dokumente werden unter `/mnt/docs` mit dem Namensformat `scan_YYYY-MM-DD_HH-MM-SS.pdf` gespeichert
- Temporäre Scan-Dateien werden unter `/tmp/scans` gespeichert und nach der PDF-Erstellung gelöscht
- Die Einstellungen für Auflösung, Farbmodus und Duplex werden im Browser-Speicher gespeichert

## Deinstallation

Um die Software zu deinstallieren:

```bash
# Web-Interface Service entfernen
sudo systemctl stop scanner-web
sudo systemctl disable scanner-web
sudo rm /etc/systemd/system/scanner-web.service
sudo systemctl daemon-reload

# Treiber deinstallieren (je nach Distribution)
sudo apt remove --purge libopenusb twaindsm kodak-i2000
# oder
sudo rpm -e libopenusb twaindsm kodak-i2000
```
