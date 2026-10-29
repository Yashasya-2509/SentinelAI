FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY backend ./backend
COPY configs ./configs
RUN pip install --no-cache-dir -e .
COPY scripts ./scripts
COPY dashboard ./dashboard
ENV SENTINELAI_ARTIFACTS=/app/artifacts
EXPOSE 8000
CMD ["uvicorn", "sentinelai.api:app", "--host", "0.0.0.0", "--port", "8000"]
