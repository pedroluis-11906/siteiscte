
from django.utils import timezone

from votacao.models import Questao, Opcao

#4.2 a)
def inserirQuestao(texto):
    q = Questao(questao_texto=texto, pub_data=timezone.now())
    q.save()

def inserirOpcao(pk, texto, votos):
    q = Questao.objects.get(pk=pk)
    q.opcao_set.create(opcao_texto=texto, votos=votos)

#4.3 a)
def verQuestoes():
    for q in Questao.objects.all():
        print(q)

#4.3 b)
def verQuestoes_textFilter(texto):
    for q in Questao.objects.filter(questao_texto__startswith=texto):
        print(q.opcao_set.all())
#4.3 c)
def verQuestoes_textVotesFilter(texto, numVotos):
    for q in Questao.objects.filter(questao_texto__startswith=texto):
        for v in q.opcao_set.all():
            if v.votos > numVotos:
                print(v)

def verQuestoes_textVotesFilterAlt(texto, numVotos):
    for q in Questao.objects.filter(questao_texto__startswith=texto):
        for o in q.opcao_set.filter(votos__gt=numVotos):
            print(o)


#4.3 d)
def verQuestoes_yearFilter(lastxYears):
    if lastxYears > 0:
        for q in Questao.objects.all():
            if q.pub_data.year > timezone.now().year - lastxYears:
                print(q)
    else:
        print('Insira um valor maior que 0.')



#4.4 a)
def totalVotos():
    count = 0
    for q in Questao.objects.all():
        for v in q.opcao_set.all():
            count = count + v.votos
    print('Numero total de votos na BD:', count)

#4.4 b)
def maisVotos():
    for q in Questao.objects.all():
        print('Texto da questao:', q.questao_texto)
        numVotos = 0
        opcao_texto = ''
        for v in q.opcao_set.all():
            if v.votos > numVotos:
                numVotos = v.votos
                opcao_texto = v.opcao_texto
        print('Texto da opcao com mais votos:', opcao_texto, '\n')




#4.2 a)
inserirQuestao('Gostas de programar para a internet?')
inserirOpcao(1, 'Adoro', 1)
inserirOpcao(1, 'Gosto', 5)
inserirOpcao(1, 'Mais ou menos', 3)
inserirOpcao(1, 'Nem por isso', 2)
inserirOpcao(1, 'Detesto', 1)

#4.2 b)
inserirQuestao('O Sporting vai ganhar a Liga Europa?')
inserirOpcao(2, 'Sim', 1906)
inserirOpcao(2, 'Não', 1)


#4.3 a)
#verQuestoes()

#4.3 b)
#verQuestoes_textFilter('Gostas de programar')
#verQuestoes_textFilter('O Sporting')

#4.3 c)
#verQuestoes_textVotesFilter('Gostas de programar', 2)
#verQuestoes_textVotesFilterAlt('Gostas de programar', 2)

#4.3 d)
#verQuestoes_yearFilter(3)

#4.4 a)
#totalVotos()

#4.4 b)
#maisVotos()



