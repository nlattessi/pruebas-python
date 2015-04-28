from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('links.db')


class BaseModel(Model):
    class Meta:
        database = db


class Categoria(BaseModel):
    # nombre
    nombre = CharField(unique=True)
    # timestamps
    timestamp = DateTimeField(default=datetime.datetime.now)
    # descripcion
    descripcion = TextField(null=True)


class Link(BaseModel):
    # url
    url = TextField()
    # timestamps
    timestamp = DateTimeField(default=datetime.datetime.now)
    # descripcion
    descripcion = TextField(null=True)
    # categoria
    categoria = ForeignKeyField(Categoria, related_name='categoria', null=True)


class Tag(BaseModel):
    nombre = CharField(unique=True)


class TagLink(BaseModel):
    tag = ForeignKeyField(Tag)
    link = ForeignKeyField(Link)


def initialize():
    """Crea la base y la tabla si no existen."""
    db.connect()
    db.create_tables([Link, Categoria, Tag, TagLink], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_links():
    """Muestra el menu de links."""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to return.")
        for key, value in menu_links.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu_links:
            clear()
            menu_links[choice]()


def menu_categorias():
    """Muestra el menu de categorias."""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to return.")
        for key, value in menu_categorias.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu_categorias:
            clear()
            menu_categorias[choice]()


def menu_loop():
    """Muestra el menu."""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_categoria():
    """Agrega una categoria."""
    data = input("Ingresa el nombre: ").lower().strip()

    if data:
        data_descripcion = None
        if input('Ingresar una descripcion? [Yn] ').lower().strip() != 'n':
            print("Descripcion:")
            data_descripcion = sys.stdin.read().strip()
        if input('Guardar categoria? [Yn] ').lower().strip() != 'n':
            Categoria.create(nombre=data, descripcion=data_descripcion)
            print("Guardada con exito")


def add_link():
    """Agrega una entrada."""
    data = input("Ingresa tu link: ").lower().strip()

    if data:

        print("Elegir categoria:")
        for categoria in Categoria.select():
            print("{}){}".format(categoria.id, categoria.nombre))
        eleccion = input("Categoria (0 para no setear): ").lower().strip()
        if eleccion != '0':
            categoria = Categoria.get(Categoria.id == eleccion)
        
        tagsString = input("Ingresar tags (separar por coma): ").lower().strip()
        tags = [tag for tag in tagsString.split(',')]
        tags2 = []
        for t in tags:
            for tg in Tag.select().where(Tag.nombre != t):
                tags2.append(t)
        print(tags2)
        dlist = []
        for tag in tags:
            d = {}
            d["nombre"] = tag
            dlist.append(d)
        with db.transaction():
            Tag.insert_many(dlist).execute()

        if input('Save link? [Yn] ').lower() != 'n':
            if categoria:
                Link.create(url=data, categoria=categoria)
            else:
                Link.create(url=data)
            print("Saved successfully!")


def view_categorias(search_query=None):
    """Muestra las categorias guardadas."""
    entries = Categoria.select().order_by(Categoria.timestamp.desc())
    if search_query:
        entries = entries.where(Categoria.nombre.contains(search_query))

    for categoria in entries:
        timestamp = categoria.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print(categoria.nombre)
        if categoria.descripcion:
            print('\n')
            print(categoria.descripcion)
        print('\n\n'+'='*len(timestamp))
        print('n) next categoria')
        print('d) delete categoria')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_categoria(categoria)


def view_links(search_query=None):
    """Muestra las entradas guardadas."""
    entries = Link.select().order_by(Link.timestamp.desc())
    if search_query:
        entries = entries.where(Link.url.contains(search_query))

    for link in entries:
        timestamp = link.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print(link.url)
        if link.categoria:
            print('categoria: {}'.format(link.categoria.nombre))
        print('\n\n'+'='*len(timestamp))
        print('n) next link')
        print('d) delete link')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_link(link)


def search_links():
    """Busca entradas a partir de un string."""
    view_links(input('Search query: '))


def search_categorias():
    """Busca categorias a partir de un string."""
    view_categorias(input('Search query: '))


def delete_link(link):
    """Borra una entrada."""
    if input("Seguro de borrar? [yN] ").lower().strip() == 'y':
        link.delete_instance()
        print("Entrada borrada.")


def delete_categoria(categoria):
    """Borra una categoria."""
    if input("Seguro de borrar? [yN] ").lower().strip() == 'y':
        for link in Link.select().where(Link.categoria == categoria.id):
            link.categoria = None
            link.save()
        categoria.delete_instance()
        print("Categoria borrada.")


menu = OrderedDict([
    ('l', menu_links),
    ('c', menu_categorias),
])

menu_links = OrderedDict([
    ('a', add_link),
    ('v', view_links),
    ('s', search_links),
])

menu_categorias = OrderedDict([
    ('a', add_categoria),
    ('v', view_categorias),
    ('s', search_categorias),
])

if __name__ == '__main__':
    initialize()
    menu_loop()
