FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir 'mcp>=1.24,<2'
COPY server.py .
CMD ["python","server.py"]
