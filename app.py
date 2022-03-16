"""Flask app for Cupcakes"""
from crypt import methods
import re
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route("/")
def index():
    """Renders html template that includes some JS"""
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """RETURN RESTFUL TODOS JSON API"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def new_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcakes"""
    cupcake = Cupcake(
        flavor = request.json['flavor'],
        rating = request.json['rating'],
        size = request.json['size'],
        image = request.json['image'] or None
    )
    db.session.add(cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Returns JSON for one specific cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates cupcake and responds w/ JSON of that updated cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake = Cupcake(
        flavor = request.json['flavor'],
        rating = request.json['rating'],
        size = request.json['size'],
        image = request.json['image']
    )
    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake.
    Returns JSON of {message: "Deleted"}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")