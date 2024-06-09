from django.shortcuts import render
from rest_framework import viewsets,generics,permissions,status
from api.models import UserProfile,Task,Attendence
from api.serializers import UserProfileSerializers,TaskSerializers,AttendenceSerializers,UserSignupSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from api.permissions import IsSuppervisor,IsIntern

# Create your views here.
class UserProfileViewsets(viewsets.ModelViewSet):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializers
    

class TaskViewsets(viewsets.ModelViewSet):
        queryset=Task.objects.all()
        serializer_class=TaskSerializers
        

        def get_permissions(self):
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                self.permission_classes = [IsAuthenticated, IsSuppervisor]
            else:
                self.permission_classes = [IsAuthenticated]
            return super().get_permissions()

        @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])
        def task_complete(self,request,pk=None):
            if request.user.role!="intern":
                raise PermissionDenied('only intern can mark task as complected')
            
            task=self.get_object()
            task.complected=True
            task.submitted_time=timezone.now()
            task.save()
            return Response({'status':'task is complected'},status=status.HTTP_200_OK)

class AttendenceViewsets(viewsets.ModelViewSet):
    queryset=Attendence.objects.all()
    serializer_class=AttendenceSerializers
    # permission_classes=[IsAuthenticated]


class AssignTaskView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    permission_classes = [IsAuthenticated,IsSuppervisor]

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsIntern])
    def mark_attendance(self, request):
        data = {
            'user': request.user.id,
            'date': timezone.now().date(),
            'entry_time': timezone.now(),
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Attendance marked'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if self.request.user.role != 'supervisor':
            raise Exception.PermissionDenied('Only supervisors can assign tasks')
        serializer.save()

class signupAPIview(APIView): 
    serializer_class = UserSignupSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh = RefreshToken.for_user(user)

            response_data= {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':serializer.data,
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class signoutapiview(APIView):
    def post (self,request,format=None):
        token=request.META['HTTP_AUTHORIZATION']
        print(token)
           
        return Response( status=status.HTTP_400_BAD_REQUEST)    


            



