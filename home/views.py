from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Person,Company,employee
from home.serializer import PersonSerializer,RegisterSerializer,LoginSerializer,CompanySerializer,EmpolyeeSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BaseAuthentication,TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action

class LoginAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                "status":False,
                "message": serializer.errors
            },status.HTTP_400_BAD_REQUEST)
        
        user =  authenticate(username = serializer.data["username"], password =  serializer.data["password"])

        if not user:
            return Response({
                "status":False,
                "message": "invalid credentials"
            },status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"status":True, "message":"user login", "token":str(token)},status=status.HTTP_201_CREATED)


class RegisterAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                "status":False,
                "message": serializer.errors
            },status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({"status":True, "message":"user crested"},status=status.HTTP_201_CREATED)



# Create your views here.
@api_view(["GET","POST"])
def index(request):
    courses = {
        "course":"Python",
        "learn":["Flask","django","tornado","FastApi"],
        "course_provider":"Scaler"
    }
    if request.method == "GET":
        print(request.GET.get("search"))
        print("You Hit the Get Method")
        return Response(courses)
    
    elif request.method == "POST":
        data = request.data
        print("*********")
        print(data["age"])
        print("*********")
        print("You Hit the Post Method")
        return Response(courses)
    
    else:
        data = request.data
        print(data)
        json_response = {
            "name":"Scaler",
            "courses":["C++","Python"],
            "method":"POST"
        }
    
    return Response(json_response) 

class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    http_method_names = ["get","post"]

    def list(self, request):
        search = request.GET.get("search")
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        serializer =  PersonSerializer(queryset, many=True)
        return Response({"status":200, "data": serializer.data}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["GET"])
    def send_mail_to_person(self ,request, pk):
        obj = Person.objects.get(pk = pk)
        serializer = PersonSerializer(obj)
        return Response({
            "status":True,
            "message":"email sent succesfully",
            "data": serializer.data
        })
    

class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            objs = Person.objects.filter(color__isnull = False)
            page = request.GET.get("page",1)
            page_size = 3
            paginator = Paginator(objs, page_size)
            serializer = PersonSerializer(paginator.page(page), many = True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response({
                "status":False,
                "message": "Invalid page"
            })
        
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data["id"])
        serializer = PersonSerializer(obj,data = data, partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id= data["id"])
        obj.delete()
        return Response({"message":"Person is Delete"})



@api_view(["GET","POST","PUT","PATCH","DELETE"])
def person(request):
    if request.method == "GET":
        objs = Person.objects.filter(color__isnull = False)
        serializer = PersonSerializer(objs, many = True)
        serializer_context={
            "request":(request),
        }
        context = serializer_context
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == "PUT":
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id = data["id"])
        serializer = PersonSerializer(obj,data = data, partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id= data["id"])
        obj.delete()
        return Response({"message":"Person is Delete"})


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = employee.objects.all()
    serializer_class = EmpolyeeSerializer