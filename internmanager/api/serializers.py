from rest_framework import serializers
from api.models import UserProfile,Task,Attendence
from django.contrib.auth import get_user_model



class UserProfileSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=UserProfile
        fields=['id', 'username','email','role']

class TaskSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Task
        fields = ['id','title','assigned_to','task_given_time','submitted_time','completed']

class AttendenceSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Attendence
        fields=['id','Name','date','Entry_time','Exit_time']
        
User=get_user_model()
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,write_only=True)
    password1 = serializers.CharField(required=True,write_only=True)
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password',
            'password1'
        ]
    extra_kwargs ={
        'password':{'write_only':True},
        'password1':{'write_only':True},
    }   
    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError("Both passwords must be the same")
        return data
    def create(self, validated_data):
        validated_data.pop('password1')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user