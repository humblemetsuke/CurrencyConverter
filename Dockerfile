FROM python:3.11-slim

# Both ENV below are used for environment variable injection,
# meaning no secret keys or sensitive data is shared in the source code.
ENV EXCHANGE_API_KEY=40263a55e1f1dbc7014ba0b7
ENV DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1389581801579745387/piGnUKYvH4Li_vWdAWUZzFxRFHDY70Ba20rL1JVkqkwxUc27-s3hOy7azplAHsRSI-er

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
