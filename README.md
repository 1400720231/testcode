#用户名秘密
```text
admin admin123

```
#celery启动
```text

 celery -A testcode worker -l info 

```

#dockerfile
```shell

docker build . -t  testcode 
docker run testcode -p 8080:8080
```