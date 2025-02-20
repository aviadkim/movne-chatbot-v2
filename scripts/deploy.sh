#!/bin/bash

# Update version file
echo "3.9.0" > VERSION

# Stage all changes
git add .

# Create commit for version 3.9.0
git commit -m "Release version 3.9.0"

# Create annotated tag for version 3.9.0
git tag -a v3.9.0 -m "Version 3.9.0"

# Push changes to main branch
git push origin main

# Push tag to remote
git push origin v3.9.0

echo "Deployment for version 3.9.0 completed successfully!"