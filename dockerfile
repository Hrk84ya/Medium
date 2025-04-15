FROM python:3.12.9-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install pandas scikit-learn numpy

EXPOSE 8080

CMD ["python", "model.py"]
