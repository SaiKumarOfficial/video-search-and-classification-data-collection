FROM python:3.9.14-slim-bullseye

COPY . /datacollection

WORKDIR /datacollection

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8030

CMD ["python", "app.py"]
