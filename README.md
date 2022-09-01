#用户名秘密
```text
admin admin123

```
#celery启动
##本地启动
```shell

 celery -A testcode worker -l error 

```
>在与manage.py下的同级目录下执行
##docker 启动
```shell
docker build -t testcode-celery -f ./CeleryDcokerfile .
docker run testcode-celery 
```
>在与manage.py下的同级目录下执行

#uwsgi 启动
##本地启动
```shell

 python manage.py runserver

```
>在与manage.py下的同级目录下执行   
##dokcer启动
```shell
docker build . -t  testcode 
docker run testcode -p 8080:8080
```
>在与manage.py下的同级目录下执行
