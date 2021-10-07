import sys,getopt,os,uuid,json,logging,time
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename="bp_itrs_integration.log",encoding='utf-8', level=logging.WARNING)
#Sends alerts to BigPanda usign curl
def send_to_bp_rest_api(appkey,bearer,jsonData):
    if bearer and appkey and jsonData:
        os.system('curl -X POST -H "Content-Type: application/json"  -H "Authorization: Bearer '+bearer+'"  https://api.bigpanda.io/data/v2/alerts  -d '+jsonData)
        return True
    else:
        return False
#Writes Json file to directory for BigPanda agent
def send_to_bp_agent(directory,jsonData):
    try:
        with open(directory+'bp_alert'+str(uuid.uuid4())+'.json','w') as outfile:
            outfile.write(jsonData)
    except EnvironmentError as error:
        logging.error('Failed to create json file: '+str(error)+'----JSON DATA'+jsonData)
    return True
#Creates JSON payload based on appkey and environment variables
def format_json(appkey,envarlist,primaryproperty,secondaryproperty):
    jsonData = "{"
    if appkey:
        jsonData+='"app_key":"'+appkey+'",'
    if primaryproperty:
        jsonData+='"primary_property":"'+primaryproperty+'",'
    if secondaryproperty:
        jsonData+='"secondary_property":"'+secondaryproperty+'",'
    jsonData+='"timestamp":"'+str(time.time())+'",'
    for envar in envarlist:
        name = envarlist.get(envar)
        envarvalue = str(os.getenv(envar,""))
        if name:
            jsonData+='"'+name+'":"'+envarvalue+'",'
        else:
            jsonData+='"'+envar+'":"'+envarvalue+'",'
    jsonData=jsonData[:-1]+"}"
    logging.debug('Generated JSON: '+jsonData)
    return jsonData
def main(argsv):
    #default dictionary of environment variables to capture
    #Envar name : Tag Name
    default_envar={
        "_SEVERITY":"status",
        "_PROBE":"probe",
        "_NETPROBE_HOST":"bp_host",
        "_MANAGED_ENTITY":"managed_entity",
        "_RULE":"bp_check",
        "_GATEWAY":"gateway",
        "_SAMPLER":"Sampler",
        "_PLUGINNAME":"plugin_name",
        "_DATAVIEW":"Dataview",
        "_ROWNAME":"row_name",
        "_COLUMN":"column",
        "_HEADLINE":"headline",
        "_attributes":"",
        "_VARIABLE":"variable",
        "_VALUE":"value",
        "_USERDATA ":"",
        "Environment":"",
        "Client":"",
        "Host":"",
        "Location":"",
        "Component":"",
        "UUID":""
        }
    #Set default values
    directory="X:/Users/bdant/Documents/Scripts/"
    appkey="123"
    bearer=""
    primaryproperty = "probe"
    secondaryproperty = "bp_check"
    optionenvar=""
    #capture options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:e:l:", ["agent=","envar","loglevel"])
    except getopt.GetoptError:
        usage(2)
    for option, arg in opts:
        if option in ("-a", "--agent"):
            directory=arg
        if option in ("-e", "--envar"):
            optionenvar=arg
        if option in ("-l","--loglevel"):
            if arg == 'debug':
                logging.setLevel(logging.DEBUG)
            elif arg == 'info':
                logging.setLevel(logging.INFO)
            elif arg == 'warning':
                logging.setLevel(logging.WARNING)
            elif arg == 'critical':
                logging.setLevel(logging.CRITICAL)
            elif arg == 'error':
                logging.setLevel(logging.ERROR)
   
    #Merge_envars
    if optionenvar:
        envarlist=default_envar+optionenvar
    else:
        envarlist=default_envar
    #create JSON
    jsonData = format_json(appkey,envarlist,primaryproperty,secondaryproperty)
    try:
        json.loads(jsonData)
    except ValueError as err:
        #write to log
        raise exception('Improperly formatted json\n'+jsonData)
        #exit()
    #send to BigPanda
    if directory:
        send_to_bp_agent(directory,jsonData)
    else:
        send_to_bp_rest_api(appkey,bearer,jsonData)
if __name__ == "__main__":
    main(sys.argv[1:])
#exit()
