import os

# Define the directory structure
directories = [
    'project_name/data/raw',
    'project_name/data/processed',
    'project_name/notebooks',
    'project_name/src/data',
    'project_name/src/api',
    'project_name/src/models',
    'project_name/src/utils',
    'project_name/tests'
]

# Create the directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create empty __init__.py files to make directories packages
init_files = [
    'project_name/src/__init__.py',
    'project_name/src/data/__init__.py',
    'project_name/src/api/__init__.py',
    'project_name/src/models/__init__.py',
    'project_name/src/utils/__init__.py'
]

for init_file in init_files:
    with open(init_file, 'w') as f:
        pass

# Create placeholder files
placeholder_files = {
    'project_name/src/data/load_data.py': "# Script to load data\n",
    'project_name/src/api/app.py': "# Main API script\n",
    'project_name/src/api/routes.py': "# API route definitions\n",
    'project_name/src/models/model.py': "# Script for model loading and prediction\n",
    'project_name/src/models/train_model.py': "# Script to train model\n",
    'project_name/src/utils/helpers.py': "# Helper functions\n",
    'project_name/tests/test_api.py': "# Tests for API\n",
    'project_name/requirements.txt': "# List of dependencies\n",
    'project_name/Dockerfile': "# Dockerfile for containerization (optional)\n",
    'project_name/README.md': "# Project overview and instructions\n",
    'project_name/.gitignore': "# Git ignore file\n"
}

for file_path, content in placeholder_files.items():
    with open(file_path, 'w') as f:
        f.write(content)

print("Directory structure created successfully.")

