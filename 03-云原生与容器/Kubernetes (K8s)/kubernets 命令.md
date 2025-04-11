# K8S 命令



```
[root@kubernetes-dev dashboard]# kubectl get svc -n kubernetes-dashboard kubernetes-dashboard-kong-proxy
NAME                              TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
kubernetes-dashboard-kong-proxy   NodePort   10.99.137.103   <none>        443:30232/TCP   3m56s


# 创建登陆Token

# 获取admin用户token
kubectl -n kubernetes-dashboard create token admin-user

# 或查看现有secret
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
```

## 创建 admin用户

`kubectl -n kubernetes-dashboard get serviceaccounts` 查看是否有admin

```yaml
# 创建admin 服务账户
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
EOF
  
# 绑定ClusterRole
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF

# 获取Token
kubectl -n kubernetes-dashboard create token admin
```

