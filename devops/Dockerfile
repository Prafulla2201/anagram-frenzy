# Use an official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the Flask application
EXPOSE 5000

# Set the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]