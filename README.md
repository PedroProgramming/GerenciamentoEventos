# Gerenciamento de Eventos

# Inicilização do projeto

# 1 - Excluir pasta 'venv'

      Criar outra utilizando: 
           Windows: python -m venv venv
           Linux: python3 -m venv venv
           
      Ativar 'venv'
           Windows: venv/Scripts/Activate
           Linux: source venv/bin/activate.

# 2 - Bibliotecas fornecidas - 'requirements.txt'
      Para instalar todas de uma só vez, basta digitar no seu terminal: 
      
      Windows: pip install -r requirements.txt
      Linux: python3 install -r requirements.txt
      
# 3 - Área administrativa
      Caso queira entra na área administrativa para fazer alterações
      
      - Abra o terminal no vsCode
      - Windows: python manage.py createsuperuser
      - linux: python3 manage.py createsuperuser
      
      username: obrigatório (será logado por ele)
      e-mail: pode ignorar
      password: obrigatório
      
      - Rodar server:
           python manage.py runserver
           
      - abrir google(ou outro navegador)
          url: 127.0.0.1:8000/admin/
          
          colocar username e password
          e pronto
  
 # Pronto
      Agora é só testar e brincar do jeito que quiserem.
      Cadastrar eventos, entrar, baixar relatório csv, gerar certificados para participantes
      pesquisar por eventos, informações suas e mais.
   
# Pedro Dev | 2023
