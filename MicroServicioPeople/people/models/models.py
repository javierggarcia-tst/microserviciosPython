# encoding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from people.models.init_db import db, ma

class Personaje(db.Model):
    """Example model"""
    __tablename__ = 'personaje'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    isAlive = Column(Boolean,nullable=False)
    placeId =Column(Integer, nullable=True)
    
    #placeId = Column(Integer, ForeignKey('lugar.id'), nullable=True)
    #place = relationship("Lugar",lazy=True);

    @property
    def serialize(self) -> dict:
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'isAlive': self.isAlive,
            'placeId': self.placeId,
        }

    def imprimir(self):
        print('id: '+ str(self.id))
        print('Nombre: '+self.name)
        print('isAlive: '+ str(self.isAlive))
        if self.placeId != None and self.place != None:
            print('Lugar: '+ str(self.place.name))
        else:
            print('Lugar: Desaparecido en combate')
        print('rey: '+ str(self.id) + ' -- ' + str(self.placeId))

class PersonajeSchema(ma.ModelSchema):
    class Meta:
        model = Personaje