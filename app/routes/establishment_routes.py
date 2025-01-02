from flask import Blueprint, jsonify, request
from app.decorators.private_route import private_route
from app.services.establishment_service import EstablishmentService
from app.services.category_service import CategoryService
from uuid import UUID
from datetime import datetime
from app.utils.slugfy import slugfy
from app.utils.week_days import week_days
from app.utils.validations import is_phone_valid, normalize_phone_number
from app.utils.file_upload import file_upload, allowed_file
import json


establishment = Blueprint('establishment', __name__)


# @establishment.route('/info', methods=['GET'])
# @private_route()
# def get_info(payload):
#   return jsonify({ 'info': payload }), 200

@establishment.route('/<string:establishment_id>/edit', methods=["PATCH"])
@private_route()
def edit_establishment(establishment_id: str):
    data = request.form
    open_days = json.loads(data.get('open_days'))['open_days'][0]
    required_fields = ['name', 'about', 'phone', 'current_picture', 'address', 'open_days', 'category_id',]
    establishment_exists = EstablishmentService.get_by_id(id=UUID(establishment_id))
    
    # CHECK IF ESTABLISHMENT EXISTS
    if not establishment_exists:
      return jsonify({
        'message': 'Estabelecimento não encontrado'
      }), 404
    
    # CHECK IF ESTABLISHMENT ACCOUNT IS ACTIVE
    if not establishment_exists.is_active:
      return jsonify({
        'message': 'A conta desse estabelecimento ainda não foi confirmada'
      })
      
    # CHECK IF CATEGORY EXISTS
    category_exists = CategoryService.find_by_id(id=UUID(data['category_id']))
    if not category_exists:
      return jsonify({
        'message': 'A categoria que você selecionou não existe'
      }), 404
  
    # CHECK IF ALL REQUIRED DATA RECEIVED IS FILLED
    validation_errors = {}       
    for key, value in data.items():
      if key in required_fields and (not value or len(value) <= 0):
        validation_errors[str(key)] = 'Campo obrigatório'
    
    if bool(validation_errors):
      return jsonify({
        'message': 'Campos vazios não são permitidos',
        'field_errors': validation_errors
      })
    
    # CHECK IF PHONE IS VALID
    if not is_phone_valid(data['phone']):
      return jsonify({
        'message': 'Número de telefone/celular inválido'
      }), 400
    
    # CHECK IF ALL INFORMATION ABOUT ESTABLISHMENT IS FILLED
    is_information_set = False
    if not bool(validation_errors):
      is_information_set = True
    
    # VALIDATION FOR OPEN_DAYS PROPERTY
    try:
      for key, value in open_days.items():
        
        if not value:
          continue
          
        if not value['open_at'] or not value['close_at']:
          raise Exception(f'Horário de abertura e/ou encerramento não encontrado para a/o {week_days[key]}')
     
      
        if datetime.strptime(value['open_at'], '%H:%M').time()  > datetime.strptime(value['close_at'], '%H:%M').time():
          raise Exception('O horário de abertura não pode ser após o horário de encerramento')
    except Exception as error:
      return jsonify({
        'message': str(error),
      }), 400
    
    # UPLOAD ESTABLISHMENT IMAGE LOGIC
    uploaded_img_url = data['current_picture']
    if request.files:

      file = request.files['picture']
      if file.filename == '':
        return jsonify({'message': 'Nenhum arquivo selecionado'}), 404

      if not allowed_file(file.filename):
        return jsonify({'message': 'Formato de arquivo não permitido. Apenas imagens são aceitas.'}), 400
      
      file_size = len(file.read()) / (1024 * 1024) # Tamanho do arquivo em MB
      
      if file_size > 2:
        return jsonify({'message': 'O tamanho do arquivo não pode ser superior a 2MB.'}), 400
      
      file.seek(0)
      
      try:
        uploaded_img_url = file_upload(file)
      except Exception as error:
        print('[FILE_UPLOAD_ERROR]', error)
        return jsonify({'message': 'Ocorreu um erro ao relizar o upload de imagem.'}), 400
      
    updated_establishment = EstablishmentService.update_establishment(
      id=UUID(establishment_id),
      name= data['name'],
      slug= slugfy(data['name']),
      about= data['about'],
      phone= normalize_phone_number(data['phone']),
      picture= uploaded_img_url,
      address= data['address'],
      open_days= open_days,
      category_id= data['category_id'],
      is_information_set= is_information_set,
    )
    
    return jsonify({
      'message': 'As informações do estabelecimento foram atualizadas com sucesso.',
      'establishment': updated_establishment.to_dict()
    }), 200