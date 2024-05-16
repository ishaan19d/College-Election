from rest_framework.response import Response
from rest_framework import status
from account.models import Student
from voting.models import ContestingCandidate
from rest_framework.views import APIView
from .permissions import IsStudentAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .serializers import ContestingCandidateSerializer, ContestingCandidateListSerializer
class NominateView(APIView):
    permission_classes = [IsStudentAuthenticated]
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except InvalidToken:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can nominate themselves.'}, status=status.HTTP_400_BAD_REQUEST)

        if ContestingCandidate.objects.filter(candidate=student).exists():
            return Response({'error': 'You have already nominated yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        position = request.data.get('position')
        por_description = request.data.get('por_description')
        manifesto = request.data.get('manifesto')

        ContestingCandidate.objects.create(
            candidate=student,
            position=position,
            por_description=por_description,
            manifesto=manifesto,
            is_approved=False
        )
        return Response({'message': 'You have successfully nominated yourself.'}, status=status.HTTP_201_CREATED)
    
class NominationListViewP(APIView):
    def get(self, request, post):
        try:
            if(post == 'p'):
                position = 'President'
            elif(post == 'vp'):
                position = 'Vice President'
            elif(post == 'gsc'):
                position = 'General Secretary - Cultural Board'
            elif(post == 'gst'):
                position = 'General Secretary - Technical Board'
            elif(post == 'gss'):
                position = 'General Secretary - Sports Board'
            else:
                return Response({'error': 'Invalid position.'}, status=status.HTTP_400_BAD_REQUEST)
            candidates = ContestingCandidate.objects.filter(position=position)
            serialized_candidates = ContestingCandidateListSerializer(candidates, many=True)
            return Response(serialized_candidates.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CandidateDetailView(APIView):
    def get(self, request, roll_number):
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=roll_number)
            serialized_candidate = ContestingCandidateSerializer(candidate)
            return Response(serialized_candidate.data, status=status.HTTP_200_OK)
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)