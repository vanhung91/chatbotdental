# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render
EXPOSE 10000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]
