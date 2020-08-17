import re
from typing import Any, Tuple, List
import json
import requests
from flask import Blueprint, jsonify
from flask import request
from globals import db
from models.Bookings import BookingModel
from permissions import token_verification
from schemas.properties import property_schema
from schemas.bookings import booking_schema
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from db import redis_client
from datetime import timedelta
properties = Blueprint('property', __name__)
here_adapter = HTTPAdapter(max_retries=3)


def is_valid_geo(data):
	return True if re.match('^(\-?\d+(\.\d+)?),\w*(\-?\d+(\.\d+)?)$', data) else False


@properties.route('', methods=['GET'])
@token_verification
def get_property_by_area():
	"""Properties detail view.
	---
	get:
		summary: 'Find properties Near a Geographic point'
		description: 'Returns a list of nerby hotels'
		operationId: "getHotelsList"
		parameters:
		- name: 'at'
		  in: 'url'
		  description: 'latitude and longitud of a location Ex (456.44,-122.455)'
		  required: true
		  type: 'integer'
		responses:
			401:
				description: 'UnAuthorized'
			500:
				description: 'Server Error'
			'200':
				content:
					application/json:
						schema: 'Property'
				description: 'Hotels Nearby'
				schema:
					$ref: '#/components/schemas/Property'
	"""
	at = request.args.get('at')
	if is_valid_geo(at) is False:
		return jsonify({'error message': 'bad parameters'}), 404
	data = get_data_from_cache(key=at)
	if data != 'None':
		print('returning from cache')
		properties_list = property_schema.dump(data, many=True)
		return jsonify(properties_list), 200
	else:
		return get_data_from_api(at)


@properties.route('/<property_id>/bookings', methods=['GET'])
@token_verification
def get_properties_bookings(property_id):
	"""Property view.
	---
	get:
		summary: 'Return Bookings of a property'
		description: ''
		operationId: 'getBookings'
		parameters:
		- in: 'path'
		  name: 'property_id'
		  description: ''
		  required: true
		  schema:
			$ref: '#/components/schemas/Property'
		responses:
			500:
				description: 'Server Error'
			404:
				description: 'Bookings could not be found'
			401:
				description: 'UnAuthorized'
			201:
				description: 'List of Bookings of a Property'
				schema:
					$ref: '#/components/schemas/Property'
	"""
	item = db.session.query(BookingModel).filter(BookingModel.property_id == property_id).all()
	if not item:
		return jsonify({'error message': 'bookings could not be found'}), 404
	return jsonify(booking_schema.dump(item, many=True)), 200


def get_data_from_cache(key: str) -> str:
	"""Data from redis."""
	if redis_client.get(key) is not None:
		return json.loads(redis_client.get(key).decode("utf-8"))
	else:
		return 'None'


def set_hotel_data_to_cache(key: str, value: dict) -> bool:
	"""Data to redis."""
	with redis_client.pipeline() as pipe:
		for h_id, hotel in value.items():
			pipe.hset(h_id, str(hotel), h_id)
		pipe.execute()
	return redis_client.bgsave()


def set_coordinates_data_to_cache(key: str, value: dict) -> bool:
	"""Data to redis."""
	state = redis_client.setex(key, timedelta(seconds=3600), value=value)
	return state


def get_data_from_api(coordinates: str) -> Tuple[Any, int]:
	"""Data from here api."""
	session = requests.Session()
	session.mount('https://places.ls.hereapi.com/places/v1/discover/explore', here_adapter)
	params = {'apiKey': '3TsWkqWCmDZzKCyXMIipJZr-2wKiFPRJdCSTuQiFtzU', 'in': coordinates + ';r=150',
	          'cat': 'hotel', 'pretty': 'pretty'}
	items = []
	try:
		response = session.get('https://places.ls.hereapi.com/places/v1/discover/explore', params=params)
		if response.status_code == 200:
			json_response = response.json()
			items = json_response['results']['items']
		else:
			return jsonify({'error message': 'unknown error'}), response.status_code
	except ConnectionError as ce:
		return jsonify({'error message': 'connections error'}), 500
	dic = {data['id']: data for data in items}
	state_coordinates = set_coordinates_data_to_cache(key=coordinates, value=str(json.dumps(items)))
	state_hotel = set_hotel_data_to_cache(key=coordinates, value=dic)
	if state_coordinates is True:
		properties_list = property_schema.dump(items, many=True)
		return jsonify(properties_list), 200
