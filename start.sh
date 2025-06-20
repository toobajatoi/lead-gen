#!/bin/bash

echo "=== Startup Debug Information ==="
echo "Current directory: $(pwd)"
echo "Files in current directory:"
/bin/ls -la
echo "PORT environment variable: $PORT"
echo "PATH environment variable: $PATH"
echo "Python version:"
/usr/local/bin/python --version
echo "Gunicorn location:"
/usr/local/bin/gunicorn --version
echo "=== Starting Application ==="

exec /usr/local/bin/gunicorn --bind 0.0.0.0:$PORT app:app 