FROM python:3.7-slim-buster
MAINTAINER xiongyao
ADD .  /code
WORKDIR  /code

RUN echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib "> /etc/apt/sources.list

RUN apt-get update -y && \
    apt-get install gcc -y && \
pip install --no-cache-dir -i https://pypi.douban.com/simple -r ./requirements.txt
EXPOSE 8080
CMD ["uwsgi","--ini", "./uwsgi.ini"]