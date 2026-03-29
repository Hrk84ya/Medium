FROM python:3.12.9-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install .

EXPOSE 8080

CMD ["python", "-m", "medium_analysis.model"]
