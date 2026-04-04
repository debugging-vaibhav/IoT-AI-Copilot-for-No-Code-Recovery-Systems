FROM python:3.12-slim

WORKDIR /app

# Install build deps for llama-cpp-python (CPU-only)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ cmake && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN CMAKE_ARGS="-DGGML_CUDA=OFF" pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces expects port 7860
ENV LAM_PORT=7860
EXPOSE 7860

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
