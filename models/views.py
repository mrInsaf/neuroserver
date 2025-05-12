from rest_framework import viewsets
from .models import GeneratedModel
from .serializers import GeneratedModelSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .nerual_network import generate_model
from .models import GeneratedModel


class GeneratedModelViewSet(viewsets.ModelViewSet):
    queryset = GeneratedModel.objects.all()
    serializer_class = GeneratedModelSerializer



@api_view(['POST'])
def generate_model_view(request):
    input_data = request.data.get('input')
    result = generate_model(input_data)
    generated_model = GeneratedModel.objects.create(name="Generated Model", file=result)
    return Response({"model": generated_model.id, "file": result})
