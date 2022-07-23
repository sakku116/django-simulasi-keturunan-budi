from django.urls import path
from . import views

urlpatterns = [
    path('anak-budi/', views.index),
    path('cucu-budi/', views.cucuBudi),
    path('bibi-dari/<str:nama>', views.bibiDari),
    path('paman-dari/<str:nama>', views.pamanDari),
    path('sepupu-dari/<str:nama>', views.sepupuDari),
    path('orang/<str:nama_or_id>', views.orang),
    path('orang/', views.orang),
    path('test/', views.test)
]