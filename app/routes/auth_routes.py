from flask import Blueprint, request, jsonify, abort
from app.services.cognito_service import cognito_service
from app.services.establishment_service import EstablishmentService
from app.utils.validations import is_email_valid, is_password_valid
from app.models.establishment_model import Establishment
from uuid import UUID
import json
from app.utils.slugfy import slugfy
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
  data = request.json 
  email = data['email']
  password = data['password']
  
  if not email or not password:
    return jsonify({
      'message': 'Campos vazios não são permitidos'
    }), 400

  if not is_email_valid(email):
    return jsonify({
      'message': 'E-mail inválido'
    }), 400
    
  if not is_password_valid(password):
    return jsonify({
      'message': 'Senha inválida'
    }), 400
  
  establishment_exists = EstablishmentService.get_by_email(email)
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado'
    }), 404
  
  response = cognito_service.sign_in(
    email=email, 
    password=password
  )
  
  return jsonify({
    'response': response
  })

@auth.route('/register', methods=['POST'])

def register():
  try:
    data = request.json 
    establishment_name = data['establishment_name']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']
    
    if not establishment_name or not password or not confirm_password or not email:
      return jsonify({
        'message': 'Preencha todos campos para continuar'
      }), 400
    
    if not is_email_valid(email):
      return jsonify({
        'message': 'O e-mail inserido não é válido'
      }), 400
    
    if not is_password_valid(password):
      return jsonify({
        'message': 'A senha inserida não é valida'
      }), 400
    
    if confirm_password != password:
      return jsonify({
        'message': 'As senhas precisam ser iguais'
      }), 400
    
    account_exists = EstablishmentService.get_by_email(email)

    if account_exists:
      return jsonify({
        'message': 'Já existe um usuário registrado com esse e-mail'
      }), 400
    
    response = cognito_service.sign_up(
      establishment_name=establishment_name,
      email=email,
      password=password,
      
    )
    
    new_establishment = EstablishmentService.create_establishment(
      id=UUID(response['UserSub']),
      is_active=bool(response['UserConfirmed']),
      email=email,
      establishment_name=establishment_name,
      slug=slugfy(establishment_name)
    )
    
    return jsonify({
      'establishment': new_establishment.to_dict(),
    }), 201
  except Exception as e:
    print('[REGISTER_ESTABLISHMENT_ERROR]',e)
    return jsonify({
      'message': 'Ocorreu um erro ao realizar seu cadastro',
    }), 400
  
@auth.route('/confirm', methods=['POST'])
def confirm_account():
  try:
    data = request.json
    email=data['email']
    confirm_code=data['confirm_code']

    cognito_service.confirm_registration(
      email=email,
      confirm_code=confirm_code
    )
    EstablishmentService.activate_establishment(email=email)
    
    return jsonify({
      "message": 'Conta ativada com sucesso!'
    }), 200
  except Exception as e:
    print('[ACTIVATE_ACCOUNT_ERROR]',e)
    return jsonify({
      "message": 'Ocorreu um erro ao ativar sua conta, tente novamente!'
    }), 400
    
@auth.route('/resend-confirmation-code/<string:establishment_id>', methods=["POST"])
def resend_confirmation_code(establishment_id: str):
  try:
    establishment_exists = EstablishmentService.get_by_id(id=establishment_id)
    
    if not establishment_exists:
      return jsonify({
        'message': 'Estabelecimento não encontrado'
      }), 404
  
    if establishment_exists.is_active:
      return jsonify({
        'message': 'Está conta já está ativa'
      }), 401
    
    cognito_service.resend_code_confirmation(email=establishment_exists.email)

    return jsonify({
      'message': 'Re-enviamos seu código de confirmação para o seu e-mail'
    }), 200
  except Exception as error:
    print('[RESEND_CODE_CONFIRMATION_ERROR]',error)
    return jsonify({
      "message": 'Ocorreu um erro ao enviar o código para seu e-mail, tente novamente!'
    }), 400
  
@auth.route('refresh-token', methods=['POST'])
def refresh_token():
  try:
    data = request.json

    response = cognito_service.refresh_token(refresh_token_code=data['refresh_token'], establishment_id=data['establishment_id'])
    
    return jsonify({
      'access_token': response['AuthenticationResult']['AccessToken'],
      'id_token': response['AuthenticationResult']['IdToken'],
      'expires_in': response['AuthenticationResult']['ExpiresIn']
    }), 200 
  except  Exception as error:
    print('[REFRESH_TOKEN_ERROR]',error)
    return jsonify({
      "message": 'Ocorreu um erro ao atualizar seu código de acesso.'
    }), 400
  
@auth.route('/logout', methods=["POST"])
def logout():
  try:
    access_token = request.headers.get('Authorization', None)

    if not access_token:
      return jsonify({
        'message': 'Token is missing'
      }), 401 
    token = access_token.split(' ')[1]
    response = cognito_service.logout(access_token=token, establishment_id='')
    print(response)
    return jsonify({
      'message': 'Usuário deslogado com sucesso!'  
    }), 200 
  except  Exception as error:
    print('[LOGOUT_ERROR]',error)
    return jsonify({
      "message": 'Ocorreu um erro ao realizar o logout, tente novamente.'
    }), 400
# ROUTE FOR RESET PASSWORD