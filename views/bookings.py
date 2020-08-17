from flask import Blueprint, jsonify
from flask import request
from globals import db
from permissions import token_verification
from schemas.bookings import booking_schema
bookings = Blueprint('booking', __name__)


@bookings.route('/', methods=['POST'])
@token_verification
def create_booking():
	"""Booking view.
	---
	post:
		summary: 'Create a Booking for a Property'
		description: ''
		operationId: 'AddBooking'
		parameters:
		- in: 'body'
		  name: 'body'
		  description: ''
		  required: true
		  schema:
			$ref: '#/components/schemas/Booking'
		responses:
			500:
				description: 'Server Error'
			401:
				description: 'UnAuthorized'
			201:
				description: 'Booking Created'
				schema:
					$ref: '#/components/schemas/Booking'
	"""
	try:
		content = request.json
		data = booking_schema.load(content)
		db.session.add(data)
		db.session.flush()
	except Exception as e:
		db.session.rollback()
		return jsonify({'error message': str(e)}), 500
	return jsonify(booking_schema.dump(data)), 201
