from .serializers import AssignmentSerializer
from .models import Assignment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
import json

# Create your views here.
class AssignmentViewSet(viewsets.ModelViewSet):

    model = Assignment
    queryset = Assignment.objects.all().order_by('pk')
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
    def get_by_class(self, request):
        request_body = json.loads(request.body)
        assignments_list = Assignment.objects.filter(
            standard__exact=request_body.get('standard', None),
            section__exact=request_body.get('section', None)
        )
        return Response({
            'assignment_list': assignments_list
        })