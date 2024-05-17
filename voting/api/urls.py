from django.urls import path
from .views import NominateView , NominationListViewP, CandidateDetailView

urlpatterns = [
    path('nominate/', NominateView.as_view(), name='nominate'),

    path('nomination-list/', NominationListViewP.as_view(), name='nominated-candidate-list'),
    path('nomination/<str:roll_number>/', CandidateDetailView.as_view(), name='candidate-detail'),

    
]