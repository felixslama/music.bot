FROM python:3.8

ADD main.py .
ADD music.py .
ADD config.yml .

RUN pip install discord.py youtube_dl music pynacl pafy pyyaml
RUN apt update
RUN apt install ffmpeg -y
CMD ["python", "./main.py"]