from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Emprendimiento, Vistas, Perfil
from .forms import EmprendimientoForm, RegistroForm

# ================================
# VISTA DE INICIO
# ================================
def inicio(request):
    if request.method == "POST":
        # Protegemos para que solo usuarios logueados puedan crear
        if not request.user.is_authenticated:
            return redirect("login")
            
        form = EmprendimientoForm(request.POST)
        if form.is_valid():
            emprendimiento = form.save(commit=False)
            emprendimiento.creador = request.user # Asignamos el usuario logueado
            emprendimiento.save()
            
            # MAGIA: Si el usuario era visitante, lo subimos a emprendedor
            if request.user.perfil.rol == 'visitante':
                request.user.perfil.rol = 'emprendedor'
                request.user.perfil.save()
                
            return redirect("emprendimientos") 
    else:
        form = EmprendimientoForm()
        
    emprendimientos = Emprendimiento.objects.filter(estado='activo').order_by("-totalVistas")

    return render(request, "emprendimientos/emprendimientos.html", {
        "emprendimientos": emprendimientos,
        "form": form,
    })

@login_required
def perfil_usuario(request):
    # Buscamos todos los emprendimientos que ha creado este usuario en específico
    mis_emprendimientos = Emprendimiento.objects.filter(creador=request.user).order_by('-fecha_creacion')
    
    return render(request, 'perfil/perfil.html', {
        'mis_emprendimientos': mis_emprendimientos
    })

# ==========================================
# VISTAS PÚBLICAS
# ==========================================

def registrar_visita(request, id, origen='general'):
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    
    # Creamos la visita pasándole el origen (wa, ig, web o general)
    Vistas.objects.create(idEmprendimiento=emprendimiento, origen=origen)
    
    # Redirección inteligente: si hizo clic en WhatsApp, lo llevamos a WhatsApp
    if origen == 'wa' and emprendimiento.link_whatsapp:
        return redirect(f"https://wa.me/{emprendimiento.link_whatsapp}")
    elif origen == 'ig' and emprendimiento.link_instagram:
        return redirect(emprendimiento.link_instagram)
    elif origen == 'web' and emprendimiento.link_web:
        return redirect(emprendimiento.link_web)
        
    # Si es 'general', recarga la página principal
    return redirect('inicio')

# ==========================================
# CRUD: EDITAR Y ELIMINAR EMPRENDIMIENTOS
# ==========================================

@login_required
def editar_emprendimiento(request, id):
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    
    # Seguridad: Verificamos que quien intenta editar sea el creador o un admin
    if request.user != emprendimiento.creador and request.user.perfil.rol != 'admin':
        return redirect('perfil')

    # Capturamos a dónde debemos volver (por defecto, al perfil)
    url_retorno = request.GET.get('next', 'perfil')

    if request.method == "POST":
        form = EmprendimientoForm(request.POST, instance=emprendimiento)
        if form.is_valid():
            form.save()
            # Redirigimos a la url capturada.
            # Si 'url_retorno' empieza con '/', es una ruta (ej. /panel/emprendimientos/).
            # Si no, asumimos que es el nombre de una vista de Django (ej. 'perfil').
            if url_retorno.startswith('/'):
                return redirect(url_retorno)
            return redirect(url_retorno)
    else:
        form = EmprendimientoForm(instance=emprendimiento)

    return render(request, "perfil/editar_emprendimiento.html", {
        "form": form,
        "emprendimiento": emprendimiento,
        "url_retorno": url_retorno # Se lo pasamos a la plantilla para no perderlo
    })

@login_required
def eliminar_emprendimiento(request, id):
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    
    # Capturamos a dónde debemos volver
    url_retorno = request.GET.get('next', 'perfil')

    # Seguridad: Solo el creador o un admin pueden borrarlo
    if request.user == emprendimiento.creador or request.user.perfil.rol == 'admin':
        emprendimiento.delete()
        
    if url_retorno.startswith('/'):
        return redirect(url_retorno)
    return redirect(url_retorno)


# ==========================================
# VISTAS DEL PANEL DE ADMINISTRACIÓN SEPARADAS
# ==========================================

@login_required
def admin_pendientes(request):
    if request.user.perfil.rol != 'admin':
        return redirect('inicio')

    query = request.GET.get('q', '')
    pendientes = Emprendimiento.objects.filter(estado='pendiente')
    if query:
        pendientes = pendientes.filter(nombre__icontains=query)

    # 1. Contamos el total real de pendientes
    cantidad_pendientes = Emprendimiento.objects.filter(estado='pendiente').count()

    return render(request, "admin/admin_pendientes.html", {
        "pendientes": pendientes,
        "query": query,
        "cantidad_pendientes": cantidad_pendientes # 2. Lo enviamos a la plantilla
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
        
    # Cambio clave: ahora redirige específicamente a la vista de pendientes
    return redirect('admin_pendientes')

# ================================
# VISTA DE REGISTRO
# ================================
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save() # Esto dispara la señal de models.py y crea el perfil "visitante"
            login(request, usuario) # Inicia sesión automáticamente
            return redirect('emprendimientos')
    else:
        form = RegistroForm()
    return render(request, 'login/registro.html', {'form': form})
