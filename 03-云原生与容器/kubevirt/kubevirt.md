# Kubevirt 安装

- kubevirt-cr.yaml

  ```yaml
  ---
  apiVersion: kubevirt.io/v1
  kind: KubeVirt
  metadata:
    name: kubevirt
    namespace: kubevirt
  spec:
    certificateRotateStrategy: {}
    configuration:
      developerConfiguration:
        useEmulation: true
        featureGates: []
    customizeComponents: {}
    imagePullPolicy: IfNotPresent
    workloadUpdateStrategy: {}
  ```

  

