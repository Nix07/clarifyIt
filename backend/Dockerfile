FROM python:3.7

RUN apt-get update
RUN apt-get --assume-yes install default-jre
RUN apt-get --assume-yes install default-jdk
RUN export JAVAHOME=/usr/bin/java

EXPOSE 5000

WORKDIR /task-clarity
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader sentiwordnet
RUN python -m nltk.downloader averaged_perceptron_tagger

COPY /app ./app
CMD ["python", "./app/app.py"]