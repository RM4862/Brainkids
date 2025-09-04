
from django.contrib import admin
from .models import Cuento, Linea


from django.contrib import admin

class LineaInline(admin.TabularInline):
	model = Linea
	extra = 1

@admin.register(Cuento)
class CuentoAdmin(admin.ModelAdmin):
	inlines = [LineaInline]
