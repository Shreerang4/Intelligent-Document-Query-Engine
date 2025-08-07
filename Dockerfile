# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-no-torch.txt requirements.txt

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install PyTorch CPU version first
RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install other requirements (excluding PyTorch dependencies)
RUN pip install -r requirements.txt

# Install sentence-transformers separately to avoid PyTorch conflicts
RUN pip install sentence-transformers==5.0.0 --no-deps && \
    pip install transformers==4.55.0 --no-deps

# Copy application code
COPY . /app/

# Make scripts executable
RUN chmod +x build.sh && chmod +x start.sh

# Run the build script
RUN ./build.sh

# Clean up to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip cache purge

# Expose port
EXPOSE 8000

# Run the application with startup script
CMD ["./start.sh"] 