```bash
git config --global user.name "zhengzongwei"
git config --global user.email zhengzongwei@foxmail.com

git config --local user.name "w_zhengzongwei"
git config --local user.email w_zhengzongwei@kingsoft.com
```

```mermaid
graph LR
    AppServer1[App Server 1] --> Backend1[Backend Service 1]
    AppServer2[App Server 2] --> Backend1
    AppServer1 --> Database[Database Cluster]
    AppServer2 --> Database
    Backend1 --> API[API Gateway]
    API --> ExternalSystem[External System]
```





