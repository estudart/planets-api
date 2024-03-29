from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flasgger import Swagger
from flask_cors import CORS
from model import *
from schemas import *

app = Flask(__name__)
CORS(app)
api = Api(app)

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "title": "Planet API",
}

swagger = Swagger(app, config=swagger_config)

class HomeResource(Resource):
    def get(self):
        """
        Welcome to the home page!

        ---
        tags:
          - Welcome
        responses:
          200:
            description: A welcome message.
        """
        return {"message": "Welcome to the home page!"}

class PlanetsResource(Resource):
    def get(self):
        """
        Get a list of planets.

        ---
        tags:
          - Planets
        responses:
          200:
            description: List of planets.
        """
        session = Session()
        planets_list = session.query(Planet).all()
        result = planets_schema.dump(planets_list)
        return result, 200

    def post(self):
        """
        Create a new planet.

        ---
        tags:
          - Planets
        parameters:
          - name: planet_name
            in: formData
            type: string
            required: true
            description: The name of the planet.
          - name: planet_type
            in: formData
            type: string
            description: The type of the planet.
          - name: home_star
            in: formData
            type: string
            description: The home star of the planet.
          - name: mass
            in: formData
            type: float
            description: The mass of the planet.
          - name: radius
            in: formData
            type: float
            description: The radius of the planet.
          - name: distance
            in: formData
            type: float
            description: The distance from home star of the planet.
          - name: image
            in: formData
            type: string
            decription: Url string for the planet image
        responses:
          201:
            description: Created.
        """
        try:
            json_data = request.form
            new_planet_data = planet_schema.dump(json_data)
            print(new_planet_data)
            new_planet = Planet(**new_planet_data)

            session = Session()
            session.add(new_planet)
            session.commit()

            return new_planet_data, 201
        except Exception as e:
            return jsonify(message='Failed to create a Planet'), 404

class PlanetResource(Resource):
    def get(self, id):
        """
        Get a single planet information.

        ---
        tags:
          - Planet
        parameters:
          - name: id
            in: path
            type: string
            required: true
            description: The planet's id
        responses:
          200:
            description: Planet found.
          404:
            description: Planet not found.
        """

        try:
            session = Session()
            planet_data = session.query(Planet).filter(Planet.planet_id == id).first()

            if not planet_data:
                return {"message": "Planet not found."}, 404
            else:
                planet_json = planet_schema.dump(planet_data)
                return planet_json, 200
        except Exception as err:
            error_msg = f'{err}'
            return {"message": error_msg}, 404

    def delete(self, id):
        """
        Delete a planet by ID.

        ---
        tags:
          - Planet
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The ID of the planet to delete.
        responses:
          200:
            description: Planet deleted.
          422:
            description: Planet not found.
        """
        try:
            session = Session()
            delete_planet = session.query(Planet).filter(Planet.planet_id == id).first()
            if not delete_planet:
                error_msg = f'Planet not found in the database'
                return {"message": error_msg}, 200
            else:
                delete = session.query(Planet).filter(Planet.planet_id == id).delete()
                session.commit()
                msg = f'Planet with id: {id}, was deleted'
                return {"message": msg}, 200
        except Exception as err:
            error_msg = f'{err}'
            return {"message": error_msg}, 422

    def put(self, id):
        """
        Update a planet by ID.

        ---
        tags:
          - Planet
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The ID of the planet to update.
          - name: planet_name
            in: formData
            type: string
            description: The name of the planet.
          - name: planet_type
            in: formData
            type: string
            description: The type of the planet.
          - name: home_star
            in: formData
            type: string
            description: The home star of the planet.
          - name: mass
            in: formData
            type: float
            description: The mass of the planet.
          - name: radius
            in: formData
            type: float
            description: The radius of the planet.
          - name: distance
            in: formData
            type: float
            description: The distance from home star of the planet.
          - name: image
            in: formData
            type: string
            decription: Url string for the planet image
        responses:
          200:
            description: Planet updated.
          404:
            description: Failed to update planet.
        """
        try:
            session = Session()
            planet = session.query(Planet).filter(Planet.planet_id == id).first()

            if not planet:
                error_msg = f'Planet does not exist in database'
                return {"message": error_msg}, 200
            else:
                for field, value in request.form.items():
                    setattr(planet, field, value)

            session.commit()

            msg = f'Planet with id: {id} updated with new values'
            return {"message": msg}, 200
        except Exception as e:
            return {"message":'Failed to update a Planet'}, 404



class UserResource(Resource):
    def get(self, id):
        """
        Get a single user info

        ---
        tags:
          - User
        parameters:
          - name: id
            in: path
            type: integer
            required: True
            description: id of the User.

        responses:
          200:
            description: Success.
        """
        try:
            session = Session()
            user = session.query(User).filter(User.id == id).first()
            user_data = user_schema.dump(user)
            return user_data, 200
        except Exception as e:
            return jsonify(message=e), 404

    def put(self, id):
        """
        Edit information about users registered.

        ---
        tags:
          - User
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: User's id.
          - name: first_name
            in: formData
            type: string
            required: false
            description: The first name of the user.
          - name: last_name
            in: formData
            type: string
            required: false
            description: The last name of user.
          - name: email
            in: formData
            type: string
            required: false
            description: The user's email.
          - name: password
            in: formData
            type: string
            required: false
            description: The user's password.
        responses:
          200:
            description: User information updated.
          404:
            description: User not found.
        """

        try:
            session = Session()
            found_user = session.query(User).filter(User.id == id).first()

            for field, value in request.form.items():
                setattr(found_user, field, value)
            
            session.commit()

            return user_schema.dump(found_user), 200
            # return {"message": f'User with id: {id}, was updated'}, 200
        
        except Exception as error:
            return jsonify(message=error), 404


    def delete(self, id):
        """
        Delete a user on this route

        ---
        tags: 
          - User
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            descripton: User's id.
        responses:
          200:
            description: User has been deleted.
          404:
            description: User not found.
        """
        try:
            session = Session()
            user_data = session.query(User).filter(User.id == id).first()

            if not user_data:
                return {"message": "User not found"}, 404
            else:
                delete_user = session.query(User).filter(User.id == id).delete()
                session.commit()
                return {"deleted": user_schema.dump(user_data)}, 200
        except Exception as error:
            return {"message": error}, 404

class UsersResource(Resource):
    def get(self):
        """
        Get all users in the base.

        ---
        tags:
          - Users
        responses:
          200:
            description: List of users.
        """
        try:
            session = Session()
            users_list = session.query(User).all()
            result = users_schema.dump(users_list)
            return result, 200
        except Exception as e:
            return jsonify(message=e)
    
    def post(self):
        """
        Create a new user

        ---
        tags:
          - Users
        parameters:
          - name: first_name
            in: formData
            type: string
            required: true
            description: The first name of the user.
          - name: last_name
            in: formData
            type: string
            required: true
            description: The last name of user.
          - name: email
            in: formData
            type: string
            required: true
            description: The user's email.
          - name: password
            in: formData
            type: string
            required: true
            description: The user's password.
        responses:
          201:
            description: Created.
        """
        try:
            json_data = request.form
            new_user = User(**json_data)

            session = Session()
            session.add(new_user)
            session.commit()

            return json_data, 201
        except Exception as e:
            return jsonify(message='Missing argument'), 404


class CreatePlanets(Resource):
    def get(self):
        neptune = {
            "planet_name": "Neptune",
            "planet_type": "Ice Giant",
            "home_star": "Sun",
            "mass": 17,
            "radius": 24622,
            "distance": 4.5,
            "image": "https://media.tenor.com/kP_nx_RIySoAAAAj/neptune-rotate.gif",
            "description": "Neptune is the farthest planet from the Sun and an ice giant. It has a deep blue coloration caused by methane in its atmosphere and active weather systems, including the fastest winds in the solar system."
        }
        earth = {
            "planet_name": "Earth",
            "planet_type": "Terrestrial",
            "home_star": "Sun",
            "mass": 5.97,
            "radius": 6371,
            "distance": 1,
            "image": "https://media.tenor.com/4A4UHbVtBIIAAAAM/globe-world.gif",
            "description": "Earth is the third planet from the Sun and the only known planet to support life. It has a diverse range of environments, including oceans, continents, and an atmosphere that sustains life."
        }
        mercury = {
            "planet_name": "Mercury",
            "planet_type": "Terrestrial",
            "home_star": "Sun",
            "mass": 0.055,
            "radius": 2439.7,
            "distance": 0.39,
            "image": "https://media.tenor.com/jAde5L1hyYIAAAAM/merury.gif",
            "description": "Mercury is the smallest and innermost planet in our solar system. It has a heavily cratered surface and extreme temperature variations."
        }
        venus = {
            "planet_name": "Venus",
            "planet_type": "Terrestrial",
            "home_star": "Sun",
            "mass": 0.815,
            "radius": 6051.8,
            "distance": 0.72,
            "image": "https://media.tenor.com/oFpT0HHJ0R4AAAAM/venus.gif",
            "description": "Venus is often called Earth's 'sister planet' due to their similar size and composition. It has a thick atmosphere of carbon dioxide, leading to a runaway greenhouse effect and making it the hottest planet in the solar system."
        }
        saturn = {
            "planet_name": "Saturn",
            "planet_type": "Gas Giant",
            "home_star": "Sun",
            "mass": 95.2,
            "radius": 58232,
            "distance": 9.58,
            "image": "https://media.tenor.com/X41MtjA-OJUAAAAM/mercury-space.gif",
            "description": "Saturn is famous for its spectacular ring system made of ice and dust particles. It is the second-largest planet and has many moons, including Titan, which has a dense atmosphere."
        }
        jupiter = {
            "planet_name": "Jupiter",
            "planet_type": "Gas Giant",
            "home_star": "Sun",
            "mass": 317.8,
            "radius": 69911,
            "distance": 5.2,
            "image": "https://media.tenor.com/Z4p3O5wUNvAAAAAM/jupiter-planet.gif",
            "description": "Jupiter is the largest planet in the solar system and a gas giant. It has a banded appearance due to its turbulent atmosphere and a prominent storm known as the Great Red Spot."
        }
        mars = {
            "planet_name": "Mars",
            "planet_type": "Terrestrial",
            "home_star": "Sun",
            "mass": 0.107,
            "radius": 3389.5,
            "distance": 1.52,
            "image": "https://media.tenor.com/SqJHatCJ40cAAAAj/mars.gif",
            "description": "Mars is known as the 'Red Planet' due to its rusty-colored surface. It has polar ice caps, canyons, and extinct volcanoes. Evidence suggests it once had liquid water on its surface."
        }
        uranus = {
            "planet_name": "Uranus",
            "planet_type": "Ice Giant",
            "home_star": "Sun",
            "mass": 14.536,
            "radius": 25362.0,
            "distance": 19.2184,
            "image": "https://media.tenor.com/Cc8vOIn32VgAAAAM/uranus-planet.gif",
            "description": "Uranus is an ice giant with a pale blue-green coloration due to methane in its atmosphere. It rotates on its side relative to its orbit and has a system of faint rings."
        }

        session = Session()

        session.add(Planet(**neptune))
        session.add(Planet(**earth))
        session.add(Planet(**mars))
        session.add(Planet(**venus))
        session.add(Planet(**jupiter))
        session.add(Planet(**saturn))
        session.add(Planet(**mercury))
        session.add(Planet(**uranus))

        session.commit()

        return {"message": "Planets were successfully created"}

api.add_resource(CreatePlanets, '/create_planets')
api.add_resource(HomeResource, '/')
api.add_resource(PlanetsResource, '/planets')
api.add_resource(PlanetResource, '/planet/<int:id>')
api.add_resource(UserResource, '/user/<int:id>')
api.add_resource(UsersResource, '/users')

if __name__ == '__main__':
    app.run(debug=True)
