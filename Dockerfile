# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Selenium and Chrome
# This is crucial for running a browser in a headless environment.
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    # Dependencies for Chrome
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    --no-install-recommends

# Download and install Google Chrome
# We need a stable, known version of Chrome for our scraper.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir makes the image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Set an environment variable to indicate we're in production
# Our Python script will use this to run Chrome in headless mode.
ENV RENDER=true

# Command to run the application using our startup script
CMD ["./start.sh"] 