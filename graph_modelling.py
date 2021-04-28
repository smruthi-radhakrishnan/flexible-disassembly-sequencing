import networkx as nx
import matplotlib.pyplot as plt
import random

def c_graph(md, gid, comp, yr, url):
	G = nx.Graph(Phone_Model=md, Teardown_Guide_ID=gid, Manufacturing_Company=comp, Release_Year=yr, Guide_URL=url)
	return G

def s_graph(md):
	G = nx.DiGraph(Phone_Model=md)
	return G

def c_node(g, index, comp_name, id,model):
	g.add_node(id, component_id=id, labelx=index, comp_name=comp_name)

def c_edge(g, n1, n2, model, tool_type, tool):
	g.add_edge(n1, n2, end_effector=tool, tool_type = tool_type)

def s_node(g1, g2, n1, n2, model, tool_type, tool):
	# print("node 1: ", g1.nodes[n1], "node 2:", g1.nodes[n2])
	name = str(g1.nodes[n1]['labelx']) + '-' + str(g1.nodes[n2]['labelx'])
	g2.add_node(name, comp_1=g1.nodes[n1]['labelx'], comp_2=g1.nodes[n2]['labelx'], end_effector=tool, tool_type = tool_type)

def s_edge(g1, g2, n1, n2, model, tool_type, tool):
	start = []
	end = []
	st_unique = set()
	end_unique = set()
	node = g2.nodes()


	for node in g2.nodes(data=True):
		if g1.nodes[n1]['labelx'] == node[1]['comp_1'] or g1.nodes[n1]['labelx'] == node[1]['comp_2']:
			end.append(node[0])
			end_unique.add(str(node[1]['comp_1']))
			end_unique.add(str(node[1]['comp_2']))

		if g1.nodes[n2]['labelx'] == node[1]['comp_1'] or g1.nodes[n2]['labelx'] == node[1]['comp_2']:
			start.append(node[0])
			st_unique.add(str(node[1]['comp_1']))
			st_unique.add(str(node[1]['comp_2']))
	

	common = st_unique.intersection(end_unique)	

	if len(end) > 1:
		for i in end:
			if i in start:
				if len(start) - len(end) > 0:
					start.remove(i)
				else:
					end.remove(i)
			s = str(common)
			if not (any(str(c) in common for c in i)):
				end.remove(i)
	if len(start) > 1:
		for i in start:
			if i in end:
				if len(start) - len(end) > 0:
					start.remove(i)
				else:
					end.remove(i)
			if not (any(str(c) in common for c in i)):
				start.remove(i)

	if len(start) == 1 and len(end) == 1:
		g2.add_edge(start[0], end[0])
	
	# print("start: ", start, "end: ", end)
	
	# 

def draw_c_graph(g, md):
	pos = nx.spring_layout(g, k=0.15, iterations=20)
	edge_labels = nx.get_edge_attributes(g, 'end_effector')
	node_labels = nx.get_node_attributes(g,'labelx')
	str_format = [str(node_labels[elem[0]]) + '-' + str(node_labels[elem[1]]) for elem in edge_labels]
	formatted_edge_labels = {(elem[0],elem[1]): str(node_labels[elem[0]]) + '-' + str(node_labels[elem[1]]) for elem in edge_labels}
	
	nx.draw_networkx_labels(g,pos,labels=node_labels,font_color='black')
	nx.draw_networkx_edge_labels(g,pos,edge_labels=edge_labels,font_color='red')
	nx.draw(g, pos, node_size = 400, font_weight='bold')

def draw_s_graph(g, md):
	pos = nx.circular_layout(g)
	nx.draw(g, pos,  node_size = 600, with_labels=True)

def draw(c_graph, s_graph, md):
	plt.subplot(121)
	draw_c_graph(c_graph, md)
	plt.subplot(122)
	plt.suptitle(md, fontsize= 16, fontweight='bold')
	draw_s_graph(s_graph, md)
	plt.tight_layout()
	# plt.plot()
	# draw_c_graph(c_graph, md)
	# plt.show()