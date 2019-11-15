from rest_framework import serializers
from ...core.serializers import LearningModelSerializer
from .models import KqJsons, KqClone, SessionDetails, GDTemplateTracker, ScaffoldJsons


class KqJsonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = KqJsons
        fields = ('__all__')


class SessionDetailsSerializer(LearningModelSerializer):

    class Meta:
        model = SessionDetails
        fields = ('__all__')


class KqCloneSerailizer(LearningModelSerializer):

    class Meta:
        model = KqClone
        fields = ('__all__')


class GDTemplateTrackerSerializer(LearningModelSerializer):

    class Meta:
        model = GDTemplateTracker
        fields = ('__all__')

class ScaffoldJsonsSerializer(LearningModelSerializer):

    class Meta:
        model = ScaffoldJsons
        fields = ('__all__')
        