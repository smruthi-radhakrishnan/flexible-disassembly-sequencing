import database_functions as fn
# import mysql.connector
import csv
import os

class Phone_Database:

	def __init__(self, db_name):
		#self, phone_model, api_url, repairability, brand, year, db_name, table
		self.db_name = db_name
		self.pw = "MYSQLp@ssword"
		connection = fn.create_server_connection("localhost", "root", self.pw)
		fn.create_database(connection, db_name)
		# self.setup_structure()
		# self.load_data()
		# self.check()

	def setup_structure(self):
		pw = self.pw
		db = self.db_name
		fn.create_phone_model_table(pw, db)
		fn.create_components_table(pw, db)
		fn.create_graphing_rules_table(pw,db)
		fn.create_table_dependencies(pw, db)


	def check(self):
		pw = self.pw
		db = self.db_name
		fn.show_database(pw, db)
		# fn.show_tables(pw, db)

	def load_data(self):
		pw = self.pw
		db = self.db_name
		mycsvdir = os.getcwd()
		datasets = ['Components.csv', 'Phone_Models.csv', 'Component_Relations.csv', 'Graphing_Rules.csv']
		table_names = ['components(component_id, name)','phone_models(model,guide_id,company,release_yr,url)','phone_component_relations(component_id,model)','graph_rules(component_1,component_2,model,relation,end_effector)']
		for i in range(0,len(datasets)):
			with open(datasets[i], newline = '') as fi:
				reader = csv.reader(fi, delimiter=',', quotechar='|')	
				for row in reader:
					row_list = '\', \''.join(row)
					row_list = '\'' + row_list + '\''
					fn.upload_data(pw, db, table_names[i],row_list)


if __name__ == "__main__":
	db = Phone_Database("smartphone_database")