#!/bin/bash

echo "=== Startup Debug Information ==="
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la
echo "PORT environment variable: $PORT"
echo "PATH environment variable: $PATH"
echo "Python version:"
python --version
echo "Gunicorn location:"
which gunicorn
echo "=== Starting Application ==="

exec gunicorn --bind 0.0.0.0:$PORT app:app 