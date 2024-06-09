from django.urls import path,include
from rest_framework import routers
from api.views import UserProfileViewsets,TaskViewsets,AttendenceViewsets,AssignTaskView,signoutapiview,AttendenceViewsets
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from api.views import signupAPIview


schema_view=get_schema_view(
    openapi.Info(
        title="INTERN_TASK API",
        default_version='v1',
        description="API documentation for intern task",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@intern_task.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,    
    permission_classes=(permissions.AllowAny,),
)

router= routers.DefaultRouter()
router.register(r'userprofile',UserProfileViewsets )
router.register('task', TaskViewsets)
router.register('attendence',AttendenceViewsets)
urlpatterns = [
    path('',include(router.urls)),
    path('tasks/<int:pk>/assign/', AssignTaskView.as_view(), name='assign-task'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('signin/', TokenObtainPairView.as_view(), name='signin'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', signupAPIview.as_view()),
    path('signout/', signoutapiview.as_view(), name='signin'),
    path('tasks/<int:pk>/taskcomplete/', TaskViewsets.as_view({'post': 'task_complete'}), name='mark-completed'),
    path('attendance/mark/', AttendenceViewsets.as_view({'post': 'mark_attendance'}), name='mark-attendance'),
]