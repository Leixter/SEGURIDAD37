from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if not username or not email or not password:
        return Response({'error': 'Todos los campos son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'El nombre de usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        
    if User.objects.filter(email=email).exists():
        return Response({'error': 'El correo ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8:
        return Response({'error': 'La contraseña debe tener al menos 8 caracteres'}, status=status.HTTP_400_BAD_REQUEST)

    # Crea el usuario encriptando la clave de forma automática en SQL Server
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)

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
    username = request.data.get('username')
    password = request.data.get('password')

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