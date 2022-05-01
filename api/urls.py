from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('assignment/', include('api.assignment.urls')),
    path('exam/', include('api.exam.urls'))
]
