import json
import requests
import time
import uuid
from api_backend.apps import helpers
from static.misc_files import messages as err
from datetime import datetime
from collections import OrderedDict
import nbformat
import copy
import fnmatch
from sentry_sdk import capture_exception
from uuid import UUID



#We check hash values of two cells in order to verify that they are correct
TEMPLATE_VALUES = ['c121357ebdcb47598fd5c5f7badc9b31','d6019e062d264461cacda31eace558c0']
VALID_OUTPUT_TYPES = ['string','number','np','function','image','dictionary', 'object', 'audio']
BASE_TASK_TEMPLATE = 'static/misc_file/generate_task.json'
BASE_NOTEBOOK_TEMPLATE = 'static/notebooks/template.ipynb'

class CellMetaData:
    def __init__(self, name=None, expected_output=None, expected_output_variance=None, expected_output_type=None, content_id=None, task_complexity=None, time_complexity=None, key=None):
        self.name = None
        self.expected_output = expected_output
        self.expected_output_variance = expected_output_variance
        self.expected_output_type = expected_output_type
        self.content_id = content_id
        self.task_complexity= task_complexity
        self.time_complexity = time_complexity
        self.solution = None
        self.key = None
        self.sid = None

class CMD(object): 
    def __init__(self, data): 
        self.__dict__ = json.loads(data) 
#TODO - check dict vs ordereddict approach
def generate_tasks(path, sid):
    with open(path) as json_data:
        data = json.load(json_data,)
    
        value_dict = OrderedDict()
        meta_dict = {}
        error_dict = OrderedDict()
        C_MetaData_List = []
        headline_set = False
        valid_template = True


        code = [c for c in data['cells'] if len(c['source']) > 0]
        indices = []
        for idx, c in enumerate(code):
            matching = fnmatch.filter(c['source'], "*#Json Description - *")
            if len(matching)>0 and idx > 1:
                indices.append(idx)

        for idx, c in enumerate(code):
            ## Compare read only values via hash values and ignore them
            if helpers.Helpers.hash_values(str(c['source'])) in TEMPLATE_VALUES and idx <2:
                continue

            if helpers.Helpers.hash_values(str(c['source'])) not in TEMPLATE_VALUES and idx <2:
                return False, err.NOT_VALID_TEMPLATE;
            
            #TODO: iterate over all entries of indicies
            if len(indices)>0:
                index=indices[0]
                res_index = None
                append_flag = False
                json_string = ""
                res = code[indices[0]]['source']
               
                for idy, r_temp in enumerate(res):
                    res[idy] = r_temp.replace('\n', '')
                    if append_flag:
                        json_string += res[idy]
                    if '#Json Description' in r_temp:
                        append_flag = True
                
                CMetaData = CellMetaData()
                CMetaDataDict = CMetaData.__dict__
                try:
                    CMetaData = CMD(json_string) 
                    CMetaDataDict['content_id'] = str(uuid.uuid4())
                except Exception as e:
                    capture_exception(e)

    
                #GR-57 DO VALIDATION OF CMETADATA -> this should be evaluated on the frontend through a UI
                #CHECK FOR
                #-Correct Type
                #-Correct Length
                #-Correct format
                #If any of these is wrong, write to error dictionary
                #If not, write val to Object

                C_MetaData_List.append(CMetaData)
            
            #Dynamically building new NB
            if len(indices) >0:
                c['source'] = c['source'][:indices[0]-1]
                c['source'].append("#____________________________________________________Do NOT modify this code:\n")
                c['source'].append("print(submit_result(sid, '" + CMetaDataDict['content_id'] + "', result))")
               
            # +1 offset so that we can insert at 0 position
            value_dict[idx+1] = c
        
        #Check if we have entries, if so we cannot add it to the database:
        if len(error_dict) > 0:
                return error_dict  

        #Add default init cell to top of cells
        temp_list = []
        temp_list.append("#Do NOT modify this code:\n")
        temp_list.append("import requests\n")
        temp_list.append("import random\n")
        temp_list.append("from IPython.display import display, Markdown, Latex, Math, Javascript\n")
        temp_list.append("from time import sleep\n")
        temp_list.append("\n")
        temp_list.append("def submit_result(sid, cid, result=None):\n")
        temp_list.append("  display(Javascript('IPython.notebook.save_checkpoint();'))\n")
        temp_list.append("  r = requests.post('http://13.48.71.20:5000/tasks', json=[{'sid': sid, 'cid': cid, 'result': result}])\n")
        temp_list.append("  return r.content\n")
        temp_list.append("\n")
        temp_list.append("#___________________________________________________\n")
        temp_list.append("sid = 'XXXX'\n")
        temp_list.append("#___________________________________________________\n")
        temp_list.append("\n")
        temp_list.append("if sid == '':\n")
        temp_list.append("  print('PLEASE FILL IN YOUR USER ID')\n")
        
        clean_entry = None
        with open(BASE_TASK_TEMPLATE) as f:
            clean_entry = json.load(f)
        
        clean_entry['source'] = temp_list

        #Final new NB
        value_dict[0] = clean_entry

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        nid =  uuid.uuid4()

        #todo: Postgres and Neo4j needs to be transactional and rollback on failure
        for k,v in value_dict.items():
            v_json = json.dumps(v)
            res = next((x for x in C_MetaData_List if x.key == k-1), None)
            cid = None if res is None else str(res.content_id)
            db_conn.register_content_jsons(str(nid),cid,str(sid),v_json,ts,k)
        
        #todo check for duplicates or see if hash values make sense in this case as we dont really need duplicate entries on the graph (neither would we need duplicate notebook entries, so we should potentially check already at notebook / task level)
        for c in C_MetaData_List:
            neo_conn.create_node_and_relationship('4bd7396b-67e4-40c8-ac6f-2696ce582974', c)
    
    return None

'''

def generate_notebook_from_tasks(nid, sid, cid=None):
    #nid - we generate a full notebook
    #cid / array of cid we only generate the related tasks
    cells = []
    data = None
    new_nid =  str(uuid.uuid4())
    gdrive_filename = new_nid + '.ipynb'
    #nb = nbformat.read('notebooks/template.json', as_version=4)
    #nbs = nbformat.writes(nb)
    with open('data_sources/template.json') as json_file:
        data = json.load(json_file)

    #Load cells from database and convert to json format
    results = db_conn.select_tasks(nid, sid)
    if results is None or len(results) == 0:
        logger.error("No tasks in DB", exc_info=True)
        raise ValueError("No tasks in DB")

    res = results[0]['json']['source']
    results[0]['json']['source'] = [r.replace('XXXX', sid) for r in res]
    for d in results:
        cells.append(d['json'])

    data['cells'] = cells
    try:
        data_temp = json.dumps(data)
        nb = nbformat.reads(data_temp, as_version=4)
    except Exception as e:
        logger.error("Invalid notebook format" + data_temp, exc_info=True)
        raise ValueError("Invalid notebook format")

    data = json.dumps(data)
    gdrive = gdrive_conn.GdriveConn(sid)
    gid = gdrive.upload_notebook(data, gdrive_filename)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = db_conn.register_gdrive_created_task(gid,sid,new_nid,ts,'')
    
    #Deliver notebook (to where? Jupyter lab?)
    return gid, new_nid
'''