#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class RestrauntResource(Resource):
    def get(self):
        restraunt = [{
            "id":rest.id,
            "name":rest.name,
            "address":rest.address
            } for rest in Restaurant.query.all()]
        if restraunt:
            return restraunt, 200




class RestrauntResourceid(Resource):
    def get(self,id):
        restraunt = Restaurant.query.get(id)
        print(restraunt)
        if restraunt:
            return restraunt.to_dict(), 200
        else:
            return {"error": "Restaurant not found"}, 404
    def delete(self,id):
        restraunt = Restaurant.query.get(id)
        if restraunt:
            db.session.delete(restraunt)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "Restaurant not found"}, 404


class PizzaResource(Resource):
    def get(self):
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        return pizzas

class RestPizzaResource(Resource):
    def post(self):
        data = request.get_json()
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")
        pizza_find = Pizza.query.get(pizza_id)
        restaurant_find = Restaurant.query.get(restaurant_id)
        if pizza_find:
            if restaurant_find:
                    if price >= 1 and price <= 30:
                        restpizza = RestaurantPizza(price=price,pizza_id=pizza_id,restaurant_id=restaurant_id)
                        db.session.add(restpizza)
                        db.session.commit()
                        return restpizza.to_dict(), 201
                    else:
                        return {"errors": ["validation errors"]}, 400

            else:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400
        


api.add_resource(PizzaResource, "/pizzas")
api.add_resource(RestrauntResource, "/restaurants")
api.add_resource(RestrauntResourceid, "/restaurants/<int:id>")
api.add_resource(RestPizzaResource, "/restaurant_pizzas")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
