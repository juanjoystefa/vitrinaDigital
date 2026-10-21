from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Emprendimiento, Vistas, Perfil
from .forms import EmprendimientoForm, RegistroForm, ProductoForm

# ==========================================
# 1. USUARIOS Y AUTENTICACIÓN
# ==========================================

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save() 
            login(request, usuario) 
            return redirect('emprendimientos')
    else:
        form = RegistroForm()
    return render(request, 'login/registro.html', {'form': form})

@login_required
def perfil_usuario(request):
    mis_emprendimientos = Emprendimiento.objects.filter(creador=request.user).order_by('-fecha_creacion')
    
    return render(request, 'perfil/perfil.html', {
        'mis_emprendimientos': mis_emprendimientos
    })


# ==========================================
# 2. EMPRENDIMIENTOS (CRUD Y PÚBLICAS)
# ==========================================

def inicio(request):
    # READ: Solo muestra la vitrina pública
    # Ordena primero por los afectados, y luego por los que tienen más vistas
    emprendimientos = Emprendimiento.objects.filter(estado='activo').order_by("estado_terremoto", "-totalVistas")
    return render(request, "emprendimientos/emprendimientos.html", {
        "emprendimientos": emprendimientos,
    })

def detalle_emprendimiento(request, id):
    # Carga la página individual del emprendimiento
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id, estado='activo')
    
    # Buscamos los productos vinculados a este emprendimiento específico
    mis_productos = emprendimiento.productos.all()
    
    # Lógica del buscador de productos
    query = request.GET.get('q', '')
    if query:
        mis_productos = mis_productos.filter(nombre__icontains=query)
        
    return render(request, "emprendimientos/detalle_emprendimiento.html", {
        "emprendimiento": emprendimiento,
        "productos": mis_productos,
        "query": query
    })

@login_required
def crear_emprendimiento(request):
    # CREATE: Lógica exclusiva para crear un nuevo proyecto
    if request.method == "POST":
        # Importante: request.FILES para recibir el logo
        form = EmprendimientoForm(request.POST, request.FILES) 
        if form.is_valid():
            emprendimiento = form.save(commit=False)
            emprendimiento.creador = request.user 
            emprendimiento.save()
            
            # Si era visitante, sube de nivel
            if request.user.perfil.rol == 'visitante':
                request.user.perfil.rol = 'emprendedor'
                request.user.perfil.save()
                
            # Lo enviamos a su perfil para que vea que quedó en estado 'pendiente'
            return redirect("perfil") 
    else:
        form = EmprendimientoForm()
        
    return render(request, "emprendimientos/crear_emprendimiento.html", {
        "form": form,
    })

@login_required
def editar_emprendimiento(request, id):
    # UPDATE
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    
    if request.user != emprendimiento.creador and request.user.perfil.rol != 'admin':
        return redirect('perfil')

    url_retorno = request.GET.get('next', 'perfil')

    if request.method == "POST":
        # CORRECCIÓN AQUÍ: request.POST y request.FILES van primero, instance de último.
        form = EmprendimientoForm(request.POST, request.FILES, instance=emprendimiento)
        if form.is_valid():
            form.save()
            if url_retorno.startswith('/'):
                return redirect(url_retorno)
            return redirect(url_retorno)
    else:
        # CORRECCIÓN AQUÍ: Solo instance (sin request.FILES cuando apenas carga la página)
        form = EmprendimientoForm(instance=emprendimiento)

    return render(request, "emprendimientos/editar_emprendimiento.html", {
        "form": form,
        "emprendimiento": emprendimiento,
        "url_retorno": url_retorno 
    })

@login_required
def eliminar_emprendimiento(request, id):
    # DELETE
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    url_retorno = request.GET.get('next', 'perfil')

    if request.user == emprendimiento.creador or request.user.perfil.rol == 'admin':
        emprendimiento.delete()
        
    if url_retorno.startswith('/'):
        return redirect(url_retorno)
    return redirect(url_retorno)

def registrar_visita(request, id, origen='general'):
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    Vistas.objects.create(idEmprendimiento=emprendimiento, origen=origen)
    
    if origen == 'wa' and emprendimiento.link_whatsapp:
        return redirect(f"https://wa.me/{emprendimiento.link_whatsapp}")
    elif origen == 'ig' and emprendimiento.link_instagram:
        return redirect(emprendimiento.link_instagram)
        
    # Cambio: Ahora la visita general redirige al perfil público del emprendimiento
    return redirect('detalle_emprendimiento', id=emprendimiento.idEmprendimiento)

@login_required
def crear_producto(request, id_emprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id_emprendimiento)
    
    # Seguridad: Verificamos que SOLO el dueño del emprendimiento pueda agregar productos
    if request.user != emprendimiento.creador:
        return redirect('detalle_emprendimiento', id=emprendimiento.idEmprendimiento)

    if request.method == "POST":
        # request.FILES es indispensable para recibir la foto del producto
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.idEmprendimiento = emprendimiento # Lo vinculamos a este emprendimiento
            producto.save()
            return redirect('detalle_emprendimiento', id=emprendimiento.idEmprendimiento)
    else:
        form = ProductoForm()

    return render(request, "emprendimientos/crear_producto.html", {
        "form": form,
        "emprendimiento": emprendimiento
    })


# ==========================================
# 3. PANEL DE ADMINISTRACIÓN
# ==========================================

@login_required
def admin_pendientes(request):
    if request.user.perfil.rol != 'admin':
        return redirect('inicio')

    query = request.GET.get('q', '')
    pendientes = Emprendimiento.objects.filter(estado='pendiente')
    if query:
        pendientes = pendientes.filter(nombre__icontains=query)

    cantidad_pendientes = Emprendimiento.objects.filter(estado='pendiente').count()

    return render(request, "admin/admin_pendientes.html", {
        "pendientes": pendientes,
        "query": query,
        "cantidad_pendientes": cantidad_pendientes 
    })

@login_required
def admin_usuarios(request):
    if request.user.perfil.rol != 'admin':
        return redirect('inicio')

    query = request.GET.get('q', '')
    usuarios = Perfil.objects.all()
    if query:
        usuarios = usuarios.filter(Q(usuario__username__icontains=query) | Q(usuario__email__icontains=query))

    cantidad_pendientes = Emprendimiento.objects.filter(estado='pendiente').count()

    return render(request, "admin/admin_usuarios.html", {
        "usuarios": usuarios,
        "query": query,
        "cantidad_pendientes": cantidad_pendientes
    })

@login_required
def admin_emprendimientos(request):
    if request.user.perfil.rol != 'admin':
        return redirect('inicio')

    query = request.GET.get('q', '')
    todos_emprendimientos = Emprendimiento.objects.all().order_by("-totalVistas")
    if query:
        todos_emprendimientos = todos_emprendimientos.filter(nombre__icontains=query)

    cantidad_pendientes = Emprendimiento.objects.filter(estado='pendiente').count()

    return render(request, "admin/admin_emprendimientos.html", {
        "emprendimientos": todos_emprendimientos,
        "query": query,
        "cantidad_pendientes": cantidad_pendientes
    })

@login_required
def cambiar_estado_emprendimiento(request, id, nuevo_estado):
    if request.user.perfil.rol != 'admin':
        return redirect('inicio')

    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    
    if nuevo_estado in dict(Emprendimiento.ESTADOS).keys():
        emprendimiento.estado = nuevo_estado
        emprendimiento.save()
        
    return redirect('admin_pendientes')