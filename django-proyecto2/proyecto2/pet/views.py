from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
import datetime
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from .models import Producto
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


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
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | Q(empresa__icontains=query)
            )
        return queryset

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

# --------------------------------

def mi_vista(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username,password= password)
    if user is not None:
        login(request,user)
    
# ----------------------------------
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

# ---------------------------------------------
@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        formulario = AltaProductoModelForm(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto actualizado con éxito')
            return redirect('listado_articulos')
    else:
        formulario = AltaProductoModelForm(instance=producto)
    return render(request, 'pet/alta_producto.html', {'formulario': formulario})

@login_required
def borrar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto borrado con éxito')
        return redirect('listado_articulos')
    return render(request, 'pet/borrar_producto.html', {'producto': producto})

@login_required
def actualizar_precios(request):
    if request.method == 'POST':
        form = ActualizarPreciosForm(request.POST)
        if form.is_valid():
            proveedor = form.cleaned_data['proveedor']
            porcentaje_incremento = form.cleaned_data['porcentaje_incremento']
            
            # Filtrar productos por proveedor
            productos = Producto.objects.filter(empresa=proveedor)
            
            if not productos.exists():
                messages.error(request, 'No se encontraron productos para el proveedor especificado.')
                return redirect('actualizar_precios')

            # Actualizar precios de todos los productos del proveedor
            for producto in productos:
                producto.precio += producto.precio * (porcentaje_incremento / 100)
                producto.save()
            
            messages.success(request, 'Precios actualizados con éxito')
            return redirect('listado_articulos')
    else:
        form = ActualizarPreciosForm()
    
    return render(request, 'pet/actualizar_precios.html', {'form': form})