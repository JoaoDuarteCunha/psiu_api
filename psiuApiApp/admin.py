from django.contrib import admin

# Register your models here.
from psiuApiApp.models import Atividade, Carona, ConhecerPessoas, Estudos, Extracurriculares, Liga
 
admin.site.register(Atividade) 
admin.site.register(Carona)
admin.site.register(Estudos) 
admin.site.register(Liga)
admin.site.register(Extracurriculares)
admin.site.register(ConhecerPessoas)  