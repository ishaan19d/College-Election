from rest_framework.response import Response
from rest_framework import status
from account.models import Student, PollingOfficer
from voting.models import ContestingCandidate, Vote
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import ContestingCandidateSerializer, ContestingCandidateListSerializer, ResultSerializer
from .utils import sign_vote_count, verify_vote_count, generate_keys
private_key, public_key = generate_keys()

class NominateView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        student_type = decoded_token.payload.get('student_type')
        if not email or not student_type:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can nominate themselves.'}, status=status.HTTP_400_BAD_REQUEST)

        if ContestingCandidate.objects.filter(candidate=student).exists():
            return Response({'error': 'You have already nominated yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        position = request.data.get('position')
        description = request.data.get('description')
        manifesto = request.data.get('manifesto')

        if position == 'General Secretary - Welfare Board' and student_type != 'PhD':
            return Response({'error': 'Only PhD students can nominate themselves for General Secretary - Welfare Board.'}, status=status.HTTP_400_BAD_REQUEST)

        ContestingCandidate.objects.create(
            candidate=student,
            position=position,
            description=description,
            manifesto=manifesto,
            nomination_approved=None
        )
        return Response({'message': 'You have successfully nominated yourself.'}, status=status.HTTP_201_CREATED)

class NominationListView(APIView):
    def get(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = Student.objects.filter(email=email).first()
        polling_officer = PollingOfficer.objects.filter(email=email).first()
        
        if not student and not polling_officer:
            return Response({'error': 'Only students and polling officers can view the nomination list.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            candidates = ContestingCandidate.objects.order_by('position')
            serialized_candidates = ContestingCandidateListSerializer(candidates, many=True)
            return Response(serialized_candidates.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CandidateDetailView(APIView):
    def get(self, request, roll_number):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = Student.objects.filter(email=email).first()
        polling_officer = PollingOfficer.objects.filter(email=email).first()
        
        if not student and not polling_officer:
            return Response({'error': 'Only students and polling officers can view the nomination detail.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=roll_number)
            serialized_candidate = ContestingCandidateSerializer(candidate)
            return Response(serialized_candidate.data, status=status.HTTP_200_OK)
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class NominationApprovalView(APIView):
    def patch(self, request, roll_number):
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=roll_number)
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        polling_officer = PollingOfficer.objects.filter(email=email).first()
        if not polling_officer:
            return Response({'error': 'Only polling officers can approve nominations.'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_approved = request.data.get('is_approved')
        if is_approved is not None:
            candidate.is_approved = is_approved
            candidate.save()
        
        return Response({'message': 'Candidate\'s nomination updated.'}, status=status.HTTP_200_OK)

class PresidentVoteView(APIView):
    def patch(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can vote.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Vote.objects.filter(voter=student, position='President').exists():
            return Response({'error': 'You have already voted for President.'}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate_roll_number = request.data.get('candidate_roll_number')
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=candidate_roll_number, position='President')
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        Vote.objects.create(voter=student, position='President')
        
        candidate.vote_count += 1
        candidate.save()
        return Response({'message': 'You have successfully voted.'}, status=status.HTTP_201_CREATED)
    
class VicePresidentVoteView(APIView):
    def patch(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can vote.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Vote.objects.filter(voter=student, position='Vice President').exists():
            return Response({'error': 'You have already voted for Vice President.'}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate_roll_number = request.data.get('candidate_roll_number')
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=candidate_roll_number, position='Vice President')
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        Vote.objects.create(voter=student, position='Vice President')
        
        candidate.vote_count += 1
        candidate.save()
        return Response({'message': 'You have successfully voted.'}, status=status.HTTP_201_CREATED)

class GSCultural(APIView):
    def patch(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can vote.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Vote.objects.filter(voter=student, position='General Secretary - Cultural Board').exists():
            return Response({'error': 'You have already voted for General Secretary - Cultural Board.'}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate_roll_number = request.data.get('candidate_roll_number')
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=candidate_roll_number, position='General Secretary - Cultural Board')
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not verify_vote_count(candidate.vote_count, candidate.vote_count_signature, public_key):
            return Response({'error': 'Unauthorized tampering with the vote count has been detected.'}, status=status.HTTP_400_BAD_REQUEST)
        
        Vote.objects.create(voter=student, position='General Secretary - Cultural Board')
        candidate.vote_count += 1
        candidate.vote_count_signature = sign_vote_count(candidate.vote_count, private_key)
        candidate.save()
        return Response({'message': 'You have successfully voted.'}, status=status.HTTP_201_CREATED)
    
class GSTechnical(APIView):
    def patch(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can vote.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Vote.objects.filter(voter=student, position='General Secretary - Technical Board').exists():
            return Response({'error': 'You have already voted for General Secretary - Technical Board.'}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate_roll_number = request.data.get('candidate_roll_number')
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=candidate_roll_number, position='General Secretary - Technical Board')
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        Vote.objects.create(voter=student, position='General Secretary - Technical Board')
        
        candidate.vote_count += 1
        candidate.save()
        return Response({'message': 'You have successfully voted.'}, status=status.HTTP_201_CREATED)
    
class GSSports(APIView):
    def patch(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can vote.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Vote.objects.filter(voter=student, position='General Secretary - Sports Board').exists():
            return Response({'error': 'You have already voted for General Secretary - Sports Board.'}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate_roll_number = request.data.get('candidate_roll_number')
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=candidate_roll_number, position='General Secretary - Sports Board')
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        Vote.objects.create(voter=student, position='General Secretary - Sports Board')
        
        candidate.vote_count += 1
        candidate.save()
        return Response({'message': 'You have successfully voted.'}, status=status.HTTP_201_CREATED)
    
class GSWelfare(APIView):
    def patch(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()
        if not student:
            return Response({'error': 'Only students can vote.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Vote.objects.filter(voter=student, position='General Secretary - Welfare Board').exists():
            return Response({'error': 'You have already voted for General Secretary - Welfare Board.'}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate_roll_number = request.data.get('candidate_roll_number')
        try:
            candidate = ContestingCandidate.objects.get(candidate__roll_number=candidate_roll_number, position='General Secretary - Welfare Board')
        except ContestingCandidate.DoesNotExist:
            return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        Vote.objects.create(voter=student, position='General Secretary - Welfare Board')
        
        candidate.vote_count += 1
        candidate.save()
        return Response({'message': 'You have successfully voted.'}, status=status.HTTP_201_CREATED)

POSITIONS = ['President', 'Vice President', 'General Secretary - Cultural Board', 'General Secretary - Technical Board', 'General Secretary - Sports Board', 'General Secretary - Welfare Board']
class Results(APIView):
    def get(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            candidates = ContestingCandidate.objects.order_by('position', '-vote_count')
            result = {}
            for position in POSITIONS:
                position_candidates = candidates.filter(position=position)
                serialized_candidates = ResultSerializer(position_candidates, many=True)
                result[position] = serialized_candidates.data
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)