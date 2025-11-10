# core/views.py
import json
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from .forms import ContratoForm
from .models import contrato
from django.core.paginator import Paginator
from django.db.models import Q
from .models import empleado, liquidacion, jornada, turno_has_jornada


User = get_user_model()

def _empleado_de_usuario(user):
    """
    Retorna el empleado enlazado al usuario autenticado.
    Tu modelo se llama 'empleado' y el campo es 'user' (OneToOne).
    """
    return empleado.objects.select_related('user').get(user=user)

def _contrato_actual(emp: empleado):
    """
    Retorna el contrato más reciente del empleado.
    Si quieres filtrar por estado 'Vigente', agrega .filter(estado="Vigente").
    """
    return (contrato.objects
            .filter(empleado=emp)
            .order_by('-fecha_inicio')
            .first())


def _rol_de(user):
    # Admin si es superuser/staff o pertenece al grupo "Admin"
    if user.is_superuser or user.is_staff or user.groups.filter(name__iexact='Admin').exists():
        return 'admin'
    return 'empleado'


# ---------- PÁGINAS ----------
def login_page(request):
    # si ya está logueado, redirige según rol
    if request.user.is_authenticated:
        return redirect('dash_admin' if _rol_de(request.user) == 'admin' else 'dash_empleado')
    return render(request, 'rrhh/login.html')


@login_required
def dashboard_empleado(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    cto = _contrato_actual(emp)

    # últimas 2 liquidaciones (tu modelo usa 'periodo' y 'liquido')
    liqs = (liquidacion.objects
            .filter(contrato__empleado=emp)
            .order_by('-periodo')[:2])

    # Horario derivado de turno_has_jornada del contrato actual
    horarios = []
    if cto and cto.turno_has_jornada_id:
        thj = cto.turno_has_jornada  # -> turno + jornada
        horarios = [{
            "dia": "-",  # tu esquema no tiene 'día' por jornada
            "entrada": thj.turno.hora_entrada,
            "salida": thj.turno.hora_salida,
            "descanso": "-",
            "observacion": thj.jornada.nombre,
        }]

    ctx = {
        "emp": emp,
        "contrato": cto,
        "liquidaciones": liqs,
        "horarios": horarios,
    }
    return render(request, 'rrhh/dashboard.html', ctx)


@login_required
def dashboard_admin(request):
    if _rol_de(request.user) != 'admin':
        return redirect('dash_empleado')

    # empleado del admin (si existe)
    admin_emp = None
    try:
        admin_emp = empleado.objects.select_related('user', 'zona_trabajo').get(user=request.user)
    except empleado.DoesNotExist:
        pass

    # sus liquidaciones (derivadas por contrato)
    admin_liqs = []
    if admin_emp:
        admin_liqs = (liquidacion.objects
                      .filter(contrato__empleado=admin_emp)
                      .order_by('-periodo')[:2])

    # listado de empleados con cargo/horario/zona
    q = request.GET.get('q', '').strip()
    empleados_qs = empleado.objects.select_related('user', 'zona_trabajo').all().order_by('id')
    if q:
        empleados_qs = empleados_qs.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q)  |
            Q(run__icontains=q) |
            Q(zona_trabajo__nombre__icontains=q)
        )

    def _contrato_actual_emp(e):
        return (contrato.objects
                .filter(empleado=e)
                .order_by('-fecha_inicio')
                .first())

    empleados_data = []
    for e in empleados_qs:
        cto = _contrato_actual_emp(e)
        cargo_nombre = cto.cargo.nombre if cto else "—"
        horario_str = "—"
        if cto and cto.turno_has_jornada_id:
            t = cto.turno_has_jornada.turno
            j = cto.turno_has_jornada.jornada
            horario_str = f"{t.hora_entrada.strftime('%H:%M')}-{t.hora_salida.strftime('%H:%M')} ({j.nombre})"
        empleados_data.append({
            "id": e.id,
            "nombre": (e.user.get_full_name() or e.user.username),
            "cargo": cargo_nombre,
            "zona": (e.zona_trabajo.nombre if e.zona_trabajo_id else "—"),
            "horario": horario_str,
        })

    return render(request, 'rrhh/dashboard_admin.html', {
        "empleados": empleados_data,
        "q": q,
        "admin_emp": admin_emp,
        "admin_liqs": admin_liqs,
    })


@login_required
def horario_jornada_page(request):
    # visible para empleados; si quieres que admin también la vea, quita el if
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')
    return render(request, 'rrhh/horario_jornada.html')



@login_required
def horario_page(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    cto = _contrato_actual(emp)

    horarios = []
    if cto and cto.turno_has_jornada_id:
        thj = cto.turno_has_jornada
        horarios = [{
            "dia": "-",
            "entrada": thj.turno.hora_entrada,
            "salida": thj.turno.hora_salida,
            "descanso": "-",
            "zona": "-",          # no existe FK a ZonaTrabajo en tu esquema
            "observacion": thj.jornada.nombre,
        }]

    return render(request, 'rrhh/horario.html', {
        "emp": emp,
        "horarios": horarios
    })


@login_required
def liquidacion_page(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    qs = (liquidacion.objects
          .filter(contrato__empleado=emp)
          .order_by('-periodo'))

    last = request.session.get('liq_last_page', 1)
    page_number = request.GET.get('page') or last
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page_number)
    request.session['liq_last_page'] = page_obj.number

    return render(request, 'rrhh/liquidacion.html', {
        "emp": emp,
        "page_obj": page_obj
    })

def is_admin(u):
    return u.is_authenticated and u.is_staff

@login_required
@user_passes_test(is_admin, login_url='/')
def contratos_admin_page(request):
    contratos = contrato.objects.select_related('empleado', 'departamento', 'cargo').order_by('-fecha_inicio')
    return render(request, 'rrhh/contratos_admin.html', {'contratos': contratos})

@login_required
@user_passes_test(is_admin, login_url='/')
def contrato_create(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato creado correctamente.')
            return redirect('contratos_admin')
    else:
        form = ContratoForm()
    return render(request, 'rrhh/contrato_form.html', {'form': form, 'titulo': 'Nuevo contrato'})

@login_required
@user_passes_test(is_admin, login_url='/')
def contrato_edit(request, pk):
    obj = get_object_or_404(contrato, pk=pk)
    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato actualizado.')
            return redirect('contratos_admin')
    else:
        form = ContratoForm(instance=obj)
    return render(request, 'rrhh/contrato_form.html', {'form': form, 'titulo': 'Editar contrato'})

@login_required
@user_passes_test(is_admin, login_url='/')
def contrato_delete(request, pk):
    obj = get_object_or_404(contrato, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Contrato eliminado.')
        return redirect('contratos_admin')
    return render(request, 'rrhh/contrato_confirm_delete.html', {'obj': obj})


# ---------- API ----------
@csrf_exempt
def login_json(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'msg': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not email or not password:
        return JsonResponse({'ok': False, 'msg': 'Faltan credenciales'}, status=400)

    try:
        u = User.objects.get(email__iexact=email)
        username = u.get_username()
    except User.DoesNotExist:
        return JsonResponse({'ok': False, 'msg': 'Usuario no encontrado o inactivo'}, status=401)

    user = authenticate(request, username=username, password=password)
    if not user or not user.is_active:
        return JsonResponse({'ok': False, 'msg': 'Credenciales inválidas'}, status=401)

    login(request, user)
    rol = _rol_de(user)
    return JsonResponse({'ok': True, 'user': {'id': user.id, 'email': user.email, 'rol': rol}})


def logout_view(request):
    logout(request)
    return redirect('login_page')


@login_required
def me(request):
    return JsonResponse({'email': request.user.email, 'rol': _rol_de(request.user)})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def horario_admin_page(request):
    # Puedes reutilizar el mismo template del empleado
    return render(request, 'rrhh/horario_jornada.html')

@login_required
def contrato_empleado_page(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    cto = _contrato_actual(emp)
    return render(request, 'rrhh/contrato.html', {"emp": emp, "contrato": cto})

@login_required
def liquidaciones_admin_page(request):
    # Listado de liquidaciones para el admin
    return render(request, 'rrhh/liquidaciones_admin.html')   # cambia el template si usas otro

def is_admin(u):  # solo staff entra al CRUD
    return u.is_authenticated and u.is_staff

@user_passes_test(is_admin)
def crud_cargo_page(request):
    return render(request, 'rrhh/crud_cargo.html')
