import database_functions as fn
import mysql.connector
from mysql.connector import Error

class Phone_Database:

	def __init__(self, db_name):
	# 	#self, phone_model, api_url, repairability, brand, year, db_name, table
		self.db_name = db_name
		self.pw = "MYSQLp@ssword"
		# self.phone_model = phone_model
		# self.api_url = url
		# self.repairability = repairability
		# self.brand = brand
		# self.year = year
		self.setup_structure()
		# self.check()

	def setup_structure(self):
		pw = self.pw
		db = self.db_name
		connection = fn.create_server_connection("localhost", "root", self.pw)
		create_database_query = "CREATE DATABASE IF NOT EXISTS {}".format(db)
		fn.create_database(connection, create_database_query)
		fn.create_phone_model_table(pw, db)
		fn.create_components_table(pw, db)
		fn.create_graphing_rules_table(pw,db)
		fn.create_table_dependencies(pw, db)


	def check(self):
		fn.show_database(self.connection)
		fn.show_tables(self.connection)
	

# class Phone:


if __name__ == "__main__":
	database = Phone_Database("smartphone_database")