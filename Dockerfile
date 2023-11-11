# Use the official Python runtime as the base image
# Original
# FROM python:3.10
# Slimmed down
FROM python:3.9-alpine

# Set the working directory within the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port that the Flask app will run on
EXPOSE 5000:5000

# Start the Flask application
CMD ["python", "script.py"]

# Build
### docker build . -t xanalysis --no-cache

# Run
### docker run -p 5000:5000 xanalysis