#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from schemas.properties import Property
from schemas.bookings import Booking
from globals import spec

spec.components.schema("Property", schema=Property)
spec.components.schema("Booking", schema=Booking)
