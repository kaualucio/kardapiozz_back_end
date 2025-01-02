from flask import Blueprint, jsonify, request
from app.decorators.private_route import private_route
from app.services.establishment_service import EstablishmentService
from app.services.product_service import ProductService
from app.services.menu_service import MenuService
from app.utils.file_upload import allowed_file, file_upload
from uuid import UUID
import json

product = Blueprint('product', __name__)

@product.route('/add-new-product', methods=["POST"])
@private_route()
def add_new_product():
  user = request.user
  data = request.form
  ingredients = json.loads(data.get('ingredients'))
  required_fields = ['name', 'image', 'price']

  empty_values_errors = {}
  for key, value in data.items():
    if key in required_fields and not value:
      empty_values_errors[str(key)] = 'Campo obrigatório'
  
  if bool(empty_values_errors):
    return jsonify({
      'message': 'Preencha todos os campos obrigatórios',
      'field_errors': empty_values_errors
    })  
  
  establishment_exists = EstablishmentService.get_active_by_id(id=UUID(user['sub']))
  
  if not establishment_exists: 
    return jsonify({
      'message': 'Não encontramos nenhum estabelecimento ativo com esse ID'
    }), 404
   
  file = request.files['image']
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
  
  new_product = ProductService.create(
    name=data['name'],
    image=uploaded_img_url,
    ingredients=ingredients,
    is_available=bool(data['is_available']),
    price=float(f'{data['price']:.4}'),
    establishment_id=UUID(user['sub'])
  )
  return jsonify({
    'message': 'Produto criado com sucesso!',
    'product': new_product.to_dict()
  }), 201
  
  
@product.route('/get-products/<string:establishment_id>', methods=["GET"])
@private_route()
def get_products(establishment_id: str):
  establishment_exists = EstablishmentService.get_active_by_id(id=UUID(establishment_id))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado'
    }), 404
    
  products = ProductService.find_all_by_establishment_id(establishment_id=UUID(establishment_id))
  serialized_products = [product.to_dict() for product in products]
  
  return jsonify({
    'products': serialized_products
  }), 200
  
@product.route('/get-menu-products/<string:establishment_id>/<string:menu_id>', methods=["GET"])
@private_route()
def get_products_menu(establishment_id: str, menu_id: str):
  print(establishment_id, menu_id)
  menu_exists = MenuService.find_menu_by_id(id=UUID(menu_id), establishment_id=UUID(establishment_id))
  
  if not menu_exists:
    return jsonify({
      'message': 'Menu não encontrado'
    }), 404
    
  menu_products = ProductService.find_all_by_menu_id(menu_id=UUID(menu_id)) 
  serialized_products = [product.to_dict() for product in menu_products]
  
  return jsonify({
    'products': serialized_products
  }), 200
  
@product.route('/get-product/<string:establishment_id>/<string:product_id>', methods=["GET"])
@private_route()
def get_product(establishment_id: str, product_id: str):
  establishment_exists = EstablishmentService.get_active_by_id(id=UUID(establishment_id))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado'
    }), 404
    
  product = ProductService.find_by_id(id=UUID(product_id))
  
  return jsonify({
    'product': product.to_dict(with_data_relations=True) if product else None
  }), 200
  
@product.route('/update', methods=["PATCH"])
@private_route()
def update_product():
  data = request.form
  establishment_id = data['establishment_id']
  product_id = data['product_id']
  ingredients = json.loads(data.get('ingredients'))
  establishment_exists = EstablishmentService.get_active_by_id(id=UUID(establishment_id))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado'
    }), 404
    
  product = ProductService.find_by_id(id=UUID(product_id))
  
  if not product:
    return jsonify({
      'message': 'Produto não encontrado'
    }), 404
  
  uploaded_img_url = data['current_image']
  if request.files:
    file = request.files['image']
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
    
  updated_product = ProductService.update(
    id=UUID(product_id), 
    name=data['name'],
    ingredients=ingredients,
    image=uploaded_img_url,
    price=float(f'{data['price']:.4}'),
    establishment_id=UUID(establishment_id),
    is_available=bool(data['is_available'])
  )
  
  return jsonify({
    'product': updated_product.to_dict()
  }), 200

@product.route('/delete/<string:establishment_id>/<string:product_id>', methods=["DELETE"])
@private_route()
def delete(establishment_id: str, product_id: str):
  establishment_exists = EstablishmentService.get_active_by_id(id=UUID(establishment_id))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado'
    }), 404
    
  product = ProductService.find_by_id(id=UUID(product_id))
  
  if not product:
    return jsonify({
      'message': 'Produto não encontrado'
    }), 404
    
  deleted_product = ProductService.delete(id=UUID(product_id))
  
  return jsonify({
    'product': deleted_product.to_dict()
  }), 200