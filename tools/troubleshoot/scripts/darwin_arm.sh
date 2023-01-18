#!/bin/sh

echo "Downloading Troubleshooting tooling..."
# Download troubleshoot command binary
curl -LJOs https://github.com/replicatedhq/troubleshoot/releases/download/v0.54.0/support-bundle_darwin_arm64.tar.gz
tar -zxf support-bundle_darwin_arm64.tar.gz
echo "Generating a list of what to collect..."
cat << 'EOF' | tee bundle-spec.yaml >/dev/null
apiVersion: troubleshoot.sh/v1beta2
kind: SupportBundle
metadata:
  name: cortex-bundle
spec:
  collectors:
    - clusterInfo: {}
    - clusterResources: {}
    - logs:
        selector:
          - app=cortex-demo-backend
        namespace: default
        limits:
          maxAge: 720h # 30*24
          maxLines: 10000
          maxBytes: 5000000
    - logs:
        selector:
          - app=cortex-demo-frontend
        namespace: default
        limits:
          maxAge: 720h # 30*24
          maxLines: 10000
          maxBytes: 5000000  

    - logs:
        selector:
          - app.kubernetes.io/name=postgresql
        namespace: default
        limits:
          maxAge: 720h # 30*24
          maxLines: 10000
          maxBytes: 5000000   
    
  analyzers:
    - clusterVersion:
        outcomes:
          - fail:
              when: "< 1.19.0"
              message: The application requires at least Kubernetes 1.20.0 or later
              uri: https://kubernetes.io
          - warn:
              when: "< 1.20.0"
              message: Your cluster meets the minimum version of Kubernetes, but we recommend you update to 1.17.0 or later.
              uri: https://kubernetes.io
          - pass:
              message: Your cluster meets the recommended and required versions of Kubernetes.
    - containerRuntime:
        outcomes:
          - pass:
              when: "== docker"
              message: A supported container runtime was found
          - pass:
              message: An unsupported container runtime was found
    - storageClass:
        checkName: Required storage classes
        storageClassName: "microk8s-hostpath"
        outcomes:
          - fail:
              message: The microk8s storage class thing was not found
          - pass:
              message: All good on storage classes
    - nodeResources:
        checkName: Must have at least 3 nodes in the cluster
        outcomes:
          - fail:
              when: "count() < 3"
              message: This application requires at least 3 nodes
          - warn:
              when: "count() < 5"
              message: This application recommends at last 5 nodes.
          - pass:
              message: This cluster has enough nodes.
    - nodeResources:
        checkName: Total CPU Cores in the cluster is 4 or greater
        outcomes:
        - fail:
            when: "sum(cpuCapacity) < 4"
            message: The cluster must contain at least 4 cores
        - pass:
            message: There are at least 4 cores in the cluster
    - nodeResources:
        checkName: Each node must have at least 40 GB of ephemeral storage
        outcomes:
        - fail:
            when: "min(ephemeralStorageCapacity) < 40Gi"
            message: Noees in this cluster do not have at least 40 GB of ephemeral storage.
            uri: https://kurl.sh/docs/install-with-kurl/system-requirements
        - warn:
            when: "min(ephemeralStorageCapacity) < 100Gi"
            message: Nodes in this cluster are recommended to have at least 100 GB of ephemeral storage.
            uri: https://kurl.sh/docs/install-with-kurl/system-requirements
        - pass:
            message: The nodes in this cluster have enough ephemeral storage.
    - ingress:
        namespace: default
        ingressName: cortex-demo-ingress
        outcomes:
          - fail:
              message: The ingress isn't ingressing
          - pass:
              message: All systems ok on ingress
EOF
echo "Starting..."

./support-bundle bundle-spec.yaml
