FROM python:3.11-slim

WORKDIR /app

COPY src/app/main.py /app/src/app/
COPY src/utils/ /app/src/utils/

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]