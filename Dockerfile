FROM tensorflow/tensorflow:latest
LABEL authors="grego"

WORKDIR /app

COPY .. /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y libgl1

RUN pip install --upgrade --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]