import configure_database as db
import database_functions as fn
import mysql.connector
from mysql.connector import Error
import graph_modelling as gm


def get_models():
	data = db.Phone_Database("smartphone_database")
	db_name = "smartphone_database"
	pw = "MYSQLp@ssword"
	models = fn.select_data(pw, db_name, '*', 'phone_models', 'model is NOT NULL')
	for model in models:
		phone = Phone(*model)
		# print(phone.__dict__)



class Phone:

	def __init__(self, model, guide_id, company, yr, url):
		self.db_name = "smartphone_database"
		self.pw = "MYSQLp@ssword"
		self.model = model
		self.guide_id = guide_id
		self.company = company
		self.yr = yr
		self.url = url
		graph = gm.graph(model, guide_id, company, yr, url)
		self.get_components(graph)
		self.get_connections(graph)
		gm.draw(graph, model)


	def get_components(self, graph):
		components = fn.select_data(self.pw, self.db_name, '*', 'phone_component_relations', 'model = \"{}\"'.format(self.model))
		for component in components:
			print(component)
			gm.node(graph, *component)
			

	def get_connections(self, graph):
		connections = fn.select_data(self.pw, self.db_name, '*', 'graph_rules', 'model = \"{}\" and relation = \"connection\"'.format(self.model))
		for connection in connections:
			gm.edge(graph, *connection)





if __name__ == "__main__":
	get_models()