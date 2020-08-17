#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from views.properties import properties
from views.bookings import bookings
from views.docs import docs
from globals import spec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.yaml_utils import load_operations_from_docstring


def initialize_routes(api):
    api.register_blueprint(properties, url_prefix='/api/properties')
    api.register_blueprint(bookings, url_prefix='/api/bookings')
    api.register_blueprint(docs)

    with api.test_request_context():
        for r in api.url_map.iter_rules():
            view = api.view_functions.get(r.endpoint)
            operations = load_operations_from_docstring(view.__doc__)
            path = FlaskPlugin.flaskpath2openapi(r.rule)
            if not operations:
                continue
            # De-reference the schemas referenced in the docstring.
            for verb in operations:
                resp = operations.get(verb).get('responses')
                for status in resp:
                    val = resp.get(status)
                    content = resp.get(status).get('schema')
                    if content:
                        pass
            # Add paths to the spec
            spec.path(view=view, path=path, operations=operations)
