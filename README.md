# Scanner Web Interface

Eine einfache Weboberfläche zum Scannen von Dokumenten über einen Netzwerk-Scanner.

## Funktionen

- Scan von Dokumenten über eine benutzerfreundliche Weboberfläche
- Unterstützung für verschiedene Auflösungen (150, 300, 600, 1200 DPI)
- Farbmodus-Auswahl (Farbe oder Schwarz/Weiß)
- Duplex-Scanning (Vorder- und Rückseite)
- Automatische PDF-Erstellung

## Voraussetzungen

- Linux-System:
  - **Empfohlen**: Ubuntu 22.04 LTS (beste Kompatibilität)
  - **Eingeschränkt unterstützt**: Ubuntu 24.04 LTS (kann zu Problemen führen)
  - **Nicht unterstützt**: Ubuntu 25.04 und neuere Versionen
- Python 3.6 oder höher
- SANE (Scanner Access Now Easy)
- Unterstützter Scanner (z.B. Kodak i2000)

## Treiberinstallation

### 1. SANE-Backend installieren

```bash
sudo apt update
sudo apt install -y sane sane-utils libsane-dev
```

### 2. Kodak i2000 Treiber installieren (falls zutreffend)

Wenn Sie einen Kodak-Scanner verwenden:

```bash
# Herunterladen der Kodak-Treiber (prüfen Sie die aktuellste Version auf der Herstellerwebseite)
wget https://www.kodak.com/docimaging/drivers/linux_drivers.tgz -O kodak_drivers.tgz
tar -xzf kodak_drivers.tgz
cd kodak_drivers

# Installation der Treiber
sudo ./install.sh

# Nach der Installation neustarten
sudo reboot
```

### 3. Scanner-Treiber überprüfen

Nach der Installation der Treiber und dem Neustart können Sie überprüfen, ob Ihr Scanner erkannt wird:

```bash
scanimage -L
```

Diese Ausgabe sollte Ihren Scanner auflisten, z.B.:
```
device 'kds_i2000:i2000' is a Kodak i2000 scanner
```

### 4. Benutzerrechte für Scanner

Stellen Sie sicher, dass Ihr Benutzer Zugriff auf den Scanner hat:

```bash
sudo usermod -a -G scanner $USER
```

Melden Sie sich ab und wieder an, damit die Änderungen wirksam werden.

## Installation des Web-Interfaces

### 1. Dateien herunterladen

Laden Sie die Projektdateien herunter und extrahieren Sie sie in ein Verzeichnis Ihrer Wahl.

### 2. Installation ausführen

Navigieren Sie zum Projektverzeichnis und führen Sie das Installationsskript aus:

```bash
cd /pfad/zum/projektverzeichnis
chmod +x install.sh
./install.sh
```

Die Installation führt folgende Schritte aus:
- Installation der benötigten Pakete
- Erstellung einer Python-Umgebung
- Installation der Python-Abhängigkeiten
- Einrichtung als Systemdienst

### 3. Überprüfen der Installation

Nach der Installation sollte der Dienst automatisch gestartet werden. Sie können den Status überprüfen mit:

```bash
sudo systemctl status scanner-web
```

## Verwendung

1. Öffnen Sie einen Webbrowser und navigieren Sie zu `http://localhost:5000` (oder die IP-Adresse des Servers)
2. Wählen Sie die gewünschten Scan-Einstellungen aus:
   - Auflösung (DPI)
   - Farbmodus
   - Beidseitiges Scannen (wenn gewünscht)
3. Klicken Sie auf "Scan starten"
4. Legen Sie Ihre Dokumente in den Dokumenteneinzug des Scanners
5. Die gescannten Dokumente werden als PDF im Verzeichnis `/mnt/docs` gespeichert

## Fehlerbehebung

### Scanner wird nicht erkannt

1. Überprüfen Sie, ob der Scanner eingeschaltet und angeschlossen ist
2. Führen Sie `scanimage -L` aus, um zu prüfen, ob der Scanner erkannt wird
3. Prüfen Sie die Logs mit `sudo journalctl -u scanner-web -f`

### Dienst startet nicht

1. Überprüfen Sie die Logs mit `sudo journalctl -u scanner-web -f`
2. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind
3. Versuchen Sie, den Dienst manuell neu zu starten: `sudo systemctl restart scanner-web`

### Scannen funktioniert nicht

1. Stellen Sie sicher, dass der Scanner im ADF-Modus (Automatischer Dokumenteneinzug) betriebsbereit ist
2. Überprüfen Sie, ob der Benutzer in der Scanner-Gruppe ist: `groups $USER`
3. Stellen Sie sicher, dass das Ausgabeverzeichnis existiert und beschreibbar ist

## Dienstmanagement

- Dienst starten: `sudo systemctl start scanner-web`
- Dienst stoppen: `sudo systemctl stop scanner-web`
- Dienst neustarten: `sudo systemctl restart scanner-web`
- Logs anzeigen: `sudo journalctl -u scanner-web -f`

## Deinstallation

Um das Web-Interface zu deinstallieren:

```bash
sudo systemctl stop scanner-web
sudo systemctl disable scanner-web
sudo rm /etc/systemd/system/scanner-web.service
sudo systemctl daemon-reload
```

Löschen Sie anschließend das Projektverzeichnis.
