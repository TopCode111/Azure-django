class KQuant:
    """Aggregation class for Knowledge Quant (KQ) - containing all information for one KQ unit

        Args:
        sid: user id
        task_complexity: task complexity for specific KQ (1-100)
        time_complexity: time complexity for specific KQ (1-100)

        Returns:
        Instantiated class

    """
    def __init__(self, kid, sid=None, task_complexity=None, time_complexity=None):
        self.sid = sid #optional - only needs to be set when its attached to a user
        self.kid = kid #cid of node
        self.k_json = [] #one json / cell per task
        self.task_complexity_agg = task_complexity
        self.time_complexity_agg = time_complexity

    def build_object(self, output_type, output_source, output_values, name, key, l_type, json_cell, k_type, time_complexity, task_complexity, media_encoding=None, output_variance=None, \
            input_type=None, input_source=None, input_values=None):

        k_input = KInput(input_type, input_source, input_values)
        k_output = KOutput(output_type, output_source, output_values, output_variance=None)
        k_properties = KProperties(name, key, l_type, time_complexity, task_complexity, media_encoding, k_input, k_output)
        k_json = (json_cell, k_type, k_properties, KAnalytics())

        self.k_json.append(k_json)
        return self

    def build_object_as_json_dict(self, output_type, output_source, output_values, name, key, l_type, json_cell, k_type, time_complexity, task_complexity, media_encoding=None, output_variance=None, \
            input_type=None, input_source=None, input_values=None):

        if k_type == "code":
            k_input = KInput(input_type, input_source, input_values)
            k_input = k_input.__dict__
            k_output = KOutput(output_type, output_source, output_values, output_variance=None)
            k_output = k_output.__dict__
            k_properties = KProperties(name, key, l_type, time_complexity, task_complexity, media_encoding, k_input, k_output)
            k_properties = k_properties.__dict__
            k_json = (json_cell, k_type, k_properties, KAnalytics().__dict__)
        else:
            k_input = []
            k_output = []
            k_properties = KProperties("", key, "", "", "", "", "", "")
            k_properties = k_properties.__dict__
            k_json = (json_cell, k_type, k_properties, KAnalytics().__dict__)

        self.k_json.append(k_json)
        return self

#Json Definition and properties of content blocks
class KJson:
    def __init__(self, json_cell, k_type, cid=None, k_properties=None, k_analytics=None):
        self.cid = cid #id of json (if code)
        self.json_cell = json_cell #should encapsulate everything
        self.k_type = k_type #Code / Markdown (doesnt have properties)
        self.k_properties = k_properties
        self.k_analytics = k_analytics

#Elementary properties of KQ
class KProperties:
    def __init__(self, name, key, l_type, time_complexity, task_complexity, media_encoding=None, k_input=None, k_output=None):
        self.name = name #name / description
        self.key = key #sequence id within the content block
        self.media_encoding = media_encoding #tuple array for media [(timestamp, durations, source)] for markdown"
        self.k_input = None
        self.k_output = None
        self.l_type = l_type #[visual, auditory, tactile]
        self.time_complexity = time_complexity
        self.task_complexity = task_complexity

#Input parameters
class KInput:
    def __init__(self, input_type, input_source, input_values):
        self.input_type = input_type
        self.input_source = input_source
        self.input_values = input_values #Array
        
#Output parameters
class KOutput:
    def __init__(self, output_type, output_source, output_values, output_variance=None):
        self.output_type = output_type
        self.output_source = output_source
        self.output_values = output_values #Array
        self.output_variance = output_variance
        
#Agg quantified results over the user population
#todo tbd
class KAnalytics:
    def __init__(self):
        pass
