from . import db

class Registro(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(64), index=True)
    password = db.Column(db.String(64), index=True)
    descripcion = db.Column(db.Text)

    def __repr__(self):
        return '<Registro %r>' % self.usuario