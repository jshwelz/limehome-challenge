#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from models.Base import Base
from sqlalchemy import Column, Integer, String


class PropertyModel(Base):
    __tablename__ = 'properties'
    publication = Column(Integer)
    publisher = Column(String)
    title = Column(String)
    number = Column(Integer)
    vol = Column(Integer)
    year = Column(Integer)
    type = Column(String)
    condition = Column(String)
    box = Column(Integer)
    copies = Column(Integer)
