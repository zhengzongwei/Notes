# Mirrors 同步策略

- openeuler

  

  ```bash
  rsync -av --partial --progress --delete  --exclude-from 'openeuler-exclude.lst' rsync://root@repo.openeuler.openatom.cn/openeuler/*  /share/mirrorHub
  
  openEuler-preview/
  bugFix/
  openEuler-22.03-LTS-SP3/ISO/source/
  openEuler-22.03-LTS-SP3/ISO/'*-debug-*'
  
  openEuler-22.03-LTS-SP3/debuginfo/
  openEuler-22.03-LTS-SP3/embedded_img/
  openEuler-22.03-LTS-SP3/source/
  ```

- debian

  ```bash
  rsync -av --partial --progress --delete --exclude-from 'debian-exclude.lst' rsync://rsync.mirrors.ustc.edu.cn/debian-cd /share/mirrorHub/debian-cd
  
  12.5.0/source/
  12.5.0-live/source/
  ```


- ubuntu

  ```bash
  rsync -av -P --delete rsync://rsync.mirrors.ustc.edu.cn/ubuntu-releases/ /share/mirrorHub/ubuntu-releases/
  ```

  

- pypi

  ```bash
  rsync -av -P --delete rsync://rsync.mirrors.ustc.edu.cn/pypi /share/mirrorHub/pypi
  ```

  

