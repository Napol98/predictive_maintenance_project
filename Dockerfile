# 1. Use an official, lightweight Python image
FROM python:3.11-slim

# 2. Set the directory inside the container where files will live
WORKDIR /app

# 3. Copy only requirements first (allows Docker to cache dependencies)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Streamlit runs on port 8501 by default
EXPOSE 8501

# 7. Command to run the dashboard
CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
