#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import redis
import os
import sys
from sqlalchemy import create_engine, orm
from typing import Optional


class SQLAlchemy:

	def __init__(self, db_url, autocommit=True):
		self._autocommit = autocommit
		self._engine = create_engine(db_url)
		self.session = None

	def connect(self):
		# autoflush: When True, all query operations will issue a flush() before proceeding.
		# autocommit: When True, the Session does not keep a persistent transaction running,
		#             and will acquire connections from the engine on an as-needed basis,
		#             returning them immediately after their use.
		# expire_on_commit: When True, all instances will be fully expired after each commit(),
		#                   so that all attribute/object access subsequent to a completed
		#                   transaction will load from the most recent database state.
		sm = orm.sessionmaker(bind=self._engine, autoflush=True, autocommit=self._autocommit,
							  expire_on_commit=True)
		self.session = orm.scoped_session(sm)

	def close(self):
		# Flush all changes to the database
		self.session.flush()
		# Close session
		self.session.close()
		# Remove session from connection pool
		self.session.remove()


def redis_connect() -> Optional[redis.Redis]:
	try:
		client = redis.Redis(
			host=os.environ.get("HOST", "localhost"),
			port=int(os.environ.get("REDIS_PORT", "6379")),
			db=0,
			socket_timeout=5)
		ping = client.ping()
		if ping is True:
			return client
	except redis.AuthenticationError:
		print("AuthenticationError")
		sys.exit(1)


redis_client = redis_connect()
