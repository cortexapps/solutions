#!/bin/sh

echo "Downloading Troubleshooting tooling..."
# Download troubleshoot command binary
curl -LJOs https://github.com/replicatedhq/troubleshoot/releases/download/v0.54.0/support-bundle_darwin_arm64.tar.gz
tar -zxf support-bundle_darwin_arm64.tar.gz
echo "Generating a list of what to collect..."
# the binary needs a yaml spec of what to collect. Instead of sending it separately
# or expecting it to be there already, let's create it dynamically
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

    - secret:
        name: cortex-docker-registry-secret
        namespace: default
        key: .dockerconfigjson
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
    - containerRuntime:
        outcomes:
          - pass:
              when: "== docker"
              message: Docker container runtime was found
          - pass:
              message: A container runtime other than Docker was found 
    - ingress:
        namespace: default
        ingressName: cortex-demo-ingress
        outcomes:
          - fail:
              message: The ingress isn't ingressing
          - pass:
              message: All systems ok on ingress

    - secret:
        checkName: Cortex Registry Check
        secretName: cortex-docker-registry-secret
        namespace: default
        key: .dockerconfigjson
        outcomes:
          - fail:
              message: The `cortex-docker-registry-secret` Secret was not found or the `docker-username` key was not detected.
          - pass:
              message: The Registry Secret was found!

    - deploymentStatus:
        name: cortex-demo-deployment-backend
        namespace: default
        outcomes:
          - fail:
              when: "absent" # note that the "absent" failure state must be listed first if used.
              message: The cortex-demo-deployment-backend deployment is not present.
          - fail:
              when: "< 1"
              message: The cortex-demo-deployment-backend deployment does not have any ready replicas.
          - warn:
              when: "= 1"
              message: The cortex-demo-deployment-backend deployment has only a single ready replica.
          - pass:
              message: There are multiple replicas of the API deployment ready.

    - deploymentStatus:
        name: cortex-demo-deployment-frontend
        namespace: default
        outcomes:
          - fail:
              when: "absent" # note that the "absent" failure state must be listed first if used.
              message: The cortex-demo-deployment-frontend deployment is not present.
          - fail:
              when: "< 1"
              message: The cortex-demo-deployment-frontend deployment does not have any ready replicas.
          - pass:
              when: "= 1"
              message: The cortex-demo-deployment-frontend deployment is ready.

    - deploymentStatus:
        name: cortex-demo-deployment-database
        namespace: default
        outcomes:
          - pass:
              when: "absent" # note that the "absent" failure state must be listed first if used.
              message: The cortex-demo-deployment-database deployment was not found.
          - fail:
              when: "<= 1"
              message: The cortex-demo-deployment-database deployment was found, which is only for demo purposes. Is this a production instance?

                
EOF
echo "Starting..."

./support-bundle bundle-spec.yaml
