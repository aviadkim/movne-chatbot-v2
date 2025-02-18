#!/bin/bash

echo "Starting Codespace cleanup..."

# Clean pip cache
clean_pip() {
    echo "Cleaning pip cache..."
    pip cache purge
    rm -rf ~/.cache/pip
}

# Clean apt cache
clean_apt() {
    echo "Cleaning apt cache..."
    sudo apt-get clean
    sudo apt-get autoremove -y
}

# Clean Docker
clean_docker() {
    echo "Cleaning Docker..."
    docker system prune -af --volumes
}

# Clean npm cache
clean_npm() {
    echo "Cleaning npm cache..."
    npm cache clean --force
}

# Run all cleanup functions
clean_pip
clean_apt
clean_docker
clean_npm

echo "Cleanup completed!"
df -h /
