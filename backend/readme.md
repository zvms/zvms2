# zvms-backend
# 镇海中学义工管理系统后端

## 配置
1. 安装mysql(记得改app.cfg里的uri)
2. 初始化数据库
    ```sql
    source sql.sql
    ```
3. 安装依赖包
    ```bash
    cd zvms/backend
    pip3 install -r requirement.txt
    ```

## 运行
```bash
flask --app zvms run
```

或

```bash
export FLASK_APP = zvms
flask run
```
