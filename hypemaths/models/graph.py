
class Graph:
	"""
	Graphs are the mathematical structures used to model pairwise relations between objects. It is not the XY(Z) graph.
	"""
	
	# vertices are set of nodes
	# edges are set of tuple of nodes
	# Todo decide if edges and vertices wants seperate classes
	def __init__(self, vertices: set = None, edges: set = None):
		self.vertices =  self._validate_vertices(vertices)
		self.edges = self._validate_edges(edges, self.vertices) 
		
	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.vertices, self.edges})"
		
	@property
	def size(self):
		"""
		Returns
		-------
		int
				The number of edges in the graph.
		"""
		return len(self.edges)
	
	@property
	def order(self):
		"""
        Returns
        -------
        int
            The number of vertices in the graph.
        """
		return len(self.vertices)
		
	def _validate_vertices(self, vertices: set):
		# set default value if undefined
		if vertices == None:
			vertices = {}
			return vertices
			
		# check data types
		if not type(vertices) == set:
			raise TypeError(f"Vertices of a graph must be a set of elements but {type(vertices)} found")
				
		return vertices
		
	def _validate_edges(self, edges: set, vertices: set):
		# set default
		if edges == None:
			return {}
			
		# check data types
		if not type(edges) == set:
			raise TypeError(f"Edges of a graph must be a set but found {type(vertices)}")
			
		for edge in edges:
			if not type(edge) == tuple:
				raise TypeError(f"An edge must be a tuple but found {type(edge)}")
			if len(edge) != 2:
				raise TypeError(f"An edge must contain 2 elements but found {len(edge)} elements")
			
			if not vertices.issuperset(set(edge)):
				raise TypeError(f"Only vertices can be used as edge joints")
		
x = Graph({1,2,3,4}, {(1,2), (2,3), (1,4)})
print(x)
# y = Graph([1,32])
# z = Graph()
# print(z)
# c = Graph(1)