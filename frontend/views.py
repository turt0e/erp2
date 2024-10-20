from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from . models import Product
from .models import Product, Order
from .forms import ProductForm, OrderForm
from .forms import  UserUpdateForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, ProductForm, OrderForm, UserUpdateForm, ProfileUpdateForm, OrderUpdateForm
from .models import Product, Order
from .decorators import admin_required, staff_required, accountant_required
from django.contrib.auth.models import Group
from .models import Profile
# Create your views here.
# def index(request):
#     return render(request, 'index.html')

# Signup View
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()          
            staff_group, created = Group.objects.get_or_create(name='Staff')
            user.groups.add(staff_group)
            Profile.objects.create(user=user) 
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Redirect based on user group
                if user.groups.filter(name='Admin').exists():
                    return redirect('admin-dashboard')
                elif user.groups.filter(name='Staff').exists():
                    return redirect('staff-dashboard')
                elif user.groups.filter(name='Accountant').exists():
                    return redirect('accountant-dashboard')
                else:
                    return redirect('index')  
            else:
                form.add_error(None, "Invalid login credentials")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')    

# profile view
def user_profile(request):
    
    return render(request, 'profile.html')

# update profile
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profileupdate.html', context)

# product view
@login_required
def index(request):
    products = Product.objects.all()

    if request.method == 'POST':
       
        if 'delete_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return redirect('index')
        
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ProductForm()

    context = {
        "products": products,
        "form": form,
    }
    return render(request, 'index.html', context)

# order view/deletion
@login_required
def index(request):
    products = Product.objects.all()  
    orders = Order.objects.all()     

    if request.method == 'POST':
        
        if 'delete_product' in request.POST:
            product_id = request.POST.get('product_id')
            if product_id:  # Ensure product_id is present
                product = get_object_or_404(Product, id=product_id)
                product.delete()
                return redirect('index') 

    
        product_form = ProductForm(request.POST)
        order_form = OrderForm(request.POST)

       
        if product_form.is_valid():
            product_form.save()
            return redirect('index')

      
        if order_form.is_valid():
            order_form.save()
            return redirect('index')

    else:
        
        product_form = ProductForm()
        order_form = OrderForm()

    context = {
        "products": products,
        "orders": orders,
        "product_form": product_form,
        "order_form": order_form,
    }
    return render(request, 'index.html', context)


# order_page
@login_required
def order_list(request):
    orders = Order.objects.all()  
    context = {
        "orders": orders,
    }
    return render(request, 'order.html', context) 


# Admin-only view
@admin_required
def admin_dashboard(request):
    products = Product.objects.all()  # Fetch products for display
    orders = Order.objects.all()      # Fetch orders if needed

    if request.method == 'POST':
        if 'delete_product' in request.POST:
            product_id = request.POST.get('product_id')
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                product.delete()
                return redirect('admin-dashboard')
        
        product_form = ProductForm(request.POST)
        order_form = OrderForm(request.POST)

        if product_form.is_valid():
            product_form.save()
            return redirect('admin-dashboard')

        if order_form.is_valid():
            order_form.save()
            return redirect('admin-dashboard')

    else:
        product_form = ProductForm()
        order_form = OrderForm()

    context = {
        "products": products,
        "orders": orders,
        "product_form": product_form,
        "order_form": order_form,
    }

    return render(request, 'index.html', context)

# Staff-only view
@staff_required
def staff_dashboard(request):
    products = Product.objects.all()  
    staff_orders = Order.objects.filter(customer=request.user)  

    if request.method == 'POST':
        # Handle order deletion
        if 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id, customer=request.user)  
            order.delete()
            return redirect('staff-dashboard')

        # Handle new order submission
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = request.user  
            order.save()
            return redirect('staff-dashboard')
    else:
        order_form = OrderForm()

    context = {
        'products': products, 
        'staff_orders': staff_orders,  
        'order_form': order_form,  
    }
    return render(request, 'staff_dashboard.html', context)

# Accountant-only view
@accountant_required
def accountant_dashboard(request):
    orders = Order.objects.all()  

    if request.method == 'POST':
        if 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return redirect('accountant-dashboard')

    context = {
        'orders': orders,  
    }
    return render(request, 'accountant_dashboard.html', context)

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('accountant-dashboard')  
    else:
        form = OrderUpdateForm(instance=order)

    context = {
        'form': form,
        'order': order,
    }
    return render(request, 'update_order.html', context)