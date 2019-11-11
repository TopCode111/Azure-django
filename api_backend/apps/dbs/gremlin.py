from gremlin_python.driver import client, serializer
from api_backend.apps.helpers import Helpers
import sys
import traceback
import uuid
from sentry_sdk import capture_exception
from django.conf import settings


class GremlinData():
    def __init__(self):
        self.edges = None
        self.vertices = None
        self.DICT_KEY = 'relations'

    def attach_scaffold_to_graph(self, key_value_dict):
        """Allows to bulk attach vertices and edges to graph. 

        Args:
        path: of Json that contains instructions for vertices / edges

        Returns:
        List of successes/errors for insert

        Raises:
        TypeError: Some argument didnt properly get filled
        """
        gremlin = Gremlin()
        col_list =  []
        data = self._prepare_edges_and_vertices(key_value_dict)
        if data is not None:
            vertices = self._get_vertices_scaffold(data)
            edges = self._get_edges_scaffold(data)
            #drop data into graph
            col_list.append(gremlin.send_to_graph(vertices))
            col_list.append(gremlin.send_to_graph(edges))
        else:
            raise TypeError('NoneType error')

        return col_list

    def attach_content_to_graph(self, key_value_dict=None):
        gremlin = Gremlin()
        gremlin.send_dict_to_graph()

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
            raise TypeError('DictType error')

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
            raise TypeError('DictType error')

        val = id_val + val

        return gremlin.check_if_exists(val)
        
    

    def _prepare_edges_and_vertices(self, key_value_dict):
        """Reads in a json file, builds relations and parses it into list- Entity - Relation -> Entity

        Args:
        path: of Json that contains instructions for vertices / edges

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
                    if Helpers.checkUUID(str(value)) is None:
                        uuid_arr.update({key:id_dict[str(value)]})
                    else:
                        uuid_arr.update(value)

                    
                val[self.DICT_KEY] = uuid_arr
                
            return data['content']
        except Exception as e:
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

#TODO: build dynamic format instructions
    def _get_vertices_scaffold(self, data):
        """Builds gremlin instructions for vertices

        Args:
        data: Structured list for further extraction of edges / vertices

        Returns:
        List of vertices ready to import

        Raises:
        Exception
        """
        vertices_list = []
        try:
            for d in data:
                val = ''
                if 'final_node' in d:
                    hid = Helpers.hash_values(d['level']+d['subject']+d['name']+str(d['final_node']))
                    val = "g.addV('{}').property('subject','{}').property('id','{}').property('name','{}').property('hid','{}').property('final_node','{}')".format(d['level'], d['subject'], d['id'], d['name'], hid, d['final_node'])
                else:
                    hid = Helpers.hash_values(d['level']+d['subject']+d['name'])
                    val = "g.addV('{}').property('subject','{}').property('id','{}').property('name','{}').property('hid','{}')".format(d['level'], d['subject'], d['id'], d['name'], hid) 
                vertices_list.append(val)
        except Exception as e:
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

        return vertices_list

#TODO: build dynamic format instructions
    def _get_edges_scaffold(self, data):
        """Builds gremlin instructions for edges

        Args:
        data: Structured list for further extraction of edges / vertices

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
                    uuid_str = str(uuid.uuid4())
                    val = "g.V('id', '{}').addE('{}').to(g.V('id','{}')).property(id,'{}')".format(d['id'], key.upper(), value, uuid_str)
                    edges_list.append(val)
        except Exception as e:
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

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
                username=settings.SECRET_LIST['gremlin-key'],
                password=settings.SECRET_LIST['gremlin-user'],
                message_serializer=serializer.GraphSONSerializersV2d0()
                )

        except Exception as e:
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

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
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

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
                    val = callback.result().one()
                    query_col.append("Success: " + query)
                else:
                    query_col.append("Error: " + query)
            except Exception as e:
                print('There was an exception: {0}'.format(e))
                traceback.print_exc(file=sys.stdout)
                
        return query_col

    def send_dict_to_graph(self, dict=None):
        #https://gremlinrestclient.readthedocs.io/en/latest/
        """tbd

        Args:
        tbd
        

        Returns:
        tbd

        Raises:
        tbd
        """
        pass