import datetime

MOCK_USERS = [{"email": "test@example.com",
				"salt": b't1faueOYK8gu6/m1y4OLvK84TFA=',
				"hashed": "9c14d34fd7ff080cc8275af874cdabdc68203efbea4050a97f2b00a7ab87f28c0f3b5e4f78089adeb0123458683a84906e51d44b979ed4228d1b7ba78c0da0c9" }]

MOCK_TABLES = [{"_id": "1", "number": "1", "owner": "test@example.com", "url": "mockurl"}]

MOCK_REQUESTS = [{"_id": "1", "table_number": "1", "table_id": "1", "time": datetime.datetime.now()}]


class MockDBHelper:
	def get_user(self, email):
		user = [x for x in MOCK_USERS if x.get("email") == email]
		if user:
			return user[0]
		return None
		
	def add_user(self, email, salt, hashed):
  		MOCK_USERS.append({"email": email, "salt": salt, "hashed":hashed})

	def add_table(self, number, owner):
  		MOCK_TABLES.append({"_id": number, "number": number, "owner": owner})
  		return number

	def update_table(self, owner_id, url):
  		for table in MOCK_TABLES:
  			if table.get("_id") == owner_id:
  				table["url"] = url
  				break

	def get_tables(self, owner_id):
  		return MOCK_TABLES

	def get_table(self, table_id):
		for table in MOCK_TABLES:
			if table["number"] == table_id:
				return table

	def delete_table(self, table_id):
		for i, table in enumerate(MOCK_TABLES):
			if table.get("_id") == table_id:
				del MOCK_TABLES[i]
				break

	def add_request(self, table_id, time):
		table = self.get_table(table_id)
		MOCK_REQUESTS.append({"_id": table_id, "owner": table[
								"owner"], "table_number": table["number"], "table_id": table_id, "time": time})
		return True

	def get_requests(self, owner_id):
		return MOCK_REQUESTS

	def delete_request(self, request_id):
		for i, request in enumerate(MOCK_REQUESTS):
			if request.get("_id") == request_id:
				del MOCK_REQUESTS[i]
				break