from rest_framework import viewsets
from rest_framework.response import Response
from .models import Team, User, Activity, Workout, Leaderboard
from .serializers import TeamSerializer, UserSerializer, ActivitySerializer, WorkoutSerializer, LeaderboardSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
