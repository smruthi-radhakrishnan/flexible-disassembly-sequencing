import phone_models as pm
import networkx as nx
import configure_database as db
import database_functions as fn
import matplotlib.pyplot as plt
import copy

def init():
	data = db.Phone_Database("smartphone_database")
	db_name = "smartphone_database"
	pw = "MYSQLp@ssword"
	models = fn.select_data(pw, db_name, '*', 'phone_models', 'model is NOT NULL')
	for model in models:
		if model[0] == 'Samsung Galaxy S8':
			phone = pm.Phone(*model)
			# plt.show()
			find_path(phone)
		


def find_path(pm):
	g1, g2 = pm.plot_graphs()
	#find all nodes
	nodes = g2.nodes(data=True)
	# print("all nodes: ", g1.nodes(data=True), "parents: ", parent_nodes)
	# initiate empty list of visited nodes
	visited=set()
	#Initiate rear panel-chassis connection as starting node (rear panel always removed first)
	component = [node['labelx'] for name,node in g1.nodes(data=True) if name =='rrpnl_1' or name == 'chss_1']
	start = [node[0] for node in g2.nodes(data=True) if node[1]['comp_1'] in component and node[1]['comp_2'] in component]
	print("start: ", start[0])
	# g3 = g2.copy()
	path_count = 0
	all_paths = []
	remaining_nodes = [node for node in g2.nodes()]
	remaining_edges = [edge for edge in g2.edges()]
	parent_nodes = [node for node, degree in g2.in_degree() if degree == 0]
	# for node in remaining_nodes:
		# print("node: ", str(node), 'remaining_edges:', remaining_edges, any(node in edge for edge in remaining_edges))

	# print(parent_nodes)
	# print("Number: ", g2.number_of_nodes())
	# single_path(visited,g2, start[0])
	# bfs_output = list(nx.bfs_edges(g2, source=start[0]))
	# print(bfs_output)
	dfs(visited, start[0], remaining_nodes, remaining_edges, all_paths)
	print(all_paths)
	

def single_path(visited, ref_g, node, path=[]):

	path = copy.deepcopy(path)

	# if len()

	
	if node not in visited:
		path.append(node)
		edges = ref_g.edges(node)
		parent_nodes = [node for node, degree in ref_g.in_degree() if degree == 0]			
		visited.add(node)
		print("node: ", node, "edges: ", edges, 'visited: ', visited, "path: ", path)# 		
		ref_g.remove_node(node)

		for next_node in parent_nodes:
			single_path(visited, ref_g, next_node, path)

		visited.remove(node)
	else:
		return path


def dfs(visited, node, remaining_nodes, remaining_edges, all_paths, current_path=[]):
	# print("yes")
	parent_nodes = [node for node in remaining_nodes if not any(node == edge[1] for edge in remaining_edges)]
	path = copy.deepcopy(current_path)
	# print("before, node:",  node,"remaining nodes: ", remaining_nodes, 'remaining_edges: ', remaining_edges, 'visited: ', visited, 'path: ', path)
	path.append(node)
	visited.add(node)
	remaining_nodes.remove(node)
	remaining_edges[:] = [edge for edge in remaining_edges if node not in edge]

	if len(remaining_nodes) == 0:
		if len(path) == len(visited):
			if set(path) == visited:
				all_paths.append(path)
			return
	else:
		# print("after, node: ", node, "remaining nodes: ", remaining_nodes, 'remaining_edges: ', remaining_edges, 'path: ', path)
		for next_node in parent_nodes:
			if next_node not in visited:	
				dfs(visited, next_node, remaining_nodes, remaining_edges, all_paths, path)
				remaining_nodes.append(next_node)
				remaining_edges[:] = [edge for edge in remaining_edges if next_node not in edge]
				# path.pop()
				visited.remove(next_node)
				# print("after, node:",  next_node,"remaining nodes: ", remaining_nodes, 'remaining_edges: ', remaining_edges, 'visited: ', visited, 'path: ', path)
		# return False



				


# 	temp_g = copy.deepcopy(ref_g)
# 	path.append(node)
# 	parent_nodes = [node for node, degree in temp_g.in_degree() if degree == 0]
# 	visited.add(node)
# 	temp_g.remove_node(node)
	
# 	edges = ref_g.edges(node)

# 	print("node: ", node, "edges: ", edges, 'visited: ', visited, "path: ", path, "nodes: ", ref_g.nodes(), 'length: ', len(ref_g.nodes()), 'condition: ', len(ref_g.nodes()) == 0)# 		
# 	# print(len(ref_g.nodes()))
# 	if len(temp_g.nodes()) == 0:
# 		print('happening?')
# 		all_paths.append(path)


# 		return

# 	for next_node in parent_nodes:
# 		if next_node not in visited:
# 			dfs(visited, temp_g, next_node, all_paths, path)

# 	return


	# path.pop()
	# visited.remove(node)
	# ref_g.add_node(node)
	# return

	# if node not in visited:
	# 	path.append(node)
	# 	edges = ref_g.edges(node)
	# 	parent_nodes = [node for node, degree in ref_g.in_degree() if degree == 0]			
	# 	visited.add(node)
	# 	# print("node: ", node, "edges: ", edges, 'visited: ', visited, "path: ", path, "number of nodes: ", len(ref_g.nodes()))# 		
	# 	ref_g.remove_node(node)

	# 	for next_node in parent_nodes:
	# 		dfs(visited, ref_g, next_node, all_paths, path)
	# # return
	
	# if len(visited) ==
	# 	all_paths.append(path)
	# 	return

	# return
	
	# print("start: ", start)
	# print(type(component[0]), type(start))

# def dfs(visited, ref_g, g_copy, node, path_count, path=[], paths=[]):
# 	#find all parent nodes
# 	path.append(node)
# 	parent_nodes = [node for node, degree in g_copy.in_degree() if degree == 0]
# 	print("here: ", visited, len(visited), g_copy.nodes(), len(g_copy.nodes()))
# 	if len(g_copy.nodes()) == 0:
# 		print("happening", g_copy.nodes())
# 		path_count+=1
# 		g_copy = ref_g.copy()
# 		print("after: ", g_copy.nodes(), len(g_copy.nodes()))
# 		# print(path)
# 		paths.append(path.copy())
# 		# visited.pop()
# 		path.pop()

# 	else:
# 		if node not in visited:
# 			edges = g_copy.edges(node)
# 			# print("before: ", g.nodes(), g.edges())
# 			# print("node: ", node, "edges: ", edges)
# 			visited.add(node)
# 			# print("here: ", path)
# 			g_copy.remove_node(node)
# 			# print("after: ", g.nodes(), g.edges(), not g.nodes())
# 			# g.remove_edge(edges[0])
# 			for next_node in parent_nodes:
# 				#calculate weight
# 				dfs(visited, ref_g, g_copy, next_node, path_count)
# 		path.pop()


# def dfs(visited, ref_g, node, path_count, path=[], paths=[]):
# 	#find all parent nodes
# 	g_copy = copy.deepcopy(ref_g)
# 	path = copy.deepcopy(path)
# 	print("path: ", path)
# 	path.append(node)

# 	parent_nodes = [node for node, degree in g_copy.in_degree() if degree == 0]
	
# 	if node not in visited:
# 			# path.append(node)
# 			# edges = g_copy.edges(node)
# 			# print("before: ", g.nodes(), g.edges())
# 			# print("node: ", node, "edges: ", edges)
# 			visited.add(node)
# 			# print("here: ", path)
# 			g_copy.remove_node(node)
# 			# print("after: ", g.nodes(), g.edges(), not g.nodes())
# 			# g.remove_edge(edges[0])
# 			for next_node in parent_nodes:
# 				#calculate weight
# 				dfs(visited, ref_g, g_copy, next_node, path_count)
# 			# path.pop()
# 	else:
# 		path_count+=1
# 		# g_copy = ref_g.copy()
# 		paths.append(path.copy())
# 		print("happening", path, paths, visited)
# 		path.pop()
# 		visited.pop()
# 		return

	# path.append(node)
	# parent_nodes = [node for node, degree in g_copy.in_degree() if degree == 0]
	# print("here: ", visited, len(visited), g_copy.nodes(), len(g_copy.nodes()))
	# if len(g_copy.nodes()) == 0:
	# 	print("happening", g_copy.nodes())
	# 	path_count+=1
	# 	g_copy = ref_g.copy()
	# 	print("after: ", g_copy.nodes(), len(g_copy.nodes()))
	# 	# print(path)
	# 	paths.append(path.copy())
	# 	# visited.pop()
	# 	path.pop()

	# else:
		
	# 	path.pop()


	# print(path_count)

	# for node in G.nodes():

	# sink_nodes = [node for node, outdegree in G.out_degree(G.nodes()).values() if outdegree == 0]
	# source_nodes = [node for node, indegree in G.in_degree(G.nodes()).values() if indegree == 0]
	# print('working?', sink_nodes, source_nodes)
	
	
	#visit only non-child nodes
	#delete node once visited
	#loop until all nodes are visited


if __name__ == "__main__":
	init()
