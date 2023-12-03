FROM python:3.9-slim-bullseye

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY assets assets
COPY flet_gui flet_gui
COPY storage storage
COPY db.db3 db.db3
COPY find_products.py find_products.py
COPY RaS_run.py RaS_run.py

ENV FLET_SERVER_PORT=8080

CMD ["python", "RaS_run.py"]
