from django.shortcuts import redirect, render,get_object_or_404
from .models import userslists,roleslists,customerlists,vendorlists,productslists,categorieslists,taxlists,saleslists,stock_analysislists,customer_analysislists,tax_reportslists,expenseslists,exp_categorieslists,todolists
import easygui
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Sum
import datetime
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
def sales_render_pdf_view(request,*args,**kwargs):
    pk=kwargs.get('pk')
    sale =get_object_or_404(saleslists,pk=pk)

    template_path = 'pdf.html'
    context = {'sale': sale}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
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
    sales_total=saleslists.objects.aggregate(salesTotal=Sum('total'))
    sales_month=saleslists.objects.filter(date__range=[datetime.datetime.today()- timedelta(days=30), datetime.datetime.today()]).aggregate(salesMonth=Sum('total'))
    expenses_total=expenseslists.objects.aggregate(expensesTotal=Sum('amount'))
    expenses_month=expenseslists.objects.filter(expense_date__range=[datetime.datetime.today()- timedelta(days=30), datetime.datetime.today()]).aggregate(expensesMonth=Sum('amount'))
    todolistarray=todolists.objects.all()
    sales_array=[]
    sales_date=[]
    sales_list_array=saleslists.objects.order_by('date')
    for i in sales_list_array:
        sales_array.append(i.total)
        sales_date.append(i.date.strftime('%Y-%b-%d'))
    expenses_array=[]
    expenses_date=[]
    expenses_list_array=expenseslists.objects.order_by('expense_date')
    for i in expenses_list_array:
        expenses_array.append(i.amount)
        expenses_date.append(i.expense_date.strftime('%Y-%b-%d'))
    return render(request,'index.html',{'sales_date':sales_date,'sales_array':sales_array,'expenses_date':expenses_date,'expenses_array':expenses_array,'todolistarray':todolistarray,'u': request.user,'sales_total':sales_total['salesTotal'],'sales_month':sales_month['salesMonth'],'expenses_total':expenses_total['expensesTotal'],'expenses_month':expenses_month['expensesMonth']})

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
def categories(request):
    if request.method=='POST':
        if(request.POST.get('name')):
            temp=categorieslists()
            temp.name=request.POST.get('name')
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            categorieslistarray=categorieslists.objects.all()
            return render(request,'categories.html',{'categorieslistarray': categorieslistarray,'u':request.user})
        else:
            categorieslistarray=categorieslists.objects.all()
            return render(request,'categories.html',{'categorieslistarray': categorieslistarray,'u':request.user})
    categorieslistarray=categorieslists.objects.all()
    return render(request,'categories.html',{'categorieslistarray': categorieslistarray,'u':request.user})

@login_required(login_url='login')
def customer_analysis(request):
    customer_analysis_customer_listarray=customerlists.objects.all()
    for i in customer_analysis_customer_listarray:
        totalsales=saleslists.objects.filter(customer_name=i.name).aggregate(number=Sum('total'))
        totalamount=saleslists.objects.filter(customer_name=i.name).aggregate(number=Sum('items_sold'))
        i.total_sales=totalsales['number']
        i.total=totalamount['number']
    customer_analysis_vendor_listarray=vendorlists.objects.all()
    for i in customer_analysis_vendor_listarray:
        totalsales=saleslists.objects.filter(customer_name=i.name).aggregate(number=Sum('total'))
        totalamount=saleslists.objects.filter(customer_name=i.name).aggregate(number=Sum('items_sold'))
        i.total_sales=totalsales['number']
        i.total=totalamount['number']
    return render(request,'customer_analysis.html',{'customer_analysis_vendor_listarray': customer_analysis_vendor_listarray,'customer_analysis_customer_listarray': customer_analysis_customer_listarray,'u':request.user})

@login_required(login_url='login')
def customer(request):
    if request.method=='POST':
        if(request.POST.get('name') and request.POST.get('email') and request.POST.get('date') and request.POST.get('phone_number')):
            temp=customerlists()
            temp.name=request.POST.get('name')
            temp.email=request.POST.get('email')
            temp.date=request.POST.get('date')
            temp.phone_number=request.POST.get('phone_number')
            temp.total=0
            temp.total_sales=0
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            customerlistarray=customerlists.objects.all()
            return render(request,'customer.html',{'customerlistarray': customerlistarray,'u':request.user})
        else:
            customerlistarray=customerlists.objects.all()
            return render(request,'customer.html',{'customerlistarray': customerlistarray,'u':request.user})

    customerlistarray=customerlists.objects.all()
    return render(request,'customer.html',{'customerlistarray': customerlistarray,'u':request.user})

@login_required(login_url='login')
def exp_categories(request):
    if request.method=='POST':
        if(request.POST.get('name')):
            temp=exp_categorieslists()
            temp.name=request.POST.get('name')
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            exp_categorieslistarray=exp_categorieslists.objects.all()
            return render(request,'exp_categories.html',{'exp_categorieslistarray': exp_categorieslistarray,'u':request.user})
        else:
            exp_categorieslistarray=exp_categorieslists.objects.all()
            return render(request,'exp_categories.html',{'exp_categorieslistarray': exp_categorieslistarray,'u':request.user})

    exp_categorieslistarray=exp_categorieslists.objects.all()
    return render(request,'exp_categories.html',{'exp_categorieslistarray': exp_categorieslistarray,'u':request.user})

@login_required(login_url='login')
def expences(request):
    if request.method=='POST':
        if(request.POST.get('branch') and request.POST.get('expense_date') and request.POST.get('expense_category') and request.POST.get('amount')):
            temp=expenseslists()
            temp.expense_date=request.POST.get('expense_date')
            temp.expense_category=request.POST.get('expense_category')
            temp.branch=request.POST.get('branch')
            temp.amount=request.POST.get('amount')
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            expenseslistarray=expenseslists.objects.all()
            return render(request,'expences.html',{'expenseslistarray': expenseslistarray,'u':request.user})
        else:
            expenseslistarray=expenseslists.objects.all()
            return render(request,'expences.html',{'expenseslistarray': expenseslistarray,'u':request.user})

    expenseslistarray=expenseslists.objects.all()
    return render(request,'expences.html',{'expenseslistarray': expenseslistarray,'u':request.user})

@login_required(login_url='login')
def products(request):
    if request.method=='POST':
        if(request.POST.get('name') and request.POST.get('category') and request.POST.get('quantity') and request.POST.get('brand')):
            temp=productslists()
            temp.name=request.POST.get('name')
            temp.category=request.POST.get('category')
            temp.quantity=request.POST.get('quantity')
            temp.brand=request.POST.get('brand')
            temp.stock=0
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            productslistarray=productslists.objects.all()
            return render(request,'products.html',{'productslistarray': productslistarray,'u':request.user})
        else:
            productslistarray=productslists.objects.all()
            return render(request,'products.html',{'productslistarray': productslistarray,'u':request.user})

    productslistarray=productslists.objects.all()
    return render(request,'products.html',{'productslistarray': productslistarray,'u':request.user})

@login_required(login_url='login')
def profile(request):
    if request.method=='POST':
        if(request.POST.get('username') and request.POST.get('password') and request.POST.get('new_password')):
            if (request.user.check_password(request.POST.get('password'))==True):
                request.user.set_password(request.POST['new_password'])
                request.user.save()
                easygui.msgbox("Password Changed")
                return render(request,'profile.html',{'u': request.user})
            else:
                easygui.msgbox("Wrong Current Password")
                return render(request,'profile.html',{'u': request.user})
        elif(request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('email')):
            request.user.email=request.POST.get('email')
            request.user.first_name=request.POST.get('first_name')
            request.user.last_name=request.POST.get('last_name')
            request.user.save()
            easygui.msgbox("Details Changed")
            return render(request,'profile.html',{'u': request.user})
        else:
            return render(request,'profile.html',{'u': request.user})
    return render(request,'profile.html',{'u': request.user})

@login_required(login_url='login')
def roles(request):
    if request.method=='POST':
        if(request.POST.get('role') and request.POST.get('Profile_box') and request.POST.get('Vendor_box') and request.POST.get('Customer_box') and request.POST.get('user_box')):
            temp=roleslists()
            temp.role=request.POST.get('role')
            temp.Profile_box=request.POST.get('Profile_box')
            temp.Vendor_box=request.POST.get('Vendor_box')
            temp.Customer_box=request.POST.get('Customer_box')
            temp.user_box=request.POST.get('user_box')
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            roleslistarray=roleslists.objects.all()
            return render(request,'roles.html',{'roleslistarray': roleslistarray,'u':request.user})
        else:
            roleslistarray=roleslists.objects.all()
            return render(request,'roles.html',{'roleslistarray': roleslistarray,'u':request.user})

    roleslistarray=roleslists.objects.all()
    return render(request,'roles.html',{'roleslistarray': roleslistarray,'u':request.user})

@login_required(login_url='login')
def sales_list(request):
    if request.method=='POST':
        if(request.POST.get('invoice_id') and request.POST.get('date') and request.POST.get('sold_to') and request.POST.get('items_sold') and request.POST.get('total') and request.POST.get('payment_status') and request.POST.get('name') and request.POST.get('customer_name') and request.POST.get('tax')):
            temp=saleslists()
            temp.invoice_id=request.POST.get('invoice_id')
            temp.date=request.POST.get('date')
            temp.sold_to=request.POST.get('sold_to')
            temp.items_sold=request.POST.get('items_sold')
            temp.total=request.POST.get('total')
            temp.payment_status=request.POST.get('payment_status')
            temp.name=request.POST.get('name')
            temp.customer_name=request.POST.get('customer_name')
            temp.tax=request.POST.get('tax')
            temp.tax_amount=0
            temp.grand_total=0
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            saleslistarray=saleslists.objects.all()
            return render(request,'sales_list.html',{'saleslistarray': saleslistarray,'u':request.user})
        else:
            saleslistarray=saleslists.objects.all()
            return render(request,'sales_list.html',{'saleslistarray': saleslistarray,'u':request.user})

    saleslistarray=saleslists.objects.all()
    return render(request,'sales_list.html',{'saleslistarray': saleslistarray,'u':request.user})

@login_required(login_url='login')
def sales(request):
    return render(request,'sales.html',{'u': request.user})

@login_required(login_url='login')
def stock_analysis(request):
    stock_analysislistarray=productslists.objects.all()
    saleslistarray=saleslists.objects.all()
    countarray=[productslists.objects.count()]
    for j in countarray:
        for i in stock_analysislistarray:
            count=saleslists.objects.filter(name=i.name).aggregate(number=Sum('items_sold'))
            # countarray[j]=(i.quantity-count['number'])
            # j=j+1
            # easygui.msgbox(i.quantity-count['number'])
            # easygui.msgbox(countarray)
            # i.stock=(i.quantity-count['number'])
            if (count['number']==None):
                i.stock=i.quantity
            else:
                i.stock=(i.quantity-count['number'])
    return render(request,'stock_analysis.html',{'stock_analysislistarray': stock_analysislistarray,'u':request.user})

@login_required(login_url='login')
def tax_report(request):
    tax_total=0
    tax_reportslistarray=saleslists.objects.all()
    for i in tax_reportslistarray:
        i.tax_amount=i.total*(i.tax/100)
        i.grand_total=i.total+i.tax_amount
        tax_total=tax_total+i.tax_amount
    return render(request,'tax_report.html',{'tax_total':tax_total,'tax_reportslistarray': tax_reportslistarray,'u':request.user})

@login_required(login_url='login')
def tax(request):
    if request.method=='POST':
        if(request.POST.get('tax_percentage') and request.POST.get('is_default') ):
            temp=taxlists()
            temp.tax_percentage=request.POST.get('tax_percentage')
            temp.is_default=request.POST.get('is_default')
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            taxlistarray=taxlists.objects.all()
            return render(request,'tax.html',{'taxlistarray': taxlistarray,'u':request.user})
        else:
            temp=taxlists()
            temp.tax_percentage=request.POST.get('tax_percentage')
            temp.is_default="False"
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            taxlistarray=taxlists.objects.all()
            return render(request,'tax.html',{'taxlistarray': taxlistarray,'u':request.user})


    taxlistarray=taxlists.objects.all()
    return render(request,'tax.html',{'taxlistarray': taxlistarray,'u':request.user})

@login_required(login_url='login')
def users(request):
    if request.method=='POST':
        if(request.POST.get('name') and request.POST.get('email') and request.POST.get('user_role') and request.POST.get('username') and request.POST.get('password')):
            temp=userslists()
            temp.name=request.POST.get('name')
            temp.email=request.POST.get('email')
            temp.user_role=request.POST.get('user_role')
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
            easygui.msgbox("User Created and Conformation mail has been sent to given mail id\nYour data has been added successfully!...","Worksales")
            userslistarray=userslists.objects.all()
            return render(request,'users.html',{'userslistarray': userslistarray,'u':request.user})
        elif(request.POST.get('name') and request.POST.get('email') and request.POST.get('user_role')):
            temp=userslists()
            temp.name=request.POST.get('name')
            temp.email=request.POST.get('email')
            temp.user_role=request.POST.get('user_role')
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            userslistarray=userslists.objects.all()
            return render(request,'users.html',{'userslistarray': userslistarray,'u':request.user})
        else:
            userslistarray=userslists.objects.all()
            return render(request,'users.html',{'userslistarray': userslistarray,'u':request.user})

    userslistarray=userslists.objects.all()
    return render(request,'users.html',{'userslistarray': userslistarray,'u':request.user})

@login_required(login_url='login')
def vendors(request):
    if request.method=='POST':
        if(request.POST.get('name') and request.POST.get('email') and request.POST.get('date') and request.POST.get('phone_number')):
            temp=vendorlists()
            temp.name=request.POST.get('name')
            temp.email=request.POST.get('email')
            temp.date=request.POST.get('date')
            temp.phone_number=request.POST.get('phone_number')
            temp.total=0
            temp.total_sales=0
            temp.save()
            easygui.msgbox("your data has been added successfully!...","Worksales")
            vendorlistarray=vendorlists.objects.all()
            return render(request,'vendors.html',{'vendorlistarray': vendorlistarray,'u':request.user})
        else:
            vendorlistarray=vendorlists.objects.all()
            return render(request,'vendors.html',{'vendorlistarray': vendorlistarray,'u':request.user})

    vendorlistarray=vendorlists.objects.all()
    return render(request,'vendors.html',{'vendorlistarray': vendorlistarray,'u':request.user})

@login_required(login_url='login')
def delete_users(request, id):  
    temp=userslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/users.html")

@login_required(login_url='login')
def delete_roles(request, id):  
    temp=roleslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/roles.html")

@login_required(login_url='login')
def delete_customer(request, id):  
    temp=customerlists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/customer.html")

@login_required(login_url='login')
def delete_vendors(request, id):  
    temp=vendorlists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/vendors.html")

@login_required(login_url='login')
def delete_products(request, id):  
    temp=productslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/products.html")

@login_required(login_url='login')
def delete_categories(request, id):  
    temp=categorieslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/categories.html")

@login_required(login_url='login')
def delete_tax(request, id):  
    temp=taxlists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/tax.html")

@login_required(login_url='login')
def delete_sales_list(request, id):  
    temp=saleslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/sales_list.html")

@login_required(login_url='login')
def delete_expences(request, id):  
    temp=expenseslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/expences.html")

@login_required(login_url='login')
def delete_exp_categories(request, id):  
    temp=exp_categorieslists.objects.get(id=id)  
    temp.delete()  
    easygui.msgbox("your data has been deleted successfully!...")
    return redirect("/exp_categories.html")


@login_required(login_url='login')
def users_edit(request,id):
    temp = userslists.objects.get(id=id)
    return render(request,'users_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def users_update(request,id):
    if request.method == 'POST':
        userslists.objects.filter(id = id).update(name=request.POST['name'],email=request.POST['email'],user_role=request.POST['user_role'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../users.html")  
    temp=userslists.objects.all()
    return render(request,'users.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def roles_edit(request,id):
    temp = roleslists.objects.get(id=id)
    return render(request,'roles_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def roles_update(request,id):
    if request.method == 'POST':
        if(request.POST.get('role') and request.POST.get('Profile_box') and request.POST.get('Vendor_box') and request.POST.get('Customer_box') and request.POST.get('user_box')):
            roleslists.objects.filter(id = id).update(role=request.POST['role'],Profile_box=request.POST['Profile_box'],Vendor_box=request.POST['Vendor_box'],Customer_box=request.POST['Customer_box'],user_box=request.POST['user_box'])
            easygui.msgbox("your data has been updated successfully!...")
            return redirect("../roles.html")
        else:
            return redirect("../roles.html")
    temp=roleslists.objects.all()
    return render(request,'roles.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def customer_edit(request,id):
    temp = customerlists.objects.get(id=id)
    return render(request,'customer_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def customer_update(request,id):
    if request.method == 'POST':
        customerlists.objects.filter(id = id).update(name=request.POST['name'],email=request.POST['email'],date=request.POST['date'],phone_number=request.POST['phone_number'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../customer.html")  
    temp=customerlists.objects.all()
    return render(request,'customer.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def vendors_edit(request,id):
    temp = vendorlists.objects.get(id=id)
    return render(request,'vendors_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def vendors_update(request,id):
    if request.method == 'POST':
        vendorlists.objects.filter(id = id).update(name=request.POST['name'],email=request.POST['email'],date=request.POST['date'],phone_number=request.POST['phone_number'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../vendors.html")  
    temp=vendorlists.objects.all()
    return render(request,'vendors.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def products_edit(request,id):
    temp = productslists.objects.get(id=id)
    return render(request,'products_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def products_update(request,id):
    if request.method == 'POST':
        productslists.objects.filter(id = id).update(name=request.POST['name'],brand=request.POST['brand'],quantity=request.POST['quantity'],category=request.POST['category'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../products.html")  
    temp=productslists.objects.all()
    return render(request,'products.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def categories_edit(request,id):
    temp = categorieslists.objects.get(id=id)
    return render(request,'categories_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def categories_update(request,id):
    if request.method == 'POST':
        categorieslists.objects.filter(id = id).update(name=request.POST['name'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../categories.html")  
    temp=categorieslists.objects.all()
    return render(request,'categories.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def tax_edit(request,id):
    temp = taxlists.objects.get(id=id)
    return render(request,'tax_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def tax_update(request,id):
    if request.method == 'POST':
        taxlists.objects.filter(id = id).update(tax_percentage=request.POST['tax_percentage'])
        if (request.POST.get('is_default')=='False'):
            taxlists.objects.filter(id = id).update(is_default='True')
        else:
            taxlists.objects.filter(id = id).update(is_default='False')
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../tax.html")  
    temp=taxlists.objects.all()
    return render(request,'tax.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def sales_list_edit(request,id):
    temp = saleslists.objects.get(id=id)
    return render(request,'sales_list_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def sales_list_view(request,id):
    temp = saleslists.objects.get(id=id)
    return render(request,'sales_list_view.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def sales_list_update(request,id):
    if request.method == 'POST':
        saleslists.objects.filter(id = id).update(invoice_id=request.POST['invoice_id'],date=request.POST['date'],sold_to=request.POST['sold_to'],items_sold=request.POST['items_sold'],total=request.POST['total'],payment_status=request.POST['payment_status'],name=request.POST['name'],customer_name=request.POST['customer_name'],tax=request.POST['tax'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../sales_list.html")  
    temp=saleslists.objects.all()
    return render(request,'sales_list.html',{'temp': temp,'u':request.user} )

@login_required(login_url='login')
def expences_edit(request,id):
    temp = expenseslists.objects.get(id=id)
    return render(request,'expences_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def expences_update(request,id):
    if request.method == 'POST':
        expenseslists.objects.filter(id = id).update(branch=request.POST['branch'],amount=request.POST['amount'],expense_category=request.POST['expense_category'],expense_date=request.POST['expense_date'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../expences.html")  
    temp=expenseslists.objects.all()
    return render(request,'expences.html',{'temp': temp,'u':request.user} ) 

@login_required(login_url='login')
def exp_categories_edit(request,id):
    temp = exp_categorieslists.objects.get(id=id)
    return render(request,'exp_categories_edit.html',{'temp':temp,'u':request.user})

@login_required(login_url='login')
def exp_categories_update(request,id):
    if request.method == 'POST':
        exp_categorieslists.objects.filter(id = id).update(name=request.POST['name'])
        easygui.msgbox("your data has been updated successfully!...")
        return redirect("../exp_categories.html")  
    temp=exp_categorieslists.objects.all()
    return render(request,'exp_categories.html',{'temp': temp,'u':request.user} ) 

