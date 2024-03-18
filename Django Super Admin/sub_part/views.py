from django.shortcuts import redirect, render,get_object_or_404
from .models import couponcodes,orderslists,ownerslists,planlists,todolists
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Avg, Sum
import easygui
import datetime
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.views.generic import View
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.urls import reverse
# Create your views here.







def landing_page(request):
    return render(request,'landing_page.html')

@login_required(login_url='login')
def orders_render_pdf_view(request,*args,**kwargs):
    pk=kwargs.get('pk')
    owner=get_object_or_404(ownerslists,pk=pk)

    template_path = 'pdf.html'
    context = {'owner': owner}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="order_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def home(request):
    return render(request, 'home.html') 

def login(request):
    if request.method == "POST":
        # check if a user exists
        # with the username and password
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        try:
            userNotActive=User.objects.get(username=request.POST['username'])
        except:
            userNotActive=None
        if user is not None:
            auth.login(request, user)
            return redirect(index)
        elif userNotActive is not None and userNotActive.check_password(request.POST['password']):
            return render(request, 'home.html', {'error': "Activate your account"})
        else:
            return render(request, 'home.html', {'error': "Invalid Login credentials."})
    else:
        return render(request, 'home.html')

def signup(request):
    if request.method == "POST":
        # to create a user
        if request.POST['password'] == request.POST['passwordagain']:
            # both the passwords matched
            # now check if a previous user exists
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'register.html', {'error': "Username Has Already Been Taken"})
            except User.DoesNotExist:
                user = User.objects.create_user(username= request.POST['username'],password= request.POST['password'],first_name= request.POST['first_name'],last_name= request.POST['last_name'],email= request.POST['email'])
                # this line cal login the user right no
                # auth.login(request, user)
                
                user.is_active=False
                user.save()
                auth.logout(request)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link=reverse('activate',kwargs={
                    'uidb64':uidb64,'token':token_generator.make_token(user)
                })
                activate_url = 'http://'+domain+link
                email_subject='Activate your account - Worksales'
                email_body='Hi User - '+user.username+\
                '\nPlease use this link to activate your account\n'+activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'donotreply@example.com',
                    [request.POST['email']],
                )
                email.send(fail_silently=False)
                easygui.msgbox("User created and conformation mail has been sent")
                return redirect(home)
        else:
            return render(request, 'register.html', {'error': "Passwords Don't Match"})
    else:
        return render(request, 'register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        #request.user.is_active=True
        pk= urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=pk)
        user.is_active=True
        user.save()
        easygui.msgbox("Your account has been activated \nYou can login now.")
        return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect(landing_page)

@login_required(login_url='login')
def index(request):
    owners=ownerslists.objects.filter(date__range=[datetime.datetime.today()- timedelta(days=30), datetime.datetime.today()])
    sales_month=ownerslists.objects.filter(date__range=[datetime.datetime.today()- timedelta(days=30), datetime.datetime.today()]).aggregate(salesMonth=Sum('price'))
    sales_total=ownerslists.objects.aggregate(salesTotal=Sum('price'))
    todolistarray=todolists.objects.all()
    sales_array=[]
    sales_date=[]
    owners_array=ownerslists.objects.order_by('date')
    for i in owners_array:
        sales_array.append(i.price)
        sales_date.append(i.date.strftime('%Y-%b-%d'))
    return render(request,'index.html',{'sales_date':sales_date,'sales_array':sales_array,'todolistarray':todolistarray,'u':request.user,'count_total':ownerslists.objects.count(),'count_month':owners.count(),'sales_total':sales_total['salesTotal'],'sales_month':sales_month['salesMonth']})

@login_required(login_url='login')
def todo_add(request):
    if request.method=='POST':
        if(request.POST.get('sentense')):
            temp=todolists()
            temp.sentense=request.POST.get('sentense')
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            return redirect("index")
    return render(request,'todo_add.html')

@login_required(login_url='login')
def delete_todo(request,id):
    temp=todolists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/index")

@login_required(login_url='login')
def coupons_edit(request,id):
    temp = couponcodes.objects.get(id=id)
    return render(request,'coupons_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def owners_edit(request,id):
    temp = ownerslists.objects.get(id=id)
    return render(request,'owners_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def coupons_update(request,id):
    if request.method == 'POST':
        couponcodes.objects.filter(id = id).update(name=request.POST['name'],code=request.POST['code'],discount=request.POST['discount'],limit=request.POST['limit'],used=request.POST['used'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../coupons")  
    temp=couponcodes.objects.all()
    return render(request,'coupons.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def owners_update(request,id):
    if request.method == 'POST':
        ownerslists.objects.filter(id = id).update(name=request.POST['name'],email=request.POST['email'],total_users=request.POST['total_users'],plan_name=request.POST['plan_name'],price=request.POST['price'],status=request.POST['status'],date=request.POST['date'],expiry_date=request.POST['expiry_date'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../owners")  
    temp=ownerslists.objects.all()
    return render(request,'owners.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def coupons(request):
    if request.method=='POST':
        if(request.POST.get('name') and request.POST.get('discount') and request.POST.get('limit') and request.POST.get('code') and request.POST.get('used')):
            temp=couponcodes()
            temp.name=request.POST.get('name')
            temp.discount=request.POST.get('discount')
            temp.limit=request.POST.get('limit')
            temp.code=request.POST.get('code')
            temp.used=request.POST.get('used')
            temp.save()
            couponcodearray=couponcodes.objects.all()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            return render(request,'coupons.html',{'couponcodearray': couponcodearray,'u':request.user} )
        else:
            couponcodearray=couponcodes.objects.all()
            return render(request,'coupons.html',{'couponcodearray': couponcodearray,'u':request.user} )

    couponcodearray=couponcodes.objects.all()
    return render(request,'coupons.html',{'couponcodearray': couponcodearray,'u':request.user} )

@login_required(login_url='login')
def orders(request):
    if request.method=='POST':
        if(request.POST.get('order_id') and request.POST.get('name') and request.POST.get('plan_name') and request.POST.get('price') and request.POST.get('status') and request.POST.get('date')):
            temp=orderslists()
            temp.name=request.POST.get('name')
            temp.order_id=request.POST.get('order_id')
            temp.plan_name=request.POST.get('plan_name')
            temp.price=request.POST.get('price')
            temp.status=request.POST.get('status')
            temp.date=request.POST.get('date')
            temp.save()
            orderslistarray=orderslists.objects.all()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            return render(request,'orders.html',{'orderslistarray': orderslistarray,'u':request.user})
        else:
            orderslistarray=orderslists.objects.all()
            return render(request,'orders.html',{'orderslistarray': orderslistarray,'u':request.user})

    orderslistarray=ownerslists.objects.all()
    return render(request,'orders.html',{'orderslistarray': orderslistarray,'u':request.user})

@login_required(login_url='login')
def owners(request):
    if request.method=='POST':
        if(request.POST.get('name') and request.POST.get('email') and request.POST.get('total_users') and request.POST.get('plan_name') and request.POST.get('date') and request.POST.get('price') and request.POST.get('status') and request.POST.get('expiry_date') and request.POST.get('username') and request.POST.get('password') ):
            temp=ownerslists()
            temp.name=request.POST.get('name')
            temp.email=request.POST.get('email')
            temp.total_users=request.POST.get('total_users')
            temp.plan_name=request.POST.get('plan_name')
            temp.date=request.POST.get('date')
            temp.price=request.POST.get('price')
            temp.status=request.POST.get('status')
            temp.expiry_date=request.POST.get('expiry_date')
            temp.save()
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
            user.is_active=False
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link=reverse('activate',kwargs={
                'uidb64':uidb64,'token':token_generator.make_token(user)
            })
            activate_url = 'http://'+domain+link
            email_subject='Activate your account - Worksales'
            email_body='Hi User - '+user.username+\
            '\nPlease use this link to activate your account\n'+activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'donotreply@example.com',
                [request.POST['email']],
            )
            email.send(fail_silently=False)
            ownerslistarray=ownerslists.objects.all()
            easygui.msgbox("User Created and Conformation mail has been sent to given mail id\nYour data has been added successfully!...","Worksales")
            return render(request,'owners.html',{'ownerslistarray': ownerslistarray,'u':request.user})
        elif(request.POST.get('name') and request.POST.get('email') and request.POST.get('total_users') and request.POST.get('plan_name') and request.POST.get('date') and request.POST.get('price') and request.POST.get('status') and request.POST.get('expiry_date') ):
            temp=ownerslists()
            temp.name=request.POST.get('name')
            temp.email=request.POST.get('email')
            temp.total_users=request.POST.get('total_users')
            temp.plan_name=request.POST.get('plan_name')
            temp.date=request.POST.get('date')
            temp.price=request.POST.get('price')
            temp.status=request.POST.get('status')
            temp.expiry_date=request.POST.get('expiry_date')
            temp.save()
            ownerslistarray=ownerslists.objects.all()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            return render(request,'owners.html',{'ownerslistarray': ownerslistarray,'u':request.user})
        else:
            ownerslistarray=ownerslists.objects.all()
            return render(request,'owners.html',{'ownerslistarray': ownerslistarray,'u':request.user})

    ownerslistarray=ownerslists.objects.all()
    return render(request,'owners.html',{'ownerslistarray': ownerslistarray,'u':request.user})

@login_required(login_url='login')
def plans(request):
    if request.method=='POST':
        if(request.POST.get('colour') and request.POST.get('price') and request.POST.get('name') and request.POST.get('users') and request.POST.get('vendors')):
            temp=planlists()
            temp.colour=request.POST.get('colour')
            temp.price=request.POST.get('price')
            temp.name=request.POST.get('name')
            temp.users=request.POST.get('users')
            temp.customers=request.POST.get('customers')
            temp.vendors=request.POST.get('vendors')
            temp.save()
            planlistarray=planlists.objects.all()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            return render(request,'plans.html',{'planlistarray': planlistarray,'u':request.user})
        else:
            planlistarray=planlists.objects.all()
            return render(request,'plans.html',{'planlistarray': planlistarray,'u':request.user})

    planlistarray=planlists.objects.all()
    return render(request,'plans.html',{'planlistarray': planlistarray,'u':request.user})

@login_required(login_url='login')
def plans_delete(request,id):
    plans=planlists.objects.get(id=id)
    plans.delete()
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/plans")

@login_required(login_url='login')
def delete_coupons(request, id):  
    temp=couponcodes.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/coupons")

@login_required(login_url='login')
def delete_owners(request, id):  
    temp=ownerslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/owners")

