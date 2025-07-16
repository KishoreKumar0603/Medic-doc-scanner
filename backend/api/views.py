from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import process_medical_document

class DocumentOCRView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        
        # Save uploaded file temporarily
        with open('temp_image.jpg', 'wb+') as temp:
            for chunk in file_obj.chunks():
                temp.write(chunk)

        # Process the document
        result = process_medical_document('temp_image.jpg')

        return Response(result)
