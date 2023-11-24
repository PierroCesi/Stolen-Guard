FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt \
    && apt-get update \
    && apt-get upgrade 

RUN mkdir stolen-guard 
COPY src stolen-guard/src
COPY ressources stolen-guard/ressources
COPY pfcowboy.session stolen-guard/pfcowboy.session

WORKDIR /stolen-guard

ENTRYPOINT ["python3", "src/StolenGuard.py"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
