FROM python:3
RUN apt-get update && apt-get install -y python3-tk

COPY requirements.txt
RUN pip install -r requirements.txt

WORKDIR .
COPY . .
CMD [ "python", "main.py" ]