MOCK_USERS = [{"email": "test@example.com",
				"salt": b't1faueOYK8gu6/m1y4OLvK84TFA=',
				"hashed": "9c14d34fd7ff080cc8275af874cdabdc68203efbea4050a97f2b00a7ab87f28c0f3b5e4f78089adeb0123458683a84906e51d44b979ed4228d1b7ba78c0da0c9" }]

class MockDBHelper:
	def get_user(self, email):
		user = [x for x in MOCK_USERS if x.get("email") == email]
		if user:
			return user[0]
		return None
		

	def add_user(self, email, salt, hashed):
  		MOCK_USERS.append({"email": email, "salt": salt, "hashed":hashed})