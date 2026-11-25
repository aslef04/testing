from django.shortcuts import render, redirect,get_object_or_404
from . models import RegisterModel,ProductAdding,RegisterViewModel
from . forms import ProductAddingForm,RegisterViewForm,UpdateForm


from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def service(request):
    return render(request,"service.html")

def connectus(request):
    return render(request,"connectus.html")

def products(request):
    if request.method == "POST":
        data = ProductAddingForm(request.POST, request.FILES)
        if data.is_valid():
            data.save()
            print("saved")  
    return render(request,"products.html")

def register(request):
    if request.method=="POST":
        image=request.FILES.get("profile")
        full_name=request.POST.get("full_name")
        user_name=request.POST.get("user_name")
        phone_number=request.POST.get("phone_number")
        gender=request.POST.get("gender")
        dob=request.POST.get("dob")
        email=request.POST.get("email")
        address=request.POST.get("address")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        mydata=RegisterModel(
            profile=image,
            full_name=full_name,
            user_name=user_name,
            phone_number=phone_number,
            gender=gender,
            dob=dob,
            email=email,
            address=address,
            password=password
        )
        mydata.save()
        print("saved")
        
    return render(request,"register.html")

def dashboard(request):
        values=[1,2,3,4,5,6,7,8,9,10] #this for testing (values) not in the dashboard only for testing purpose ,not want.
        mydata=RegisterModel.objects.all()
        form=RegisterViewModel.objects.all()
        return render(request,"dashboard.html",{"data":values,"mydata":mydata,"form":form})

def update(request, pk):

    data = RegisterModel.objects.get(id=pk)

    if request.method == "POST":
        if request.FILES.get("profile"):
            data.profile = request.FILES.get("profile")

        data.full_name = request.POST.get("full_name")
        data.user_name = request.POST.get("user_name")
        data.phone_number = request.POST.get("phone_number")
        data.gender = request.POST.get("gender")
        data.dob = request.POST.get("dob")
        data.email = request.POST.get("email")
        data.address = request.POST.get("address")

        if request.POST.get("password"):
            data.password = request.POST.get("password")

        data.save()
        print("saved")

    return render(request, "update.html", {"data": data})


def delete(request,jk):
    data=RegisterModel.objects.get(id=jk)
    if request.method =="POST":
        data.delete()
        return redirect("dashboard")
    return render(request, "delete.html")


def login_view(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")

        data = RegisterModel.objects.filter(user_name=name).first()
        if data and data.password == password:
            request.session['username']=data.user_name
            request.session['fullname']=data.full_name
            request.session['email']=data.email
            request.session['user_id']=data.id
            print(request.session.items())
            response = redirect("dashboard")
            response.set_cookie("username",data.user_name,max_age=60,expires=True)
            response.set_cookie("fullname",data.full_name,max_age=3600)
            return response

    return render(request,"login.html")


# def login_view(request):
#     if request.method == "POST":
#         name = request.POST.get("username")
#         password = request.POST.get("password")

#         data = RegisterModel.objects.filter(
#             user_name=name,
#             password=password
#         ).exists()

#         if data == True:
#             return redirect("dashboard")
#         else:
#             return render(request, "login.html", {
#                 "error": "Invalid username or password"
#             })

#     return render(request, "login.html")


def register_view(request):
    if request.method =="POST":
        form=RegisterViewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            print("saved")
            subject = "Registrartion Successfull"
            message = f"""
                    Hello {full_name},
                    Your registration has been completed successfully,

                    Thank you,
                    """
            send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
            messages.success(request, "Registrartion Successfull")        
    else:
        form = RegisterViewForm()
    return render(request,"register_view.html",{"form":form})


def update_list(request,jk):
    user = get_object_or_404(RegisterViewModel, id=jk)
    if request.method == "POST":
        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = UpdateForm(instance=user)
    return render(request,"update_list.html",{"data":form})


def profile(request):
    if not request.session.get("user_id"):
        return redirect("login")
    user = RegisterModel.objects.get(id = request.session.get("user_id"))
    return render(request,"profile.html",{"user":user})

def logout(request):
    response = redirect("login")
    response.delete_cookie("username")
    response.delete_cookie("fullname")
    return response



from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import StudentSerializer
from . models import Student
from rest_framework import status

class StudentList(APIView):
    def post(self,request):
        serializer = StudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        student = Student.objects.all()
        serializer = StudentSerializer(student,many = True)
        return Response(serializer.data)


class StudentDetail(APIView):
    def get_object(self,id):
        return get_object_or_404(Student,id=id)

    def get(self,request,id):
        stud = self.get_object(id)
        serializer = StudentSerializer(stud)
        return Response(serializer.data)    


    def put(self,request,id):
        stud = self.get_object(id)
        serializer = StudentSerializer(stud,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request,id):
            stud = self.get_object(id)
            serializer = StudentSerializer(stud,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,id):
        stud = Student.objects.get(id=id)
        stud.delete()
        return Response({"message":"Student deleted"}, status=status.HTTP_200_OK)