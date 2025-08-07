#!/usr/bin/env python3
import os
import sys
import subprocess

# Get PORT from environment variable
port = os.environ.get('PORT', '8000')

# Validate PORT is a number
try:
    port_int = int(port)
    print(f"Starting application on port {port_int}")
except ValueError:
    print(f"Invalid PORT value: '{port}', using default 8000")
    port_int = 8000

# Start uvicorn
cmd = [
    sys.executable, "-m", "uvicorn", 
    "main:app", 
    "--host", "0.0.0.0", 
    "--port", str(port_int)
]

print(f"Executing: {' '.join(cmd)}")
os.execv(sys.executable, [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(port_int)]) 