#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from models.Base import Base
from sqlalchemy import Column, Integer, String, Date


class BookingModel(Base):
    __tablename__ = 'properties'
    guest_id = Column(String)
    startdate = Column(Date)
    enddate = Column(Date)
    room_id = Column(String)
    property_id = Column(String)
    property_name = Column(String)
