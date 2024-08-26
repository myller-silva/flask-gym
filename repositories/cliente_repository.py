from models import Cliente
from config import db

class ClienteRepository:
    def __init__(self):
        self.model = Cliente

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, cliente_id):
        return self.model.query.get_or_404(cliente_id)

    def add(self, cliente):
        db.session.add(cliente)
        db.session.commit()

    def delete(self, cliente):
        db.session.delete(cliente)
        db.session.commit()

    def get_paginated(self, page, per_page):
        return self.model.query.paginate(page=page, per_page=per_page)
    
    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
