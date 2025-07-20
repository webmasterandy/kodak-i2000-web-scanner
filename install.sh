#!/bin/bash

set -e

INSTALL_DIR="$(pwd)"
SERVICE_NAME="scanner-web"
USER="andy"

echo "Installing Scanner Web Interface..."

# Stop and remove existing service if it exists
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Stopping existing service..."
    sudo systemctl stop "$SERVICE_NAME"
fi

if systemctl is-enabled --quiet "$SERVICE_NAME" 2>/dev/null; then
    echo "Disabling existing service..."
    sudo systemctl disable "$SERVICE_NAME"
fi

if [[ -f "/etc/systemd/system/$SERVICE_NAME.service" ]]; then
    echo "Removing existing service file..."
    sudo rm -f "/etc/systemd/system/$SERVICE_NAME.service"
    sudo systemctl daemon-reload
fi

# Remove existing virtual environment
if [[ -d "$INSTALL_DIR/venv" ]]; then
    echo "Removing existing virtual environment..."
    rm -rf "$INSTALL_DIR/venv"
fi

# Install required packages
echo "Installing required packages..."
sudo apt update
sudo apt install -y python3-venv python3-pip

# Create new virtual environment
echo "Creating Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"

echo "Installing Python dependencies..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install flask img2pdf

# Create output directories
echo "Creating output directories..."
sudo mkdir -p /tmp/scans
sudo mkdir -p /mnt/docs

# Set ownership and permissions
echo "Setting file permissions..."
sudo chown "$USER:$(id -gn $USER)" /tmp/scans /mnt/docs

# Add andy user to scanner group for device access
echo "Adding user to scanner group..."
sudo usermod -a -G scanner "$USER" || echo "Could not add user to scanner group"

# Create new systemd service file
echo "Creating systemd service..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null << EOF
[Unit]
Description=Scanner Web Interface
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/run.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "Service file created."

# Reload systemd and enable service
echo "Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

# Wait a moment for service to start
sleep 2

echo "Installation complete!"
echo "Service status:"
sudo systemctl status "$SERVICE_NAME" --no-pager
echo ""
echo "Checking if venv was created:"
ls -la "$INSTALL_DIR/"
echo ""
echo "The scanner web interface should be running on http://localhost:5000"
echo "To view logs: sudo journalctl -u $SERVICE_NAME -f"
echo "To restart: sudo systemctl restart $SERVICE_NAME"
echo "To stop: sudo systemctl stop $SERVICE_NAME"
echo "To view logs: sudo journalctl -u $SERVICE_NAME -f"
echo "To restart: sudo systemctl restart $SERVICE_NAME"
echo "To stop: sudo systemctl stop $SERVICE_NAME"
echo ""
echo "Note: Use './install.sh --force' to force recreate venv and service"
