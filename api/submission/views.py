from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
import json
from .models import Submission
from .serializers import SubmissionSerializer

# Create your views here.
class SubmissionViewSet(viewsets.ModelViewSet):

    model = Submission
    queryset = Submission.objects.all().order_by('id')
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def filter_by_criteria(self, request):
        request_body = json.loads(request.body)
        criteria_query_mapping = {
            'assignment_id': lambda assignment_id: Q(assignment_id__exact=assignment_id),
            'submitted_by': lambda submitted_by: Q(submitted_by__exact=submitted_by)
        }
        filter_query_array = []
        for key, value in request_body.items():
            if value["should_filter"]:
                filter_query = criteria_query_mapping.get(key)(value['filter_value'])
                filter_query_array.append(filter_query)
        query = filter_query_array.pop()
        for filter_query in filter_query_array:
            query &= filter_query
        submissions_list = Submission.objects.filter(query)
        serialized_submissions_list = []
        for submission in submissions_list:
            serialized_submissions_list.append(SubmissionSerializer(submission).data)
        
        return Response(status=200, data=serialized_submissions_list)
