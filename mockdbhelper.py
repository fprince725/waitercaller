class MockDBHelper:
	def connect(self, database="crimemap"):
		pass

	def get_all_inputs(self):
		return []

	def add_input(self, data):
		pass

	def clear_all(self):
		pass

	def add_crime(self, category, date, latitude, longitude, description):
		pass

	def get_all_crimes(self):
		print("MockDBHelper")
		return [{ 'latitude': 41.25936796982442, 
    		'longitude': -95.98527431488037, 
    		'date': "2000-01-01", 
    		'category': "mugging", 
    		'description': "mock description"}]


		