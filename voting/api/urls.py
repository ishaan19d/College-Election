from django.urls import path
from .views import NominateView , NominationListView, CandidateDetailView, NominationApprovalView, PresidentVoteView, VicePresidentVoteView, GSCultural, GSSports, GSTechnical

urlpatterns = [
    path('nominate/', NominateView.as_view(), name='nominate'),

    path('nomination-list/', NominationListView.as_view(), name='nominated-candidate-list'),
    path('nomination/<str:roll_number>/', CandidateDetailView.as_view(), name='candidate-detail'),

    path('nomination-status/<str:roll_number>/', NominationApprovalView.as_view(), name='query-nomination'),

    path('president-vote/', PresidentVoteView.as_view(), name='president-vote'),
    path('vice-president-vote/', VicePresidentVoteView.as_view(), name='vice-president-vote'),
    path('gs-cultural-vote/', GSCultural.as_view(), name='gs-cultural-vote'),
    path('gs-sports-vote/', GSSports.as_view(), name='gs-sports-vote'),
    path('gs-technical-vote/', GSTechnical.as_view(), name='gs-technical-vote'),
]