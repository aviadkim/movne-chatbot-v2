#!/bin/bash

# Deployment script for version 3.8.1
# This script handles the deployment process for version 3.8.1

# Update version file
echo "3.8.1" > VERSION

# Stage all changes
git add .

# Create commit for version 3.8.1
git commit -m "Release version 3.8.1"

# Create annotated tag for version 3.8.1
git tag -a v3.8.1 -m "Version 3.8.1"

# Push changes to main branch
git push origin main

# Push tag to remote
git push origin v3.8.1

echo "Deployment for version 3.8.1 completed successfully!"