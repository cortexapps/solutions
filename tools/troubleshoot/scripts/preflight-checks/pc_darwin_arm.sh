#!/bin/sh

echo "Downloading Preflight tooling..."
# Download troubleshoot command binary
curl -LJOs https://github.com/replicatedhq/troubleshoot/releases/download/v0.54.0/preflight_darwin_arm64.tar.gz
tar -zxf preflight_darwin_arm64.tar.gz
echo "Generating a list of what to check..."
# the binary needs a yaml spec of what to collect. Instead of sending it separately
# or expecting it to be there already, let's create it dynamically
cat << 'EOF' | tee pc-spec.yaml >/dev/null
apiVersion: troubleshoot.sh/v1beta2
kind: Preflight
metadata:
  name: cortex-bundle
spec:
  collectors:
    - clusterInfo: {}
    - clusterResources: {}
    - secret:
        name: cortex-docker-registry-secret
        namespace: default
        key: .dockerconfigjson
        includeValue: false  
    - secret:
        name: cortex-secret
        namespace: default
        key: DB_HOST
        includeValue: false       
  analyzers:
    - clusterVersion:
        outcomes:
          - fail:
              when: "< 1.20.0"
              message: You are running a very old version of Kubernetes
              uri: https://kubernetes.io
          - warn:
              when: "< 1.24.0"
              message: Your cluster meets the minimum version of Kubernetes, but we recommend you update to 1.17.0 or later.
              uri: https://kubernetes.io
          - pass:
              message: Your cluster is running a newer versions of Kubernetes.
    - nodeResources:
        checkName: Every node in the cluster must have at least 16Gi of memory
        outcomes:
          - warn:
              when: "min(memoryCapacity) <= 16Gi"
              message: There is less than 16 Gi of memory
          - pass:
              message: All nodes have at least 16 GB of memory          
    - containerRuntime:
        outcomes:
          - pass:
              when: "== docker"
              message: Docker container runtime was found
          - pass:
              message: A container runtime other than Docker was found

    - secret:
        checkName: Cortex Registry Secret Check
        secretName: cortex-docker-registry-secret
        namespace: default
        key: .dockerconfigjson
        outcomes:
          - warn:
              message: The `cortex-docker-registry-secret` Secret was not found or the `docker-username` key was not detected. This is needed before you deploy the Helm Chart! Check https://docs.cortex.io/docs/self-managed#basics
          - pass:
              message: The Registry Secret was found!
    - secret:
        checkName: Cortex Secret Check
        secretName: cortex-secret
        namespace: default
        key: DB_HOST
        outcomes:
          - warn:
              message: The `cortex-secret` Secret was not found or there is a problem with it. Is this going to be a demo or production instance? Check https://docs.cortex.io/docs/self-managed#persistent-database for more info.
          - pass:
              message: The Registry Secret was found!          
    - deploymentStatus:
        name: ingress-nginx-controller
        namespace: ingress-nginx
        outcomes:
          - fail:
              when: "absent" # note that the "absent" failure state must be listed first if used.
              message: Did not find an NGINX deployment . 
          - fail:
              when: "< 1"
              message: The NGINX Ingress controller deployment does not have any ready replicas.
          - pass:
              when: "= 1"
              message: The NGINX Ingress controller deployment looks good!
   
                
EOF
echo "Starting..."

./preflight pc-spec.yaml
