import re
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from .serializers import ActivosSerializer, ParamTiposActivoSerializer
from .models import Activo, ParamTipoActivo 
from .models import Riesgo, CatalogoAmenaza, CatalogoVulnerabilidad
from .serializers import RiesgoSerializer, CatalogoAmenazaSerializer, CatalogoVulnerabilidadSerializer
from .models import CatalogoISO, ControlEmpresa, TratamientoRiesgo, HistorialTratamientoRiesgo
from .serializers import CatalogoISOSerializer, ControlEmpresaSerializer, TratamientoRiesgoSerializer, HistorialTratamientoSerializer2

# 1. Listar TODOS los activos y crear NUEVOS (GET y POST)
@api_view(['GET', 'POST'])
def lista_activos(request):
    if request.method == 'GET':
        activos_db = Activo.objects.all()
        traductor = ActivosSerializer(activos_db, many=True)
        return Response(traductor.data)

    elif request.method == 'POST':
        traductor = ActivosSerializer(data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data, status=status.HTTP_201_CREATED)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Traer las categorías (GET)
@api_view(['GET'])
def lista_tipos_activo(request):
    tipos_db = ParamTipoActivo.objects.all()
    traductor = ParamTiposActivoSerializer(tipos_db, many=True)
    return Response(traductor.data)


# 3. Leer, MODIFICAR o ELIMINAR un activo específico (GET, PUT, DELETE)
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_activo(request, pk):
    try:
        activo = Activo.objects.get(pk=pk)
    except Activo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        traductor = ActivosSerializer(activo)
        return Response(traductor.data)

    elif request.method == 'PUT':
        traductor = ActivosSerializer(activo, data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ========================================================
# 4. SISTEMA DE LOGIN Y REGISTRO (Mapeado a auth_user)
# ========================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def registro_usuario(request):
    first_name = (request.data.get('first_name') or '').strip()
    last_name = (request.data.get('last_name') or '').strip()
    email = (request.data.get('email') or '').strip()
    password = request.data.get('password') or ''
    password_confirm = request.data.get('password_confirm') or ''

    # --- Campos obligatorios ---
    if not first_name or not last_name or not email or not password:
        return Response({'error': 'Nombre, apellido, correo y contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

    if len(first_name) < 2:
        return Response({'error': 'El nombre debe tener al menos 2 caracteres'}, status=status.HTTP_400_BAD_REQUEST)

    if len(last_name) < 2:
        return Response({'error': 'El apellido debe tener al menos 2 caracteres'}, status=status.HTTP_400_BAD_REQUEST)

    # --- Correo válido y único ---
    try:
        validate_email(email)
    except DjangoValidationError:
        return Response({'error': 'El correo electrónico no es válido'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email__iexact=email).exists():
        return Response({'error': 'El correo ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

    # --- Confirmación de contraseña ---
    if password != password_confirm:
        return Response({'error': 'Las contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

    # --- Requisitos de contraseña segura ---
    requisitos_faltantes = []
    if len(password) < 8:
        requisitos_faltantes.append('al menos 8 caracteres')
    if not re.search(r'[A-Z]', password):
        requisitos_faltantes.append('una letra mayúscula')
    if not re.search(r'[a-z]', password):
        requisitos_faltantes.append('una letra minúscula')
    if not re.search(r'\d', password):
        requisitos_faltantes.append('un número')
    if not re.search(r'[^A-Za-z0-9]', password):
        requisitos_faltantes.append('un carácter especial')

    if requisitos_faltantes:
        return Response(
            {'error': f'La contraseña debe tener {", ".join(requisitos_faltantes)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_password(password)
    except DjangoValidationError as e:
        return Response({'error': ' '.join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

    # --- Username autogenerado a partir del correo (el usuario inicia sesión con su correo) ---
    username_base = re.sub(r'[^A-Za-z0-9_.]', '', email.split('@')[0]) or 'usuario'
    username = username_base
    contador = 1
    while User.objects.filter(username=username).exists():
        username = f'{username_base}{contador}'
        contador += 1

    # Crea el usuario encriptando la clave de forma automática en SQL Server
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return Response({'message': 'Usuario creado exitosamente', 'username': username}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def lista_amenazas(request):
    datos = CatalogoAmenaza.objects.all()
    return Response(CatalogoAmenazaSerializer(datos, many=True).data)

@api_view(['GET'])
def lista_vulnerabilidades(request):
    datos = CatalogoVulnerabilidad.objects.all()
    return Response(CatalogoVulnerabilidadSerializer(datos, many=True).data)

@api_view(['GET', 'POST'])
def lista_riesgos(request):
    if request.method == 'GET':
        riesgos_db = Riesgo.objects.all().order_by('-fecha_registro')
        return Response(RiesgoSerializer(riesgos_db, many=True).data)
    elif request.method == 'POST':
        traductor = RiesgoSerializer(data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data, status=status.HTTP_201_CREATED)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_riesgo(request, pk):
    try:
        riesgo = Riesgo.objects.get(pk=pk)
    except Riesgo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(RiesgoSerializer(riesgo).data)
    elif request.method == 'PUT':
        traductor = RiesgoSerializer(riesgo, data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        riesgo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):
    # El usuario inicia sesión con su correo; se acepta 'username' por compatibilidad.
    email = (request.data.get('email') or request.data.get('username') or '').strip()
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Ingresa tu correo y contraseña'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario_db = User.objects.get(email__iexact=email)
        username = usuario_db.username
    except User.DoesNotExist:
        username = email  # permite seguir iniciando sesión con username directo si ya lo conoce

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'Inicio de sesión correcto'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Este usuario está deshabilitado'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Credenciales incorrectas, intenta de nuevo'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def lista_catalogo_iso(request):
    datos = CatalogoISO.objects.all().order_by('id_control')
    return Response(CatalogoISOSerializer(datos, many=True).data)

@api_view(['GET', 'POST'])
def lista_controles_empresa(request):
    if request.method == 'GET':
        datos = ControlEmpresa.objects.all()
        return Response(ControlEmpresaSerializer(datos, many=True).data)
    elif request.method == 'POST':
        traductor = ControlEmpresaSerializer(data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data, status=status.HTTP_201_CREATED)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_control_empresa(request, pk):
    try:
        control = ControlEmpresa.objects.get(pk=pk)
    except ControlEmpresa.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ControlEmpresaSerializer(control).data)

    elif request.method == 'PUT':
        traductor = ControlEmpresaSerializer(control, data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        control.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def lista_tratamientos(request):
    if request.method == 'GET':
        datos = TratamientoRiesgo.objects.all().order_by('-fecha_actualizacion')
        return Response(TratamientoRiesgoSerializer(datos, many=True).data)
    elif request.method == 'POST':
        traductor = TratamientoRiesgoSerializer(data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data, status=status.HTTP_201_CREATED)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_tratamiento(request, pk):
    try:
        tratamiento = TratamientoRiesgo.objects.get(pk=pk)
    except TratamientoRiesgo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TratamientoRiesgoSerializer(tratamiento).data)
    elif request.method == 'PUT':
        traductor = TratamientoRiesgoSerializer(tratamiento, data=request.data)
        if traductor.is_valid():
            traductor.save()
            return Response(traductor.data)
        return Response(traductor.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tratamiento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)