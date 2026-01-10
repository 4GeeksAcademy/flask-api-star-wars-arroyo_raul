"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from sqlalchemy import select
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Person, Planet, User, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def handle_hello():

    people = db.session.execute(select(Person)).scalars().all()
    response_body = [person.serialize() for person in people]
    if not response_body:
        return jsonify({"error": "No people found"}), 404
    return jsonify(response_body), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
   person = db.session.get(Person, person_id)
   if person is None:
       return jsonify({"error": "Person not found"}), 404
   return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = db.session.execute(select(Planet)).scalars().all()
    response_body = [planet.serialize() for planet in planets]
    if not response_body:
        return jsonify({"error": "No planets found"}), 404
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    response_body = [user.serialize() for user in users]
    if not response_body:
        return jsonify({"error": "Users not found"}), 404
    return jsonify(response_body), 200

@app.route('/<int:user_id>/favorites', methods=["GET"])
def get_user_favorites(user_id):
    favorites = db.session.execute(select(Favorite).where(Favorite.user_id == user_id)).scalars().all()
    response_body = [fav.serialize() for fav in favorites]
    if not response_body:
        return jsonify({"error": f"Favorites in user {user_id} not found"}), 404
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planeta_id>', methods=["POST"])
def add_favorite_planet(planeta_id):
    planet = Favorite(planet_id = planeta_id, person_id = None, user_id = 2)
    db.session.add(planet)
    db.session.commit()

    response_body = planet.serialize()

    if not planet:
        return jsonify({"error": f"Error to adding planet {planeta_id} to favorites"}), 404
    return jsonify(response_body), 200

@app.route('/favorite/person/<int:persona_id>', methods=["POST"])
def add_favorite_person(persona_id):
    persona = Favorite(planet_id = None, person_id = persona_id, user_id = 2)
    db.session.add(persona)
    db.session.commit()

    response_body = persona.serialize()

    if not persona:
        return jsonify({"error": f"Error to adding person {persona_id} to favorites"}), 404
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planeta_id>', methods=["DELETE"])
def del_favorite_planet(planeta_id):
    planeta = db.session.execute(select(Favorite).where(Favorite.planet_id == planeta_id)).scalar_one_or_none()
    db.session.delete(planeta)
    db.session.commit()

    if not planeta:
        return jsonify({"error": f"Error to deleting {planeta_id} to favorites"}), 404
    return jsonify({"success": f"Deleted planet {planeta_id} succesful!!"}), 200

@app.route('/favorite/person/<int:persona_id>', methods=["DELETE"])
def del_favorite_person(persona_id):
    person = db.session.execute(select(Favorite).where(Favorite.person_id == persona_id)).scalar_one_or_none()
    db.session.delete(person)
    db.session.commit()

    if not person:
        return jsonify({"error": f"Error to deleting {persona_id} to favorites"}), 404
    return jsonify({"success": f"Deleted person {persona_id} succesful!!"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
