from api_backend.apps.apis.classes.kquant import KQuant

class User:
    """User class clones KQ and keeps track of the interaction between the User and KQ
    Further provides Aggregtation classes that aggregated interactions
    Attached to the topmost graph node

    Args:
    sid: user id

    Returns:
    Instantiated class

    """
    def __init__(self, sid):
        self.sid = sid
        self.l_permissions = None

        #all in relation to the individual node ids
        self.agg_subject_detail = [] #aggregates on KID
        self.agg_KQuant = [] #aggregates on CID
        self.KQuant = [] #lstrength / ltaskprogress / ltype / lsignals / adaptability


    def build_object(self, cid):
        l_type = LType()
        self.l_type = l_type.get_l_type()
        self.l_permissions = LPermissions()
        l_signals = LSignals()
        l_adaptability = LAdaptability()
        l_task_progress = LTaskProgress()
        l_strength = LStrength() #measures in both directions
        l_session = LSession()
        l_rating = LRating()
       

        #happens on the smallest unit / per cell -> cid 
        kq_clone = KQuantClone(cid, l_strength, l_signals, l_task_progress, l_type, l_adaptability, l_session, l_rating)
        self.KQuant.append(kq_clone)
        return self

    def build_agg_subject_detail(self):
        #DoStuff - return aggregated subject detail
        agg_subject_detail = None
        self.agg_subject_detail.append(agg_subject_detail)
        return self

    def build_agg_KQuant(self, cid):
        #DoStuff - return aggregated KQuant
        agg_kquant = None
        self.agg_KQuant.append(agg_kquant)
        return self

   

class Subject_Detail_Agg:
    def __init__(self, kquant_agg):
        self.kquant = kquant_agg
        self.agg_l_strength = None
        self.agg_task_progress = None
        self.agg_l_signals = None
        self.agg_l_type = None
        self.agg_l_adaptability = None
        self.agg_l_rating = None

    def build_agg_subject_detail(self):
        pass

class KQuantAgg:
    def __init__(self, cid, kquant):
        self.cid = cid
        self.kquant = kquant
        self.agg_l_strength = None
        self.agg_task_progress = None
        self.agg_l_signals = None
        self.agg_l_type = None
        self.agg_l_adaptability = None
        self.agg_session = None
        self.agg_rating = None

    def build_agg_KQuant(self):
        pass

class LSession:
    def __init__(self, start_time=None, stop_time=None):
        self.start_time = start_time
        self.stop_time = stop_time

class KQuantClone:
    def __init__(self,cid, l_strength, l_signals, l_progress_task, l_type, l_adaptability, l_session, l_rating):
        self.cid = cid
        self.l_strength = l_strength
        self.l_progress_task = l_progress_task
        self.l_signals = l_signals
        self.l_type = l_type
        self.l_adaptability = l_adaptability
        self.l_session = l_session
        self.l_rating = l_rating

        def get_kq_clone(self, sid):
            return self

#https://en.wikipedia.org/wiki/Learning_styles
#https://curiosity.com/topics/learning-styles-dont-actually-exist-curiosity?utm_source=podcast&utm_medium=social&utm_campaign=20190628learning
#TODO: Requires discussion
#one approach would be to figure out their weaknesses and improve them specifically on the weaknesses on a metalevel!!!!!!!!!
#What kind of learner type (categories) in relation to the tasks the learner managed
#the better he manages a (complex) task, the more we can assume the learner is of a certain type
class LType:
    def __init__(self, visual=None, auditory=None, tactile=None):
        self.visual = visual
        self.auditory = auditory
        self.tactile = tactile

    def get_l_type(self):
        return self

    def get_l_type_agg(self):
        return self

#Todo how to determine what is a strenght or a weakness in a binary sense (in relation to others?)
#We can use this data for serving tasks / we can combine a strong with a weak topic/task
#Learners strengths (categories)
class LStrength:
    def __init__(self, cid=None, topic_id=None, evaluation_score=None, time_diff=None, time_absolute=None, l_strength=None):
        self.cid = cid
        self.topic_id = topic_id #final node on the skeleton graph
        self.evaluation_score = evaluation_score #result he achieved on a task
        self.time_diff = time_diff #time_diff relative to defined time complexity
        self.time_absolute = time_absolute #how long did it take him to work on a task
        self.l_strength= l_strength #combination of time, evaluation score and other factors

    def get_l_strength(self):
        return self

    def get_l_strength_agg(self):
        return self

#What is the learners progress in varying units, ideally we want to see progress and high complexity
class LSubjectProgress:
    def __init__(self, progess=None, complexity=None, kid=None, evaluation_score=None):
        self.kid = kid #final node on the skeleton graph
        self.progress = progress
        self.complexity = complexity
        self.evaluation_score = evaluation_score
    
    def get_l_subject_progress(self):
        return self

    def get_l_subject_progress_agg(self):
        return self
    
class LTaskProgress:
    def __init__(self, progess=None, complexity=None, topic_id=None, evaluation_score=None):
        self.topic_id = topic_id #content node
        self.progress = progress
        self.complexity = complexity
        self.evaluation_score = evaluation_score
        self.interactions = []
        
    def get_l_task_progress(self):
        return self

    def get_l_task_progress_agg(self):
        return self

#How well does the learner adapt to challenges
#todo open question
class LAdaptability:
    def __init__(self):
        pass

    def get_l_adaptability(self, sid):
        return self

    def get_l_tadaptability_agg(self):
        return self

class LRating:
    def __init__(self):
        pass

    def get_l_adaptability(self, sid):
        return self

    def get_l_tadaptability_agg(self):
        return self

#Premissions for User
#https://optlearning.atlassian.net/browse/LEAR-64?atlOrigin=eyJpIjoiZGVjOGNlM2ZiMmI0NDUwMmE2NDMxMTk4YWQyZWRmMTIiLCJwIjoiaiJ9
class LPermissions:
     def __init__(self, role=None, created_by=None, created=None, last_login=None, gdrive_token=None):
        self.role = role
        self.gdrive_token = gdrive_token
        self.created_by = created_by
        self.created = created
        self.last_login = last_login

#Signals we catch of the learner measuring exhaustion / attention / in relation to tasks and time etc
#The learners "focus curve"
class LSignals:
    def __init__(self, attention=None, exhaustion=None, speed=None, rel_time=None, abs_time=None, time_of_day=None):
        self.attention = attention
        self.exhaustion = exhaustion
        self.speed = speed #in relation to time complexity in relative terms
        self.rel_time = rel_time #time as in rel (to learning)
        self.abs_time = abs_time #time as in absolute (to a session)
        self.time_of_day = time_of_day #time as in absolute (during the day)

    def get_l_signals(self, sid):
        return self

    def get_l_signals_agg(self):
        return self
