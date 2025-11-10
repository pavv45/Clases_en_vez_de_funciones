"""
CONSULTAS ORM - Sistema de Nóminas
Estudiante: [Tu Nombre]
Fecha: [Fecha actual]
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PracticaExp1.settings')
django.setup()

# Importar modelos
from nomina.models import Empleado, Nomina, NominaDetalle
from prestamos.models import Prestamo, TipoPrestamo
from sobretiempo.models import Sobretiempo, TipoSobretiempo
from django.db.models import Sum, Avg, Count, Max, Min, Q, F
from datetime import date, datetime

print("=" * 80)
print("CONSULTAS ORM - SISTEMA DE NÓMINAS")
print("=" * 80)

# ============================================================================
# 1. MODELO EMPLEADO
# ============================================================================

print("\n" + "=" * 80)
print("1. MODELO EMPLEADO")
print("=" * 80)

# --- 1.1 CREAR 5 EMPLEADOS ---
print("\n--- 1.1 CREAR 5 EMPLEADOS ---")

empleados_crear = [
    {
        'cedula': '1234567890',
        'nombre': 'Juan Pérez',
        'departamento': 'Ventas',
        'cargo': 'Vendedor',
        'sueldo': 1200.00,
        'fecha_ingreso': date(2024, 1, 15)
    },
    {
        'cedula': '0987654321',
        'nombre': 'María López',
        'departamento': 'Contabilidad',
        'cargo': 'Contador',
        'sueldo': 1500.00,
        'fecha_ingreso': date(2023, 6, 10)
    },
    {
        'cedula': '1122334455',
        'nombre': 'Carlos Mendoza',
        'departamento': 'Sistemas',
        'cargo': 'Desarrollador',
        'sueldo': 1800.00,
        'fecha_ingreso': date(2024, 3, 20)
    },
    {
        'cedula': '5544332211',
        'nombre': 'Ana Rodríguez',
        'departamento': 'Recursos Humanos',
        'cargo': 'Asistente',
        'sueldo': 1100.00,
        'fecha_ingreso': date(2023, 9, 5)
    },
    {
        'cedula': '6677889900',
        'nombre': 'Pedro Gómez',
        'departamento': 'Ventas',
        'cargo': 'Gerente',
        'sueldo': 2000.00,
        'fecha_ingreso': date(2022, 2, 1)
    }
]

for emp_data in empleados_crear:
    try:
        empleado = Empleado.objects.create(**emp_data)
        print(f"✅ Empleado creado: {empleado.nombre} - {empleado.cargo}")
    except Exception as e:
        print(f"❌ Error creando empleado: {e}")


# --- 1.2 ACTUALIZAR 5 EMPLEADOS ---
print("\n--- 1.2 ACTUALIZAR 5 EMPLEADOS ---")

# Actualización 1: Con update()
count = Empleado.objects.filter(cedula='1234567890').update(sueldo=1300.00)
print(f"✅ Actualizado 1: {count} empleado(s) - Sueldo aumentado")

# Actualización 2: Con save()
try:
    empleado = Empleado.objects.get(cedula='0987654321')
    empleado.cargo = 'Contador Senior'
    empleado.save()
    print(f"✅ Actualizado 2: {empleado.nombre} - Cargo cambiado a {empleado.cargo}")
except:
    print("❌ Empleado no encontrado")

# Actualización 3: Cambiar departamento
count = Empleado.objects.filter(cedula='1122334455').update(departamento='TI')
print(f"✅ Actualizado 3: {count} empleado(s) - Departamento cambiado")

# Actualización 4: Aumentar sueldo a todos de Ventas
count = Empleado.objects.filter(departamento='Ventas').update(sueldo=1400.00)
print(f"✅ Actualizado 4: {count} empleado(s) de Ventas - Sueldo aumentado")

# Actualización 5: Cambiar fecha de ingreso
count = Empleado.objects.filter(cedula='6677889900').update(fecha_ingreso=date(2022, 1, 15))
print(f"✅ Actualizado 5: {count} empleado(s) - Fecha de ingreso actualizada")


# --- 1.3 LISTAR 10 EMPLEADOS CON FILTROS ---
print("\n--- 1.3 LISTAR 10 EMPLEADOS CON FILTROS ---")

# Consulta 1: Todos los empleados
print("\n1. Todos los empleados:")
empleados = Empleado.objects.all()
for emp in empleados:
    print(f"   - {emp.nombre} ({emp.cargo})")

# Consulta 2: Empleados con sueldo mayor a 1200
print("\n2. Empleados con sueldo > 1200:")
empleados = Empleado.objects.filter(sueldo__gt=1200)
for emp in empleados:
    print(f"   - {emp.nombre}: ${emp.sueldo}")

# Consulta 3: Empleados del departamento que contenga 'Ventas'
print("\n3. Empleados de Ventas:")
empleados = Empleado.objects.filter(departamento__icontains='Ventas')
for emp in empleados:
    print(f"   - {emp.nombre} - {emp.departamento}")

# Consulta 4: Empleados cuyo nombre empieza con 'M'
print("\n4. Empleados cuyo nombre empieza con 'M':")
empleados = Empleado.objects.filter(nombre__startswith='M')
for emp in empleados:
    print(f"   - {emp.nombre}")

# Consulta 5: Empleados cuyo nombre termina con 'ez'
print("\n5. Empleados cuyo nombre termina con 'ez':")
empleados = Empleado.objects.filter(nombre__endswith='ez')
for emp in empleados:
    print(f"   - {emp.nombre}")

# Consulta 6: Empleados con sueldo entre 1000 y 1500
print("\n6. Empleados con sueldo entre 1000 y 1500:")
empleados = Empleado.objects.filter(sueldo__range=[1000, 1500])
for emp in empleados:
    print(f"   - {emp.nombre}: ${emp.sueldo}")

# Consulta 7: Empleados que NO son de Ventas
print("\n7. Empleados que NO son de Ventas:")
empleados = Empleado.objects.exclude(departamento='Ventas')
for emp in empleados:
    print(f"   - {emp.nombre} - {emp.departamento}")

# Consulta 8: Obtener un empleado por cédula
print("\n8. Empleado por cédula específica:")
try:
    empleado = Empleado.objects.get(cedula='1234567890')
    print(f"   - {empleado.nombre} - {empleado.cargo}")
except:
    print("   - Empleado no encontrado")

# Consulta 9: Empleados ingresados en 2024
print("\n9. Empleados ingresados en 2024:")
empleados = Empleado.objects.filter(fecha_ingreso__year=2024)
for emp in empleados:
    print(f"   - {emp.nombre} - Ingreso: {emp.fecha_ingreso}")

# Consulta 10: Empleados con sueldo menor a 1200
print("\n10. Empleados con sueldo < 1200:")
empleados = Empleado.objects.filter(sueldo__lt=1200)
for emp in empleados:
    print(f"   - {emp.nombre}: ${emp.sueldo}")


# --- 1.4 ELIMINAR 2 EMPLEADOS ---
print("\n--- 1.4 ELIMINAR 2 EMPLEADOS ---")

# Eliminación 1: Eliminar por cédula específica
try:
    empleado = Empleado.objects.get(cedula='1234567890')
    nombre = empleado.nombre
    empleado.delete()
    print(f"✅ Eliminado 1: {nombre}")
except:
    print("❌ Empleado no encontrado para eliminar")

# Eliminación 2: Eliminar empleados con sueldo menor a 1000
count = Empleado.objects.filter(sueldo__lt=1000).delete()
print(f"✅ Eliminado 2: {count[0]} empleado(s) con sueldo < 1000")


# ============================================================================
# 2. MODELO PRÉSTAMO
# ============================================================================

print("\n" + "=" * 80)
print("2. MODELO PRÉSTAMO")
print("=" * 80)

# --- 2.1 CREAR 5 PRÉSTAMOS ---
print("\n--- 2.1 CREAR 5 PRÉSTAMOS ---")

# Obtener empleados y tipos de préstamo existentes
empleados_disponibles = Empleado.objects.all()[:5]
tipos_prestamo = TipoPrestamo.objects.all()

if empleados_disponibles.exists() and tipos_prestamo.exists():
    prestamos_crear = [
    {
        'empleado': empleados_disponibles[0],
        'tipo_prestamo': tipos_prestamo[0],
        'fecha_prestamo': date(2024, 1, 10),
        'monto': Decimal('500.00'),
        'numero_cuotas': 12
    },
    {
        'empleado': empleados_disponibles[1] if len(empleados_disponibles) > 1 else empleados_disponibles[0],
        'tipo_prestamo': tipos_prestamo[0],
        'fecha_prestamo': date(2024, 2, 15),
        'monto': Decimal('800.00'),
        'numero_cuotas': 24
    },
    {
        'empleado': empleados_disponibles[2] if len(empleados_disponibles) > 2 else empleados_disponibles[0],
        'tipo_prestamo': tipos_prestamo[1] if len(tipos_prestamo) > 1 else tipos_prestamo[0],
        'fecha_prestamo': date(2024, 3, 5),
        'monto': Decimal('1200.00'),
        'numero_cuotas': 18
    },
    {
        'empleado': empleados_disponibles[3] if len(empleados_disponibles) > 3 else empleados_disponibles[0],
        'tipo_prestamo': tipos_prestamo[0],
        'fecha_prestamo': date(2023, 12, 20),
        'monto': Decimal('300.00'),
        'numero_cuotas': 6
    },
    {
        'empleado': empleados_disponibles[4] if len(empleados_disponibles) > 4 else empleados_disponibles[0],
        'tipo_prestamo': tipos_prestamo[1] if len(tipos_prestamo) > 1 else tipos_prestamo[0],
        'fecha_prestamo': date(2024, 4, 1),
        'monto': Decimal('1500.00'),
        'numero_cuotas': 36
    }
]

    
    for prestamo_data in prestamos_crear:
        try:
            prestamo = Prestamo.objects.create(**prestamo_data)
            print(f"✅ Préstamo creado: {prestamo.empleado.nombre} - ${prestamo.monto}")
        except Exception as e:
            print(f"❌ Error creando préstamo: {e}")
else:
    print("❌ No hay empleados o tipos de préstamo disponibles")


# --- 2.2 ACTUALIZAR 5 PRÉSTAMOS ---
print("\n--- 2.2 ACTUALIZAR 5 PRÉSTAMOS ---")

# Actualización 1: Cambiar número de cuotas
prestamos = Prestamo.objects.all()[:1]
if prestamos.exists():
    count = Prestamo.objects.filter(id=prestamos[0].id).update(numero_cuotas=10)
    print(f"✅ Actualizado 1: {count} préstamo(s) - Cuotas cambiadas a 10")
else:
    print("❌ No hay préstamos para actualizar")

# Actualización 2: Actualizar monto con save()
prestamos = Prestamo.objects.all()[1:2]
if prestamos.exists():
    try:
        prestamo = prestamos[0]
        prestamo.monto = Decimal('900.00')
        prestamo.save()
        print(f"✅ Actualizado 2: Préstamo de {prestamo.empleado.nombre} - Monto: ${prestamo.monto}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Actualización 3: Cambiar fecha de préstamo
prestamos = Prestamo.objects.all()[2:3]
if prestamos.exists():
    count = Prestamo.objects.filter(id=prestamos[0].id).update(fecha_prestamo=date(2024, 5, 1))
    print(f"✅ Actualizado 3: {count} préstamo(s) - Fecha actualizada")

# Actualización 4: Actualizar cuotas de préstamos mayores a 1000
count = Prestamo.objects.filter(monto__gt=1000).update(numero_cuotas=30)
print(f"✅ Actualizado 4: {count} préstamo(s) > $1000 - Cuotas a 30")

# Actualización 5: Cambiar tipo de préstamo
prestamos = Prestamo.objects.all()[3:4]
if prestamos.exists() and tipos_prestamo.exists():
    count = Prestamo.objects.filter(id=prestamos[0].id).update(tipo_prestamo=tipos_prestamo[0])
    print(f"✅ Actualizado 5: {count} préstamo(s) - Tipo cambiado")


# --- 2.3 LISTAR 10 PRÉSTAMOS CON FILTROS ---
print("\n--- 2.3 LISTAR 10 PRÉSTAMOS CON FILTROS ---")

# Consulta 1: Todos los préstamos
print("\n1. Todos los préstamos:")
prestamos = Prestamo.objects.all()
for p in prestamos:
    print(f"   - {p.empleado.nombre}: ${p.monto} - {p.numero_cuotas} cuotas")

# Consulta 2: Préstamos mayores o iguales a 500
print("\n2. Préstamos >= $500:")
prestamos = Prestamo.objects.filter(monto__gte=500)
for p in prestamos:
    print(f"   - {p.empleado.nombre}: ${p.monto}")

# Consulta 3: Préstamos menores o iguales a 1000
print("\n3. Préstamos <= $1000:")
prestamos = Prestamo.objects.filter(monto__lte=1000)
for p in prestamos:
    print(f"   - {p.empleado.nombre}: ${p.monto}")

# Consulta 4: Préstamos del año 2024
print("\n4. Préstamos del año 2024:")
prestamos = Prestamo.objects.filter(fecha_prestamo__year=2024)
for p in prestamos:
    print(f"   - {p.empleado.nombre} - Fecha: {p.fecha_prestamo}")

# Consulta 5: Préstamos en un rango de fechas
print("\n5. Préstamos entre enero y marzo 2024:")
prestamos = Prestamo.objects.filter(fecha_prestamo__range=[date(2024, 1, 1), date(2024, 3, 31)])
for p in prestamos:
    print(f"   - {p.empleado.nombre} - {p.fecha_prestamo}")

# Consulta 6: Préstamos de un tipo específico
print("\n6. Préstamos por tipo:")
if tipos_prestamo.exists():
    prestamos = Prestamo.objects.filter(tipo_prestamo=tipos_prestamo[0])
    for p in prestamos:
        print(f"   - {p.empleado.nombre} - Tipo: {p.tipo_prestamo.descripcion}")

# Consulta 7: Préstamos con más de 12 cuotas
print("\n7. Préstamos con más de 12 cuotas:")
prestamos = Prestamo.objects.filter(numero_cuotas__gt=12)
for p in prestamos:
    print(f"   - {p.empleado.nombre}: {p.numero_cuotas} cuotas")

# Consulta 8: Préstamos de un empleado específico
print("\n8. Préstamos por empleado:")
if empleados_disponibles.exists():
    prestamos = Prestamo.objects.filter(empleado=empleados_disponibles[0])
    for p in prestamos:
        print(f"   - ${p.monto} - {p.fecha_prestamo}")

# Consulta 9: Préstamos ordenados por monto descendente
print("\n9. Préstamos ordenados por monto (mayor a menor):")
prestamos = Prestamo.objects.all().order_by('-monto')[:5]
for p in prestamos:
    print(f"   - {p.empleado.nombre}: ${p.monto}")

# Consulta 10: Préstamos con saldo pendiente
print("\n10. Préstamos con saldo pendiente:")
prestamos = Prestamo.objects.filter(saldo__gt=0)
for p in prestamos:
    print(f"   - {p.empleado.nombre}: Saldo ${p.saldo}")


# --- 2.4 ELIMINAR 2 PRÉSTAMOS ---
print("\n--- 2.4 ELIMINAR 2 PRÉSTAMOS ---")

# Eliminación 1: Eliminar préstamos con monto menor a 400
count = Prestamo.objects.filter(monto__lt=400).delete()
print(f"✅ Eliminado 1: {count[0]} préstamo(s) con monto < $400")

# Eliminación 2: Eliminar un préstamo específico
prestamos_eliminar = Prestamo.objects.all()[:1]
if prestamos_eliminar.exists():
    try:
        prestamo = prestamos_eliminar[0]
        empleado_nombre = prestamo.empleado.nombre
        prestamo.delete()
        print(f"✅ Eliminado 2: Préstamo de {empleado_nombre}")
    except Exception as e:
        print(f"❌ Error eliminando préstamo: {e}")
else:
    print("❌ No hay préstamos para eliminar")
    
    
    
    # ============================================================================
# 3. MODELO SOBRETIEMPO
# ============================================================================

print("\n" + "=" * 80)
print("3. MODELO SOBRETIEMPO")
print("=" * 80)

# --- 3.1 CREAR 5 SOBRETIEMPOS ---
print("\n--- 3.1 CREAR 5 SOBRETIEMPOS ---")

# Obtener empleados y tipos de sobretiempo existentes
empleados_disponibles = Empleado.objects.all()[:5]
tipos_sobretiempo = TipoSobretiempo.objects.all()

if empleados_disponibles.exists() and tipos_sobretiempo.exists():
    sobretiempos_crear = [
        {
            'empleado': empleados_disponibles[0],
            'fecha_registro': date(2024, 10, 5),
            'tipo_sobretiempo': tipos_sobretiempo[0],
            'numero_horas': Decimal('8.0')
        },
        {
            'empleado': empleados_disponibles[1] if len(empleados_disponibles) > 1 else empleados_disponibles[0],
            'fecha_registro': date(2024, 10, 10),
            'tipo_sobretiempo': tipos_sobretiempo[1] if len(tipos_sobretiempo) > 1 else tipos_sobretiempo[0],
            'numero_horas': Decimal('12.5')
        },
        {
            'empleado': empleados_disponibles[2] if len(empleados_disponibles) > 2 else empleados_disponibles[0],
            'fecha_registro': date(2024, 10, 15),
            'tipo_sobretiempo': tipos_sobretiempo[0],
            'numero_horas': Decimal('6.0')
        },
        {
            'empleado': empleados_disponibles[3] if len(empleados_disponibles) > 3 else empleados_disponibles[0],
            'fecha_registro': date(2024, 11, 1),
            'tipo_sobretiempo': tipos_sobretiempo[1] if len(tipos_sobretiempo) > 1 else tipos_sobretiempo[0],
            'numero_horas': Decimal('10.0')
        },
        {
            'empleado': empleados_disponibles[4] if len(empleados_disponibles) > 4 else empleados_disponibles[0],
            'fecha_registro': date(2024, 11, 5),
            'tipo_sobretiempo': tipos_sobretiempo[0],
            'numero_horas': Decimal('15.5')
        }
    ]
    
    for sobretiempo_data in sobretiempos_crear:
        try:
            sobretiempo = Sobretiempo.objects.create(**sobretiempo_data)
            print(f"✅ Sobretiempo creado: {sobretiempo.empleado.nombre} - {sobretiempo.numero_horas} hrs - ${sobretiempo.valor:.2f}")
        except Exception as e:
            print(f"❌ Error creando sobretiempo: {e}")
else:
    print("❌ No hay empleados o tipos de sobretiempo disponibles")


# --- 3.2 ACTUALIZAR 5 SOBRETIEMPOS ---
print("\n--- 3.2 ACTUALIZAR 5 SOBRETIEMPOS ---")

# Actualización 1: Cambiar número de horas
sobretiempos = Sobretiempo.objects.all()[:1]
if sobretiempos.exists():
    sobretiempo = sobretiempos[0]
    sobretiempo.numero_horas = Decimal('10.0')
    sobretiempo.save()
    print(f"✅ Actualizado 1: {sobretiempo.empleado.nombre} - {sobretiempo.numero_horas} hrs")
else:
    print("❌ No hay sobretiempos para actualizar")

# Actualización 2: Cambiar fecha de registro
sobretiempos = Sobretiempo.objects.all()[1:2]
if sobretiempos.exists():
    count = Sobretiempo.objects.filter(id=sobretiempos[0].id).update(fecha_registro=date(2024, 11, 10))
    print(f"✅ Actualizado 2: {count} sobretiempo(s) - Fecha actualizada")

# Actualización 3: Cambiar tipo de sobretiempo
sobretiempos = Sobretiempo.objects.all()[2:3]
if sobretiempos.exists() and tipos_sobretiempo.exists():
    count = Sobretiempo.objects.filter(id=sobretiempos[0].id).update(tipo_sobretiempo=tipos_sobretiempo[0])
    print(f"✅ Actualizado 3: {count} sobretiempo(s) - Tipo cambiado")

# Actualización 4: Actualizar horas de sobretiempos mayores a 10
sobretiempos = Sobretiempo.objects.filter(numero_horas__gt=10)
if sobretiempos.exists():
    for st in sobretiempos:
        st.numero_horas = Decimal('12.0')
        st.save()
    print(f"✅ Actualizado 4: {sobretiempos.count()} sobretiempo(s) con > 10 hrs")

# Actualización 5: Cambiar fecha de un rango
count = Sobretiempo.objects.filter(
    fecha_registro__range=[date(2024, 11, 1), date(2024, 11, 30)]
).update(fecha_registro=date(2024, 11, 15))
print(f"✅ Actualizado 5: {count} sobretiempo(s) de noviembre")


# --- 3.3 LISTAR 10 SOBRETIEMPOS CON FILTROS ---
print("\n--- 3.3 LISTAR 10 SOBRETIEMPOS CON FILTROS ---")

# Consulta 1: Todos los sobretiempos
print("\n1. Todos los sobretiempos:")
sobretiempos = Sobretiempo.objects.all()
for st in sobretiempos:
    print(f"   - {st.empleado.nombre}: {st.numero_horas} hrs - ${st.valor:.2f}")

# Consulta 2: Sobretiempos con más de 8 horas
print("\n2. Sobretiempos con más de 8 horas:")
sobretiempos = Sobretiempo.objects.filter(numero_horas__gt=8)
for st in sobretiempos:
    print(f"   - {st.empleado.nombre}: {st.numero_horas} hrs")

# Consulta 3: Sobretiempos de noviembre 2024
print("\n3. Sobretiempos de noviembre 2024:")
sobretiempos = Sobretiempo.objects.filter(
    fecha_registro__year=2024,
    fecha_registro__month=11
)
for st in sobretiempos:
    print(f"   - {st.empleado.nombre} - {st.fecha_registro}")

# Consulta 4: Sobretiempos por rango de fechas
print("\n4. Sobretiempos entre octubre y noviembre 2024:")
sobretiempos = Sobretiempo.objects.filter(
    fecha_registro__range=[date(2024, 10, 1), date(2024, 11, 30)]
)
for st in sobretiempos:
    print(f"   - {st.empleado.nombre} - {st.fecha_registro}")

# Consulta 5: Sobretiempos de un empleado específico
print("\n5. Sobretiempos por empleado:")
if empleados_disponibles.exists():
    sobretiempos = Sobretiempo.objects.filter(empleado=empleados_disponibles[0])
    for st in sobretiempos:
        print(f"   - {st.numero_horas} hrs - {st.fecha_registro}")

# Consulta 6: Sobretiempos por tipo
print("\n6. Sobretiempos por tipo:")
if tipos_sobretiempo.exists():
    sobretiempos = Sobretiempo.objects.filter(tipo_sobretiempo=tipos_sobretiempo[0])
    for st in sobretiempos:
        print(f"   - {st.empleado.nombre} - Tipo: {st.tipo_sobretiempo.descripcion}")

# Consulta 7: Sobretiempos con valor mayor a 50
print("\n7. Sobretiempos con valor > $50:")
sobretiempos = Sobretiempo.objects.filter(valor__gt=50)
for st in sobretiempos:
    print(f"   - {st.empleado.nombre}: ${st.valor:.2f}")

# Consulta 8: Sobretiempos ordenados por horas descendente
print("\n8. Sobretiempos ordenados por horas (mayor a menor):")
sobretiempos = Sobretiempo.objects.all().order_by('-numero_horas')[:5]
for st in sobretiempos:
    print(f"   - {st.empleado.nombre}: {st.numero_horas} hrs")

# Consulta 9: Sobretiempos del año 2024
print("\n9. Sobretiempos del año 2024:")
sobretiempos = Sobretiempo.objects.filter(fecha_registro__year=2024)
for st in sobretiempos:
    print(f"   - {st.empleado.nombre} - {st.fecha_registro}")

# Consulta 10: Sobretiempos con menos de 10 horas
print("\n10. Sobretiempos con menos de 10 horas:")
sobretiempos = Sobretiempo.objects.filter(numero_horas__lt=10)
for st in sobretiempos:
    print(f"   - {st.empleado.nombre}: {st.numero_horas} hrs")


# --- 3.4 ELIMINAR 2 SOBRETIEMPOS ---
print("\n--- 3.4 ELIMINAR 2 SOBRETIEMPOS ---")

# Eliminación 1: Eliminar sobretiempos con menos de 5 horas
count = Sobretiempo.objects.filter(numero_horas__lt=5).delete()
print(f"✅ Eliminado 1: {count[0]} sobretiempo(s) con < 5 hrs")

# Eliminación 2: Eliminar un sobretiempo específico
sobretiempos_eliminar = Sobretiempo.objects.all()[:1]
if sobretiempos_eliminar.exists():
    try:
        sobretiempo = sobretiempos_eliminar[0]
        empleado_nombre = sobretiempo.empleado.nombre
        sobretiempo.delete()
        print(f"✅ Eliminado 2: Sobretiempo de {empleado_nombre}")
    except Exception as e:
        print(f"❌ Error eliminando sobretiempo: {e}")
else:
    print("❌ No hay sobretiempos para eliminar")
    
    
    # ============================================================================
# 4. MODELO NÓMINA
# ============================================================================

print("\n" + "=" * 80)
print("4. MODELO NÓMINA")
print("=" * 80)

# --- 4.1 CREAR 5 NÓMINAS ---
print("\n--- 4.1 CREAR 5 NÓMINAS ---")

nominas_crear = [
    {
        'aniomes': '202401',
        'fecha_generacion': date(2024, 1, 31),
        'descripcion': 'Nómina Enero 2024'
    },
    {
        'aniomes': '202402',
        'fecha_generacion': date(2024, 2, 29),
        'descripcion': 'Nómina Febrero 2024'
    },
    {
        'aniomes': '202403',
        'fecha_generacion': date(2024, 3, 31),
        'descripcion': 'Nómina Marzo 2024'
    },
    {
        'aniomes': '202404',
        'fecha_generacion': date(2024, 4, 30),
        'descripcion': 'Nómina Abril 2024'
    },
    {
        'aniomes': '202405',
        'fecha_generacion': date(2024, 5, 31),
        'descripcion': 'Nómina Mayo 2024'
    }
]

for nomina_data in nominas_crear:
    try:
        nomina = Nomina.objects.create(**nomina_data)
        print(f"✅ Nómina creada: {nomina.aniomes} - {nomina.descripcion}")
    except Exception as e:
        print(f"❌ Error creando nómina: {e}")


# --- 4.2 ACTUALIZAR 5 NÓMINAS ---
print("\n--- 4.2 ACTUALIZAR 5 NÓMINAS ---")

# Actualización 1: Cambiar descripción
nominas = Nomina.objects.filter(aniomes='202401')
if nominas.exists():
    count = nominas.update(descripcion='Nómina de Enero 2024 - Actualizada')
    print(f"✅ Actualizado 1: {count} nómina(s) - Descripción actualizada")

# Actualización 2: Cambiar fecha de generación con save()
nominas = Nomina.objects.filter(aniomes='202402')
if nominas.exists():
    nomina = nominas[0]
    nomina.fecha_generacion = date(2024, 2, 28)
    nomina.save()
    print(f"✅ Actualizado 2: Nómina {nomina.aniomes} - Fecha actualizada")

# Actualización 3: Actualizar descripción de varias nóminas
count = Nomina.objects.filter(aniomes__in=['202403', '202404']).update(
    descripcion='Nómina Trimestre 1'
)
print(f"✅ Actualizado 3: {count} nómina(s) - Descripción en lote")

# Actualización 4: Cambiar fecha de una nómina específica
nominas = Nomina.objects.filter(aniomes='202405')
if nominas.exists():
    count = nominas.update(fecha_generacion=date(2024, 5, 30))
    print(f"✅ Actualizado 4: {count} nómina(s) - Fecha cambiada")

# Actualización 5: Actualizar todas las nóminas de 2024
count = Nomina.objects.filter(aniomes__startswith='2024').update(
    descripcion='Nóminas año 2024'
)
print(f"✅ Actualizado 5: {count} nómina(s) del 2024")


# --- 4.3 LISTAR 10 NÓMINAS CON FILTROS ---
print("\n--- 4.3 LISTAR 10 NÓMINAS CON FILTROS ---")

# Consulta 1: Todas las nóminas
print("\n1. Todas las nóminas:")
nominas = Nomina.objects.all()
for n in nominas:
    print(f"   - {n.aniomes} - {n.descripcion}")

# Consulta 2: Nóminas del año 2024
print("\n2. Nóminas del año 2024:")
nominas = Nomina.objects.filter(aniomes__startswith='2024')
for n in nominas:
    print(f"   - {n.aniomes} - {n.fecha_generacion}")

# Consulta 3: Nóminas generadas en un rango de fechas
print("\n3. Nóminas generadas entre enero y marzo 2024:")
nominas = Nomina.objects.filter(
    fecha_generacion__range=[date(2024, 1, 1), date(2024, 3, 31)]
)
for n in nominas:
    print(f"   - {n.aniomes} - {n.fecha_generacion}")

# Consulta 4: Nómina específica por periodo
print("\n4. Nómina específica (202401):")
try:
    nomina = Nomina.objects.get(aniomes='202401')
    print(f"   - {nomina.aniomes} - {nomina.descripcion}")
except:
    print("   - Nómina no encontrada")

# Consulta 5: Nóminas que contengan 'Enero' en la descripción
print("\n5. Nóminas con 'Enero' en descripción:")
nominas = Nomina.objects.filter(descripcion__icontains='Enero')
for n in nominas:
    print(f"   - {n.aniomes} - {n.descripcion}")

# Consulta 6: Nóminas ordenadas por fecha descendente
print("\n6. Nóminas ordenadas por fecha (más reciente primero):")
nominas = Nomina.objects.all().order_by('-fecha_generacion')[:5]
for n in nominas:
    print(f"   - {n.aniomes} - {n.fecha_generacion}")

# Consulta 7: Nóminas de un mes específico
print("\n7. Nóminas que terminan en '01' (enero):")
nominas = Nomina.objects.filter(aniomes__endswith='01')
for n in nominas:
    print(f"   - {n.aniomes}")

# Consulta 8: Nóminas excluyendo un periodo
print("\n8. Nóminas excluyendo 202401:")
nominas = Nomina.objects.exclude(aniomes='202401')
for n in nominas:
    print(f"   - {n.aniomes}")

# Consulta 9: Nóminas generadas en mayo
print("\n9. Nóminas generadas en mayo:")
nominas = Nomina.objects.filter(
    fecha_generacion__year=2024,
    fecha_generacion__month=5
)
for n in nominas:
    print(f"   - {n.aniomes} - {n.fecha_generacion}")

# Consulta 10: Contar total de nóminas
print("\n10. Total de nóminas registradas:")
total = Nomina.objects.count()
print(f"   - Total: {total} nómina(s)")


# --- 4.4 ELIMINAR 2 NÓMINAS ---
print("\n--- 4.4 ELIMINAR 2 NÓMINAS ---")

# Eliminación 1: Eliminar nóminas antiguas
count = Nomina.objects.filter(aniomes='202401').delete()
print(f"✅ Eliminado 1: {count[0]} nómina(s) del periodo 202401")

# Eliminación 2: Eliminar una nómina específica
nominas_eliminar = Nomina.objects.filter(aniomes='202402')
if nominas_eliminar.exists():
    try:
        nomina = nominas_eliminar[0]
        periodo = nomina.aniomes
        nomina.delete()
        print(f"✅ Eliminado 2: Nómina del periodo {periodo}")
    except Exception as e:
        print(f"❌ Error eliminando nómina: {e}")
else:
    print("❌ No hay nóminas para eliminar")
    
    
    
    # ============================================================================
# 5. MODELO NÓMINA DETALLE
# ============================================================================

print("\n" + "=" * 80)
print("5. MODELO NÓMINA DETALLE")
print("=" * 80)

# --- 5.1 CREAR 5 DETALLES DE NÓMINA ---
print("\n--- 5.1 CREAR 5 DETALLES DE NÓMINA ---")

# Obtener nóminas y empleados disponibles
nominas_disponibles = Nomina.objects.all()[:3]
empleados_disponibles = Empleado.objects.all()[:5]

if nominas_disponibles.exists() and empleados_disponibles.exists():
    detalles_crear = []
    
    for i, empleado in enumerate(empleados_disponibles):
        if i < len(nominas_disponibles):
            nomina = nominas_disponibles[i % len(nominas_disponibles)]
        else:
            nomina = nominas_disponibles[0]
        
        detalle_data = {
            'nomina': nomina,
            'empleado': empleado,
            'sueldo': empleado.sueldo,
            'bono': empleado.sueldo * Decimal('0.1'),  # 10% de bono
            'prestamo': empleado.sueldo * Decimal('0.15'),  # 15% de descuentos
        }
        detalles_crear.append(detalle_data)
    
    for detalle_data in detalles_crear:
        try:
            # Verificar si ya existe
            existe = NominaDetalle.objects.filter(
                nomina=detalle_data['nomina'],
                empleado=detalle_data['empleado']
            ).exists()
            
            if not existe:
                detalle = NominaDetalle.objects.create(**detalle_data)
                print(f"✅ Detalle creado: {detalle.empleado.nombre} - Nómina {detalle.nomina.aniomes}")
            else:
                print(f"⚠️ Detalle ya existe: {detalle_data['empleado'].nombre}")
        except Exception as e:
            print(f"❌ Error creando detalle: {e}")
else:
    print("❌ No hay nóminas o empleados disponibles")


# --- 5.2 ACTUALIZAR 5 DETALLES ---
print("\n--- 5.2 ACTUALIZAR 5 DETALLES ---")

# Actualización 1: Cambiar ingresos
# Actualización 1: Cambiar bono
detalles = NominaDetalle.objects.all()[:1]
if detalles.exists():
    detalle = detalles[0]
    detalle.bono = 150.00
    detalle.save()
    print(f"✅ Actualizado 1: {detalle.empleado.nombre} - Bono: ${detalle.bono}")

# Actualización 2: Cambiar préstamo con update()
detalles = NominaDetalle.objects.all()[1:2]
if detalles.exists():
    count = NominaDetalle.objects.filter(id=detalles[0].id).update(prestamo=200.00)
    print(f"✅ Actualizado 2: {count} detalle(s) - Préstamo actualizado")

# Actualización 3: Actualizar todos los detalles de una nómina
if nominas_disponibles.exists():
    count = NominaDetalle.objects.filter(nomina=nominas_disponibles[0]).update(bono=100.00)
    print(f"✅ Actualizado 3: {count} detalle(s) de la nómina {nominas_disponibles[0].aniomes}")

# Actualización 4: Aumentar bono en 10%
detalles = NominaDetalle.objects.all()[:2]
for detalle in detalles:
    detalle.bono = detalle.bono * Decimal('1.10')
    detalle.save()
print(f"✅ Actualizado 4: Bono aumentado 10% a {detalles.count()} detalle(s)")

# Actualización 5: Cambiar sueldo
detalles = NominaDetalle.objects.all()[2:3]
if detalles.exists():
    count = NominaDetalle.objects.filter(id=detalles[0].id).update(sueldo=1500.00)
    print(f"✅ Actualizado 5: {count} detalle(s) - Sueldo actualizado")


# --- 5.3 LISTAR 10 DETALLES CON FILTROS Y JOINS ---
print("\n--- 5.3 LISTAR 10 DETALLES CON FILTROS Y JOINS ---")

# Consulta 1: Todos los detalles con datos de empleado y nómina
print("\n1. Todos los detalles:")
detalles = NominaDetalle.objects.select_related('empleado', 'nomina').all()
for d in detalles:
    print(f"   - {d.empleado.nombre} - Nómina: {d.nomina.aniomes} - Neto: ${d.neto:.2f}")

# Consulta 2: Detalles de una nómina específica
print("\n2. Detalles de una nómina específica:")
if nominas_disponibles.exists():
    detalles = NominaDetalle.objects.filter(nomina=nominas_disponibles[0])
    for d in detalles:
        print(f"   - {d.empleado.nombre}: ${d.neto:.2f}")

# Consulta 3: Detalles de un empleado específico
print("\n3. Detalles de un empleado específico:")
if empleados_disponibles.exists():
    detalles = NominaDetalle.objects.filter(empleado=empleados_disponibles[0])
    for d in detalles:
        print(f"   - Nómina {d.nomina.aniomes}: ${d.neto:.2f}")

# Consulta 4: Detalles con total mayor a 1000
print("\n4. Detalles con total > $1000:")
detalles = NominaDetalle.objects.filter(neto__gt=1000)
for d in detalles:
    print(f"   - {d.empleado.nombre}: ${d.neto:.2f}")

# Consulta 5: Detalles filtrando por nombre de empleado (JOIN)
print("\n5. Detalles de empleados cuyo nombre contiene 'a':")
detalles = NominaDetalle.objects.filter(empleado__nombre__icontains='a')
for d in detalles:
    print(f"   - {d.empleado.nombre} - ${d.neto:.2f}")

# Consulta 6: Detalles filtrando por periodo de nómina (JOIN)
print("\n6. Detalles de nóminas de 2024:")
detalles = NominaDetalle.objects.filter(nomina__aniomes__startswith='2024')
for d in detalles:
    print(f"   - {d.empleado.nombre} - Periodo: {d.nomina.aniomes}")

# Consulta 7: Detalles con ingresos mayores a 100
print("\n7. Detalles con bono > $100:")
detalles = NominaDetalle.objects.filter(bono__gt=100)
for d in detalles:
    print(f"   - {d.empleado.nombre}: bono ${d.bono:.2f}")

# Consulta 8: Detalles con egresos menores a 200
print("\n8. Detalles con prestamo < $200:")
detalles = NominaDetalle.objects.filter(prestamo__lt=200)
for d in detalles:
    print(f"   - {d.empleado.nombre}: Prestamo ${d.prestamo:.2f}")

# Consulta 9: Detalles ordenados por total descendente
print("\n9. Detalles ordenados por total (mayor a menor):")
detalles = NominaDetalle.objects.all().order_by('-neto')[:5]
for d in detalles:
    print(f"   - {d.empleado.nombre}: ${d.neto:.2f}")

# Consulta 10: Detalles por departamento del empleado (JOIN)
print("\n10. Detalles de empleados del departamento 'Ventas':")
detalles = NominaDetalle.objects.filter(empleado__departamento__icontains='Ventas')
for d in detalles:
    print(f"   - {d.empleado.nombre} - Dept: {d.empleado.departamento}")


# --- 5.4 ELIMINAR 2 DETALLES ---
print("\n--- 5.4 ELIMINAR 2 DETALLES ---")

# Eliminación 1: Eliminar detalles con total menor a 500
count = NominaDetalle.objects.filter(neto__lt=500).delete()
print(f"✅ Eliminado 1: {count[0]} detalle(s) con neto < $500")

# Eliminación 2: Eliminar un detalle específico
detalles_eliminar = NominaDetalle.objects.all()[:1]
if detalles_eliminar.exists():
    try:
        detalle = detalles_eliminar[0]
        empleado_nombre = detalle.empleado.nombre
        detalle.delete()
        print(f"✅ Eliminado 2: Detalle de {empleado_nombre}")
    except Exception as e:
        print(f"❌ Error eliminando detalle: {e}")
else:
    print("❌ No hay detalles para eliminar")
    
    
    
    # ============================================================================
# 6. CONSULTAS AGREGADAS Y ANOTADAS (10 consultas adicionales)
# ============================================================================

print("\n" + "=" * 80)
print("6. CONSULTAS AGREGADAS Y ANOTADAS")
print("=" * 80)

# Consulta 1: Total de préstamos por empleado
print("\n1. Total de préstamos por empleado:")
resultado = Prestamo.objects.values('empleado__nombre').annotate(
    total_monto=Sum('monto'),
    cantidad=Count('id')
).order_by('-total_monto')
for r in resultado:
    print(f"   - {r['empleado__nombre']}: ${r['total_monto']:.2f} ({r['cantidad']} préstamos)")

# Consulta 2: Promedio de sueldos por departamento
print("\n2. Promedio de sueldos por departamento:")
resultado = Empleado.objects.values('departamento').annotate(
    promedio_sueldo=Avg('sueldo'),
    total_empleados=Count('id')
).order_by('-promedio_sueldo')
for r in resultado:
    print(f"   - {r['departamento']}: ${r['promedio_sueldo']:.2f} ({r['total_empleados']} empleados)")

# Consulta 3: Total de horas extra acumuladas por empleado
print("\n3. Total de horas extra por empleado:")
resultado = Sobretiempo.objects.values('empleado__nombre').annotate(
    total_horas=Sum('numero_horas'),
    total_valor=Sum('valor')
).order_by('-total_horas')
for r in resultado:
    print(f"   - {r['empleado__nombre']}: {r['total_horas']} hrs - ${r['total_valor']:.2f}")

# Consulta 4: Total a pagar por nómina
# Consulta 4: Total a pagar por cada nómina
print("\n4. Total a pagar por cada nómina:")
resultado = NominaDetalle.objects.values('nomina__aniomes').annotate(
    total_pagar=Sum('neto'),
    cantidad_empleados=Count('empleado')
).order_by('-nomina__aniomes')
for r in resultado:
    print(f"   - Nómina {r['nomina__aniomes']}: ${r['total_pagar']:.2f} ({r['cantidad_empleados']} empleados)")


# Consulta 5: Número de empleados por año de ingreso
print("\n5. Número de empleados por año de ingreso:")
resultado = Empleado.objects.values('fecha_ingreso__year').annotate(
    total=Count('id')
).order_by('-fecha_ingreso__year')
for r in resultado:
    print(f"   - Año {r['fecha_ingreso__year']}: {r['total']} empleado(s)")

# Consulta 6: Sueldo máximo, mínimo y promedio general
print("\n6. Estadísticas generales de sueldos:")
resultado = Empleado.objects.aggregate(
    sueldo_max=Max('sueldo'),
    sueldo_min=Min('sueldo'),
    sueldo_promedio=Avg('sueldo'),
    total_empleados=Count('id')
)
print(f"   - Máximo: ${resultado['sueldo_max']:.2f}")
print(f"   - Mínimo: ${resultado['sueldo_min']:.2f}")
print(f"   - Promedio: ${resultado['sueldo_promedio']:.2f}")
print(f"   - Total empleados: {resultado['total_empleados']}")

# Consulta 7: Total de préstamos por tipo de préstamo
print("\n7. Total de préstamos por tipo:")
resultado = Prestamo.objects.values('tipo_prestamo__descripcion').annotate(
    total_monto=Sum('monto'),
    cantidad=Count('id'),
    promedio=Avg('monto')
).order_by('-total_monto')
for r in resultado:
    print(f"   - {r['tipo_prestamo__descripcion']}: ${r['total_monto']:.2f} ({r['cantidad']} préstamos, promedio: ${r['promedio']:.2f})")

# Consulta 8: Total de sobretiempos por tipo
print("\n8. Total de sobretiempos por tipo:")
resultado = Sobretiempo.objects.values('tipo_sobretiempo__descripcion').annotate(
    total_horas=Sum('numero_horas'),
    total_valor=Sum('valor'),
    cantidad=Count('id')
).order_by('-total_valor')
for r in resultado:
    print(f"   - {r['tipo_sobretiempo__descripcion']}: {r['total_horas']} hrs - ${r['total_valor']:.2f} ({r['cantidad']} registros)")

# Consulta 9: Empleados con sus totales de préstamos y sobretiempos
print("\n9. Resumen por empleado (préstamos y sobretiempos):")
empleados = Empleado.objects.all()[:5]  # Primeros 5 empleados
for emp in empleados:
    total_prestamos = Prestamo.objects.filter(empleado=emp).aggregate(total=Sum('monto'))['total'] or 0
    total_sobretiempos = Sobretiempo.objects.filter(empleado=emp).aggregate(total=Sum('valor'))['total'] or 0
    print(f"   - {emp.nombre}:")
    print(f"     Préstamos: ${total_prestamos:.2f}")
    print(f"     Sobretiempos: ${total_sobretiempos:.2f}")

# Consulta 10: Empleados por cargo con sueldo promedio
print("\n10. Empleados por cargo con estadísticas:")
resultado = Empleado.objects.values('cargo').annotate(
    cantidad=Count('id'),
    sueldo_promedio=Avg('sueldo'),
    sueldo_total=Sum('sueldo')
).order_by('-cantidad')
for r in resultado:
    print(f"   - {r['cargo']}: {r['cantidad']} empleado(s)")
    print(f"     Promedio: ${r['sueldo_promedio']:.2f}, Total: ${r['sueldo_total']:.2f}")


print("\n" + "=" * 80)
print("✅ FIN DE LAS CONSULTAS ORM")
print("=" * 80)