import os
import sys
import subprocess

# Add the project root to the system path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Run main.py using subprocess
try:
    subprocess.run(
        [sys.executable, os.path.join(project_root, "main.py")],
        check=True
    )
except subprocess.CalledProcessError as e:
    print("❌ Failed to run CurrencyConverter:", e)
