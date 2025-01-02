from flask import Blueprint, request, jsonify
from uuid import UUID

from app.decorators.private_route import private_route
from app.services.establishment_service import EstablishmentService
from app.services.menu_service import MenuService
menu = Blueprint('menu', __name__)

@menu.route('/add-new-menu', methods=['POST'])
@private_route()
def new_menu():
  data = request.json
  user = request.user
  
  if not data['name']:
    return jsonify({
      'message': 'Escolha um nome para o cardápio'
    }), 400
  
  establishment_exists = EstablishmentService.get_by_id(id=UUID(user['sub']))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado',
    }), 404
    
  new_menu = MenuService.create(
    name=data['name'], 
    products=data['products'], 
    establishment_id=UUID(user['sub']),
    is_active=data['is_active']
  )
  
  return jsonify({
    'message': 'Menu criado com sucesso!',
    'menu': new_menu.to_dict(with_data_relations=True)
  }), 201
  
@menu.route('/get-menus/<string:establishment_id>', methods=['GET'])
@private_route()
def get_menus(establishment_id: str):
  establishment_exists = EstablishmentService.get_by_id(id=UUID(establishment_id))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado',
    }), 404
    
  menus = MenuService.find_all_menus_by_establishment_id(establishment_id=UUID(establishment_id))
  serialized_menus = [menu.to_dict(with_data_relations=True) for menu in menus]
  return jsonify({
    'menus': serialized_menus
  }), 200

@menu.route('/get-menu/<string:menu_id>', methods=['GET'])
@private_route()
def get_menu(menu_id: str):
  user = request.user
  
  establishment_exists = EstablishmentService.get_by_id(id=UUID(user['sub']))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado',
    }), 404
    
  menu = MenuService.find_menu_by_id(id=UUID(menu_id), establishment_id=UUID(user['sub']))
  
  return jsonify({
    'menu': menu.to_dict(with_data_relations=True)
  }), 200

@menu.route('/update', methods=['PATCH'])
@private_route()
def update_menu():
  data = request.json
  user = request.user
  
  if not data['name']:
    return jsonify({
      'message': 'Escolha um nome para o cardápio'
    }), 400
  
  establishment_exists = EstablishmentService.get_by_id(id=UUID(user['sub']))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado',
    }), 404
    
  menu = MenuService.find_menu_by_id(id=UUID(data['menu_id']), establishment_id=UUID(user['sub']))
  
  if not menu:
    return jsonify({
      'message': 'Cardápio não encontrado',
    }), 404
    
  updated_menu = MenuService.update(
    menu_id=UUID(data['menu_id']), 
    name=data['name'], 
    products=data['products'], 
    establishment_id=UUID(user['sub']),
    is_active=data['is_active']
  )
  
  return jsonify({
    'message': 'Menu editado com sucesso!',
    'menu': updated_menu.to_dict(with_data_relations=True)
  }), 200
  
  
@menu.route('/delete/<string:menu_id>', methods=['DELETE'])
@private_route()
def delete_menu(menu_id: str):
  user = request.user
  
  establishment_exists = EstablishmentService.get_by_id(id=UUID(user['sub']))
  
  if not establishment_exists:
    return jsonify({
      'message': 'Estabelecimento não encontrado',
    }), 404
    
  menu = MenuService.find_menu_by_id(id=UUID(menu_id), establishment_id=UUID(user['sub']))
  
  if not menu:
    return jsonify({
      'message': 'Cardápio não encontrado',
    }), 404
    
  deleted_menu = MenuService.delete(menu_id=UUID(menu_id), establishment_id=UUID(user['sub']))
  
  return jsonify({
    'menu': deleted_menu.to_dict(with_data_relations=True)
  }), 200