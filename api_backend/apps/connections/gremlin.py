from gremlin_python.driver import client, serializer
import sys
import traceback
import json
import uuid


class GremlinData():
    def __init__(self):
        self.edges = None
        self.vertices = None

    def attach_data_to_graph(self, path):
        """Allow to bulk attach vertices and edges to graph. Ignore duplicates

        Args:
        path: of Json that contains instructions for vertices / edges

        Returns:
        List of successes/errors for insert

        Raises:
        TypeError: Some argument didnt properly get filled
        """
        gremlin = Gremlin()
        data = self.prepare_edges_and_vertices(path)
        if data is not None:
            edges = self.get_edges(data)
            vertices = self.get_vertices(data)
            #drop data into graph
            gremlin.send_to_graph(vertices)
            gremlin.send_to_graph(edges)
        else:
            raise TypeError('NoneType error')


    def prepare_edges_and_vertices(self, path):
        """Reads in a json file, builds relations and parses it into list

        Args:
        path: of Json that contains instructions for vertices / edges

        Returns:
        data: Structured list for further extraction of edges / vertices

        Raises:
        TypeError: Some argument didnt properly get filled
        """
        try:
            with open(path, "r") as read_file:
                data = json.load(read_file)
                # Create vertices
                #Get all the ids - throw in dictionary and attach UUIDs
                id_dict = {}
                for d in data['content']:
                    if d['relationship_name'] not in d:
                        raise KeyError("wrong key given in data")

                    uuid_str = str(uuid.uuid4())
                    if not d['id'] in id_dict:
                        id_dict[d['id']] = uuid_str
                    d['id'] = uuid_str

                for val in data['content']:
                    #build new array and attach
                    uuid_arr = []
                    relationship_name = d['relationship_name']
                    for _, value in enumerate(val[relationship_name]):
                        uuid_arr.append(id_dict[str(value)])

                    val[relationship_name] = uuid_arr
                    
                return data['content']
        except Exception as e:
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

    def get_vertices(self, data):
        """Extracts formatted list of vertices

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
                val = "g.addV('{}').property('subject','{}').property('id','{}').property('name','{}')".format(d['level'], d['subject'], d['id'], d['name'])
                vertices_list.append(val)
        except Exception as e:
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

        return vertices_list

    def get_edges(self, data):
        """Extracts formatted list of edges

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
                relationship_name = d['relationship_name']
                for r in d[relationship_name]:
                    val = "g.V('{}').addE('{}').to('{}')".format(d['id'], relationship_name.upper(), r)
                    edges_list.append(val)
        except Exception as e:
            print('There was an exception: {0}'.format(e))
            traceback.print_exc(file=sys.stdout)

        return edges_list


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
                username="/dbs/kq/colls/kq_graph_id",
                password="",
                message_serializer=serializer.GraphSONSerializersV2d0()
                )

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
                    query_col.append("Success: " + callback.result().one())
                else:
                    query_col.append("Error: " + callback.result().one())
            except Exception as e:
                print('There was an exception: {0}'.format(e))
                traceback.print_exc(file=sys.stdout)
                
        return query_col
