#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from marshmallow import fields, post_load
from marshmallow.schema import Schema
from models.Bookings import BookingModel


class Booking(Schema):
	id = fields.Int(dump_only=True)
	guest_id = fields.String(required=True)
	startdate = fields.Date(required=True)
	enddate = fields.Date(required=True)
	room_id = fields.String(required=True)
	property_id = fields.String(required=True)
	property_name = fields.String()
	# @post_load: Register a method to invoke after deserializing an object.
	#             The method receives the deserialized data and returns the processed data.

	@post_load
	def make_booking(self, data,  **kwargs):
		return BookingModel(**data)


booking_schema = Booking()
