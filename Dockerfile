FROM python:3.11-slim

WORKDIR /code

# Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create a directory for logs (needed for safety.py audit logs)
RUN mkdir -p /root/logs

# Copy all project files
COPY . .

# Expose port 7860 (Hugging Face's default port)
EXPOSE 7860

# Run Uvicorn pointing to your server file
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]