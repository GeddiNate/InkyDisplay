#!/bin/bash

# Create a virtual environment
VENV_DIR="inky_display"
python3 -m venv "$VENV_DIR"

source "$VENV_DIR/bin/activate"

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate


#create python vitual environment
SERVICE_NAME=inky_display

# Check if the service file exists
SERVICE_FILE="${SERVICE_NAME}.service"
if [ ! -f "$SERVICE_FILE" ]; then
    echo "Error: Service file '$SERVICE_FILE' not found."
    exit 1
fi

# Move the service file to the systemd directory
sudo cp "$SERVICE_FILE" "/etc/systemd/system/"

# Reload systemd to pick up the new service file
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

# Display status information
sudo systemctl status "$SERVICE_NAME"

echo "Service '$SERVICE_NAME' has been set up and started."
