#!/usr/bin/python
import sys,getopt,os,uuid,json

# Sends alerts to BigPanda usign curl
def send_to_bp_rest_api(appkey, bearer, jsonData):
    if bearer and appkey and jsonData:
        os.system('curl -X POST -H "Content-Type: application/json"  -H "Authorization: Bearer ' +
                  bearer+'"  https://api.bigpanda.io/data/v2/alerts  -d '+jsonData)
        return True
    else:
        return False
        
        
# Writes Json file to directory for BigPanda agent
def send_to_bp_agent(directory, jsonData):
    #with open(directory+'bp_alert'+str(uuid.uuid4())+'.json', 'w') as outfile:
    with open(os.open(directory+'bp_alert'+str(uuid.uuid4())+'.json', os.O_CREAT | os.O_WRONLY, 0o777), 'w') as outfile:
        outfile.write(jsonData)
    return True
    
    
#Capture Environement Variables    
def getAlertTags(envarlist):
    incident_identifier = "_GATEWAY_MANAGED_ENTITY_SAMPLER_DATAVIEW_ROWNAME_COLUMN_HEADLINE"
    tagValues = {}
    for envar,name in envarlist.items():
        envarvalue = str(os.getenv(envar, ""))
        incident_identifier=incident_identifier.replace(envar, envarvalue)
        if name == 'status' and envarvalue.lower() not in ['critical', 'warning', 'ok', 'acknowledged', 'unknown']:
            tagValues[name] = "unknown"
            tagValues["orignal_status"]=envarvalue
        elif name:
            tagValues[name]=envarvalue
        else:
            tagValues[envar] = envarvalue
    tagValues["incident_identifier"]=incident_identifier
    return tagValues
    
    
# Add appkey, primary and secondary properties before converting to json payload
def format_json(appkey, tagValues, primaryproperty, secondaryproperty):
    
    tagValues["app_key"]=appkey
    if type(primaryproperty) is list:
        for tag in primaryproperty:
            print("primaryLoop:"+tag)
            if tagValues.get(tag):
                tagValues["primary_property"] = tag
                break
    else:
        tagValue["primary_property"] = primaryproperty
        
    if type(secondaryproperty) is list:
        for tag in secondaryproperty:
            print("secondaryLoop:"+tag)
            if tagValues.get(tag):
                tagValues["secondary_property"] = tag
                break
    else:
        tagValue["secondary_property"] = secondaryproperty   
        
    jsonData = json.dumps(tagValues)
    return jsonData


def main(argsv):
    # default dictionary of environment variables to capture
    # Envar name : Tag Name
    default_envar = {
        "_SEVERITY": "status",
        "_GATEWAY": "gateway",
        "_PROBE": "probe",
        "_NETPROBE_HOST": "",
        "_MANAGED_ENTITY": "managed_entity",
        "_RULE": "bp_check",
        "_SAMPLER": "Sampler",
        "_PLUGINNAME": "plugin_name",
        "_DATAVIEW": "Dataview",
        "_ROWNAME": "row_name",
        "_COLUMN": "column",
        "_HEADLINE": "headline",
        "_attributes": "",
        "Environment": "",
        "Client": "",
        "Host": "bp_host",
        "Location": "",
        "Component": "",
        "UUID": "",
        "_VARIABLE": "variable",
        "_VALUE": "value",
        "_triggerDetails": "trigger",
        "_LOGNAME": "logname",
        "_USERDATA ": ""}
        
        
    # Set default values
    directory = "/var/lib/bigpanda/queue/"
    appkey = "86d68ce77ea1e7e3a6e909375cfff73e"
    bearer = "Bearer c45a4cfe9201e0822b7fd220c1310759"
    primaryproperty = ["bp_host","_NETPROBE_HOST","gateway"]
    secondaryproperty = ["bp_check"]

    
    
    # capture options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:", ["agent="])
    except getopt.GetoptError:
        usage(2)
    for option, arg in opts:
        if option in ("-a", "--agent"):
            directory = arg


    #get envar values
    tagValues = getAlertTags(default_envar)
 
    
    # create JSON
    jsonData = format_json(appkey, tagValues, primaryproperty, secondaryproperty)
    print(jsonData)
    try:
        json.loads(jsonData)
    except ValueError as err:
        # write to log
        raise exception('Improperly formatted json\n'+jsonData)
        exit()
    # send to BigPanda
    if directory:
        send_to_bp_agent(directory, jsonData)
    else:
        send_to_bp_rest_api(appkey, bearer, jsonData)


if __name__ == "__main__":
    main(sys.argv[1:])
exit()
