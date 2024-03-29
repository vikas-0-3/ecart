from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import CreateUserForm, LeadForm, ProductForm, ContactForm, TaskForm, ContractForm, SalesForm, DeliveryboyForm, ProfileForm, SocialForm, ClaimForm
from .models import Lead, Product, Contact, Task, Contract, Sales, Deliveryboy, Logs, Profile, Documents, Knowledge, Social, Quoteitem, Quotations, Leave, Claim, Room, Message, Events
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
import time

date = datetime.date.today()

from django.contrib.auth.models import User

#email 
from django.conf import settings
from django.core.mail import send_mail



# Create your views here.


def dashboard(request):
    return render(request, "dashboard.html", {})
    
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created for'+form.cleaned_data.get('username'))
                return redirect('login')

        return render(request, "register.html", {'form' : form})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                user = User.objects.get(id=request.user.id)
                profile = Profile.objects.get(userid=request.user.id)
                obj2 = Logs(userid=user, description="Login at  "+str(time.ctime()), profile_id=profile)
                obj2.save()
                
                return redirect('home')
            else:
                context["message"] = "Username or Password is incorrect"
        return render(request, "login.html", context)

def logoutuser(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(userid=request.user.id)
    obj2 = Logs(userid=user, description="Logout at  "+str(time.ctime()), profile_id=profile)
    obj2.save()
    logout(request)
    
    return redirect('login')

@login_required(login_url='login')
def home(request):
    context = {}

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip

    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["countlead"] = Lead.objects.count()
    context["countcontact"] = Contact.objects.count()
    context["countproducts"] = Product.objects.count()
    context["countcontracts"] = Contract.objects.count()
    context["countsales"] = Sales.objects.count()
    context["countdeliveryboy"] = Deliveryboy.objects.count()

    context["contractdata"] = Contract.objects.all().order_by('id')[:6]
    ttl = Task.objects.filter(addedby=request.user.id).count()
    if(ttl):
        context["totaltask"] = ttl
        context["activecount"] = int(Task.objects.filter(status="Active", addedby=request.user.id).count()/ttl*100)
        context["pendingcount"] = int(Task.objects.filter(status="Pending", addedby=request.user.id).count()/ttl*100)
        context["completecount"] = int(Task.objects.filter(status="Completed", addedby=request.user.id).count()/ttl*100)
        context["inactivecount"] = int(Task.objects.filter(status="Inactive", addedby=request.user.id).count()/ttl*100)
    else:
        context["totaltask"] = 0 
        context["activecount"] = 0 
        context["pendingcount"] = 0 
        context["completecount"] = 0 
        context["inactivecount"] = 0 


    context["logsdata"] = Logs.objects.all().order_by('-id')[:10]
    context["socialdata"] = Social.objects.get(id=1)




    return render(request, "User/index.html", context)


@login_required(login_url='login')
def email(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()

    context["maillist"] = User.objects.all()

    if request.method == 'POST':
        to = request.POST.get('to')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
    
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to, ]
        send_mail( subject, message, email_from, recipient_list )
        context["message"] = "Email is sent to {}".format(to)

    
    return render(request, "User/email/email.html", context)



@login_required(login_url='login')
def logs(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["logsdata"] = Logs.objects.all().order_by('-id')
    
    return render(request, "User/logs/logs.html", context)


@login_required(login_url='login')
def socialhandle(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["socialdata"] = Social.objects.all()
    
    obj = get_object_or_404(Social, id = '1')
    form = SocialForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated Social Handle", profile_id_id=profileid.id)
        obj2.save()
        return redirect('socialhandle')
    else:
        print(form.errors)
    
    return render(request, "User/settings/social.html", context)


@login_required(login_url='login')
def documents(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Documents.objects.all()
    if request.method == 'POST':
        doc = request.POST

        title = doc['title']
        files = request.FILES.getlist('document')
        user = User.objects.get(id=request.user.id)

        for file in files:
            docdata = Documents.objects.create(
                title=title,
                addedby=user,
                document=file,
            )

        profileid = Profile.objects.get(userid_id=request.user.id)
        
        obj2 = Logs(userid=user, description="Added a new Document with id "+str(Documents.objects.latest('id').id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('documents')
    
    return render(request, "User/documents/document.html", context)


@login_required(login_url='login')
def deletedoc(request, id):
    obj = get_object_or_404(Documents, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Document with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('documents')


@login_required(login_url='login')
def deleteknowledge(request, id):
    obj = get_object_or_404(Knowledge, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Knowledge base with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('knowledge')

    

@login_required(login_url='login')
def knowledge(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Knowledge.objects.all()
    if request.method == 'POST':
        doc = request.POST

        title = doc['title']
        files = request.FILES.getlist('document')
        user = User.objects.get(id=request.user.id)

        for file in files:
            docdata = Knowledge.objects.create(
                title=title,
                addedby=user,
                document=file,
            )

        profileid = Profile.objects.get(userid_id=request.user.id)
        
        obj2 = Logs(userid=user, description="Added new files in Knowledge base with id "+str(Documents.objects.latest('id').id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('knowledge')

    
    return render(request, "User/documents/knowledge.html", context)


@login_required(login_url='login')
def userprofiles(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Profile.objects.all()
    
    return render(request, "User/settings/userprofiles.html", context)


@login_required(login_url='login')
def adduser(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()


    if request.method == 'POST':
        User.objects.create_user(
            email=request.POST['user_email'],
            password=request.POST['user_phone'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            username=request.POST['first_name']
        )
        latest_id = User.objects.latest('id').id

        Profile.objects.create(
            user_image = request.FILES['user_image'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            user_email=request.POST['user_email'],
            user_phone=request.POST['user_phone'],
            dob=request.POST['dob'],
            points=request.POST['points'],
            facebook = request.POST['facebook'],
            instagram = request.POST['instagram'],
            linkedin = request.POST['linkedin'],
            github = request.POST['github'],

            about = request.POST['about'],
            address = request.POST['address'],
            id_proof = request.FILES['id_proof'],
            designation = request.POST['designation'],
            working_from = request.POST['working_from'],
            working_to = request.POST['working_to'],
            updated_at = "",
            gender = request.POST['gender'],
            project = request.POST['project'],
            userid_id = latest_id,
            
        )
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="added a new user", profile_id_id=profileid.id)
        obj2.save()

        return redirect('userprofiles')

    return render(request, "User/settings/adduser.html", context)

@login_required(login_url='login')
def edituserprofile(request, id):
    context ={}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()

    obj = get_object_or_404(Profile, id = id)

    
    form = ProfileForm(request.POST or None, request.FILES or None, instance = obj)
    if form.is_valid():
        form.save()
        

        User.objects.filter(id=getUserRegisteredId(id).userid_id).update(
            email=request.POST['user_email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            username=request.POST['first_name']
        )

        

        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated a Profile", profile_id_id=profileid.id)
        obj2.save()
        return redirect('userprofiles')
    else:
        print(form.errors)

    context["data"] = form


    return render(request, "User/settings/edituserprofile.html", context)


def getUserRegisteredId(id):
    return get_object_or_404(Profile, id = id)



@login_required(login_url='login')
def profile(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
 
    dataqr = get_object_or_404(Profile, userid = request.user.id)
    context["data"] = dataqr
        
    context["profileqr"] = "\nFull Name : "+str(dataqr.first_name )+str(dataqr.last_name)+"\nEmail : "+str(dataqr.user_email)+"\nPhone : "+str(dataqr.user_phone)+"\nGender : "+str(dataqr.gender)+"\nDOB : "+str(dataqr.dob)+"\nAbout : "+str(dataqr.about)+"\nDesignation : "+str(dataqr.designation)+"\nWorking Hours : "+str(dataqr.working_from)+"-"+str(dataqr.working_to)+"\nAddress : "+str(dataqr.address)+"\nFacebook : "+str(dataqr.facebook)+"\nInstagram : "+str(dataqr.instagram)+"\nLinked In : "+str(dataqr.linkedin)+"\nGithub : "+str(dataqr.github)
    return render(request, "User/profile/profile.html", context)

@login_required(login_url='login')
def editprofile(request):
    context ={}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()

    obj = get_object_or_404(Profile, userid = request.user.id)
    form = ProfileForm(request.POST or None, request.FILES or None, instance = obj)
    if form.is_valid():
        form.save()

        User.objects.filter(id=request.user.id).update(
            email=request.POST['user_email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            username=request.POST['first_name']
        )


        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated their Profile", profile_id_id=profileid.id)
        obj2.save()
        return redirect('profile')
    else:
        print(form.errors)

    context["data"] = form

    return render(request, "User/profile/editprofile.html", context)


@login_required(login_url='login')
def deleteuser(request, id):
    obj = get_object_or_404(User, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a User with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('userprofiles')





#-------------------------------------------------  over -----------------------------------
                            ############## sales #######
                            ############## sales #######
                            ############## sales #######        
                            ############## sales #######
                            ############## sales #######
# --------------------------       Lead operations view, add, delete , edit  ----------------------------




@login_required(login_url='login')
def sales(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Sales.objects.all()
    return render(request, "User/sales/sales.html", context)



@login_required(login_url='login')
def editsale(request, id):
    context ={}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["qdata"] = Quotations.objects.all()
    context["deliveryboydata"] = Deliveryboy.objects.all()
  
    obj = get_object_or_404(Sales, id = id)
    form = SalesForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated a Sale with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('sales')

    context["data"] = form
    return render(request, "User/sales/editsale.html", context)


@login_required(login_url='login')
def addsale(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["qdata"] = Quotations.objects.all()
    context["deliveryboydata"] = Deliveryboy.objects.all()

    form = SalesForm(request.POST or None)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Added a Sale with id "+str(Sales.objects.latest('id').id), profile_id_id=profileid.id)
        obj2.save()
        return redirect("sales")
    else:
        print(form.errors)

    return render(request, "User/sales/addsale.html", context)

@login_required(login_url='login')
def deletesale(request, id):
    obj = get_object_or_404(Sales, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Sale with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('sales')



#-------------------------------------------------  over -----------------------------------
                            #         ######       #        ###### #
                            #         #           # #       #       #
                            #         ######     #   #      #        #
                            #         #         #######     #       #
                            #######   ######   #       #    #######
# --------------------------       Lead operations view, add, delete , edit  ----------------------------


@login_required(login_url='login')
def lead(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Lead.objects.all()

    return render(request, "User/lead/lead.html", context)

@login_required(login_url='login')
def editlead(request, id):
    context ={}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
  
    obj = get_object_or_404(Lead, id = id)
    form = LeadForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated a Lead with id "+str(Lead.objects.latest('id').id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('lead')

    context["data"] = form
    arr = ["Open", "Contacted", "Qualified", "Unqualified"]
    context["opt"] = arr
    return render(request, "User/lead/editlead.html", context)


@login_required(login_url='login')
def addlead(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    form = LeadForm(request.POST or None)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Added a Lead with id"+str(Lead.objects.latest('id').id), profile_id_id=profileid.id)
        obj2.save()
        return redirect("lead")

    return render(request, "User/lead/addlead.html", context)

@login_required(login_url='login')
def deletelead(request, id):
    obj = get_object_or_404(Lead, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Lead with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('lead')

    
#------------------------------------------------- Lead over -----------------------------------


                                                ####
                                                ####
                                                ####

# --------------------------       products operations view, add, delete , edit  ----------------------------


@login_required(login_url='login')
def products(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Product.objects.all()
    return render(request, "User/product/products.html", context)


@login_required(login_url='login')
def addproduct(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            profileid = Profile.objects.get(userid_id=request.user.id)
            user = User.objects.get(id=request.user.id)
            obj2 = Logs(userid=user, description="Added a Product with id "+str(Product.objects.latest('id').id), profile_id_id=profileid.id)
            obj2.save()
            request.session.error = 'Product added successfully';
            return redirect('products')
        else:
            print(form.errors)


    return render(request, "User/product/addproduct.html", context)

@login_required(login_url='login')
def deleteproduct(request, id):
    obj = get_object_or_404(Product, id = id)
    profileid = Profile.objects.get(userid_id=request.user.id)

    if request.method =="GET":

        obj.delete()
      
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Product with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        
    return redirect('products')


@login_required(login_url='login')
def editproduct(request, id):
    context ={}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    obj = get_object_or_404(Product, id = id)
    form = ProductForm(request.POST or None , request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated a Product with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('products')
    else:
        print(form.errors)


    context["data"] = form
    arr = ["Food", "Software", "Hardware", "Transport", "Clothes", "Others"]
    context["opt"] = arr
    return render(request, "User/product/editproduct.html", context)


#------------------------------------------------- product over ---------------------------------------------------------------------

                                 #######       # #        #         #    #########        #         #######   #########  
                                #            #     #      #  #      #        #           # #       #              #      
                               #            #       #     #    #    #        #          #   #     #               #      
                                #            #     #      #      #  #        #         #######     #              #      
                                 #######       # #        #         #        #        #       #     #######       #      

# --------------------------       Contact operations view, add, delete , edit  ----------------------------------------------

@login_required(login_url='login')
def contact(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Contact.objects.all()
    return render(request, "User/contact/contact.html", context)


# def contact(request):

#     return render(request, "User/contact/contact.html")


@login_required(login_url='login')
def addcontact(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            profileid = Profile.objects.get(userid_id=request.user.id)
            user = User.objects.get(id=request.user.id)
            obj2 = Logs(userid=user, description="Added a Contact with contact id "+str(Contact.objects.latest('id').id), profile_id_id=profileid.id)
            obj2.save()

            return redirect('contact')
    return render(request, "User/contact/addcontact.html",context)

@login_required(login_url='login')
def deletecontact(request, id):
    obj = get_object_or_404(Contact, id = id)
    if request.method =="GET":
        obj.delete()

        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Contact with contact id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        
    return redirect('contact')


@login_required(login_url='login')
def editcontact(request, id):
    context ={}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    obj = get_object_or_404(Contact, id = id)
    form = ContactForm(request.POST or None , request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated a Contact with contact id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('contact')

    context["data"] = form
    return render(request, "User/contact/editcontact.html", context)



@login_required(login_url='login')
def contactqrcode(request, id):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    dataqr = get_object_or_404(Contact, id = id)

    context["data"] = "Person Name : "+str(dataqr.full_name)+"\nPerson Email : "+str(dataqr.user_email)+"\nPerson Phone : "+str(dataqr.user_phone)+"\nCompany Name : "+str(dataqr.company_name)+"\nCompany Location : "+str(dataqr.company_location)
    
    return render(request, "User/contact/contactqrcode.html", context)


#-------------------------------------------------  over -----------------------------------
                       ###########       #        #######   #  #
                            #           # #      #          # #
                            #          #   #      ######    ##
                            #         #######           #   # #
                            #        #       #   #######    #   #
# --------------------------       Lead operations view, add, delete , edit  ----------------------------




@login_required(login_url='login')
def tasks(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Task.objects.filter(addedby=request.user.id).all()
    ttl = Task.objects.filter(addedby=request.user.id).count()
    if(ttl):
        context["totaltask"] = ttl
        context["activecount"] = int(Task.objects.filter(status="Active", addedby=request.user.id).count()/ttl*100)
        context["pendingcount"] = int(Task.objects.filter(status="Pending", addedby=request.user.id).count()/ttl*100)
        context["completecount"] = int(Task.objects.filter(status="Completed", addedby=request.user.id).count()/ttl*100)
        context["inactivecount"] = int(Task.objects.filter(status="Inactive", addedby=request.user.id).count()/ttl*100)
    else:
        context["totaltask"] = 0 
        context["activecount"] = 0 
        context["pendingcount"] = 0 
        context["completecount"] = 0 
        context["inactivecount"] = 0 

    current_week = date.today().isocalendar()[1]
    today = datetime.date.today()

    context["curretweek"] = Task.objects.filter(created_at__week=current_week, status="Completed", addedby=request.user.id).count()
    context["curretweektotal"] = Task.objects.filter(created_at__week=current_week, addedby=request.user.id).count()
    context["currentweekpercentage"] = int(context["curretweek"] / context["curretweektotal"]*100) if context["curretweektotal"] != 0 else 0

    context["pastweek"] = Task.objects.filter(created_at__week=current_week-1, status="Completed", addedby=request.user.id).count()
    context["pastweektotal"] = Task.objects.filter(created_at__week=current_week-1, addedby=request.user.id).count()
    context["pastweekpercentage"] = int(context["pastweek"] / context["pastweektotal"]*100) if context["pastweektotal"] != 0 else 0

    context["currentmonth"] = Task.objects.filter(created_at__year=today.year, created_at__month=today.month, status="Completed", addedby=request.user.id).count()
    context["currentmonthtotal"] = Task.objects.filter(created_at__year=today.year, created_at__month=today.month, addedby=request.user.id).count()
    context["currentmonthpercentage"] = int(context["currentmonth"] / context["currentmonthtotal"]*100) if context["currentmonthtotal"] != 0 else 0

    context["pastmonth"] = Task.objects.filter(created_at__year=today.year, created_at__month=today.month-1, status="Completed", addedby=request.user.id).count()
    context["pastmonthtotal"] = Task.objects.filter(created_at__year=today.year, created_at__month=today.month-1, addedby=request.user.id).count()
    context["pastmonthpercentage"] = int(context["pastmonth"] / context["pastmonthtotal"]*100) if context["pastmonthtotal"] != 0 else 0

    context["currentyear"] = Task.objects.filter(created_at__year=today.year, status="Completed", addedby=request.user.id).count()
    context["currentyeartotal"] = Task.objects.filter(created_at__year=today.year, addedby=request.user.id).count()
    context["currentyearpercentage"] = int(context["currentyear"] / context["currentyeartotal"]*100) if context["currentyeartotal"] != 0 else 0
   


    return render(request, "User/tasks/tasks.html", context)


    
@login_required(login_url='login')
def addtask(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    arr = ["Active", "Completed", "Pending", "Inactive"]
    context["opt"] = arr
    if request.method == 'POST':
        # request.addedby = request.user.id
        form = TaskForm(request.POST, request.FILES)
        
  
        if form.is_valid():
            form.save()
            profileid = Profile.objects.get(userid_id=request.user.id)
            user = User.objects.get(id=request.user.id)
            obj2 = Logs(userid=user, description="Added a Task with id "+str(Task.objects.latest('id').id), profile_id_id=profileid.id)
            obj2.save()
            return redirect('tasks')
        else:
            print(form.errors)

    return render(request, "User/tasks/addtask.html", context)

@login_required(login_url='login')
def deletetask(request, id):
    obj = get_object_or_404(Task, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Task with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('tasks')

@login_required(login_url='login')
def edittask(request, id):
    context ={}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    arr = ["Active", "Completed", "Pending", "Inactive"]
    context["opt"] = arr
    obj = get_object_or_404(Task, id = id)
    form = TaskForm(request.POST or None , request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Update a Task with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('tasks')
    else:
        print(form.errors)

    context["data"] = form
    # context["dd"] = datetime.strptime(form.cleaned_data["deadline"], "%d-%b-%Y-%H:%M:%S")
    # print(dd)
    return render(request, "User/tasks/edittask.html", context)






#-------------------------------------------------  over -----------------------------------
                      #contract
                      #contract
                      #contract
                      #contract
# --------------------------       Lead operations view, add, delete , edit  ----------------------------









@login_required(login_url='login')
def contracts(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Contract.objects.all()
    return render(request, "User/contract/contracts.html", context)


@login_required(login_url='login')
def addcontract(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["customersdata"] = Contact.objects.all()
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            profileid = Profile.objects.get(userid_id=request.user.id)
            user = User.objects.get(id=request.user.id)
            obj2 = Logs(userid=user, description="Added a Contract with id "+str(Contract.objects.latest('id').id), profile_id_id=profileid.id)
            obj2.save()
            return redirect('contracts')
        else:
            print(form.errors)

    return render(request, "User/contract/addcontract.html", context)

@login_required(login_url='login')
def deletecontract(request, id):
    obj = get_object_or_404(Contract, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Contract with contract id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('contracts')

@login_required(login_url='login')
def editcontract(request, id):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["customersdata"] = Contact.objects.all()
    obj = get_object_or_404(Contract, id = id)
    form = ContractForm(request.POST or None , request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated a Contract with contract id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('contracts')
    else:
        print(form.errors)

    context["data"] = form
    return render(request, "User/contract/editcontract.html", context)





#------------------------------------------------- Lead over -----------------------------------


                                                #salesperson

# --------------------------       products operations view, add, delete , edit  ----------------------------


@login_required(login_url='login')
def deliveryboy(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Deliveryboy.objects.all()
    return render(request, "User/deliveryboy/deliveryboy.html", context)


@login_required(login_url='login')
def adddeliveryboy(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    
    if request.method == 'POST':
        form = DeliveryboyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            profileid = Profile.objects.get(userid_id=request.user.id)
            user = User.objects.get(id=request.user.id)
            obj2 = Logs(userid=user, description="Added a DeliveryBoy with id "+str(Deliveryboy.objects.latest('id').id), profile_id_id=profileid.id)
            obj2.save()
            return redirect('deliveryboy')
        else:
            print(form.errors)

    return render(request, "User/deliveryboy/adddeliveryboy.html", context)

    



@login_required(login_url='login')
def deletedeliveryboy(request, id):
    obj = get_object_or_404(Deliveryboy, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Deliveryboy with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('deliveryboy')



@login_required(login_url='login')
def editdeliveryboy(request, id):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["deliveryboydata"] = Deliveryboy.objects.all()
    obj = get_object_or_404(Deliveryboy, id = id)
    form = DeliveryboyForm(request.POST or None , request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated a DeliveryBoy with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('deliveryboy')
    else:
        print(form.errors)

    context["data"] = form
    return render(request, "User/deliveryboy/editdeliveryboy.html", context)



#--------------------------------------------------------------------------

                                #calander


#--------------------------------------------------------------------------


@login_required(login_url='login')
def calander(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()


    if request.method == 'POST':
        Events.objects.create(
                eventdate = request.POST['eventdate'],
                eventtitle = request.POST['title'],
                description = request.POST['description'],
                addedby = User.objects.get(id=request.user.id),
        )

        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Added a event with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
        return redirect('calander')



    return render(request, "User/calander/calander.html", context)





#--------------------------------------------------------------------------
                          # Quotations                                  
                          # Quotations                                            
                          # Quotations                  
                          # Quotations                  
#--------------------------------------------------------------------------


@login_required(login_url='login')
def quotation(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Quotations.objects.all()
    return render(request, "User/quotation/quotation.html", context)

@login_required(login_url='login')
def addquotation(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["customers"] = Contact.objects.all()
    context["products"] = Product.objects.all()


    if request.method == 'POST':

        Quotations.objects.create(
                customer_name = request.POST['customer_name'],
                title = request.POST['title'],
                note = request.POST['note'],
                status = request.POST['status'],
                discount = request.POST['discount'],
                shipping = request.POST['shipping'],
                tax = request.POST['gst'],
                grand_total = request.POST['gtotal'],
                addedby = User.objects.get(id=request.user.id),
        )


        myid = Quotations.objects.latest('id').id


        product_code = request.POST.getlist('product_id[]')
        product_name = request.POST.getlist('product_name[]')
        product_price = request.POST.getlist('product_price[]')
        product_quantity = request.POST.getlist('product_quantity[]')
        product_total = request.POST.getlist('product_total[]')

        for i in range(0, len(product_code)):
            Quoteitem.objects.create(
                quotation_id = Quotations.objects.get(id=myid),
                product_code = product_code[i],
                product_name = product_name[i],
                product_price = product_price[i],
                product_quantity = product_quantity[i],
                product_total = product_total[i],
            )



        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Added a Quotation with id "+str(myid), profile_id_id=profileid.id)
        obj2.save()


  
        return redirect('quotation')


    return render(request, "User/quotation/addquotation.html", context)

@login_required(login_url='login')
def deletequotation(request, id):
    obj = get_object_or_404(Quotations, id = id)
    obj2 = get_object_or_404(Quoteitem, id = id)
    if request.method =="GET":
        obj.delete()
        obj2.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Task with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('tasks')

@login_required(login_url='login')
def viewquotation(request, id):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["quot"] = get_object_or_404(Quotations, id=id)
    context["quotitems"] = Quoteitem.objects.filter(quotation_id_id=id).all()
    return render(request, "User/quotation/viewquotation.html", context)


@login_required(login_url='login')
def leave(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Leave.objects.filter(addedby=request.user.id).all()

    if request.method == 'POST':
        Leave.objects.create(
                purpose = request.POST['purpose'],
                from_date = request.POST['from_date'],
                to_date = request.POST['to_date'],
                description = request.POST['description'],
                status = "Pending",
                addedby = User.objects.get(id=request.user.id),
        )
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="apply for a Leave ", profile_id_id=profileid.id)
        obj2.save()

        return redirect('leave')
    return render(request, "User/leave/leave.html", context)


@login_required(login_url='login')
def editleave(request, id):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    obj = get_object_or_404(Leave, id = id)
    context["leavedata"] = obj
    if request.method == "POST":
        Leave.objects.filter(pk=id).update(
            purpose=request.POST['purpose'],
            from_date = request.POST['from_date'], 
            to_date = request.POST['to_date'], 
            description = request.POST['description']
        )

        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated their leave", profile_id_id=profileid.id)
        obj2.save()
        return redirect('leave')

    return render(request, "User/leave/editleave.html", context)

@login_required(login_url='login')
def deleteleave(request, id):
    obj = get_object_or_404(Leave, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Leave with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('leave')


@login_required(login_url='login')
def manageleave(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Leave.objects.all()
    return render(request, "User/leave/manageleave.html", context)


@login_required(login_url='login')
def declineleave(request, id):
    Leave.objects.filter(pk=id).update(status = "Rejected",)
    profileid = Profile.objects.get(userid_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    obj2 = Logs(userid=user, description="Rejected a leave with id"+str(id), profile_id_id=profileid.id)
    obj2.save()
    return redirect('manageleave')


@login_required(login_url='login')
def acceptleave(request, id):
    Leave.objects.filter(pk=id).update(status = "Accepted",)
    profileid = Profile.objects.get(userid_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    obj2 = Logs(userid=user, description="Accepted a leave with id"+str(id), profile_id_id=profileid.id)
    obj2.save()
    return redirect('manageleave')



@login_required(login_url='login')
def claim(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Claim.objects.filter(addedby=request.user.id).all()

    if request.method == 'POST':
        Claim.objects.create(
                purpose = request.POST['purpose'],
                title = request.POST['title'],
                from_date = request.POST['from_date'],
                to_date = request.POST['to_date'],
                amount = request.POST['amount'],
                description = request.POST['description'],
                status = "Pending",
                addedby = User.objects.get(id=request.user.id),
        )
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="apply for a Claim ", profile_id_id=profileid.id)
        obj2.save()

        return redirect('claim')
    return render(request, "User/claim/claim.html", context)

@login_required(login_url='login')
def deleteclaim(request, id):
    obj = get_object_or_404(Claim, id = id)
    if request.method =="GET":
        obj.delete()
        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Deleted a Claim with id "+str(id), profile_id_id=profileid.id)
        obj2.save()
    return redirect('claim')


@login_required(login_url='login')
def editclaim(request, id):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    obj = get_object_or_404(Claim, id = id)
    context["claimdata"] = obj
    if request.method == "POST":
        Claim.objects.filter(pk=id).update(
                purpose = request.POST['purpose'],
                title = request.POST['title'],
                from_date = request.POST['from_date'],
                to_date = request.POST['to_date'],
                amount = request.POST['amount'],
                description = request.POST['description'],
        )

        profileid = Profile.objects.get(userid_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        obj2 = Logs(userid=user, description="Updated their claim", profile_id_id=profileid.id)
        obj2.save()
        return redirect('claim')

    return render(request, "User/claim/editclaim.html", context)

@login_required(login_url='login')
def manageclaim(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    context["data"] = Claim.objects.all()
    return render(request, "User/claim/manageclaim.html", context)

@login_required(login_url='login')
def declineclaim(request, id):
    Claim.objects.filter(pk=id).update(status = "Rejected",)
    profileid = Profile.objects.get(userid_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    obj2 = Logs(userid=user, description="Rejected a claim with id"+str(id), profile_id_id=profileid.id)
    obj2.save()
    return redirect('manageclaim')


@login_required(login_url='login')
def acceptclaim(request, id):
    Claim.objects.filter(pk=id).update(status = "Accepted",)
    profileid = Profile.objects.get(userid_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    obj2 = Logs(userid=user, description="Accepted a claim with id"+str(id), profile_id_id=profileid.id)
    obj2.save()
    return redirect('manageclaim')



##############################################3


############        chat        ###############

###############################################

@login_required(login_url='login')
def chat(request):
    context = {}
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context["ip_address"] = ip


    context["eventdata"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).all()
    context["eventcount"] = Events.objects.filter(addedby=request.user.id, eventdate=date.today()).count()
    # context["data"] = Leave.objects.all()
    return render(request, "Chats/chat.html", context)

@login_required(login_url='login')
def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = "discussionCorner"

    new_message = Message.objects.create(value=message, user=username, room=room_id, userid=request.user.id)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required(login_url='login')
def getMessages(request):
    messages = Message.objects.filter(room="discussionCorner")
    return JsonResponse({"messages":list(messages.values())})


@login_required(login_url='login')
def getMyEvents(request):
    myeventsdata = Events.objects.filter(addedby=request.user.id).all()
    return JsonResponse({"data":list(myeventsdata.values())})