from random import choice

def processar_resposta(texto_recebido,nome_usuario):
    mensagem_erro = ["Desculpe, não entendi :/",
                     "Não entendi, poderia escrever com outras palavras?",
                     "Hmmmm, essa eu não sei.",
                     "Não entendi, poderia reformular a pergunta?"
                     ]

    texto_recebido = texto_recebido.lower()

    if "comprovante" in texto_recebido or "declaração" in texto_recebido or "declaraçao" in texto_recebido:
        return("\U0001F4C3 Para emitir o comprovante de matricula ou declaração de vínculo você deve:"
              "\n 1- entrar no sigaa https://sigs.ufrpe.br/sigaa/verTelaLogin."
              "\n 2- clique na aba ensino"
              "\n 3- clique em emitir atestado de mátricula ou emitir declaração de vínculo"
              "\n  \U0001F4E9 Para saber mais envie um email com sua dúvida para o coordenação do seu curso:\n\n"
              "coordenacao.civil.uacsa@ufrpe.br\n"
              "coordenacao.materiais.uacsa@ufrpe.br\n"
              "coordenacao.eletrica.uacsa@ufrpe.br\n"
              "coordenacao.eletronica.uacsa@ufrpe.br\n"
              "coordenacao.mecanica.uacsa@ufrpe.br\n")
    elif "dispensa" in texto_recebido or "dispensa de disciplina" in texto_recebido or "dispensar cadeira" in texto_recebido or "dispensar" in texto_recebido:
        return("\U0001F6AB Requisitos para dispensar disciplina:"
              "\n 1- os conteúdos das disciplinas devem ser equivalentes em 80%"
              "\n 2- a carga horária deve ser igual ou superior"
              "\n 3- A disciplina deve ser regularmente oferecida pela instituição onde foi cursada\n"
              "\n\U0001F4E9 Para saber mais envie um email com sua dúvida para o coordenação do seu curso:\n\n"
              "coordenacao.civil.uacsa@ufrpe.br\n"
              "coordenacao.materiais.uacsa@ufrpe.br\n"
              "coordenacao.eletrica.uacsa@ufrpe.br\n"
              "coordenacao.eletronica.uacsa@ufrpe.br\n"
              "coordenacao.mecanica.uacsa@ufrpe.br\n")
    elif "estágio" in texto_recebido or "estagio" in texto_recebido or "eso" in texto_recebido:
        return("\U0001F477 instruções para formalizar estágio"
              "\n lista com instruções:"
              "\n 1- Realizar matrícula no sig@ a matrícula fica pendente até o envio do termo de compromisso"
              "\n 2- Solicitar o seguro no sítio da PREG até o dia 18 de cada mês."
              "\n 3- Preencher corretamente o termo de compromisso disponível na página da PREG"
              "\n 4- Enviar por e-mail o termo de compromisso para assinatura de todas as parte."
              "\n 5- os estudantes que farão estágio presencial, recolher as assinaturas a punho e enviar documento escaneado\n"
              "\n  \U0001F4E9Para saber mais envie um email com sua dúvida para cge.preg@ufrpe.br")
    elif "acompanhado" in texto_recebido or "acompanhados" in texto_recebido or "desligáveis" in texto_recebido or "desligaveis" in texto_recebido or "desligavel" in texto_recebido or "desligável" in texto_recebido or "desligado" in texto_recebido or "desligamento" in texto_recebido:
        return("\U0001F198 instruções para alunos acompanhados e desligáveis:"
              "\n o discente será desligado se:"
              "\n 1- Ultrapassar o prazo máximo de integralização curricular que é igual ao prazo normal mais 70% do prazo normal"
              "\n 2- Extrapolar o número máximo de trancamentos de matrícula que é de 4 semestres."
              "\n 3- Estiver impossibilitado de integralizar o currículo nos períodos letivos restantes, antes de completado o prazo limite para conclusão do curso,"
              "levando-se em consideração os prérequisitos das disciplinas (ou períodos necessários), limites semestrais de matrícula em disciplinas e compatibilidade de horário"
              "\n 4- Matricular-se na mesma disciplina, sem aproveitamento, por quatro vezes (consecutivas ou não).\n"
              "\n  \U0001F4E9 Para saber mais envie um email com sua dúvida para o coordenação do seu curso:\n\n"
              "coordenacao.civil.uacsa@ufrpe.br\n"
              "coordenacao.materiais.uacsa@ufrpe.br\n"
              "coordenacao.eletrica.uacsa@ufrpe.br\n"
              "coordenacao.eletronica.uacsa@ufrpe.br\n"
              "coordenacao.mecanica.uacsa@ufrpe.br\n")
    else:
        return(choice(mensagem_erro))
