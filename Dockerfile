# Use the official Python image
FROM python:3.12.3-slim

# Set up a working directory
WORKDIR /code

# Install necessary dependencies for ODBC and pyodbc
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt from the backend directory
COPY ./backend/requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code from the backend directory
COPY ./backend/app /code/app

# Set the PYTHONPATH for correct imports
ENV PYTHONPATH=/code/app

# Expose the port that FastAPI will run on
EXPOSE 80

# Run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
