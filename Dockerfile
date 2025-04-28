# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy local files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask is running on
EXPOSE 3000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=3000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
