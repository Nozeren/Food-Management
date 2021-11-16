from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Category,Ingredient, To_buy 
from .forms import CreaterUserForm
import os.path
@login_required(login_url='login')
def buy_list(request):
    category=request.GET.get('category')
    if category == None:
        ingredients_list = To_buy.objects.filter(user=request.user).order_by('category')
    else:
        ingredients_list = To_buy.objects.filter(user=request.user,category__name=category)

    categories = Category.objects.all()
    
    if request.method == 'POST':
        data= request.POST
        print(data)
        if 'minus' in data: 
            ingr=To_buy.objects.get(name=data['minus'])
            ingr.quantity-=1
            ingr.save()  
        if 'plus' in data:
            ingr= To_buy.objects.get(name=data['plus'])
            ingr.quantity+=1
            ingr.save()
        if 'check' in data:
            ingr= To_buy.objects.get(name=data['check'])
            category, created = Category.objects.get_or_create(name=ingr.category)
            new= Ingredient.objects.create(
                category=category,
                name=ingr.name,
                quantity=ingr.quantity,
                image=ingr.name+".png"
            )
            ingr.delete()
    
    context= {"ingredients":ingredients_list,"categories":categories}
    return render(request,'stock/to_buy.html',context)



@login_required(login_url='login')
def ingredients(request):
    category=request.GET.get('category')
    if category == None:
        photos = Ingredient.objects.filter(user=request.user)
    else:
        photos = Ingredient.objects.filter(user=request.user,category__name=category)
        
    categories = Category.objects.all()
    if request.method == 'POST':
        data= request.POST
        if 'minus' in data: 
            ingr=Ingredient.objects.get(user=request.user,name=data['minus'])
            ingr.quantity-=1
            if ingr.quantity<=0:
                to_buy= To_buy.objects.create(
                                user=request.user,
                                name=ingr.name,
                                quantity=1,
                                category=ingr.category
                            )                
                ingr.delete()

            else:
                ingr.save()  
        if 'plus' in data:
            ingr= Ingredient.objects.get(user=request.user,name=data['plus'])
            ingr.quantity+=1
            ingr.save()
            
    
    context= {'categories':categories,'photos':photos}
    return render(request,'stock/ingredients.html',context)

@login_required(login_url='login')
def add_ingredient(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        if os.path.isfile(f"static/images/{data['ingredient']}.jpg"):
            image=f"{data['ingredient']}.jpg"
        elif os.path.isfile(f"static/images/{data['ingredient']}.png"):
            image=f"{data['ingredient']}.png"
        else:
            image='no_image.png'
        
        if data['category'] != 'none':
            category= Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category=None
        
        if Ingredient.objects.filter(user=request.user,name=data['ingredient']).exists():
            messages.warning(request, 'The ingredient already exists')
        else:  
            ingr= Ingredient.objects.create(
                user=request.user,
                category=category,
                name=data['ingredient'],
                quantity=data['quantity'],
                image=image,
            )
            return redirect('stock')
    context= {'categories':categories}
    return render(request,'stock/add.html',context)


@login_required(login_url='login')
def add_buy(request):
    categories = Category.objects.all() 
    if request.method == 'POST':
        data = request.POST
        if data['category'] != 'none':
            category= Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category=None
        
        if To_buy.objects.filter(user=request.user,name=data['ingredient']).exists():
            messages.warning(request, 'The ingredient already exists')
        else:  
            ingr= To_buy.objects.create(
                user=request.user,
                category=category,
                name=data['ingredient'],
                quantity=data['quantity']
            )
            return redirect('buy')
    context= {'categories':categories}
    return render(request,'stock/add.html',context)

def logout_page(request):
    logout(request)
    return redirect('login')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('stock')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request, user)
                return redirect('stock')
            else:
                messages.info(request, 'Username or Password is incorrect')
                
        return render(request,'stock/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('stock')
    else:
        form=CreaterUserForm()
        if request.method == 'POST':
            form =CreaterUserForm(request.POST)
            if form.is_valid():
                form.save()
                user= form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
            
        context={'form':form}
        return render(request,'stock/register.html',context)