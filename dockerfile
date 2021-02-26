FROM python:3.8.5-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
CMD ["python","app.py"]

#https://www.youtube.com/watch?v=3BxLyZWwYoI&t=366s