import unittest

from hypemaths import Graph

class GraphAttributesTests(unittest.TestCase):
	"""Tests for checking the values of a Graph when it gets created"""
	def test_graph_vertices(self) -> None:
		test_cases = (
			(Graph(), []),
			(Graph(
				{1,2,3,4,5,6}), 
			{1,2,3,4,5,6}),			
		)
		
		for graph, graph_vertices in test_cases:
			self.assertEqual(graph.vertices, graph_vertices)
			
	def test_graph_edges(self) -> None:
		test_cases = (
			(Graph(), []),
			(Graph({1,2,3,4}, {(1,2), (2,3)}), {(1,2), (2,3)}),			
		)
		
		for graph, graph_edges in test_cases:
			self.assertEqual(graph.edges, graph_edges)
			
	def test_graph_order(self) -> None:
		test_cases = (
			(Graph(), 0),
			(Graph({1,2,3,4,5,6}), 6),			
		)
		
		for graph, graph_order in test_cases:
			self.assertEqual(graph.order, graph_order)
			
	def test_graph_size(self) -> None:
		test_cases = (
			(Graph({}, {}), 0),
			(Graph({1,2,3,4,5,6}), 0),
			(Graph({1,2,3,4}, {(1,2), (2,3), (3,4)}), 3)			
		)
		
		for graph, graph_size in test_cases:
			self.assertEqual(graph.size, graph_size)