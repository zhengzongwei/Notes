# rpm包构建

## 环境搭建

```
dnf install rpmdevtools* git
```



## libguestfs-winsupport

```
dnf install libtool libgcrypt-devel libconfig-devel libattr-devel gnutls-devel fuse-devel automake automake
```

## libguestfs

```
sudo dnf builddep SPECS/libguestfs.spec
```

