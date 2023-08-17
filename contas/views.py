from django.shortcuts import render, redirect
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from datetime import datetime, timedelta

def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
        return redirect('/contas/definir_contas')

def atualizar_datas_pagamento():
    contas = ContaPagar.objects.filter(pago=False)
    for conta in contas:
        dias_apos_vencimento = datetime.now().day - conta.dia_pagamento
        if dias_apos_vencimento > 0:
            nova_data_pagamento = datetime.now() + timedelta(days=dias_apos_vencimento)
        else:
            nova_data_pagamento = datetime.now() - timedelta(days=abs(dias_apos_vencimento))
        conta.dia_pagamento = nova_data_pagamento.day
        conta.save()


def pagar_conta(request, conta_id):
    conta = ContaPagar.objects.get(pk=conta_id)
    if not conta.pago:
        conta.pago = True
        conta.save()
        conta_paga = ContaPaga(conta=conta, data_pagamento=datetime.now())
        conta_paga.save()
        messages.add_message(request, constants.SUCCESS, 'Conta paga com sucesso')
    return redirect('ver_contas')

def ver_contas(request):
    MES_ATUAL = datetime.now().month
    
    contas_vencidas = ContaPagar.objects.filter(dia_pagamento__lt=datetime.now().day, pago=False)
    contas_proximas_vencimento = ContaPagar.objects.filter(dia_pagamento__gte=datetime.now().day, dia_pagamento__lte=datetime.now().day + 5, pago=False)
    restantes = ContaPagar.objects.filter(dia_pagamento__gt=datetime.now().day + 5, pago=False)
    
    total_contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).count()

    return render(request, 'ver_contas.html', {'contas_vencidas': contas_vencidas, 
                                               'contas_proximas_vencimento': contas_proximas_vencimento, 
                                               'restantes': restantes, 
                                               'total_contas_pagas': total_contas_pagas
    })