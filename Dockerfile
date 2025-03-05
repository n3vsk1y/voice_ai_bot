FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

RUN ln -s /usr/bin/ffmpeg /app/ffmpeg
ENV FFMPEG_PATH="/app/ffmpeg"

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.main"]

