
import os
import sys
import subprocess

# Add the project root to PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Run the root logger as a module so imports resolve correctly
try:
    subprocess.run([sys.executable, "-m", "modular_logger.root_logger"], check=True)
except subprocess.CalledProcessError as e:
    print("❌ Failed to run modular_logger:", e)
