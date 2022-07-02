from django.urls import path
# from django.conf.urls import url
from .views import *
# import re as r

urlpatterns = [
    path('pdf_gen/',pdf_generator,name="pdf_generator"),
    path('pdf_gen2/',gen_pdf,name="getPDF"),
]

