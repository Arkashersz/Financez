from django.shortcuts import render
from perfil.models import Categoria
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def update_valor_categoria(request, id):
    return HttpResponse(id)