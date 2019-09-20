# encoding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from place.models.init_db import db, ma

class Lugar(db.Model):
    """Example model"""
    __tablename__ = 'lugar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    @property
    def serialize(self) -> dict:
        """Return object data in easily serializeable format"""

        return {
            'id': self.id,
            'name': self.name,
        }

    def imprimir(self):
        print('id: '+ str(self.id))
        print('Nombre: '+self.name)

class LugarSchema(ma.ModelSchema):
    class Meta:
        model = Lugar