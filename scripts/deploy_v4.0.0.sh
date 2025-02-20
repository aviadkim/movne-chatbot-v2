#!/bin/bash

# Deployment script for version 4.0.0
# This script handles the deployment process for version 4.0.0

# Update version file
echo "4.0.0" > VERSION

# Stage all changes
git add .

# Create commit for version 4.0.0
git commit -m "Release version 4.0.0"

# Create annotated tag for version 4.0.0
git tag -a v4.0.0 -m "Version 4.0.0"

# Push changes to main branch
git push origin main

# Push tag to remote
git push origin v4.0.0

echo "Deployment for version 4.0.0 completed successfully!"