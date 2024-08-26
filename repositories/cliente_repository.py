# repositories/cliente_repository.py

from models import Cliente
from config import db

class ClienteRepository:
    def add(self, cliente):
        db.session.add(cliente)
        db.session.commit()

    def get_by_id(self, cliente_id):
        return Cliente.query.get(cliente_id)

    def get_by_email(self, email):
        return Cliente.query.filter_by(email=email).first()

    def get_paginated(self, page, per_page):
        return Cliente.query.paginate(page=page, per_page=per_page)

    def delete(self, cliente):
        db.session.delete(cliente)
        db.session.commit()
