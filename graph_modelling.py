import networkx as nx
import matplotlib.pyplot as plt

# def init():
	

# def get_data():

def graph(md, gid, comp, yr, url):
	G = nx.Graph(Phone_Model=md, Teardown_Guide_ID=gid, Manufacturing_Company=comp, Release_Year=yr, Guide_URL=url)
	return G

def node(g, name, id):
	g.add_node(name, component_id=id)

def edge(g, n1, n2, model, type, tool):
	g.add_edge(n1, n2, end_effector=tool)


def draw(g, md):
	fig = plt.figure()
	fig.suptitle(md, fontsize=20)
	nx.draw(g, with_labels=True, font_weight='bold')
	plt.show()