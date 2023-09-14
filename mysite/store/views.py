

from django.http import HttpResponse
from .models import Laptop, Brand, Image,Cart
from account.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Laptop
from .forms import LaptopForm, ImageForm, UserForm, BrandForm
from account.forms import SignUpForm

from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from account.views import login_view

class EditImageView(UpdateView):
    model = Image
    form_class = ImageForm
    template_name = 'edit_image.html'

    def form_valid(self, form):
        form.save()
        return redirect('view_images')


class DeleteImageView(DeleteView):
    model = Image
    template_name = 'delete_image.html'
    success_url = reverse_lazy('view_images')


@login_required(login_url='login_view')
def index(request):
    if request.user.is_superuser:
        print(request.user)
        return render(request, 'base.html')
    else:
        return redirect('login_view')

@login_required(login_url='login_view')
def lapList(request):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        lap_list = Laptop.objects.all()
        context = {'laptop_list': lap_list}
        return render(request, 'lapList.html', context)

@login_required(login_url='login_view')
def add_laptop(request):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        brands = Brand.objects.all()

        if request.method == 'POST':
            form = LaptopForm(request.POST)
            if form.is_valid():
                laptop = form.save()
                return redirect('lapList')
        else:
            form = LaptopForm()
        if form.errors:
            errors = form.errors
        else:
            errors = None
        return render(request, 'add_laptop.html', {'form': form, 'brands': brands, 'errors': errors})

@login_required(login_url='login_view')
def laptop_update(request, pk):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        laptop = get_object_or_404(Laptop, id=pk)
        if request.method == 'POST':
            form = LaptopForm(request.POST, instance=laptop)
            if form.is_valid():
                form.save()
                return redirect('lapList')
        else:
            form = LaptopForm(instance=laptop)

        return render(request, 'laptop_update.html', {'form': form})

@login_required(login_url='login_view')
def delete_laptop(request, pk):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        laptop = Laptop.objects.get(id=pk)
        if request.method == 'POST':
            laptop.delete()
            return redirect('lapList')
        context = {'item': laptop}
        return render(request, 'delete_laptop.html', context)

@login_required(login_url='login_view')
def laptop_detail(request, laptop_id):
    if request.user.is_superuser:
        template = 'base.html'
        laptop = get_object_or_404(Laptop, id=laptop_id)
        images = Image.objects.filter(laptop=laptop)
        print(request.user.is_superuser)
        return render(request, 'laptop_detail.html', {'laptop': laptop, 'images': images, 'template':template})
    else:
        template = 'main.html'
        laptop = get_object_or_404(Laptop, id=laptop_id)
        images = Image.objects.filter(laptop=laptop)
        cart = Cart.objects.filter(customer=request.user).first()
        return render(request, 'laptop_detail.html', {'laptop': laptop, 'images': images, 'template':template,"cart":cart})

    

@login_required(login_url='login_view')
def delete(request):
    # delete
    lapList()

@login_required(login_url='login_view')
def upload_image(request):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('view_images')
        else:
            form = ImageForm()
            laptops = Laptop.objects.all()
        return render(request, 'upload_image.html', {'form': form, 'laptops': laptops})

@login_required(login_url='login_view')
def view_images(request):
    laptops = Laptop.objects.all()
    images = []
    for laptop in laptops:
        images.append(Image.objects.filter(laptop=laptop))
    return render(request, 'view_images.html', {'laptops': laptops, 'images': images})

# CUSTOMER
@login_required(login_url='login_view')
def users_list(request):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        usersList =  User.objects.filter(is_customer = True)
        return render(request, 'users_list.html',{'usersList':usersList })

@login_required(login_url='login_view')
def user_detail(request, user_id):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        user = get_object_or_404(User, id=user_id)
        return render(request, 'user_detail.html', {'user': user})

@login_required(login_url='login_view')
def user_update(request, pk):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        user = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('users')
        else:
            initial_role = 'Customer' if user.is_customer else 'Admin'
            form = UserForm(instance=user, initial={'role': initial_role})
        return render(request, 'user_update.html', {'form': form})

@login_required(login_url='login_view')
def user_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        user = User.objects.get(id=pk)
        if request.method == 'POST':
            user.delete()
            return redirect('users')
        context = {'item': user}
        return render(request, 'user_delete.html', context)

@login_required(login_url='login_view')
def user_add(request):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                return redirect('users')
        else:
            form = SignUpForm()
        if form.errors:
            errors = form.errors
        else:
            errors = None

        return render(request, 'user_add.html', {'form': form, 'errors': errors})

# Brand
@login_required(login_url='login_view')
def brand_list(request):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        brand_list =  Brand.objects.all()
        return render(request, 'brand_list.html',{'brand_list':brand_list })

@login_required(login_url='login_view')
def brand_detail(request, brand_id):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        brand = get_object_or_404(Brand, id=brand_id)
        return render(request, 'brand_detail.html', {'brand': brand})

@login_required(login_url='login_view')
def brand_add(request):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        if request.method == 'POST':
            form = BrandForm(request.POST)
            if form.is_valid():
                brand = form.save()
                return redirect('brand_list')
        else:
            form = BrandForm()
        if form.errors:
            errors = form.errors
        else:
            errors = None

        return render(request, 'brand_add.html', {'form': form, 'errors': errors})

@login_required(login_url='login_view')
def brand_update(request, brand_id):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        brand = get_object_or_404(Brand, id=brand_id)
        if request.method == 'POST':
            form = BrandForm(request.POST, instance=brand)
            if form.is_valid():
                form.save()
                return redirect('brand_list')
        else:
            form = BrandForm(instance=brand)

        return render(request, 'brand_update.html', {'form': form})

@login_required(login_url='login_view')
def brand_delete(request, brand_id):
    if not request.user.is_superuser:
        return redirect('login_view')
    else:
        brand = Brand.objects.get(id=brand_id)
        if request.method == 'POST':
            brand.delete()
            return redirect('brand_list')
        context = {'brand_id': brand}
        return render(request, 'brand_delete.html', context)

@login_required(login_url='login_view')
def delete(request):
    # delete
    brand_list()