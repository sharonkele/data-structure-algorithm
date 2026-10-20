import networkx as nx
import matplotlib.pyplot as plt


# a) Create and depict the original connected graph using matplotlib.
# b) Call the MyMinimumSpanningTree function.
# a. State which MST algorithm you are following.
# b. Show the creation of the MST step by step using the console.
# c) Depict the final MST using matplotlib.

def MyMinimumSpanningTree(Graph) -> nx.Graph:
    """
    Calculate an MST using Kruskal's algorithm.
    Print each edge decision and return the MST.
    """
    mst = nx.Graph()
    mst.add_nodes_from(Graph.nodes(data=True))

    # Sort edges from lowest to highest weight
    edges = sorted(
        Graph.edges(data=True),
        key=lambda edge: edge[2].get("weight", 1)
    )

    print("\nKruskal's Algorithm")
    print("Edges are considered in ascending weight order.")

    for u, v, data in edges:
        weight = data.get("weight", 1)

        # Adding an edge is allowed only if it does not
        # create a cycle.
        mst.add_edge(u, v, **data)

        if nx.is_forest(mst):
            print(
                f"ACCEPT: {u} -- {v}, weight = {weight}"
            )
        else:
            mst.remove_edge(u, v)
            print(
                f"REJECT: {u} -- {v}, weight = {weight} "
                "(would create a cycle)"
            )

        # An MST on n nodes has n - 1 edges
        if mst.number_of_edges() == Graph.number_of_nodes() - 1:
            break

    if not nx.is_tree(mst):
        raise ValueError("The input graph must be connected.")

    print("\nFinal MST edges:")
    for u, v, data in mst.edges(data=True):
        print(f"{u} -- {v}: {data['weight']}")

    total_weight = sum(
        data["weight"] for _, _, data in mst.edges(data=True)
    )
    print("Total MST weight:", total_weight)

    return mst


# ---------------------------------
# Create the original graph
# ---------------------------------

G = nx.Graph()

edges = [
    (1, 2, 4),
    (1, 3, 3),
    (1, 4, 7),
    (2, 3, 1),
    (2, 4, 5),
    (2, 5, 8),
    (3, 4, 6),
    (3, 5, 2),
    (3, 6, 9),
    (4, 5, 4),
    (5, 6, 3)
]

G.add_weighted_edges_from(edges)

print("Original graph:")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# Draw the original graph
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(7, 5))
nx.draw(
    G, pos, with_labels=True,
    node_color="lightblue", node_size=800
)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=nx.get_edge_attributes(G, "weight")
)
plt.title("Original Weighted Graph")
plt.show()

# ---------------------------------
# Run the MST algorithm
# ---------------------------------

MST = MyMinimumSpanningTree(G)

# ---------------------------------
# Draw the final MST
# ---------------------------------

plt.figure(figsize=(7, 5))
nx.draw(
    MST, pos, with_labels=True,
    node_color="lightgreen", node_size=800,
    edge_color="red", width=2
)
nx.draw_networkx_edge_labels(
    MST, pos, edge_labels=nx.get_edge_attributes(MST, "weight")
)
plt.title("Minimum Spanning Tree - Kruskal's Algorithm")
plt.show()