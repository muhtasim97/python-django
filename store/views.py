from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password,make_password
from django.http import HttpResponse
from .models.product import Product
from .models.catagory import Category
from .models.customer import Customer
from .models.orders import Order
from django.views import View

class Index(View):
    def get(self,request):
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}

        products=None
        categories=Category.get_category()
        categoryId=request.GET.get('category')
        if categoryId:
            products = Product.get_all_product_data_by_category_id(categoryId)
        else:
            products = Product.get_all_product_data()
        data={}
        data['products']=products
        data['categories']=categories
        print('you are-',request.session.get('email'))
        return render(request,'index.html',data)
    def post(self,request):
        product_id=request.POST.get('p_id')
        remove_from_cart=request.POST.get('remove')
        print(product_id)
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product_id)  #----get the value of the  product_id key
            if quantity:
                if remove_from_cart:
                    if quantity<=1:
                        cart.pop(product_id)
                    else:
                        cart[product_id]=quantity-1
                else:
                    cart[product_id]=quantity+1
            else:
                cart[product_id]=1
        else:
            cart={}
            cart[product_id]=1
            
        request.session['cart']=cart
        print(request.session['cart'])
        return redirect('homepage')
        

class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
        firstname=request.POST['fname']
        lastname=request.POST['lname']
        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']
        error_message=None
        if not firstname:
            error_message="Fill the first name"
        elif len(firstname)<5:
            error_message="Firstname must be longer than 4 character"
        elif not lastname:
            error_message="Fill the last name"
        elif len(password)<6:
            error_message="Password lenght must be atleast 7"
        elif Customer.objects.filter(email=email):
            error_message="Email address already exists"


        if not error_message:
            password=make_password(password)
            customerlist=Customer( firstname=firstname,lastname=lastname ,phone= phone ,email=email, password=password )
            customerlist.save()
            return redirect('homepage')
        else:    
            values={
            'error': error_message,
            'firstname':firstname,
            'lastname': lastname,
            'phone': phone,
            'email': email,
            }
            return render(request,'signup.html',values)


#---------------login class ----------------

def match_customer(email):

    try:
        return Customer.objects.get(email=email)
    except:
        return False


class Login(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        find_customer=match_customer(email)
        #data_error=None
        if find_customer:
            print(find_customer.password)
            print(password)
            match_password= check_password(password,find_customer.password)
            print(match_password)
            if match_password:
               request.session['customer_id']=find_customer.id 
               request.session['email']=find_customer.email
               return redirect('homepage')
            else:
                data_error="Email or password not matched"
                return render(request,'login.html', { 'error':data_error })
        else:
            data_error="Email or password not matched"
            return render(request,'login.html', { 'error':data_error })

class Cart(View):
    def get(self,request):
        list_of_product_id=list(request.session.get('cart').keys())
        products_find=Product.product_info(list_of_product_id)
        print(products_find)
        return render(request,'cart.html',{'products_find':products_find})


class Checkout(View):
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer_id')
        cart=request.session.get('cart')
        products=Product.product_info(list(cart.keys()))
        print(address,phone,customer,cart,products)

        if customer:
            for product in products:
                order_obj=Order(customer=Customer(id=customer),
                                product=product,
                                quantity=cart.get(str(product.id)),
                                address=address,
                                phone=phone)
                order_obj.order_save() #method 
                request.session['cart']={}   
            return redirect('homepage')     
        else:
            return redirect('login') 
            


class Orders(View):
    def get(self,request):
        customer=request.session.get('customer_id')
        if customer:
            orders=Order.order_list(customer)  #method
            print(orders)
            return render(request,'orders.html', {'orders':orders})
        
        else:
            return redirect('login') 





def logout(request):
    request.session.clear()
    return redirect('login')
