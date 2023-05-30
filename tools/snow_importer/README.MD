## ServiceNow Importer

ServiceNow Importer is a script to help you import items from your CMDB to Cortex as Services. The script could easily be modified to also import items from ServiceNow as Resources

## API tokens

The script reads the tokens from environment variables.

For the Cortex API Token, assign it to a `CORTEX_API_TOKEN` environment variable. To obtain the API Token, go to `Settings` > `API Keys`. Note that only Administrators have access to get API keys.

For the ServiceNow Token, assing it to the `SNOW_API_TOKEN` environment variable. The script uses `Basic` authentication so you will need to Base64 encode your `username`:`password`.
You can use a tool like this [one](https://www.debugbear.com/basic-auth-header-generator) to do the encoding.

### Configuraiton

The script by default reads in all records from the `cmdb_appl` table but is set as a variable(`s_table`) so you can change this if the records you wish to import are stored in a different table. 
If you wish to only update a subset of the records, add the nescessary `sysparm_query` to the `service-url` variable.

### Ownership

The script reads in the `owned by` field to get the user that owns the item. It retrieves the user'a email from ServiceNow and sets it as the owner in Cortex.

### Links

The script will add a link to the corresponding ServiceNow Item

### Custom Data

The script will add the ServiceNow sys_id as custom data to the service in Cortex
