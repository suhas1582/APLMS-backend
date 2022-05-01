from rest_framework import routers
from .views import ExamViewSet

router = routers.SimpleRouter()
router.register('', ExamViewSet)
urlpatterns = router.urls
