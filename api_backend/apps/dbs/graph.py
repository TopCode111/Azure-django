from gremlin_python.driver import client, serializer
from api_backend.apps.helpers import Helpers
import sys
import traceback
import uuid
import json
from sentry_sdk import capture_exception, capture_message
from django.conf import settings

from api_backend.apps.apis.models import ScaffoldJsons

class GremlinData():
    def __init__(self):
        self.edges = None
        self.vertices = None
        self.DICT_KEY = 'relations'

    #TODO: every nested object, like a Dictionary, we just drop out of the collection, replace it by an ID
    #and put it on NoSQL/SQL DB

    def attach_scaffold_to_graph(self, key_value_dict, exclude_keys):
        """Attaches Scaffold to graph (vertices and edges) - bulk

        Args:
        key_value_dict: list of dict that holds the the properties of vertices / edges

        Returns:
        List of successes/errors for insert

        Raises:
        TypeError: Some argument didnt properly get filled
        """
        gremlin = Gremlin()
        col_list =  []
        data = self._prepare_edges_and_vertices_array(key_value_dict)
        if data is not None:
            vertices = self._get_vertices_scaffold(data, exclude_keys)
            edges = self._get_edges_scaffold(data)
            #drop data into graph
            col_list.append(gremlin.send_to_graph(vertices))
            col_list.append(gremlin.send_to_graph(edges))
        else:
            capture_message('NoneType error')

        return col_list

    def attach_content_to_graph(self, key_value_dict, exclude_keys):
        """Attaches content to graph (vertices and edges)

        Args:
        key_value_dict: dict that holds the the properties of vertices / edges

        Returns:
        List of successes/errors for insert

        Raises:
        TypeError: Some argument didnt properly get filled
        """
        
        col_list =  []
        vertices = self._get_vertices_content(key_value_dict, exclude_keys)
        edges = self._get_edges_content(key_value_dict)
        gremlin = Gremlin()
        col_list.append(gremlin.send_to_graph(vertices))
        col_list.append(gremlin.send_to_graph(edges))

        return col_list

    #TODO: attach user to graph
    def attach_user_to_graph(self, key_value_dict=None):
        gremlin = Gremlin()
        pass

    def update_data_on_graph(self, id_in_graph, key_value_dict):
        """Updates existing properties in vertices

        Args:
        id_in_graph: id or property of vertice we want to update
        key_value_dict: dictionary key / value for values to change

        Returns:
        List of successes/errors for insert

        Raises:
        TypeError: Some argument didnt properly get filled
        """
        gremlin = Gremlin()
        val = ''
        val_list = []
        try:
            id_val = "g.V('{}')".format(id_in_graph)
            for key, value in key_value_dict.items():
                val += ".property('{}','{}')".format(key, value)
        except Exception as e:
            capture_exception(e)

        val = id_val + val
        val_list.append(val)
        return gremlin.send_to_graph(val_list)
    
    def data_exists(self, key_value_dict):
        """Checks if vertices/nodes on graphs exists by checking the properties provided in dict form

        Args:
        key_value_dict: Key Value of property to check for

        Returns:
        bool: True - Exists / False - Not

        Raises:
        TypeError: Some argument didnt properly get filled
        """

        gremlin = Gremlin()
        val = ''
        try:
            id_val = "g.V()"
            for key, value in key_value_dict.items():
                val += ".has('{}','{}')".format(key, value)
        except Exception as e:
            capture_exception(e)

        val = id_val + val

        return gremlin.check_if_exists(val)
    
    def _prepare_edges_and_vertices_array(self, key_value_dict):
        """Reads in a json file, builds relations and parses it into list- Entity - Relation -> Entity

        Args:
        key_value_dict: JSON that contains data for vertices and edges

        Returns:
        data: Structured list for further extraction of edges / vertices

        Raises:
        TypeError: Some argument didnt properly get filled
        """
        try:
            
            data = key_value_dict
            # Create vertices
            #Get all the ids - throw in dictionary and attach UUIDs
            id_dict = {}
            for d in data['content']:
                uuid_str = str(uuid.uuid4())
                if not d['id'] in id_dict:
                    id_dict[d['id']] = uuid_str
                d['id'] = uuid_str

            for val in data['content']:
                #build new array and attach
                uuid_arr = {}
                if self.DICT_KEY not in val:
                    continue
                for key, value in val[self.DICT_KEY].items():
                    temp_arr = []
                    for v in value:
                        if Helpers.checkUUID(str(v)) is None:
                            #uuid_arr.update({key:id_dict[str(v)]})
                            temp_arr.append(id_dict[v])
                        else:
                            temp_arr.append(v)
                            #uuid_arr.update(v)
                    
                    uuid_arr.update({key:temp_arr})
                    
                val[self.DICT_KEY] = uuid_arr
                
            return data['content']
        except Exception as e:
            capture_exception(e)

#TODO: build dynamic format instructions
    def _get_vertices_scaffold(self, data, exclude_keys):
        """Builds gremlin instructions for scaffold vertices
        All properties containing leading with "p_" are expected to be json dictionaries and get persisted into a json store (Postgres for now)
        The inital content then gets replaced by a reference id

        Args:
        data: Structured list(dict) for extraction of vertices

        Returns:
        List of vertices ready to import

        Raises:
        Exception
        """
        vertices_list = []
        try:
            for d in data:
                val =  "g.addV('{}')".format(d['level'])
                for key, value in d.items():
                
                    if key in exclude_keys:
                        continue

                    if "p_" in key:
                        d[key] = str(uuid.uuid4())
                        try:
                            ScaffoldJsons(d[key], d['sid'], json.dumps(value)).save()
                        except Exception as e:
                            capture_exception(e)

                    if isinstance(value, list):
                        value = ''.join(value)
                    val += ".property('{}','{}')".format(key, value)
                vertices_list.append(val)
        except Exception as e:
            capture_exception(e)

        return vertices_list

    def _get_vertices_content(self, data, exclude_keys):
            """Builds gremlin instructions for content vertices from dictionary by iterating and extracting key_values
            All properties containing leading with "p_" are expected to be json dictionaries and get persisted into a json store (Postgres for now)
            The inital content then gets replaced by a reference id

            Args:
            data: Structured dict for further extraction of edges / vertices
            exclude_keys: List of keys to be excluded for insert

            Returns:
            Gremlin insert statement

            Raises:
            Exception
            """
            
            try:
                val =  "g.addV('{}')".format(data['level'])
                for key, value in data.items():
                    if key in exclude_keys:
                        continue

                    if "p_" in key:
                        d[key] = str(uuid.uuid4())
                        try:
                            ScaffoldJsons(d[key], data['sid'], json.dumps(value)).save()
                        except Exception as e:
                            capture_exception(e)

                    if isinstance(value, list):
                        value = ''.join(value)
                    val += ".property('{}','{}')".format(key, value)
                list_val = [val]
                return list_val

            except Exception as e:
                capture_exception(e)

#TODO: build dynamic format instructions
    def _get_edges_scaffold(self, data):
        """Builds gremlin instructions for edges

        Args:
        data: Structured list for further extraction of vertices

        Returns:
        List of edges ready to import

        Raises:
        Exception
        """
        edges_list = []
        try:
            for d in data:
                if self.DICT_KEY not in d:
                    continue
                for key, value in d[self.DICT_KEY].items():
                    for v in value:
                        uuid_str = str(uuid.uuid4())
                        val = "g.V('id', '{}').addE('{}').to(g.V('id','{}')).property(id,'{}')".format(v, key.upper(), d['id'], uuid_str)
                        edges_list.append(val)
        except Exception as e:
            capture_exception(e)

        return edges_list

    def _get_edges_content(self, data):
        """Builds gremlin instructions for edges

        Args:
        relation_ids: list of relation_ids that define childs to which we attach the parent vertice on scaffold graph
        parent_id: content vertice id

        Returns:
        List of edges ready to import

        Raises:
        Exception
        """
        edges_list = []
        try:
            for key, value in data.items():
                if self.DICT_KEY != key:
                    continue
                for k_1, v_1 in value.items():
                    for v in v_1:
                        uuid_str = str(uuid.uuid4())
                        val = "g.V('id', '{}').addE('{}').to(g.V('id','{}')).property(id,'{}')".format(data['id'], k_1.upper(), v, uuid_str)
                        edges_list.append(val)
        except Exception as e:
            capture_exception(e)

        return edges_list

#todos ignore duplicates
#add property changes
class Gremlin():
    def __init__(self):
        self.client = self.graph_connect()

    def graph_connect(self):
        """Connects to graph db

        Args:
        

        Returns:
        client connection

        Raises:
        Exception
        """
        try:
            return client.Client('wss://kq2.gremlin.cosmos.azure.com:443/', 'g',
                username=settings.SECRET_LIST['gremlin-user'],
                password=settings.SECRET_LIST['gremlin-key'],
                message_serializer=serializer.GraphSONSerializersV2d0()
                )

        except Exception as e:
            capture_exception(e)

    def check_if_exists(self, query):
        """Checks if a edge or vertice exists on a graph

        Args:
        statements: list of formatted stratements
        

        Returns:
        has_result: List of Success/Error results

        Raises:
        Exception
        """
        try:
            callback = self.client.submitAsync(query)
            if len(callback.result().one()) > 0:
                return True
            else:
                return False
        except Exception as e:
            capture_exception(e)

    '''
    "g.addV('problem_set').property('level','problem_set').property('subject','00000000-0000-0000-0000-000000000000').property('id','88746993-8573-42db-8263-a3e9ec2a7819').property('name','problem_set1').property('defined_input','1,2,3').property('defined_solution','problem_set1').property('expected_output','2,4,6').property('expected_output_variance','0').property('expected_output_type','number').property('task_complexity','40').property('time_complexity','40').property('cid','9b43f8f7-5993-46bd-aae3-5e77d8d4052a')"

    '''
    def send_to_graph(self, statements):
        """sends prepared execution statements to graph db

        Args:
        statements: list of formatted stratements for CRU(D)
        

        Returns:
        query_col: List of Success/Error results

        Raises:
        Exception
        """
        query_col = []
        for query in statements:
            try:
                callback = self.client.submitAsync(query)
                if callback.result() is not None:
                    query_col.append("Success: " + query)
                else:
                    query_col.append("Error: " + query)
            except Exception as e:
                capture_exception(e)
                
        return query_col

    