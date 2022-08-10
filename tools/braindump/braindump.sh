#!/bin/bash 

# This is your helm deployment name
# If you need to find this, please use "helm list" to find the Cortex deployment name
HELM_MANIFEST="cortex"

# This is your backend deployment name.
# If you need to find this, please use "kubectl get deployments"
CORTEX_BACKEND_DEPLOYMENT="cortex-deployment-backend"

mkdir braindump; cd braindump/
helm get manifest $HELM_MANIFEST > helm-manifest.yaml
kubectl get po -o json -l cortex > pods.json
kubectl logs --since=8h deploymnent/$CORTEX_BACKEND_DEPLOYMENT > backend-logs.log
cd ..
tar -xzcf braindump.tar.gz braindump

echo "\n\n############################## CORTEX BRAINDUMP COMPLED ###################################"
echo "Please send the generated file \'braindump.tar.gz\' to Cortex support at help@cortex.io!"
echo "###########################################################################################\n\n"
