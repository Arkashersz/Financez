from django.shortcuts import render
from perfil.models import Categoria

# Create your views here.
def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})