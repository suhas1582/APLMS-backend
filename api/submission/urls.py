from rest_framework import routers
from .views import SubmissionViewSet

router = routers.SimpleRouter()
router.register('', SubmissionViewSet)
urlpatterns = router.urls
