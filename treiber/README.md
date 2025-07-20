## Datei extrahieren
tar -xzf LinuxSoftware_i2000_v4.14.x86_64.deb.tar.gz

## In Verzeichnis wechseln
cd LinuxSoftware_i2000_v4.14.x86_64

## Treiber installieren
sudo dpkg -i *.deb

## Falls Abhängigkeitsfehler:
sudo apt install -f
