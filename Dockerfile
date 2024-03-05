FROM python:3.12

ARG DIR=/code

WORKDIR $DIR

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Start uvicorn
CMD ["uvicorn", "--bind", "0.0.0.0:8000", "-k"]
