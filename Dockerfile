# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory inside the container
WORKDIR /usr/src/tests

# Copy all files from the current directory to the working directory
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install unzip and wget, add Google Chrome repository, and install Google Chrome
RUN apt-get update && apt-get install -y \
    unzip \
    wget \
    gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Command to run the Python test runner script
CMD ["python", "parallel_test_runner_sample.py"]
