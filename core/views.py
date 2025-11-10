import json
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import empleado, liquidacion, jornada, turno_has_jornada,ZonaTrabajo,contrato,turno,cargo
from .forms import EmpleadoZonaForm, ZonaTrabajoForm
from django.contrib import messages
from .forms import ContratoForm
from .forms import CargoForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect



User = get_user_model()


def _empleado_de_usuario(user):
    return empleado.objects.select_related('user').get(user=user)


def _contrato_actual(emp: empleado):
    return (contrato.objects
            .filter(empleado=emp)
            .order_by('-fecha_inicio')
            .first())


def _rol_de(user):
    if user.is_superuser or user.is_staff or user.groups.filter(name__iexact='Admin').exists():
        return 'admin'
    return 'empleado'


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dash_admin' if _rol_de(request.user) == 'admin' else 'dash_empleado')
    return render(request, 'rrhh/login.html')


@login_required
def dashboard_empleado(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    cto = _contrato_actual(emp)

    liqs = (liquidacion.objects
            .filter(contrato__empleado=emp)
            .order_by('-periodo')[:2])

    horarios = []
    thj = None

    # 1) Solo intentamos traer la relación si realmente hay FK
    if cto and getattr(cto, "turno_has_jornada_id", None):
        try:
            thj = cto.turno_has_jornada  # <-- ESTA línea faltaba en tu código
        except ObjectDoesNotExist:
            thj = None

    # 2) Si existe la relación y sus sub-objetos, armamos el horario; si no, ponemos guiones
    if thj and getattr(thj, "turno", None) and getattr(thj, "jornada", None):
        horarios = [{
            "dia": "-",
            "entrada": thj.turno.hora_entrada,
            "salida": thj.turno.hora_salida,
            "descanso": "-",
            "observacion": thj.jornada.nombre,
        }]
    else:
        horarios = [{
            "dia": "-",
            "entrada": "-",
            "salida": "-",
            "descanso": "-",
            "observacion": "-",
        }]


    return render(request, 'rrhh/dashboard.html', {
        "emp": emp,
        "contrato": cto,
        "liquidaciones": liqs,
        "horarios": horarios,
    })


@login_required
def dashboard_admin(request):
    if _rol_de(request.user) != 'admin':
        return redirect('dash_empleado')

    try:
        admin_emp = empleado.objects.select_related('user', 'zona_trabajo').get(user=request.user)
    except empleado.DoesNotExist:
        admin_emp = None

    admin_liqs = []
    if admin_emp:
        admin_liqs = (liquidacion.objects
                      .filter(contrato__empleado=admin_emp)
                      .order_by('-periodo')[:2])

    q = request.GET.get('q', '').strip()
    empleados_qs = empleado.objects.select_related('user', 'zona_trabajo').order_by('id')
    if q:
        empleados_qs = empleados_qs.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(run__icontains=q) |
            Q(zona_trabajo__nombre__icontains=q)
        )

    empleados_data = []
    for e in empleados_qs:
        cto = _contrato_actual(e)
        cargo_nombre = cto.cargo.nombre if cto else "—"

        # ✅ Evita error jornada.DoesNotExist
        horario_str = "-"

        if cto and getattr(cto, "turno_has_jornada_id", None):
            try:
                thj = cto.turno_has_jornada  # esta línea puede lanzar RelatedObjectDoesNotExist
                turno = getattr(thj, "turno", None)
                jornada = getattr(thj, "jornada", None)
                ent = getattr(turno, "hora_entrada", None)
                sal = getattr(turno, "hora_salida", None)
                nom = getattr(jornada, "nombre", None)

                if ent and sal and nom:
                    # Si son TimeField/DatetimeField, strftime; si ya son str, conviértelo con str()
                    ent_txt = ent.strftime("%H:%M") if hasattr(ent, "strftime") else str(ent)
                    sal_txt = sal.strftime("%H:%M") if hasattr(sal, "strftime") else str(sal)
                    horario_str = f"{ent_txt}-{sal_txt} ({nom})"
                else:
                    horario_str = "-"
            except (ObjectDoesNotExist, AttributeError):
                horario_str = "-"
        else:
             horario_str = "-"
        empleados_data.append({
            "id": e.id,
            "nombre": e.user.get_full_name() or e.user.username,
            "cargo": cargo_nombre,
            "zona": e.zona_trabajo.nombre if e.zona_trabajo_id else "—",
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
    return redirect('horario_jornada')


@login_required
def horario_page(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    cto = _contrato_actual(emp)

    horarios = []
    if cto and cto.turno_has_jornada_id:
        thj = cto.turno_has_jornada
        if thj and thj.turno and thj.jornada:
            horarios = [{
                "dia": "-",
                "entrada": thj.turno.hora_entrada,
                "salida": thj.turno.hora_salida,
                "descanso": "-",
                "zona": "-",
                "observacion": thj.jornada.nombre,
            }]

    return render(request, 'rrhh/horario.html', {"emp": emp, "horarios": horarios})


@login_required
def liquidacion_page(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    qs = liquidacion.objects.filter(contrato__empleado=emp).order_by('-periodo')

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
    contratos_qs = contrato.objects.select_related('empleado', 'departamento', 'cargo').order_by('-fecha_inicio')
    return render(request, 'rrhh/contratos_admin.html', {'contratos': contratos_qs})


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

# ---------------------------
# CRUD Zonas de Trabajo
# ---------------------------
@login_required
@user_passes_test(is_admin, login_url='/')
def zonas_list(request):
    q = request.GET.get("q", "").strip()

    zonas = ZonaTrabajo.objects.all().order_by("nombre")
    if q:
        zonas = zonas.filter(
            Q(nombre__icontains=q) |
            Q(area__icontains=q) |
            Q(ubicacion__icontains=q) |
            Q(supervisor__icontains=q)
        )

    paginator = Paginator(zonas, 5)               # ← 5 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)    # ← objeto de página

    return render(request, "rrhh/zonas_list.html", {
        "q": q,
        "page_obj": page_obj,                     # ← pásalo al template
    })

@login_required
@user_passes_test(is_admin, login_url='/')
def zona_create(request):
    if request.method == "POST":
        form = ZonaTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona creada correctamente.")
            return redirect("zonas_list")
    else:
        form = ZonaTrabajoForm()
    return render(request, "rrhh/zona_form.html", {"form": form, "titulo": "Nueva zona"})

@login_required
@user_passes_test(is_admin, login_url='/')
def zona_edit(request, pk):
    z = get_object_or_404(ZonaTrabajo, pk=pk)
    if request.method == "POST":
        form = ZonaTrabajoForm(request.POST, instance=z)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona actualizada.")
            return redirect("zonas_list")
    else:
        form = ZonaTrabajoForm(instance=z)
    return render(request, "rrhh/zona_form.html", {"form": form, "titulo": "Editar zona"})

@login_required
@user_passes_test(is_admin, login_url='/')
def zona_delete(request, pk):
    z = get_object_or_404(ZonaTrabajo, pk=pk)
    if request.method == "POST":
        z.delete()
        messages.success(request, "Zona eliminada.")
        return redirect("zonas_list")
    return render(request, "rrhh/zona_confirm_delete.html", {"obj": z})

# ---------------------------
# Asignar/Cambiar zona a Empleado
# ---------------------------
@login_required
@user_passes_test(is_admin, login_url='/')
def empleado_zonas_list(request):
    q = request.GET.get("q", "").strip()
    emps = empleado.objects.select_related("user", "zona_trabajo").order_by("id")
    if q:
        emps = emps.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(run__icontains=q) |
            Q(zona_trabajo__nombre__icontains=q)
        )
    return render(request, "rrhh/empleado_zonas_list.html", {"empleados": emps, "q": q})

@login_required
@user_passes_test(is_admin, login_url='/')
def empleado_zona_edit(request, pk):
    emp = get_object_or_404(empleado.objects.select_related("user", "zona_trabajo"), pk=pk)
    if request.method == "POST":
        form = EmpleadoZonaForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona asignada/actualizada para el empleado.")
            return redirect("empleado_zonas_list")
    else:
        form = EmpleadoZonaForm(instance=emp)

    return render(
        request,
        "rrhh/empleado_zona_form.html",
        {"form": form, "empleado": emp, "titulo": f"Zona de {emp.user.get_full_name() or emp.user.username}"}
    )


# ✅ CRUD HORARIOS
@login_required
@user_passes_test(is_admin, login_url='/')
def horario_jornada_list(request):
    horarios = turno_has_jornada.objects.select_related('turno', 'jornada').all()
    return render(request, 'rrhh/horario_jornada.html', {"horarios": horarios})


@login_required
@user_passes_test(is_admin, login_url='/')
def horario_jornada_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        inicio = request.POST.get("hora_inicio")
        fin = request.POST.get("hora_fin")

        j = jornada.objects.create(nombre=nombre, horas_semanales=40)
        t = turno.objects.create(hora_entrada=inicio, hora_salida=fin)
        turno_has_jornada.objects.create(turno=t, jornada=j)

        messages.success(request, "Horario creado correctamente.")
        return redirect('horario_jornada')

    return redirect('horario_jornada')


@login_required
@user_passes_test(is_admin, login_url='/')
def horario_jornada_update(request, pk):
    h = get_object_or_404(turno_has_jornada, pk=pk)

    if request.method == "POST":
        h.jornada.nombre = request.POST.get("nombre")
        h.turno.hora_entrada = request.POST.get("hora_inicio")
        h.turno.hora_salida = request.POST.get("hora_fin")

        h.jornada.save()
        h.turno.save()

        messages.success(request, "Horario actualizado.")
        return redirect('horario_jornada')

    return redirect('horario_jornada')


@login_required
@user_passes_test(is_admin, login_url='/')
def horario_jornada_delete(request, pk):
    h = get_object_or_404(turno_has_jornada, pk=pk)
    h.turno.delete()
    h.jornada.delete()
    h.delete()
    messages.success(request, "Horario eliminado.")
    return redirect('horario_jornada')


def logout_view(request):
    logout(request)
    return redirect('login_page')


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


@login_required
def me(request):
    return JsonResponse({'email': request.user.email, 'rol': _rol_de(request.user)})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def horario_admin_page(request):
    return redirect('horario_jornada')


@login_required
def contrato_empleado_page(request):
    if _rol_de(request.user) != 'empleado':
        return redirect('dash_admin')

    emp = _empleado_de_usuario(request.user)
    cto = _contrato_actual(emp)
    return render(request, 'rrhh/contrato.html', {"emp": emp, "contrato": cto})


@login_required
def liquidaciones_admin_page(request):
    return render(request, 'rrhh/liquidaciones_admin.html')


def is_admin(u):
    return u.is_authenticated and u.is_staff


@user_passes_test(is_admin)
def crud_cargo_page(request):
    return render(request, 'rrhh/crud_cargo.html')

@login_required
def liquidaciones_list(request):
    """
    Lista las liquidaciones del empleado asociado al usuario logueado.
    Sirve para /dashboard/liquidaciones/ y /dashboard-admin/liquidaciones/
    """
    # localizar empleado del usuario
    emp = None
    try:
        emp = empleado.objects.get(user=request.user)
    except empleado.DoesNotExist:
        emp = None

    qs = liquidacion.objects.none()
    if emp:
        qs = (liquidacion.objects
              .filter(contrato__empleado=emp)
              .select_related('contrato')
              .order_by('-periodo'))

    # paginación
    paginator = Paginator(qs, 10)  # 10 filas por página (ajusta si quieres)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # para el botón "Volver al dashboard"
    back_name = 'dash_admin' if _rol_de(request.user) == 'admin' else 'dash_empleado'

    context = {
        'page_obj': page_obj,
        'liqs': page_obj.object_list,    # comodidad en el template
        'back_name': back_name,
    }
    return render(request, 'rrhh/liquidaciones_list.html', context)



@login_required
def horario_jornada(request):
    horarios = turno_has_jornada.objects.select_related('turno', 'jornada').all()
    return render(request, 'rrhh/horario_jornada.html', {
        'horarios': horarios
    })
@login_required
def horario_create(request):
    turnos = turno.objects.all()
    jornadas = jornada.objects.all()

    if request.method == 'POST':
        t = request.POST.get('turno')
        j = request.POST.get('jornada')
        turno_sel = turno.objects.get(pk=t)
        jornada_sel = jornada.objects.get(pk=j)

        turno_has_jornada.objects.create(turno=turno_sel, jornada=jornada_sel)

        messages.success(request, "Horario creado correctamente ✅")
        return redirect('horario_jornada')

    return render(request, 'rrhh/horario_form.html', {
        'turnos': turnos,
        'jornadas': jornadas
    })



@login_required
def horario_update(request, pk):
    horario = get_object_or_404(turno_has_jornada, id=pk)
    turnos = turno.objects.all()
    jornadas = jornada.objects.all()

    if request.method == "POST":
        horario.turno = get_object_or_404(turno, id=request.POST.get('turno'))
        horario.jornada = get_object_or_404(jornada, id=request.POST.get('jornada'))
        horario.save()
        return redirect('horario_jornada')

    return render(request, 'rrhh/horario_form.html', {
        'horario': horario,
        'turnos': turnos,
        'jornadas': jornadas,
        'accion': 'Editar'
    })


@login_required
def horario_delete(request, pk):
    horario = get_object_or_404(turno_has_jornada, id=pk)
    horario.delete()
    return redirect('horario_jornada')

#CRUD Cargos

@login_required
def gestion_cargos(request):
    q = request.GET.get("q", "").strip()
    cargos = cargo.objects.all().order_by("id")   # si tu BaseModel filtra por status y no ves nada, usa cargo._base_manager.all()
    if q:
        cargos = cargos.filter(Q(nombre__icontains=q) | Q(description__icontains=q))
    return render(request, "rrhh/crud_cargo.html", {"cargos": cargos, "q": q})

@login_required
def cargo_create(request):
    if request.method == "POST":
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo creado correctamente.")
            return redirect("crud_cargo")
    else:
        form = CargoForm()
    return render(request, "rrhh/cargo_form.html", {"form": form, "title": "Nuevo Cargo"})

@login_required
def cargo_edit(request, pk):
    obj = get_object_or_404(cargo, pk=pk)
    if request.method == "POST":
        form = CargoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo actualizado.")
            return redirect("crud_cargo")
    else:
        form = CargoForm(instance=obj)
    return render(request, "rrhh/cargo_form.html", {"form": form, "title": "Editar Cargo"})

@login_required
def cargo_delete(request, pk):
    obj = get_object_or_404(cargo, pk=pk)
    if request.method == "POST":
        # Si prefieres “borrado lógico”, comenta la línea siguiente y marca status='INACTIVE'
        obj.delete()
        messages.success(request, "Cargo eliminado.")
        return redirect("crud_cargo")
    return render(request, "rrhh/cargo_confirm_delete.html", {"obj": obj})

@login_required
def empleado_cargo_edit(request, pk):
    emp = get_object_or_404(empleado, pk=pk)
    cargos = cargo.objects.order_by("nombre")

    if request.method == "POST":
        cargo_id = request.POST.get("cargo_id", "").strip()
        emp.cargo = cargo.objects.get(pk=cargo_id) if cargo_id else None
        emp.save(update_fields=["cargo"])
        messages.success(request, "Cargo actualizado correctamente.")
        return redirect("empleado_cargo_edit", pk=emp.id)

    ctx = {"emp": emp, "cargos": cargos}
    return render(request, "rrhh/empleado_cargo_edit.html", ctx)