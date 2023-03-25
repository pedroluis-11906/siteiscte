from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Questao, Opcao, Aluno
from django.urls import reverse


def index(request):
    if 'error_message' in request.session:
        del request.session['error_message']

    if request.user.is_authenticated:
        try:
            aluno = Aluno.objects.get(user=request.user)
            request.session['num_votos'] = aluno.num_votos
            print(request.session['num_votos'])
        except (KeyError, Aluno.DoesNotExist):
            pass

    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}

    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao, })


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_selecionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta novo form para votar
        return render(request, 'votacao/detalhe.html',
                      {'questao': questao,
                       'error_message': "Não escolheu uma opção",
                       })
    else:
        try:
            aluno = Aluno.objects.get(user=request.user)
            if aluno.num_votos < 19:
                aluno.num_votos += 1
                aluno.save()
            else:
                request.session['error_message'] = 'O Aluno atingiu o número de votos permitido'
                return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao_id, )))
        except (KeyError, Aluno.DoesNotExist):
            pass

        opcao_selecionada.votos += 1
        opcao_selecionada.save()

    return HttpResponseRedirect(reverse('votacao:resultados', args=(questao_id,)))


def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')


def inserirquestao(request):
    questao_texto = request.POST['questaotexto']
    print(questao_texto)
    if questao_texto:
        questao = Questao(questao_texto=questao_texto, pub_data=timezone.now())
        questao.save()
        return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request, 'votacao/criarquestao.html', {'error_message': "Introduza o texto da questao!"})


def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})


def inseriropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    # usar questao.opcao_set.create()
    opcaotexto = request.POST['opcaotexto']
    if opcaotexto:
        questao.opcao_set.create(questao=questao, opcao_texto=opcaotexto)
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao_id,)))
    else:
        return render(request, 'votacao/criaropcao.html',
                      {'questao': questao, 'error_message': "Introduza o texto da opcão!"})


def fazlogin(request):
    if request.method == 'POST':
        # tratar os dados do form de login, neste caso username e password
        name = request.POST['username']
        passwd = request.POST['password']

        u = authenticate(username=name, password=passwd)
        if u is not None:
            login(request, u)
            return HttpResponseRedirect(reverse('votacao:index'))

        else:
            # return do formulário de login
            return render(request, 'votacao/login.html', {'msg_erro': 'Credenciais inválidas!'})
    else:
        return render(request, 'votacao/login.html')


def fazlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))


def registar(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        passwd = request.POST['password']
        curso = request.POST['curso']

        u = User.objects.create_user(username=name, email=email, password=passwd)
        Aluno.objects.create(user=u, curso=curso)
        return HttpResponseRedirect(reverse('votacao:fazlogin'))
    return render(request, 'votacao/registar.html')


@login_required
def verperfil(request):
    aluno = Aluno.objects.get(user=request.user)
    return render(request, 'votacao/verperfil.html', {'aluno': aluno})


def apagarquestao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))


def apagaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_selecionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/detalhe.html',
                      {'questao': questao,
                       'error_message': "Não escolheu uma opção",
                       })
    else:
        opcao_selecionada.delete()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao_id,)))