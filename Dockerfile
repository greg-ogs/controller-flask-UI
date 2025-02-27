FROM tensorflow/tensorflow:latest
LABEL authors="grego"

WORKDIR /app

COPY ./app /app

COPY requirements.txt /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y libgl1

RUN python -m pip install --upgrade pip

RUN pip install --upgrade --ignore-installed blinker --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]