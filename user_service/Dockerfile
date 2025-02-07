# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port Django runs on
EXPOSE 3001

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:3001"]