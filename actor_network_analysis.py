"""
Actor Collaboration Network Analysis

This module builds and analyzes an actor collaboration network,
computing assortativity and comparing it with randomized and configuration models.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple
import random


class ActorNetworkAnalyzer:
    """Analyzes assortativity in actor collaboration networks."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.original_network = None
        self.randomized_network = None
        self.config_model_network = None
        
    def create_sample_network(self, num_actors: int = 20, 
                             num_movies: int = 15) -> nx.Graph:
        """
        Create a sample actor co-appearance network for demonstration.
        
        Args:
            num_actors: Number of actors in the network
            num_movies: Number of movies
            
        Returns:
            networkx.Graph: Actor co-appearance network
        """
        G = nx.Graph()
        G.add_nodes_from(range(num_actors))
        
        # Create movies with random actor casts
        random.seed(42)
        np.random.seed(42)
        
        for movie_id in range(num_movies):
            # Random number of actors per movie (3-8)
            cast_size = random.randint(3, 8)
            cast = random.sample(range(num_actors), 
                                min(cast_size, num_actors))
            
            # Add edges between all pairs of actors in the cast
            for i in range(len(cast)):
                for j in range(i + 1, len(cast)):
                    if G.has_edge(cast[i], cast[j]):
                        # Increase weight if edge exists
                        G[cast[i]][cast[j]]['weight'] += 1
                    else:
                        G.add_edge(cast[i], cast[j], weight=1)
        
        return G
    
    def load_network(self, G: nx.Graph) -> None:
        """
        Load or set the network to analyze.
        
        Args:
            G: networkx.Graph object representing the actor network
        """
        self.original_network = G.copy()
    
    def compute_assortativity(self, G: nx.Graph) -> float:
        """
        Compute degree assortativity coefficient.
        
        Args:
            G: networkx.Graph object
            
        Returns:
            float: Assortativity coefficient
        """
        return nx.degree_assortativity_coefficient(G)
    
    def degree_preserving_randomization(self, num_swaps: int = None) -> nx.Graph:
        """
        Perform degree-preserving randomization (edge swapping).
        
        Randomly rewires edges while preserving the degree sequence:
        - Pick edges (u1, v1) and (u2, v2)
        - Rewire to (u1, v2) and (u2, v1)
        - Ensure no self-loops or duplicate edges
        
        Args:
            num_swaps: Number of swap attempts. Default is 10 * number of edges
            
        Returns:
            networkx.Graph: Randomized network
        """
        G_rand = self.original_network.copy()
        
        if num_swaps is None:
            num_swaps = 10 * G_rand.number_of_edges()
        
        edges = list(G_rand.edges())
        successful_swaps = 0
        
        for _ in range(num_swaps):
            if len(edges) < 2:
                break
                
            # Pick two random edges
            edge1 = random.choice(edges)
            edge2 = random.choice(edges)
            
            if edge1 == edge2:
                continue
            
            u1, v1 = edge1
            u2, v2 = edge2
            
            # Check if rewiring is valid
            # New edges would be (u1, v2) and (u2, v1)
            if u1 == u2 or v1 == v2:
                # Shared node, skip
                continue
            
            if u1 == v2 or v1 == u2:
                # Would create same edge, skip
                continue
            
            if G_rand.has_edge(u1, v2) or G_rand.has_edge(u2, v1):
                # Would create duplicate, skip
                continue
            
            if u1 == v2 or u2 == v1:
                # Would create self-loop, skip
                continue
            
            # Perform the swap
            G_rand.remove_edge(u1, v1)
            G_rand.remove_edge(u2, v2)
            G_rand.add_edge(u1, v2)
            G_rand.add_edge(u2, v1)
            
            successful_swaps += 1
            edges = list(G_rand.edges())
        
        print(f"Successful swaps: {successful_swaps} out of {num_swaps} attempts")
        self.randomized_network = G_rand
        return G_rand
    
    def configuration_model(self) -> nx.Graph:
        """
        Generate a random network with the same degree sequence.
        
        Uses NetworkX configuration model.
        
        Returns:
            networkx.Graph: Configuration model network
        """
        degree_sequence = [G.degree(n) for n in self.original_network.nodes()]
        
        # Generate configuration model
        G_config = nx.configuration_model(degree_sequence)
        
        # Remove self-loops and parallel edges
        G_config.remove_edges_from(nx.selfloop_edges(G_config))
        G_config = nx.Graph(G_config)
        
        self.config_model_network = G_config
        return G_config
    
    def print_analysis(self) -> None:
        """Print analysis results."""
        if self.original_network is None:
            print("Error: No network loaded. Use load_network() first.")
            return
        
        print("=" * 60)
        print("ACTOR COLLABORATION NETWORK ANALYSIS")
        print("=" * 60)
        
        # Original network statistics
        print("\n[ORIGINAL NETWORK]")
        print(f"Nodes: {self.original_network.number_of_nodes()}")
        print(f"Edges: {self.original_network.number_of_edges()}")
        print(f"Density: {nx.density(self.original_network):.4f}")
        
        assortativity_orig = self.compute_assortativity(self.original_network)
        print(f"Degree Assortativity: {assortativity_orig:.4f}")
        
        # Degree-preserving randomization
        print("\n[DEGREE-PRESERVING RANDOMIZATION]")
        self.degree_preserving_randomization()
        assortativity_rand = self.compute_assortativity(self.randomized_network)
        print(f"Degree Assortativity: {assortativity_rand:.4f}")
        print(f"Change: {assortativity_rand - assortativity_orig:.4f}")
        
        # Configuration model
        print("\n[CONFIGURATION MODEL]")
        self.configuration_model()
        assortativity_config = self.compute_assortativity(self.config_model_network)
        print(f"Degree Assortativity: {assortativity_config:.4f}")
        print(f"Change from original: {assortativity_config - assortativity_orig:.4f}")
        
        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Original:            {assortativity_orig:8.4f}")
        print(f"Randomized:          {assortativity_rand:8.4f}")
        print(f"Configuration Model: {assortativity_config:8.4f}")
        print("=" * 60)
    
    def plot_degree_distribution(self) -> None:
        """Plot degree distribution of the original network."""
        if self.original_network is None:
            print("Error: No network loaded.")
            return
        
        degrees = [self.original_network.degree(n) 
                   for n in self.original_network.nodes()]
        
        plt.figure(figsize=(10, 5))
        
        plt.hist(degrees, bins=20, alpha=0.7, color='blue', edgecolor='black')
        plt.xlabel('Node Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution of Actor Network')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('degree_distribution.png', dpi=150)
        print("Saved degree distribution to 'degree_distribution.png'")
        plt.show()
    
    def plot_network(self, max_nodes: int = 30) -> None:
        """Visualize the network (for small networks).
        
        Args:
            max_nodes: Only plot if network has <= max_nodes
        """
        if self.original_network is None:
            print("Error: No network loaded.")
            return
        
        if self.original_network.number_of_nodes() > max_nodes:
            print(f"Network too large ({self.original_network.number_of_nodes()} nodes). "
                  f"Only plotting networks with <= {max_nodes} nodes.")
            return
        
        plt.figure(figsize=(10, 8))
        
        # Use spring layout
        pos = nx.spring_layout(self.original_network, k=0.5, iterations=50)
        
        # Draw network
        nx.draw_networkx_nodes(self.original_network, pos, 
                              node_color='lightblue', 
                              node_size=300)
        nx.draw_networkx_edges(self.original_network, pos, 
                              alpha=0.5)
        nx.draw_networkx_labels(self.original_network, pos, 
                               font_size=8)
        
        plt.title('Actor Collaboration Network')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('network_visualization.png', dpi=150)
        print("Saved network visualization to 'network_visualization.png'")
        plt.show()


def main():
    """Main execution function."""
    # Create analyzer
    analyzer = ActorNetworkAnalyzer()
    
    # Create sample network
    print("Creating sample actor collaboration network...")
    G = analyzer.create_sample_network(num_actors=20, num_movies=15)
    
    # Load network
    analyzer.load_network(G)
    
    # Run analysis
    analyzer.print_analysis()
    
    # Visualize
    print("\nGenerating visualizations...")
    analyzer.plot_degree_distribution()
    analyzer.plot_network()


if __name__ == "__main__":
    main()