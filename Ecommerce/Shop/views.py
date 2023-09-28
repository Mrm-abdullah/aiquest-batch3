from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer_Info, Cart, Product, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
# from . models import Product, Customer, Cart, OrderPlaced
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@login_required
def payment_done(request):
   user = request.user
   custid = request.GET.get('custid')
   customer = Customer_Info.objects.get(id=custid)
   cart = Cart.objects.filter(user=user)
   for c in cart:
      OrderPlaced(user=user, Customer=customer, product = c.product, quantity = c.quantity).save()
      c.delete()

   return redirect('orders') 

@login_required
def checkout(request):
     user = request.user
     totalitem = 0
     if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
     add = Customer_Info.objects.filter(user=user)
     cart_items = Cart.objects.filter(user=user)
     amount = 00
     shipping_amount = 100
     totalamount = 00
     cart_product = [p for p in Cart.objects.all() if p.user==user]
     if cart_product:
          for p in cart_product:
               tempamount = (p.quantity * p.product.discountprice)
               amount += tempamount  
               totalamount = amount + shipping_amount 
     return render(request, 'Shop/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem':totalitem })

#Remove cart
@login_required
def remove_cart(request):
     if request.method == 'GET':
          prod_id = request.GET['prod_id']
          c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          c.delete()
          amount = 0
          shipping_amount = 100
          cart_product = [p for p in Cart.objects.all() if p.user==request.user]
     for p in cart_product:
          tempamount = (p.quantity * p.product.discountprice)
          amount += tempamount  
          totalamount = amount + shipping_amount
     data = {
         'amount': amount,
         'totalamount': totalamount
     }
     return JsonResponse(data)

class ProductView(View):
    def get(self, request):
     gentspants = Product.objects.filter(category='GP')
     borkha = Product.objects.filter(category='B')
     BabyFashion = Product.objects.filter(category='BF')
     Sharee = Product.objects.filter(category='S')
     Lehegga = Product.objects.filter(category='L')
     totalitem = 0
     if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
     contex={
          'gentspants': gentspants,
          'borkha': borkha,
          'BabyFashion': BabyFashion,
          'Sharee': Sharee,
          'Lehegga': Lehegga,
          'totalitem': totalitem,
     }
     return render(request, 'Shop/home.html', contex)

class ProductdetailView(View):
     def get(self, request, pk):
          product = Product.objects.get(pk=pk)
          
          similar_product = Product.objects.filter(category=product.category)

          totalitem = 0
          if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
          item_already_in_cart = False
          if request.user.is_authenticated:
               item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
          contex={
               'product': product,
               'item_already_in_cart':item_already_in_cart,
               'totalitem':totalitem,
               'similar_product':similar_product,
          }
          return render(request, 'Shop/productdetail.html', contex)

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 if Cart.objects.filter(Q(product=product.id) & Q(user=user)).exists():
     return redirect('showcart')
 Cart(user=user, product=product).save()
 return redirect('showcart')

@login_required
def Minus_Cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      
      c.quantity -=1
      c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discountprice)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)

@login_required
def plus_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      
      c.quantity +=1
      c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discountprice)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)

@login_required
def show_cart(request):
     if request.user.is_authenticated:
          user = request.user
          cart = Cart.objects.filter(user=user)
          amount = 0.0
          shipping_amount = 100.0
          total = 0.0
          totalitem = 0
          if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
          cart_product = [p for p in Cart.objects.all() if p.user==user]
          if cart_product:
               for p in cart_product:
                    tempamount = (p.quantity * p.product.discountprice)
                    amount += tempamount  
                    totalamount = amount + shipping_amount
               return render(request, 'Shop/addtocart.html', {'carts':cart, 'totalamount':totalamount,'amount':amount,'totalitem':totalitem })
          else:
               return render(request, 'Shop/emptycart.html')
     else:
          return redirect('/')

def buy_now(request):
 return render(request, 'Shop/buynow.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
     def get(self, request):
          form = CustomerProfileForm
          totalitem = 0
          if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
          contex={
          'form':form,
          'totalitem':totalitem,
          }
          return render(request, 'Shop/profile.html', contex)
   
     def post(self, request):
          form = CustomerProfileForm(request.POST)
          if form.is_valid():
               usr = request.user
               name = form.cleaned_data['name']
               division = form.cleaned_data['division']
               district = form.cleaned_data['district']
               thana = form.cleaned_data['thana']
               villorroad = form.cleaned_data['villorroad']
               zipcode = form.cleaned_data['zipcode']
               reg = Customer_Info(user=usr,name=name, division=division,district=district, thana=thana, villorroad=villorroad, zipcode=zipcode)
               reg.save()
               messages.success(request, 'Congratulations! Profile Updated Successfully')
          contex={
               'form':form,
          }
          return render(request, 'Shop/profile.html',contex)

@login_required
def address(request):
     add = Customer_Info.objects.filter(user=request.user)
     totalitem = 0
     if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
     contex={
          'add':add,
          'totalitem':totalitem,
     }
     return render(request, 'Shop/address.html', contex)

class LehengaView(View):
     def get(self, request, data=None):
          if data == None:
               lehenggas = Product.objects.filter(category='L')
          elif data == 'hello' or data == 'hi':
               lehenggas = Product.objects.filter(category='L').filter(brand=data)
          elif data == 'bellow':
               lehenggas = Product.objects.filter(category='L').filter(discountprice__lt=550)
          elif data == 'above':
               lehenggas = Product.objects.filter(category='L').filter(discountprice__gt=550)
          contex = {
               'lehenggas':lehenggas, 
          }
          return render(request, 'Shop/lehenga.html', contex)

class CustomerRegistrationView(View):
  def get(self, request):
     form = CustomerRegistrationForm()
     return render(request, 'Shop/customerregistration.html', {'form':form})
  
  def post(self, request):
     form = CustomerRegistrationForm(request.POST)
     if form.is_valid():
        messages.success(request,'Congratulations registration done.')
        form.save()
     return render(request, 'Shop/customerregistration.html', {'form':form})

def login(request):
     return render(request, 'Shop/login.html')

def customerregistration(request):
     return render(request, 'Shop/customerregistration.html')

@login_required
def orders(request):
     totalitem = 0
     if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
     op = OrderPlaced.objects.filter(user=request.user)
     return render(request, 'Shop/orders.html', {'order_placed':op,'totalitem':totalitem})

