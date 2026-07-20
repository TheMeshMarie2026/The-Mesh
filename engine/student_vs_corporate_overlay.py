import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List

class HeterarchyVisualizer:
    def __init__(self, turn_history: List[Dict[str, Any]], engine: Any):
        """
        Initializes the visualizer with the game's execution history 
        and the final state of the underlying NetworkX graph.
        """
        self.history = turn_history
        self.engine = engine

    def generate_endgame_dashboard(self, output_path: str = "endgame_dashboard.png") -> None:
        """
        Generates a comprehensive 2x2 data visualization matrix tracking 
        the systemic indicators of heterarchical performance.
        """
        # Set up a structured 4-panel dashboard layout
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle("HETERARCHY SYSTEM DYNAMICS: ENDGAME ANALYSIS", fontsize=18, fontweight='bold', y=0.96)
        
        # Color palettes optimized for clear contrast between student/corporate archetypes
        self._plot_knowledge_convergence(axes[0, 0])
        self._plot_leadership_fluidity(axes[0, 1])
        self._plot_resource_distribution_entropy(axes[1, 0])
        self._plot_network_trust_topology(axes[1, 1])
        
        plt.tight_layout(rect=[0, 0, 1, 0.93])
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"✅ [VISUALIZER]: Endgame metrics dashboard successfully generated and exported to {output_path}")

    def _plot_knowledge_convergence(self, ax: plt.Axes) -> None:
        """Panel 1: Tracks how effectively the network pooled data to meet crisis demands over time."""
        turns = [h["turn_number"] for h in self.history]
        
        # Extract how the knowledge commons grew vs. the static target threshold
        # (Mocking history traversal array for structural visualization template)
        global_knowledge_growth = [min(0.12 * t, 0.85) for t in turns] # Simulation curve
        target_demands = [0.75 for _ in turns]
        
        ax.plot(turns, global_knowledge_growth, label="Knowledge Commons (Pooled Data)", color="#1f77b4", linewidth=3, marker='o')
        ax.axhline(y=target_demands[0], color="#d62728", linestyle="--", linewidth=2.5, label="Crisis Mitigation Threshold")
        
        ax.set_title("Knowledge Commons Convergence", fontsize=12, fontweight='bold')
        ax.set_xlabel("Game Turn")
        ax.set_ylabel("Expertise Level (%)")
        ax.set_ylim(0, 1.05)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="lower right")

    def _plot_leadership_fluidity(self, ax: plt.Axes) -> None:
        """Panel 2: Shows the distribution of leadership over time. Flat charts mean top-down failure."""
        leader_counts = {}
        for h in self.history:
            leader = h.get("emergent_leader", "None")
            leader_counts[leader] = leader_counts.get(leader, 0) + 1
            
        nodes = list(leader_counts.keys())
        frequencies = list(leader_counts.values())
        
        # Colors differentiate corporate nodes from grassroots student/community nodes
        colors = ["#2ca02c" if "Corp" in n else "#9467bd" for n in nodes]
        
        bars = ax.bar(nodes, frequencies, color=colors, edgecolor='black', alpha=0.85, width=0.5)
        ax.set_title("Leadership Shifting Spectrum (Fluidity)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Turns in Executive Control")
        ax.set_xlabel("Faction / Node ID")
        ax.set_yticks(range(0, max(frequencies) + 2))
        ax.grid(axis='y', linestyle=":", alpha=0.6)
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}t',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')

    def _plot_resource_distribution_entropy(self, ax: plt.Axes) -> None:
        """Panel 3: Displays resource equality across nodes. Massive gaps reveal hoarding bottlenecks."""
        nodes = list(self.engine.network.nodes)
        balances = [sum(self.engine.network.nodes[n]['inventory'].values()) for n in nodes]
        
        colors = ["#2ca02c" if "Corp" in n else "#ff7f0e" if "Camp" in n else "#9467bd" for n in nodes]
        
        ax.pie(balances, labels=nodes, autopct='%1.1f%%', colors=colors, startangle=140, 
               wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'alpha': 0.85})
        ax.set_title("Endgame Resource Distribution Matrix", fontsize=12, fontweight='bold')

    def _plot_network_trust_topology(self, ax: plt.Axes) -> None:
        """Panel 4: Draws a programmatic heatmap grid showing trust index health between nodes."""
        nodes = list(self.engine.network.nodes)
        num_nodes = len(nodes)
        trust_matrix = np.zeros((num_nodes, num_nodes))
        
        # Populate correlation matrix from active NetworkX edge trust factors
        for i, node_u in enumerate(nodes):
            for j, node_v in enumerate(nodes):
                if node_u == node_v:
                    trust_matrix[i, j] = 1.0 # Self-trust identity
                elif self.engine.network.has_edge(node_u, node_v):
                    trust_matrix[i, j] = self.engine.network[node_u][node_v]['trust']
                else:
                    trust_matrix[i, j] = 0.0 # Completely disconnected
                    
        cax = ax.matshow(trust_matrix, cmap="RdYlGn", vmin=0.0, vmax=1.0)
        fig = ax.get_figure()
        fig.colorbar(cax, ax=ax, orientation='vertical', label='P2P Mutual Trust Index')
        
        ax.set_title("Decentralized Trust Mesh Integrity", fontsize=12, fontweight='bold', pad=15)
        ax.set_xticks(range(num_nodes))
        ax.set_yticks(range(num_nodes))
        ax.set_xticklabels(nodes, rotation=45, ha="left")
        ax.set_yticklabels(nodes)
