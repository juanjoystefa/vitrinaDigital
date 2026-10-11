from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Emprendimiento, Vistas, Perfil
from .forms import EmprendimientoForm, RegistroForm

# ==========================================
# 1. VISTAS PÚBLICAS
# ==========================================

def inicio(request):
    if request.method == "POST":
        form = EmprendimientoForm(request.POST)
        if form.is_valid():
            # Por defecto, el modelo guardará el estado como 'pendiente'
            form.save()
            return redirect("emprendimientos") 
    else:
        form = EmprendimientoForm()
        
    # Solo mostramos los emprendimientos que ya fueron aceptados ('activo')
    emprendimientos = Emprendimiento.objects.filter(estado='activo').order_by("-totalVistas")

    return render(request, "emprendimientos/emprendimientos.html", {
        "emprendimientos": emprendimientos,
        "form": form,
    })

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
# 2. VISTAS DEL PANEL DE ADMINISTRACIÓN
# ==========================================

def admin_dashboard(request):
    # Nota: Aquí deberías validar si el usuario logueado tiene el rol 'admin'
    
    # Capturamos lo que el admin escriba en los buscadores
    query = request.GET.get('q', '')

    # Consultamos las 3 tablas
    pendientes = Emprendimiento.objects.filter(estado='pendiente')
    usuarios = Perfil.objects.all()
    todos_emprendimientos = Emprendimiento.objects.all().order_by("-totalVistas")

    # Si hay una búsqueda, filtramos los resultados
    if query:
        pendientes = pendientes.filter(nombre__icontains=query)
        usuarios = usuarios.filter(Q(usuario__username__icontains=query) | Q(usuario__email__icontains=query))
        todos_emprendimientos = todos_emprendimientos.filter(nombre__icontains=query)

    return render(request, "admin/admin_dashboard.html", {
        "pendientes": pendientes,
        "usuarios": usuarios,
        "emprendimientos": todos_emprendimientos,
        "query": query
    })

def cambiar_estado_emprendimiento(request, id, nuevo_estado):
    # Esta vista se ejecuta cuando el admin da clic en "Aceptar" o "Rechazar"
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    
    # Validamos que el estado exista y lo actualizamos
    if nuevo_estado in dict(Emprendimiento.ESTADOS).keys():
        emprendimiento.estado = nuevo_estado
        emprendimiento.save()
        
    return redirect('admin_dashboard')

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


# ================================
# VISTA DE INICIO (Actualizada)
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