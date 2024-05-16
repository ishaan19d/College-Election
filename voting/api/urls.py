from django.urls import path
from .views import NominateView , NominationListViewP, CandidateDetailView

urlpatterns = [
    path('nominate/', NominateView.as_view(), name='nominate'),

    path('nomination-list/<str:post>/', NominationListViewP.as_view(), name='presidential'),
    # path('nomination-list/vp/', NominationListViewP.as_view(), name='presidential'),
    # path('nomination-list/gsc/', NominationListViewP.as_view(), name='presidential'),
    # path('nomination-list/gst/', NominationListViewP.as_view(), name='presidential'),
    # path('nomination-list/gss/', NominationListViewP.as_view(), name='presidential'),
    path('nomination/<str:roll_number>/', CandidateDetailView.as_view(), name='candidate-detail'),
]