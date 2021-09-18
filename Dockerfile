FROM python:3.8

ADD main.py .
ADD music.py .

RUN pip install discord.py youtube_dl music pynacl
RUN apt update
RUN apt install ffmpeg -y
CMD ["python", "./main.py"]