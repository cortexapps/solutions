# This script adds the following block to a cortex YAML under the info tag:
#
#  x-cortex-static-analysis:
#    sonarqube:
#      project: <prefix>-<entity tag>
#      alias: <prefix>-<entity tag>
prefix="prefix-here"

# Use this if you want to change the entity, but only write it to disk and not change it in the instance.
# You can review manually and then update with this:
# for entity in `ls -1 *.yaml;
# do
#    cortex catalog create -f ${entity}
# done
for entity in $(cortex catalog list -t service | jq -r ".entities[].tag")
do
   echo "entity = $entity"
   cortex catalog descriptor -y -t ${entity} | yq ".info += {\"x-cortex-static-analysis\": { \"sonarqube\": { \"project\": \"${prefix}-${entity}\", \"alias\": \"${prefix}-${entity}\" } } }" > ${entity}.yaml
done

# Uncomment and Use this if you want to modify and update in a single command.  This will not save the entity to disk.
#for entity in $(cortex catalog list -t service | jq -r ".entities[].tag")
#do
#   echo "entity = $entity"
#   cortex catalog descriptor -y -t ${entity} | yq ".info += {\"x-cortex-static-analysis\": { \"sonarqube\": { \"project\": \"${prefix}-${entity}\", \"alias\": \"${prefix}-${entity}\" } } }" | cortex catalog create -f-
#done
