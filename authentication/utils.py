import re
from django.contrib import messages
from django.contrib.messages import constants

def validate_password(request, password, confirmar_senha):

    if len(password) < 5:
        messages.add_message(request, constants.ERROR, 'Senha menor que 5 digitos')
        return False
    
    if not password == confirmar_senha:
        messages.add_message(request, constants.ERROR, 'Senhas difirentes')
        return False

    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False
    

    return True

def validate_fields(*args):
    return all(arg.strip() != '' for arg in args)