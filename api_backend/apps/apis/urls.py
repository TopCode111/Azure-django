from django.urls import path, include
from rest_framework_nested import routers

from . import views as v

router = routers.DefaultRouter()

router.register(r'notebooks', v.NotebooksViewSet)
router.register(r'tasks', v.TasksViewSet)
router.register(r'pathfinders', v.PathfindersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('notebooks/user/<sid>', v.UserAllNotebooksView.as_view()),
    path('notebooks/<nid>/users/<sid>', v.UserNotebookView.as_view()),
    path('tasks/rating/<cid>', v.SubmitCheckoutView.as_view()),
    path('signals', v.UserSignalsView.as_view()),
    path('aggregations/<type>/<cid>/users/<sid>', v.UserKQAggregatesViewSet.as_view()),
    path('aggregations/<type>/<kid>/users/<sid>', v.UserSubjectDetailViewSet.as_view()),
    path('aggregations/<type>/<cid>', v.AllUserKQAggregateViewSet.as_view()),
    path('pathfinders/down/<kid>', v.DownNavigationView.as_view()),
    path('pathfinders/up/<kid>', v.UpNavigationView.as_view()),
]
