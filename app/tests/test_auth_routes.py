from unittest.mock import MagicMock
from app.services.cognito_service import cognito_service
from app.utils.slugfy import slugfy
from uuid import UUID, uuid4
from app.models.establishment_model import Establishment
import json
def test_return_a_error_if_email_empty(client):
  """ Verify if the email field was passed """
  payload = {
    "email": "",
    "password": "@Validpass123"
  }
  response = client.post('/auth/login', json=payload)
  assert response.status_code == 400
  assert response.json['message'] == 'Campos vazios não são permitidos'
  
def test_return_a_error_if_password_empty(client):
  """ Verify if the password field was passed """
  
  payload = {
    "email": "teste@email.com",
    "password": ""
  }
  response = client.post('/auth/login', json=payload)
  assert response.status_code == 400
  assert response.json['message'] == 'Campos vazios não são permitidos'

def test_return_a_error_if_email_is_not_valid(client):
  """ Verify if the email passed is a valid email """
  payload = {
    'email': 'teste.com', 
    'password': 'test123456'
  }
  response = client.post('/auth/login', json=payload)
  assert response.json['message'] == 'E-mail inválido'
  assert response.status_code == 400

def test_return_a_error_if_password_is_less_than_8_char(client):
  """ Verify if the password is less than 8 characters """
  payload = {
    'email': 'teste@test.com', 
    'password': '123456',
  }
  response = client.post('/auth/login', json=payload)
  assert response.json['message'] == 'Senha inválida'
  assert response.status_code == 400
  
def test_return_a_error_if_password_theres_no_especial_char(client):
  """ Verify if the password theres no especial character """
  payload = {
    'email': 'teste@test.com', 
    'password': '12345678',
  }
  response = client.post('/auth/login', json=payload)
  assert response.json['message'] == 'Senha inválida'
  assert response.status_code == 400
  
def test_return_a_error_if_password_theres_no_letters(client):
  """ Verify if the password there is no letters """
  payload = {
    'email': 'teste@test.com', 
    'password': '@1234567',
  }
  response = client.post('/auth/login', json=payload)
  assert response.json['message'] == 'Senha inválida'
  assert response.status_code == 400
  
def test_return_a_error_if_establishment_doesnt_exist(client):
  """ Verify if the establishment doesn't exists """
  payload = {
    'email': 'teste@test.com', 
    'password': '@Test12345',
  }
  response = client.post('/auth/login', json=payload)
  assert response.json['message'] == 'Estabelecimento não encontrado'
  assert response.status_code == 404
  
def test_return_a_error_if_establishment_doesnt_exist(client, mocker):
  """ Verify if the establishment doesn't exists """
  payload = {
    "email": "testemail@test.com",
    "password": "@Validpass123"
  }
  
  # Return a valid mocked value for sign in method in cognito service
  mock_sign_in = mocker.patch("app.services.cognito_service.cognito_service.sign_in")
  mock_sign_in.return_value = {
    "AccessToken": "mocked_access_token",
    "RefreshToken": "mocked_refresh_token",
    "IdToken": "mocked_id_token",
    "ExpiresIn": 3600
  }
  
  # Return a valid mocked value for get by email method in establishment service
  mock_get_by_email = mocker.patch("app.services.establishment_service.EstablishmentService.get_by_email")
  mock_get_by_email.return_value = True
    
  response = client.post('/auth/login', json=payload)
  assert response.json['access_token'] == mock_sign_in.return_value['AccessToken']
  assert response.json['refresh_token'] == mock_sign_in.return_value['RefreshToken']
  assert response.json['id_token'] == mock_sign_in.return_value['IdToken']
  assert response.json['expires_in'] == mock_sign_in.return_value['ExpiresIn']
  assert response.status_code == 200
  
def test_register_email_data_was_sent(client):
  """ Verify if the email wasn't sent in the request body """
  payload = {
    'establishment_name': 'Test',
    'email': '',
    'password': "@Test123456",
    'confirm_password': "@Test123456",
  }
  response = client.post('/auth/register', json=payload)
  assert response.json['message'] == 'Preencha todos campos para continuar'
  assert response.status_code == 400
  
def test_register_name_data_was_sent(client):
  """ Verify if the name wasn't sent in the request body """
  payload = {
    'establishment_name': '',
    'email': 'test@test.com',
    'password': "@Test123456",
    'confirm_password': "@Test123456",
  }
  response = client.post('/auth/register', json=payload)
  assert response.json['message'] == 'Preencha todos campos para continuar'
  assert response.status_code == 400

def test_register_password_data_was_sent(client):
  """ Verify if the password wasn't sent in the request body """
  payload = {
    'establishment_name': 'Test Name',
    'email': 'test@test.com',
    'password': "",
    'confirm_password': "@Test123456",
  }
  response = client.post('/auth/register', json=payload)
  assert response.json['message'] == 'Preencha todos campos para continuar'
  assert response.status_code == 400

def test_register_confirm_password_data_was_sent(client):
  """ Verify if the confirm password wasn't sent in the request body """
  payload = {
    'establishment_name': 'Test Name',
    'email': 'test@test.com',
    'password': "@Test123456",
    'confirm_password': "",
  }
  response = client.post('/auth/register', json=payload)
  assert response.json['message'] == 'Preencha todos campos para continuar'
  assert response.status_code == 400
  
def test_register_confirm_password_and_password_match(client):
  """ Verify if the confirm password and password are not equal """
  payload = {
    'establishment_name': 'Test Name',
    'email': 'test@test.com',
    'password': "@Test123456",
    'confirm_password': "@Test123457",
  }
  response = client.post('/auth/register', json=payload)
  assert response.json['message'] == 'As senhas precisam ser iguais'
  assert response.status_code == 400

def test_register_establishment_already_exists(client, mocker):
  """ Verify if there's already one establishment with the email sent """
  payload = {
    'establishment_name': 'Test Name',
    'email': 'test@test.com',
    'password': "@Test123456",
    'confirm_password': "@Test123456",
  }
  # Return a valid mocked value for get by email method in establishment service
  mock_get_by_email = mocker.patch('app.services.establishment_service.EstablishmentService.get_by_email')
  mock_get_by_email.return_value = True
  
  response = client.post('/auth/register', json=payload)
  assert response.json['message'] == 'Já existe um usuário registrado com esse e-mail'
  assert response.status_code == 400

def test_register_establishment_is_created(client, mocker):
  """ Verify if the establishment is created successfuly"""
  payload = {
    'establishment_name': 'Test Name',
    'email': 'test@test.com',
    'password': "@Test123456",
    'confirm_password': "@Test123456",
  }
  # Return a valid mocked value for get by email method in establishment service
  mock_get_by_email = mocker.patch('app.services.establishment_service.EstablishmentService.get_by_email')
  mock_get_by_email.return_value = False
  
  # Return registered user in cognito service
  mock_sign_up = mocker.patch('app.services.cognito_service.cognito_service.sign_up')
  mock_sign_up.return_value = {
    'UserSub': uuid4().hex,
    'UserConfirmed': False,
  }
  
  mock_create_establishment = mocker.patch('app.services.establishment_service.EstablishmentService.create_establishment')
  mock_create_establishment.return_value = Establishment(
    id=UUID(mock_sign_up.return_value['UserSub']),
    is_active=bool(mock_sign_up.return_value['UserConfirmed']),
    email=payload['email'],
    name=payload['establishment_name'],
    slug=slugfy(payload['establishment_name'])
  )
  response = client.post('/auth/register', json=payload)
  assert UUID(response.json['establishment']['id']) == UUID(mock_sign_up.return_value['UserSub'])
  assert response.status_code == 201
  
  
def test_confirm_establishment_account(client, mocker):
  """ Verify if the establishment is activated"""
  payload = {
    'email': 'test@test.com',
    'confirm_code': 'confirm_code_test'
  }
  
  # Return registered user in cognito service
  mocker.patch('app.services.cognito_service.cognito_service.confirm_registration')
  
  mocker.patch('app.services.establishment_service.EstablishmentService.activate_establishment')
  response = client.post('/auth/confirm', json=payload)
  assert response.json['message'] == 'Conta ativada com sucesso!'
  assert response.status_code == 200
  

def test_resend_code_confirmation_check_if_exists(client, mocker):
  """ Verify if the establishment_id is valid """
  establishment_id = 'id_test'
  
  mock_get_by_id = mocker.patch('app.services.establishment_service.EstablishmentService.get_by_id')
  mock_get_by_id.return_value = False
  
  
  response = client.post(f'/auth/resend-confirmation-code/{establishment_id}')
  assert response.json['message'] == 'Estabelecimento não encontrado'
  assert response.status_code == 404

def test_resend_code_confirmation_check_if_is_already_active(client, mocker):
  """ Verify if the establishment_id is valid """
  establishment_id = 'id_test'
  
  mock_get_by_id = mocker.patch('app.services.establishment_service.EstablishmentService.get_by_id')
  mock_get_by_id.return_value = Establishment(
    id=UUID(uuid4().hex),
    is_active=True,
    email='test@email.com',
    name='Name Test',
    slug=slugfy('Name Test')
  )
  
  response = client.post(f'/auth/resend-confirmation-code/{establishment_id}')
  assert response.json['message'] == 'Está conta já está ativa'
  assert response.status_code == 401

def test_resend_code_confirmation(client, mocker):
  """ Verify if the establishment_id is valid """
  establishment_id = 'id_test'
  
  mock_get_by_id = mocker.patch('app.services.establishment_service.EstablishmentService.get_by_id')
  mock_get_by_id.return_value = Establishment(
    id=UUID(uuid4().hex),
    is_active=False,
    email='test@email.com',
    name='Name Test',
    slug=slugfy('Name Test')
  )
  
  mocker.patch('app.services.cognito_service.cognito_service.resend_code_confirmation')
  
  response = client.post(f'/auth/resend-confirmation-code/{establishment_id}')
  assert response.json['message'] == 'Re-enviamos seu código de confirmação para o seu e-mail'
  assert response.status_code == 200