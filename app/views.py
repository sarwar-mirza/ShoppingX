from django.shortcuts import render
from django.views import View
from .models import Customer, Cart, Product, OrderPlaced
from .forms import CustomerRegistrationForm, ProfileCustomerForm
from django.contrib import messages


class ProductHomeView(View):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')

  context = {'topwears': topwears, 'bottomwears':bottomwears, 'mobiles':mobiles}
  return render(request, 'app/home.html', context)



class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html', {'product':product})



def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

class ProfileViewCustomer(View):
 def get(self, request):
  fm = ProfileCustomerForm()
  return render(request, 'app/profile.html', {'form':fm, 'active':'btn-primary'})
 
 def post(self, request):
  fm = ProfileCustomerForm(request.POST)

  if fm.is_valid():
   usr = request.user
   name = fm.cleaned_data['name']
   locality = fm.cleaned_data['locality']
   city = fm.cleaned_data['city']
   state = fm.cleaned_data['state']
   zipcode = fm.cleaned_data['zipcode']

   reg = Customer( user= usr, name=name, locality= locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations !! Profile Updated Successfully. ')
  return render(request, 'app/profile.html', {'form':fm, 'active':'btn-primary'})


class AddressView(View):
 def get(self, request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html', {'address':add, 'active':'btn-primary'})



def orders(request):
 return render(request, 'app/orders.html')


def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Apple' or data == 'Samsung' or data == 'Nokia':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'Below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'Above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

 return render(request, 'app/mobile.html', {'mobiles':mobiles})



def login(request):
 return render(request, 'app/login.html')



class CustomerRegistrationView(View):
 def get(self, request):
  fm = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':fm})
 
 def post(self, request):
  fm = CustomerRegistrationForm(request.POST)
  if fm.is_valid():
   messages.success(request, 'Congratulations Your registration successfully done !!!')
   fm.save()
  return render (request, 'app/customerregistration.html', {'form':fm})

def checkout(request):
 return render(request, 'app/checkout.html')
