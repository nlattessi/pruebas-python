from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, String
from flask.ext.restful import Api, Resource
from flask.ext.restful import reqparse
from flask.ext.restful import fields, marshal

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

api = Api(app)

"""class Categoria(db.Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), unique=True)
    links = db.relationship('Link', backref='categoria', lazy='dynamic')
"""

class Link(db.Model):
    id = Column(Integer, primary_key=True)
    url = Column(Text, unique=True)
    descripcion = Column(Text, unique=False)
    #categoria_id = Column(Integer, db.ForeignKey('categoria.id'))

    def __init__(self, url, descripcion):
        self.url = url
        self.descripcion = descripcion

db.create_all()

link_fields = {
    'descripcion': fields.String,
    'url': fields.String,
    'uri': fields.Url('link')
}

class LinkListAPI(Resource):
    def get(self):
        links = Link.query.all()
        return {'links': [marshal(link, link_fields) for link in links]}

    def post(self):
        link_url = request.json['url']
        link_descripcion = request.json['descripcion']
        link = Link(link_url, link_descripcion)
        db.session.add(link)
        db.session.commit()
        return {'link': marshal(link, link_fields)}, 201

class LinkAPI(Resource):
    def get(self, id):
        link = Link.query.get_or_404(id)
        return {'link': marshal(link, link_fields)}


    def put(self, id):
        link = Link.query.get_or_404(id)
        if 'url' in request.json:
            link.url = request.json['url']
        if 'descripcion' in request.json:
            link.descripcion = request.json['descripcion']
        db.session.commit()
        return {'link': marshal(link, link_fields)}


    def delete(self, id):
        link = Link.query.get_or_404(id)
        db.session.delete(link)
        db.session.commit()
        return {'result': True}


api.add_resource(LinkListAPI, '/api/links', endpoint='links')
api.add_resource(LinkAPI, '/api/links/<int:id>', endpoint='link')


@app.route('/')
def index():
    return app.send_static_file("api.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)