import networkx as nx
import random

class MeshNetwork:
    """
    A heterarchical network representing corporate and student nodes.
    Each node has:
        - Knowledge (float)
        - Leadership_Weight (float)
        - Resource_Capacity (float)
    """

    def __init__(self):
        # Directed graph supports heterarchical influence flows
        self.G = nx.DiGraph()

    def add_agent(self, agent_id, agent_type, 
                  knowledge=None, 
                  leadership_weight=None, 
                  resource_capacity=None):
        """
        Dynamically add a corporate or student agent with attributes.
        If attributes are not provided, initialize them randomly.
        """

        # Default dynamic initialization
        knowledge = knowledge if knowledge is not None else round(random.uniform(0.1, 1.0), 3)
        leadership_weight = leadership_weight if leadership_weight is not None else round(random.uniform(0.0, 1.0), 3)
        resource_capacity = resource_capacity if resource_capacity is not None else round(random.uniform(0.1, 10.0), 2)

        self.G.add_node(agent_id,
                        type=agent_type,
                        Knowledge=knowledge,
                        Leadership_Weight=leadership_weight,
                        Resource_Capacity=resource_capacity)

    def add_influence(self, source, target, weight=None):
        """
        Add a directional influence edge between nodes.
        """
        weight = weight if weight is not None else round(random.uniform(0.1, 1.0), 3)
        self.G.add_edge(source, target, influence_weight=weight)

    def initialize_from_lists(self, corporate_list, student_list):
        """
        Dynamically initialize the graph from lists of agent names.
        """
        for corp in corporate_list:
            self.add_agent(agent_id=corp, agent_type="corporate")

        for student in student_list:
            self.add_agent(agent_id=student, agent_type="student")

        # Create heterarchical influence edges
        all_nodes = list(self.G.nodes())
        for src in all_nodes:
            for tgt in all_nodes:
                if src != tgt:
                    # Randomly decide if an influence edge exists
                    if random.random() < 0.3:  # 30% chance of connection
                        self.add_influence(src, tgt)

    def summary(self):
        """
        Print a readable summary of the heterarchical Mesh network.
        """
        print("=== Mesh Network Summary ===")
        print(f"Nodes: {len(self.G.nodes())}")
        print(f"Edges: {len(self.G.edges())}\n")

        for node, attrs in self.G.nodes(data=True):
            print(f"{node} ({attrs['type']}): {attrs}")

        print("\nInfluence Edges:")
        for src, tgt, attrs in self.G.edges(data=True):
            print(f"{src} -> {tgt} | weight={attrs['influence_weight']}")


# Example usage:
if __name__ == "__main__":
    corporate_nodes = ["Corp_A", "Corp_B", "Corp_C"]
    student_nodes = ["Student_1", "Student_2", "Student_3", "Student_4"]

    mesh = MeshNetwork()
    mesh.initialize_from_lists(corporate_nodes, student_nodes)
    mesh.summary()
