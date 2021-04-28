import phone_models as pm
import networkx as nx
import configure_database as db
import database_functions as fn
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import copy
import sys
import cProfile
import re
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


def init():
	data = db.Phone_Database("smartphone_database")
	db_name = "smartphone_database"
	pw = "MYSQLp@ssword"
	models = fn.select_data(pw, db_name, '*', 'phone_models', 'model is NOT NULL')
	for model in models:
		# print(model[0])
		if model[0] == 'Galaxy S8':
			phone = pm.Phone(*model)
			# plt.show()
			find_path(phone)
			


def find_path(pm):
	g1, g2 = pm.plot_graphs()
	
	#find all nodes
	nodes = g2.nodes(data=True)
	# Initiate empty list of visited nodes
	visited=set()
	
	#Initiate rear panel-chassis connection as starting node (rear panel always removed first)
	component = [node['labelx'] for name,node in g1.nodes(data=True) if name =='rrpnl_1' or name == 'chss_1']
	start = [node[0] for node in g2.nodes(data=True) if node[1]['comp_1'] in component and node[1]['comp_2'] in component]
	battery = [node['labelx'] for name,node in g1.nodes(data=True) if name =='batt_1' or name == 'chss_1']
	battery = str(battery[0]) + '-' + str(battery[1])

	all_paths = []
	data = {}
	remaining_nodes = [node for node in g2.nodes()]
	remaining_edges = [edge for edge in g2.edges()]
	parent_nodes = [node for node, degree in g2.in_degree() if degree == 0]

	time = 0
	changes = 0
	min_index = 30
	p, d = dfs(nodes, visited, start[0], battery, min_index, remaining_nodes, remaining_edges, all_paths, data, time, changes)

	min_time = min(int(seq['time']) for seq in d.values())
	max_safety = min(int(seq['safety']) for seq in d.values())
	best_seqs = [k for k, v in d.items() if d[k]['time']==min_time or d[k]['safety']==max_safety] 


	df = pd.DataFrame.from_dict(d, orient='index')
	df.index.name = 'Sequence Number'
	# df.plot.scatter(x='safety', y='time', c='changes')
	
	plt.figure()
	# sns.violinplot(x='time',y='safety', data=df, scale='count', width=0.9, inner=None, orient='h', color='.8')
	sns.stripplot(x='time', y='safety', hue='changes', data=df, jitter= 0.35, orient='h', palette='Spectral', size=6, alpha=.7, linewidth = 0.5)
	plt.ylim(reversed(plt.ylim()))
	plt.legend(title="Tool changes", bbox_to_anchor=(1.01, 1))
	plt.title("Sequence distribution against objectives: safety, tool changes and time taken")
	plt.show()

	
	print("Number of quickest sequences:", len(best_seqs))
	# for seq in best_seqs:
	# 	print(best_seqs
	


def calculate_objectives(nodes, n1, n2):
	# print("nodes:", nodes, "n1: ", n1, "n2: ", n2, "end effectors: ", nodes[n1]['end_effector'], nodes[n2]['end_effector'])
	
	time = TOOL_TIME[nodes[n1]['end_effector']] + random.randint(0, 2)
	check_nodes = set(str(nodes[n1]['end_effector'])).intersection(set(str(nodes[n2]['end_effector'])))
	
	if check_nodes and any(char.isalpha() for char in check_nodes):
		change = 0
	else:
		time+= CHANGE_TIME[nodes[n1]['end_effector']]
		change = 1

	return time, change

def dfs(node_data, visited, node, battery, min_index, remaining_nodes, remaining_edges, all_paths, data, time, changes, current_path=[]):
	parent_nodes = [node for node in remaining_nodes if not any(node == edge[1] for edge in remaining_edges)]
	# print("parent nodes: ", parent_nodes, "node data: ", node_data, "battery: ", battery)
	# new_changes = changes + calculate_changes(node, path[-1])
	
	if battery in parent_nodes:
		min_index = min(min_index, len(visited))   

	path = copy.deepcopy(current_path)
	path.append(node)
	# print("before, time:", time)
	if len(path) > 1:
		temp_time, temp_change = calculate_objectives(node_data, node, path[-2])
	else:
		temp_time = 0
		temp_change = 0


	
	new_changes = changes + temp_change
	new_time = time + temp_time
	visited.add(node)
	remaining_nodes.remove(node)
	remaining_edges[:] = [edge for edge in remaining_edges if node not in edge]

	if len(remaining_nodes) == 0:
		if len(path) == len(visited):
			if set(path) == visited:
				all_paths.append(path)
				data[all_paths.index(path)] = {'time': new_time, 'changes': new_changes, 'safety': path.index(battery) - min_index}
				return all_paths, data
	else:
		for next_node in parent_nodes:
			if next_node not in visited:	
				all_paths, data = dfs(node_data, visited, next_node, battery, min_index, remaining_nodes, remaining_edges, all_paths, data, new_time, new_changes, path)
				remaining_nodes.append(next_node)
				remaining_edges[:] = [edge for edge in remaining_edges if next_node not in edge]
				visited.remove(next_node)
	
		return all_paths, data


if __name__ == "__main__":
	init()