from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Exam
from .serializers import ExamSerializer
from rest_framework.permissions import IsAuthenticated
import json
from django.db.models import Q

# Create your views here.
class ExamViewSet(viewsets.ModelViewSet):

    model = Exam
    queryset = Exam.objects.all().order_by('id')
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def filter_by_criteria(self, request):
        criteria_query_mapping = {
            'standard': lambda standard: Q(standard__exact=standard),
            'section': lambda section: Q(section__exact=section),
            'exam_type': lambda exam_type: Q(exam_type__exact=exam_type)
        }
        request_body = json.loads(request.body)
        filter_query_array = []
        for key, value in request_body.items():
            if value['should_filter']:
                filter_query = criteria_query_mapping.get(key)(value['filter_value'])
                filter_query_array.append(filter_query)
        query = filter_query_array.pop()
        for filter_query in filter_query_array:
            query &= filter_query
        exam_list = Exam.objects.filter(query)
        serialized_exam_list = []
        for exam in exam_list:
            serialized_exam_list.append(ExamSerializer(exam).data)
        return Response(status=200, data=serialized_exam_list)