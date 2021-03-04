# Chatbot UACSA 

Este é um chatbot de Telegram não-oficial para que sejam tiradas dúvidas
sobre a Unidade Acadêmica do Cabo de Santo Agostinho (UACSA) da
Universidade Federal Rural de Pernambuco (UFRPE).

## Instalação

Basta instalar as dependências através de 

```
pip install -r requirements.txt
```

ou 
```
pip3 install -r requirements.txt
```

## Execução

Para iniciar o servidor pelo prompt de comandos de windows
 basta executar ```run_windows.bat```.
 Isso irá executar o servidor em modo de desenvolvimento.
 
Para Linux ou Mac é preciso executar os seguintes comandos no terminal:
```
export FLASK_APP=flask_app.py
export FLASK_ENV=development
flask run
```

## Desenvolvimento

- Escreva nomes de funções, parâmetros e variáveis em inglês.
- Após modificar um arquivo Python use o comando Code/Reformat File

## Produção

Ao colocar em produção é preciso inserir o token do bot do Telegram no arquivo
chatbotUACSA/telegram/bot_token