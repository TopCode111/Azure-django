from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework import viewsets


class LearningModelViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    pagination_class = (None)

    def get_serializer_context(self):
        context = super(LearningModelViewSet, self).get_serializer_context()

        if self.request.user.is_superuser:
            context['table'] = None
        elif not hasattr(self.request.user, 'table'):
            raise PermissionDenied()
        else:
            context['table'] = self.request.user.table
        return context
