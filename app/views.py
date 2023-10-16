from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Cart, Product, OrderPlaced
from .forms import CustomerRegistrationForm, ProfileCustomerForm
from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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

  item_already_in_cart = False      # same product select user
  item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

  return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})



@login_required

def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)

 Cart(user=user, product=product).save()

 return redirect('/cart')


@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)

  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]

  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity  *  p.product.discounted_price)
    amount += tempamount
    totalamount = amount + shipping_amount
   return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
  else:
   return render(request, 'app/emptycart.html')
   

# Quantity plus, minus, remove

def plus_cart(request):                     # Plus Quantity
 if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()

    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      #totalamount = amount + shipping_amount

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
    }

    return JsonResponse(data)
 

def minus_cart(request):                                      # minus Quantity
 if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -= 1
    c.save()

    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
    }

    return JsonResponse(data)
 


def remove_cart(request):                     # Remove Quantity
 if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    
    c.delete()

    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      

    data = {
      'amount': amount,
      'totalamount': amount + shipping_amount
    }

    return JsonResponse(data)
 
    




def buy_now(request):
 return render(request, 'app/buynow.html')


@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class AddressView(View):
 def get(self, request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html', {'address':add, 'active':'btn-primary'})


@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})



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
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)

 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0.0

 cart_product = [p for p in Cart.objects.all() if p.user == request.user]

 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  totalamount = amount + shipping_amount
 return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items': cart_items})


@login_required
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart_items = Cart.objects.filter(user=user)

 for c in cart_items:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect("orders")

