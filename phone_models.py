import configure_database as db
import database_functions as fn
import mysql.connector
from mysql.connector import Error
import graph_modelling as gm


def main():
	data = db.Phone_Database("smartphone_database")
	db_name = "smartphone_database"
	pw = "MYSQLp@ssword"
	models = fn.select_data(pw, db_name, '*', 'phone_models', 'model is NOT NULL')
	for model in models:
		Phone(*model)

class Phone:

	def __init__(self, model, guide_id, company, yr, url):
		self.db_name = "smartphone_database"
		self.pw = "MYSQLp@ssword"
		self.model = model
		self.guide_id = guide_id
		self.company = company
		self.yr = yr
		self.url = url
		g = self.plot_graphs()

	def get_components(self):
		components = fn.select_data(self.pw, self.db_name,'components.name, phone_component_relations.component_id, phone_component_relations.model', 'components inner join phone_component_relations on components.component_id = phone_component_relations.component_id','phone_component_relations.model = \"{}\"'.format(self.model))
		return components
			
	def get_rules(self, relation): 
		rules = fn.select_data(self.pw, self.db_name, '*', 'graph_rules', 'model = \"{}\" and relation = \"{}\"'.format(self.model, relation))
		return rules


	def plot_graphs(self):
		component_graph = gm.c_graph(self.model, self.guide_id, self.company, self.yr, self.url)
		sequence_graph = gm.s_graph(self.model)
		components = self.get_components()
		c_rules = self.get_rules('connection')
		s_rules = self.get_rules('pre-requisite')

		for index, component in enumerate(components):
			gm.c_node(component_graph, index + 1, *component)
			# print("component: ", component, component_graph.nodes(data=True))

		for rule in c_rules:
			# print("Rule: ", rule)
			gm.c_edge(component_graph, *rule)
			gm.s_node(component_graph, sequence_graph, *rule)
		
		for rule in s_rules:	
			gm.s_edge(component_graph, sequence_graph, *rule)

		gm.draw(component_graph, sequence_graph, self.model)

		return component_graph, sequence_graph


if __name__ == "__main__":
	main()