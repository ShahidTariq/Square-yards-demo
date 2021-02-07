from django.urls import path, include

urlpatterns = [
    path('', include('demo.urls'), name='home')
]
