from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
import jwt
import datetime
from .models import User, Organization, Role, Member
from .serializers import UserSerializer, OrganizationSerializer, RoleSerializer, MemberSerializer
from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

@api_view(['POST'])
def sign_in(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user:
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, settings.SECRET_KEY, algorithm='HS256')
        return Response({'access_token': token})
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def sign_up(request):
    email = request.data.get('email')
    password = make_password(request.data.get('password'))
    org_name = request.data.get('org_name')

    user = User.objects.create(email=email, password=password)
    organization = Organization.objects.create(name=org_name)
    role = Role.objects.create(name='owner', org=organization)
    Member.objects.create(user=user, org=organization, role=role)

    return Response({'message': 'User and organization created successfully'})

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    new_password = make_password(request.data.get('new_password'))
    User.objects.filter(email=email).update(password=new_password)
    return Response({'message': 'Password updated successfully'})

@api_view(['POST'])
def invite_member(request):
    email = request.data.get('email')
    org_id = request.data.get('org_id')
    role_name = request.data.get('role')
    
    user = User.objects.create(email=email, password=make_password('temporary'))
    org = Organization.objects.get(id=org_id)
    role = Role.objects.create(name=role_name, org=org)
    Member.objects.create(user=user, org=org, role=role)
    
    return Response({'message': 'Member invited successfully'})

@api_view(['POST'])
def delete_member(request):
    user_id = request.data.get('user_id')
    org_id = request.data.get('org_id')
    
    Member.objects.filter(user_id=user_id, org_id=org_id).delete()
    
    return Response({'message': 'Member deleted successfully'})

@api_view(['POST'])
def update_member_role(request):
    user_id = request.data.get('user_id')
    org_id = request.data.get('org_id')
    new_role = request.data.get('new_role')
    
    member = Member.objects.get(user_id=user_id, org_id=org_id)
    role = Role.objects.create(name=new_role, org=member.org)
    member.role = role
    member.save()
    
    return Response({'message': 'Member role updated successfully'})
