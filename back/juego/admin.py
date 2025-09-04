
from django.contrib import admin
from .models import Cuento, Linea


from django.contrib import admin


class LineaInline(admin.TabularInline):
	model = Linea
	extra = 1

def generar_pictogramas_cuento(modeladmin, request, queryset):
	for cuento in queryset:
		for linea in cuento.lineas.all():
			linea.generar_pictogramas()
	modeladmin.message_user(request, "Pictogramas generados para todas las líneas seleccionadas.")

generar_pictogramas_cuento.short_description = "Generar pictogramas para todas las líneas del cuento"

@admin.register(Cuento)
class CuentoAdmin(admin.ModelAdmin):
	inlines = [LineaInline]
	actions = [generar_pictogramas_cuento]
