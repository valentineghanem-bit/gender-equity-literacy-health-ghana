FROM python:3.11-slim
LABEL org.opencontainers.image.title="gender-equity-literacy-health-ghana"
LABEL org.opencontainers.image.authors="Valentine Golden Ghanem"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "run_all.sh"]
