# core/views.py
import json
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

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
    return render(request, 'rrhh/dashboard.html')


@login_required
def dashboard_admin(request):
    if _rol_de(request.user) != 'admin':
        return redirect('dash_empleado')
    return render(request, 'rrhh/dashboard_admin.html')


@login_required
def horario_jornada_page(request):
    # visible para empleados; si quieres que admin también la vea, quita el if
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')
    return render(request, 'rrhh/horario_jornada.html')


@login_required
def liquidacion_page(request):
    # visible para empleados
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')
    return render(request, 'rrhh/liquidacion.html')


@login_required
def contratos_admin_page(request):
    # visible para admin
    if _rol_de(request.user) != 'admin':
        return redirect('dash_empleado')
    return render(request, 'rrhh/contratos_admin.html')


@login_required
def contrato_admin_page(request):
    # visible para admin
    if _rol_de(request.user) != 'admin':
        return redirect('dash_empleado')
    return render(request, 'rrhh/contrato.html')


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
    # Renderiza el contrato del empleado
    return render(request, 'rrhh/contrato.html')

@login_required
def liquidaciones_admin_page(request):
    # Listado de liquidaciones para el admin
    return render(request, 'rrhh/liquidacion.html')   # cambia el template si usas otro
