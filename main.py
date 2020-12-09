from datetime import datetime
from random import choice
import csv

mensagem_boas_vindas_madrugada = ["Olá, boa madrugada!",
                                  "Também não conseguiu dormir? Vamos Conversar!",
                                  "Boa madrugada, sou o chatbot da UACSA. Como posso te ajudar?"
                                  ]

mensagem_boas_vindas_manha = ["Olá, bom dia!",
                              "Bom dia, como vai?",
                              "Bom dia, sou o chatbot da UACSA. Como posso te ajudar?"
                              ]

mensagem_boas_vindas_tarde = ["Olá, boa tarde!",
                              "Boa tarde, sou o chatbot da UACSA. Como posso te ajudar?"]

mensagem_boas_vindas_noite = ["Olá, boa noite!",
                              "Boa noite, sou o chatbot da UACSA. Como posso te ajudar?"]

mensagem_erro = ["Desculpe, não entendi :/",
                 "Poderia escrever com outras palavras?",
                 "Hmmmm, essa eu não sei. Tente outra opção",
                 "Não entendi, poderia reformular a pergunta?"
                 ]

mensagem_despedida = ["Até logo!",
                      "Até mais!",
                      "Até a próxima!",
                      "Tchau, até logo!",
                      "Até breve!",
                      ]

# Função que escolhe a mensagem de boas vindas de acordo com o horário
def boas_vindas():
    now = datetime.now()
    hora = int(now.strftime("%H"))  # hora em que o programa foi executado
    if hora <= 4:
        return choice(mensagem_boas_vindas_madrugada)
    elif 4 < hora <= 11:
        return choice(mensagem_boas_vindas_manha)
    elif 11 < hora <= 18:
        return choice(mensagem_boas_vindas_tarde)
    elif hora > 18:
        return choice(mensagem_boas_vindas_noite)


print(boas_vindas())

print("\nOpções de Pesquisa:"
      "\n  -PLE"
      "\n  -Data de matrícula"
      "\n  -E-mail dos professores"
      "\n  -Uacsa"
      "\n  -Cursos"
      "\n  -Pesquisa"
      "\n  -Extensão"
      "\n  -Horário das disciplinas"
      "\n  -Calendário Acadêmico"
      "\n  -NAPS"
      "\n  -Apoio Pedagógico"
      "\nOu digite 0 para sair\n")


def resposta_email():
    reader = csv.DictReader(open('email.csv'))  # Abrindo o arquivo csv com nome e email dos professores
    dados_professores = []
    for line in reader:
        dados_professores.append(line)
    professor_requerido = input("Digite o nome do professor(a) >>> ").lower()
    continuar = True
    while continuar:
        possiveis_professores = []
        for professor in dados_professores:
            if professor_requerido in professor["nome"]:
                possiveis_professores.append(professor)
        if not possiveis_professores:
            print("Não achamos nenhum professor cadastrado com esse nome :("
                  "\nDigite o nome do professor novamente ou digite 0 para cancelar.")
            professor_requerido = input(">>> ").lower()
            if professor_requerido == "0":
                print("\nPara ver a lista completa de professores, acesse:"
                      "https://uacsa.ufrpe.br/br/docentes/")
                continuar = False
        else:
            print("Encontramos", len(possiveis_professores), "professor(es) com esse nome:\n")
            for professor in possiveis_professores:
                print("Nome Completo:", professor["nome_upper"], "\te-mail:", professor["email"])
            print("\nPara ver a lista completa de professores, acesse: "
                  "https://uacsa.ufrpe.br/br/docentes/")
            continuar = False
    return ""


executar = True

while executar:
    resposta = input(">>>").lower()

    if "ple" in resposta:
        if "obrigado" in resposta or "obrigatorio" in resposta or "obrigatório" in resposta:
            print("A matrícula no PLE será facultativa ao discente com vínculo ativo "
                  "\n(matriculado, matrícula vínculo ou trancado) nos cursos de graduação UFRPE")
        elif "limite" in resposta or "maximo" in resposta or "máximo" in resposta:
            print("O discente poderá cursar, no máximo, 240 horas de unidades curriculares durante o PLE "
                  "\n(o que dá em média 4 matérias), não havendo carga horária mínima para matrícula.")
        elif "cancelar" in resposta or "trancar" in resposta or "desistir" in resposta:
            print("Não se faz necessário alterações de matrícula (cancelamento de unidades curriculares "
                  "\ne/ou trancamento de matrícula) durante o PLE.")
        elif "reprova" in resposta or "reprovar" in resposta or "reprovação" in resposta:
            print("Caso você reprove no PLE, essa reprovação não contará para seu histórico :)")
        elif "2020.2" in resposta or "calouro" in resposta or "novato" in resposta:
            print("Os discentes ingressantes 2020.2 aprovados nos cursos de graduação da UFRPE, por meio do SISU, "
                  "\npoderão participar do PLE na forma de aluno especial, cursando unidades curriculares isoladas.")
        else:
            print("Os Períodos Letivos Excepcionais são períodos extras ofertados com aulas remotas."
                  "\n Já tivemos o primeiro período (de 17/08 a 23/10) e o segundo começou no dia 30/11.")

    elif "data" in resposta or "matricula" in resposta or "matrícula" in resposta:
        print("Para os alunos concluintes, acompanhados ou desligáveis, "
              "o período de matrícula será nos dias 18/11 e 19/11."
              "\nPara os demais, o período de matrícula será do dia 23/11 ao dia 26/11."
              "\nLembrando que a matrícula será feita pelo SIGAA: https://sigs.ufrpe.br/ ")
    elif "e-mail" in resposta or "email" in resposta or "professor" in resposta:
        resposta_email()
    elif "uacsa" in resposta:
        print("A UACSA é o Campus das Engenharias da UFRPE, localizado no município do Cabo de Santo Agostinho. "
              "Saiba mais em https://uacsa.ufrpe.br/br/apresentação/")
    elif "cursos" in resposta:
        print("São oferecidos cinco cursos de Engenharia: Civil, Elétrica, Eletrônica, Mecânica e de Materiais, "
              "além da pós graduação em Engenharia Física."
              "\nVeja mais sobre os cursos de graduação em https://uacsa.ufrpe.br/br/graduacao/"
              "\nE sobre o curso de pós graduação: https://www.ppengfis.ufrpe.br ")
    elif "pesquisa" in resposta:
        print("Pesquisa: são ações desenvolvidas com o objetivo de fomentar"
              "\n as atividades de pesquisa dentro das universidades. "
              "\nGeralmente acontecem através da monografia, no Trabalho de Conclusão de Curso (TCC),"
              "\n ou Iniciação Científica. ")
    elif "extensão" in resposta or "extensão" in resposta:
        print("Resposta resposta da opção 'extensão'")
        # TODO resposta da opção "extensão"
    elif "horario" in resposta or "horário" in resposta or "disciplina" in resposta:
        print(
            "O horário das disciplinas da UACSA está disponível em: "
            "https://uacsa.ufrpe.br/br/noticia/disponíveis-os-horários-das-disciplinas-ple-20204 ")
    elif "calendário" in resposta or "calendario" in resposta:
        print(
            "O Calendário acadêmico está disponível em: "
            "https://ufrpe.br/br/content/divulgado-calendário-acadêmico-20204-completo-do-ple-ufrpe ")
    elif "naps" in resposta or "saude" in resposta or "saúde" in resposta:
        print("Resposta resposta da opção 'naps'")
        # TODO resposta da opção "naps"
    elif "apoio" in resposta or "pedagogico" in resposta or "pedagógico" in resposta:
        print("Resposta resposta da opção 'Apoio Pedagógico'")
        # TODO resposta da opção "Apoio Pedagógico"
    elif resposta == "0":
        print(choice(mensagem_despedida))
        executar = False
    else:
        print(choice(mensagem_erro))
