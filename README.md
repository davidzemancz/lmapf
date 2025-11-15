# Python Virtual Environment Setup

This project uses a Python virtual environment to manage dependencies.

## Setup and Activation

### Activate the virtual environment

On macOS/Linux:
```bash
source .venv/bin/activate
```

On Windows:
```bash
.venv\Scripts\activate
```

### Verify activation

Once activated, your terminal prompt should be prefixed with `(venv)`.

You can verify Python is using the virtual environment:
```bash
which python
```

### Install dependencies

After activating the virtual environment, install required packages:
```bash
pip install -r requirements.txt
```

### Deactivate the virtual environment

When you're done working:
```bash
deactivate
```

## Quick Start

```bash
# Activate the environment
source .venv/bin/activate

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Run the main
python main.py

# Deactivate when done
deactivate
```

## Adding New Packages

When you install new packages, update the requirements file:
```bash
pip freeze > requirements.txt
```
