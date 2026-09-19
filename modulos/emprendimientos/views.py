from django.shortcuts import render, redirect, get_object_or_404
from .models import Emprendimiento, Vistas
from .forms import EmprendimientoForm

def inicio(request):
    # 1. Procesar el formulario si se está enviando
    if request.method == "POST":
        form = EmprendimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inicio") # Recarga la página después de guardar
    else:
        form = EmprendimientoForm()
    # 2. Obtener los emprendimientos Ordenados por más visitas
    # EL signo menos antes del totalVisitas significa orden descendete (mayor a menor)
    emprendimientos = Emprendimiento.objects.all().order_by("-totalVistas")

    return render(request, "emprendimientos.html", {
        "emprendimientos": emprendimientos,
        "form": form,
    })

def registrar_visita(request, id):
    # Buscamos el emprendimiento al que le dieron clic
    emprendimiento = get_object_or_404(Emprendimiento, idEmprendimiento=id)
    
    # Creamos un nuevo registro en la tabla Visitas
    # Como en la Opción 1 modificamos el save(), esto automáticamente suma 1 a total_visitas
    Vistas.objects.create(idEmprendimiento=emprendimiento)
    
    # Redirigimos de vuelta a la página principal
    return redirect('inicio')