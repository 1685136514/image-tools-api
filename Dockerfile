FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY app.py .

EXPOSE 5050

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "app:app"]
