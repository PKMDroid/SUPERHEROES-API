from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([h.to_dict(only=('id', 'name', 'super_name')) for h in heroes]), 200


@app.route('/heroes/<int:id>')
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    hero_dict = hero.to_dict(only=('id', 'name', 'super_name', 'hero_powers'))
    for hp in hero_dict['hero_powers']:
        hp['power'] = Power.query.get(hp['power_id']).to_dict(only=('id', 'name', 'description'))
    
    return jsonify(hero_dict), 200


@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict(only=('id', 'name', 'description')) for p in powers]), 200


@app.route('/powers/<int:id>')
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict(only=('id', 'name', 'description'))), 200


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    try:
        if 'description' in data:
            power.description = data['description']
        db.session.commit()
        return jsonify(power.to_dict(only=('id', 'name', 'description'))), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        hero_power = HeroPower(
            strength=data.get('strength'),
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id')
        )
        db.session.add(hero_power)
        db.session.commit()
        
        response = hero_power.to_dict(only=('id', 'hero_id', 'power_id', 'strength'))
        response['hero'] = Hero.query.get(hero_power.hero_id).to_dict(only=('id', 'name', 'super_name'))
        response['power'] = Power.query.get(hero_power.power_id).to_dict(only=('id', 'name', 'description'))
        
        return jsonify(response), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)