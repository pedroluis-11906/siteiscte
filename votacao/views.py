from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Questao, Opcao, Aluno
from django.urls import reverse

import os


def test_superuser(user):
    return user.is_superuser


def index(request):
    if 'error_message' in request.session:
        del request.session['error_message']

    if request.user.is_authenticated:
        try:
            aluno = Aluno.objects.get(user=request.user)
            request.session['num_votos'] = aluno.num_votos

        except (KeyError, Aluno.DoesNotExist):
            pass

        pic_list = os.listdir('votacao/static/media/')
        fs = FileSystemStorage()
        for filename in pic_list:
            if filename.startswith(request.user.username + '_'):
                profile_pic_url = fs.url(filename)
                request.session['profile_pic_url'] = profile_pic_url
                break

    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}

    return render(request, 'votacao/index.html', context)


@login_required(login_url='/votacao/fazlogin')
def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao, })


@login_required(login_url='/votacao/fazlogin')
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


@login_required(login_url='/votacao/fazlogin')
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
                return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao_id,)))
        except (KeyError, Aluno.DoesNotExist):
            pass

        opcao_selecionada.votos += 1
        opcao_selecionada.save()

    return HttpResponseRedirect(reverse('votacao:resultados', args=(questao_id,)))


@user_passes_test(test_superuser, login_url='/votacao/')
def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')


@user_passes_test(test_superuser, login_url='/votacao/')
def inserirquestao(request):
    questao_texto = request.POST['questaotexto']
    print(questao_texto)
    if questao_texto:
        questao = Questao(questao_texto=questao_texto, pub_data=timezone.now())
        questao.save()
        return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request, 'votacao/criarquestao.html', {'error_message': "Introduza o texto da questão!"})


@user_passes_test(test_superuser, login_url='/votacao/')
def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})


@user_passes_test(test_superuser, login_url='/votacao/')
def inseriropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
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


@login_required(login_url='/votacao/fazlogin')
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


@login_required(login_url='/votacao/fazlogin')
def verperfil(request):
    return render(request, 'votacao/verperfil.html',)


@user_passes_test(test_superuser, login_url='/votacao/')
def apagarquestao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))


@user_passes_test(test_superuser, login_url='/votacao/')
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


@login_required(login_url='/votacao/fazlogin')
def upload_profimg(request):
    if request.method == 'POST' and 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        pic_list = os.listdir('votacao/static/media/')
        for fn in pic_list:
            if fn.startswith(request.user.username + '_'):
                os.remove('votacao/static/media/' + fn)
                break

        filename = fs.save(request.user.username + '_' + myfile.name, myfile)
        profile_pic_url = fs.url(filename)
        request.session['profile_pic_url'] = profile_pic_url
        return HttpResponseRedirect(reverse('votacao:verperfil'))
    return HttpResponseRedirect(reverse('votacao:verperfil'))
