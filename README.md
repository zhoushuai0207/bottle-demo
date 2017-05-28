# bottle-demo
bottle-demo 基于sqlite3 和bottle 使用示例



### 本地方式启动 ###
python main.py
默认启动的 http://0.0.0.0:9090


### 镜像方式启动 docker 镜像地址 ###
```
docker pull zhoushuai0207/chinac-demo
启动命令 ： docker run -d --net=host zhoushuai0207/chinac-demo:v1.0 sh -c "python /var/chinac/main.py"
```

### API接口文档地址 ###
```
http://www.sosoapi.com/pass/apidoc/share/forward.htm?shareKey=ce2758220bd4ddab102c829cef1ed974
```

### 请求示例 ###

## 新增主机信息
```
curl -X POST \
  http://127.0.0.1:9090/hosts \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 9d0abb20-cbb8-9585-c196-df2ba096350b' \
  -d '{
  "hostname": "heloname",
  "mac":"ajdfkdf",
  "cpu": 1,
  "mem": 1
}'
```

## 编辑主机信息

```
curl -X PUT \
  http://192.168.74.128:9090/hosts/06166c21422711e7a770c80aa9b7d602 \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: c521c9bd-6f9e-63ff-0bc3-ffca53b6192d' \
  -d '{
  "hostname": "heloname",
  "mac":"ajdfkdf",
  "cpu": 1,
  "mem": 1
}'
```

## 获取单个主机信息
```
curl -X GET \
  http://192.168.74.128:9090/hosts/06166c21422711e7a770c80aa9b7d602 \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 90d289c0-6f70-88e4-43af-bff47a075465'
```


## 删除单个主机

```
curl -X DELETE \
  http://192.168.74.128:9090/hosts/06166c21422711e7a770c80aa9b7d602 \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 614a7557-aa0a-9550-868a-cb9756d46164'
```


## 过滤主机信息

```
curl -X GET \
  'http://127.0.01:9090/hosts?filter=a' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 0a47f793-d6b3-26a8-eebc-d0744c93c88c'
```



## 全部主机信息

```
curl -X GET \
  'http://127.0.01:9090/hosts' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 0a47f793-d6b3-26a8-eebc-d0744c93c88c'
```
