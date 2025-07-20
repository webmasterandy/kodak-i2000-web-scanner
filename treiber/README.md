# Kodak i2000 Treiber Installation

## Download
[Kodak i2000 Treiber herunterladen](https://1drv.ms/u/c/58ea869005fe4428/EWP870PbGaJOjAHuyPxzz40BTnXdj2FiQHd4Ooh1Wh2LZw?e=tbqLQc)

```bash
# Datei extrahieren
tar -xzf LinuxSoftware_i2000_v4.14.x86_64.deb.tar.gz

# In Verzeichnis wechseln
cd LinuxSoftware_i2000_v4.14.x86_64

# Treiber installieren
sudo dpkg -i *.deb

# Falls Abhängigkeitsfehler:
sudo apt install -f
```
