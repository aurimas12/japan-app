from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import spacy

nlp = spacy.load("en_core_web_sm")

@api_view(['POST'])
def analyze_text(request):
    text = request.data.get("text", "")
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return Response({"entities": entities})