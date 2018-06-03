import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class SportCategory(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1000))
    price = Column(String(8))
    sport_id = Column(Integer, ForeignKey('category.id'))
    sport = relationship(SportCategory)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }


engine = create_engine('sqlite:///sportmenu.db')


Base.metadata.create_all(engine)
