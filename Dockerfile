FROM python:3

WORKDIR /src

COPY . .

CMD ["python", "src/audit.py"]