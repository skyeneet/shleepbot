FROM python:3
RUN pip3 install discord
ADD . /shleepbot
WORKDIR /shleepbot
RUN mkdir -p storage/
CMD [ "python3", "./run.py"]
