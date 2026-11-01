import networkx as nx
import matplotlib.pyplot as plt
import random

#Create random graph 

def generate_random_graph(num_nodes=6, num_edges=11):
    if num_nodes < 6:
        raise ValueError("The graph must have at least 6 nodes.")

    max_edges = num_nodes * (num_nodes - 1) // 2

    if num_edges < num_nodes - 1 or num_edges > max_edges:
        raise ValueError(
            "A connected simple graph needs between "
            "num_nodes - 1 and num_nodes*(num_nodes-1)//2 edges."
        )

    G = nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))

    # First, create a random spanning tree to guarantee connectivity
    nodes = list(G.nodes())
    random.shuffle(nodes)

    for i in range(1, num_nodes):
        u = nodes[i]
        v = random.choice(nodes[:i])
        weight = random.randint(1, 20)
        G.add_edge(u, v, weight=weight)

    # Add random extra edges until the requested edge count is reached
    while G.number_of_edges() < num_edges:
        u, v = random.sample(list(G.nodes()), 2)

        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=random.randint(1, 20))

    return G


def MyMinimumSpanningTree(Graph) -> nx.Graph:

    mst = nx.Graph()
    mst.add_nodes_from(Graph.nodes(data=True))

    # Sort edges by weight
    edges = sorted(
        Graph.edges(data=True),
        key=lambda edge: edge[2]["weight"]
    )

    print("\n--- Kruskal's Algorithm ---")

    for u, v, data in edges:
        weight = data["weight"]

        # Temporarily add the edge
        mst.add_edge(u, v, **data)

        if nx.is_forest(mst):
            print(f"ACCEPT: {u} -- {v}, weight = {weight}")
        else:
            mst.remove_edge(u, v)
            print(
                f"REJECT: {u} -- {v}, weight = {weight} "
                "(cycle created)"
            )

        # A spanning tree has V - 1 edges
        if mst.number_of_edges() == Graph.number_of_nodes() - 1:
            break

    if not nx.is_tree(mst):
        raise ValueError("Input graph must be connected.")

    total_weight = sum(
        data["weight"]
        for _, _, data in mst.edges(data=True)
    )

    print("\nMST edges:")
    for u, v, data in mst.edges(data=True):
        print(f"{u} -- {v}: {data['weight']}")

    print("Total MST weight:", total_weight)

    return mst


def display_graph(G, pos, title, edge_color="black"):
    plt.figure(figsize=(8, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=900,
        font_weight="bold",
        edge_color=edge_color,
        width=2
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=nx.get_edge_attributes(G, "weight")
    )

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()




def main():

    # Generate a different random graph on each run
    G = generate_random_graph(
        num_nodes=6,
        num_edges=11
    )

    print("Original Graph")
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())
    print("Connected:", nx.is_connected(G))

    # Use the same layout for a fair visual comparison
    pos = nx.spring_layout(G, seed=42)

    display_graph(
        G, pos,
        "Original Random Weighted Graph"
    )

    # Calculate the MST
    MST = MyMinimumSpanningTree(G)

    print("\nMST node count:", MST.number_of_nodes())
    print("MST edge count:", MST.number_of_edges())
    print("MST is a tree:", nx.is_tree(MST))

    # Display the final MST
    display_graph(
        MST, pos,
        "Minimum Spanning Tree (Kruskal)",
        edge_color="red"
    )


if __name__ == "__main__":
      main()