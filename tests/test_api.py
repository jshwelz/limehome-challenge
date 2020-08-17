#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import json
from app import init_app
from globals import config
from db import redis_client
from sqlalchemy_utils import database_exists, drop_database

runner = init_app().test_cli_runner()
admin_token = runner.invoke(args=['generate_admin_jwt', 'josh']).output


# scope: Run once per test function. The setup portion is run before each test using the fixture.
# autouse: Invoke fixture automatically without declaring a function argument explicitly.
@pytest.fixture(scope='function', autouse=True)
def setup_api(request):
	# Init HTTP web server
	app = init_app()
	# Create and delete database
	if not database_exists(config.DATABASE_URL):
		runner.invoke(args=['create_tables'])

	def tear_down():
		drop_database(config.DATABASE_URL)

	request.addfinalizer(tear_down)
	testing_client = app.test_client()
	return testing_client


def test_create_booking(setup_api):
	booking = {
		"guest_id": "rem-josh",
		"startdate": "2020-10-10",
		"enddate": "2020-11-11",
		"room_id": "srf4445",
		"property_id": "45"
	}

	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.post('/api/bookings', data=json.dumps(booking), follow_redirects=True,
								content_type='application/json', headers=headers)
	response_message = json.loads(response.data.decode('utf-8'))
	assert response.status_code == 201
	assert response_message['guest_id'] == 'rem-josh'
	assert response_message['property_id'] == '45'


def test_list_bookings_by_id(setup_api):
	booking = {
		"guest_id": "rem-josh",
		"startdate": "2020-10-10",
		"enddate": "2020-11-11",
		"room_id": "srf4445",
		"property_id": "45",
		"property_name": "Hotel 1"
	}

	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.post('/api/bookings', data=json.dumps(booking), follow_redirects=True,
								content_type='application/json', headers=headers)
	response_message = json.loads(response.data.decode('utf-8'))
	assert response.status_code == 201

	booking = {
		"guest_id": "limehome-guest",
		"startdate": "2020-10-10",
		"enddate": "2020-11-11",
		"room_id": "srf4445",
		"property_id": "45",
		"property_name": "Hotel 2"
	}

	response = setup_api.post('/api/bookings', data=json.dumps(booking), follow_redirects=True,
								content_type='application/json', headers=headers)

	response_message = json.loads(response.data.decode('utf-8'))
	assert response.status_code == 201

	response = setup_api.get('/api/properties/45/bookings', follow_redirects=True,
								content_type='application/json', headers=headers)

	assert response.status_code == 200
	response_message = json.loads(response.data.decode('utf-8'))

	assert response_message == [
		{
			"guest_id": "rem-josh",
			"startdate": "2020-10-10",
			"enddate": "2020-11-11",
			"room_id": "srf4445",
			"property_id": "45",
			'id': 1,
			"property_name": "Hotel 1"
		},
		{
			"guest_id": "limehome-guest",
			"startdate": "2020-10-10",
			"enddate": "2020-11-11",
			"room_id": "srf4445",
			"property_id": "45",
			'id': 2,
			"property_name": "Hotel 2"
		}
	]


def test_get_hotels_by_coordinates(setup_api):
	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.get('api/properties?at=37.791106,-122.407715', follow_redirects=True,
								content_type='application/json', headers=headers)

	response_message = json.loads(response.data)
	assert response.status_code == 200
	assert 'title' in response_message[0]
	assert 'openingHours' in response_message[0]
