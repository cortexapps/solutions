## Testing Commands

Command I am using to test the python script. I set my cortex API token and cortex tag as env variables ($CORTEX_API_TOKEN & $CORTEX_TAG).

```shell
python3 deploy.py -k $CORTEX_API_TOKEN -g $CORTEX_TAG -s 12345 -t DEPLOY -e UAT -u SUCCESS -m "Application deployed" -d "Johnny B Goode" -l jbgoode@yourorg.com
```

The above command will create an event like this on the service you specify with the CORTEX_TAG:

![Deploy Event](img/deploy-event.png)