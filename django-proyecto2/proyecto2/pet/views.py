from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.contrib.auth import authenticate, login
from .forms import *
from django.shortcuts import redirect
from django.contrib import messages
from .models import Producto
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


def index(request):
    context ={
        
        'fecha_hora':datetime.datetime.now()

    }

    return render(request, 'pet/index.html', context)

# def listado_articulos(request):

#     productos=Producto.objects.all()#query
#     context= {
#         'productos':productos
        
#     }

    # return render(request, 'pet/listado_articulos.html', context)
# forma de hacerlo con clases

class ArticuloListView(LoginRequiredMixin, ListView):
    model=Producto
    context_object_name='productos'
    template_name='pet/listado_articulos.html'
    ordering = ['ean']


# def alta_profucto(request):
#     context={}
#     form = AltaProductoForm(request.POST)
#     if request.method == "GET":
#         context['alta_producto_form'] = AltaProductoForm()
#     else: 
#         context['alta_producto_form'] = form

#         if form.is_valid():
#             nuevo_producto= Producto(
#                 nombre=form.cleaned_data['nombre'],
#                 descripcion=form.cleaned_data['descripcion'],
#                 precio=form.cleaned_data['precio'],
#                 ean=form.cleaned_data['ean'],
#                 imagen_url=form.cleaned_data['imagen_url'])
#             nuevo_producto.save()
#             messages.info(request, 'articulo dado de alta')
            
#             return redirect('index')

#     return render(request, 'pet/alta_producto.html',context)


#  formulario con model form
@login_required
def alta_producto(request):
    context = {}

    if request.method == 'GET':
        formulario=AltaProductoModelForm()
    else:
        formulario=AltaProductoModelForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.info(request, 'articulo dado de alta')
            
            return redirect('index')
    context['formulario']= formulario
    return render(request,'pet/alta_producto.html',context )

def mi_vista(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username,password= password)
    if user is not None:
        login(request,user)
    

def cerrar_logout(request):
    logout(request)
    messages.success(request, 'Sesion cerrada')

    return redirect('index')



@user_passes_test(lambda u: u.is_superuser)
def create_admin_view(request):
    if request.method == 'POST':
        form = CreateAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Usuario dado de alta')

            return redirect('index')
    else:
        form = CreateAdminForm()

    return render(request, 'pet/create_admin.html', {'form': form})
