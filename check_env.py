import sys
import os

print("=== Virtual Environment Check ===\n")

# 1. Check if inside a venv
in_venv = sys.prefix != sys.base_prefix # Verifies if the current installation is different than the base
print(f"In virtual environment: {in_venv}")

# 2. Show key paths
print(f"Python executable:  {sys.executable}")
print(f"sys.prefix:         {sys.prefix}")
print(f"sys.base_prefix:    {sys.base_prefix}")

# 3. Show VIRTUAL_ENV variable
venv_path = os.environ.get("VIRTUAL_ENV")
print(f"VIRTUAL_ENV:        {venv_path or 'Not set'}") # Gets the variable from .environ

# 4. Test that pip works
import subprocess
result = subprocess.run(
    [sys.executable, "-m", "pip", "--version"],
    capture_output=True, text=True
)
print(f"\npip: {result.stdout.strip()}")

# 5. Test a basic import
try:
    import json
    print(f"\nStandard library import (json): OK")
except ImportError:
    print("\nStandard library import (json): FAILED")

print("\n=== Done ===")   