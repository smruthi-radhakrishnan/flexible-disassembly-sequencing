import phone_models as pm
import networkx as nx
import configure_database as db
import database_functions as fn
import matplotlib.pyplot as plt
import pants
import math
import random


TOOL_TIME = {'A-1': 20,
			 'A-2': 30,
			 'A-3': 40,
			 'F': 15,
			 'S-4': 48,
			 'S-2': 24,
			 'S_5': 60,
			 'S-15': 180
	
}

CHANGE_TIME = {'A-1': 40,
			 'A-2': 40,
			 'A-3': 40,
			 'F': 20,
			 'S-4': 30,
			 'S-2': 30,
			 'S_5': 30,
			 'S-15': 30
	
}

INVALID_SEQUENCE_COST = 1000



def init():
	data = db.Phone_Database("smartphone_database")
	db_name = "smartphone_database"
	pw = "MYSQLp@ssword"
	models = fn.select_data(pw, db_name, '*', 'phone_models', 'model is NOT NULL')
	for model in models:
		# print(model[0])
		if model[0] == 'Galaxy S8':
			phone = pm.Phone(*model)
			find_path(phone)





def find_path(pm):
	g1, g2 = pm.plot_graphs()
	# plt.show()
	node_info = g2.nodes(data=True)
	node_list = [node for node in g2.nodes()]
	print("node list:", node_list)
	edges = [edge for edge in g2.edges()]
	component = [node['labelx'] for name,node in g1.nodes(data=True) if name =='rrpnl_1' or name == 'chss_1']
	start = [node[0] for node in g2.nodes(data=True) if node[1]['comp_1'] in component and node[1]['comp_2'] in component]
	print("start: ", start)
	visited = set()

	def objective(a, b):
		# parent_nodes = [node for node in remaining_nodes if not any(node == edge[1] for edge in remaining_edges)]
		# print("nodes:", nodes, "edges:", edges)


		print("check path:", pants.Ant.path.__dict__)

		cost = 0
		
		for edge in edges:
			if a in edge and not any(visited) in edge:
				cost+= INVALID_SEQUENCE_COST
			elif b in edge and not any(visited) in edge:
				cost+= INVALID_SEQUENCE_COST
				
		cost += TOOL_TIME[node_info[a]['end_effector']] + random.randint(0, 2)
		check_nodes = set(str(node_info[a]['end_effector'])).intersection(set(str(node_info[b]['end_effector'])))
		
		if check_nodes and any(char.isalpha() for char in check_nodes):
			change = 0
		else:
			cost+= CHANGE_TIME[node_info[a]['end_effector']]
			change = 1


		return cost
	

	world = pants.World(node_list, objective)
	# ant = pants.Ant(alpha = 0.5, beta = 2.25)
	# ant.initialize(world, start=start[0])
	# print(ant.__dict__)
	solver = pants.Solver(ant_count = 5, limit = 150, q=3, beta=5)
	solutions = solver.solutions(world)

	for solution in solutions:
		print("nodes:", solution.tour)
		# print("path:", solution.path)
		print("cost:", solution.distance)




	
if __name__ == "__main__":
	init()