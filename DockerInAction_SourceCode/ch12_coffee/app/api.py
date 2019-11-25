from flask import Blueprint, jsonify, request, Response
from sqlalchemy.exc import IntegrityError

from model import CoffeeShop

from . import db

import json
import os

api = Blueprint('api', __name__)

@api.route('/coffeeshops/')
def get_coffeeshops():
    coffeeshops = CoffeeShop.query.all()
    coffeeshops_json = [coffeeshop.to_json() for coffeeshop in coffeeshops]
    return jsonify(coffeeshops=coffeeshops_json)

@api.route('/coffeeshops/', methods=['POST'])
def add_coffeeshop():
    coffeeshop = CoffeeShop.from_json(request.get_json())
    try:
        db.session.add(coffeeshop)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        response = jsonify(message='A coffee shop with that name already exists')
        response.status_code = 400
        return response
    return Response(status=201)

