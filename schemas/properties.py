#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from marshmallow import fields, post_load
from marshmallow.schema import Schema
from models.Properties import PropertyModel


class AlternativeNamesSchema(Schema):
	name = fields.String()
	language = fields.String()


class OpeningHours(Schema):
	text = fields.String()
	label = fields.String()
	isOpen = fields.Boolean()


class Property(Schema):
	id = fields.String(dump_only=True)
	title = fields.String()
	averageRating = fields.String()
	vicinity = fields.String()
	openingHours = fields.Nested(OpeningHours())
	alternativeNames = fields.Nested(AlternativeNamesSchema())
	# @post_load: Register a method to invoke after deserializing an object.
	#             The method receives the deserialized data and returns the processed data.

	@post_load
	def make_property(self, data,  **kwargs):
		return PropertyModel(**data)


property_schema = Property()
