## Run this file periodically to update the joggler_network.html file

## Using this as a workaround - at the time of writing, Networkx is not supported in streamlit.

import pandas as pd
import numpy as np
from itertools import combinations

import networkx as nx
import plotly.graph_objects as go

def prepare_data(data):
    '''
    Output:
    - A list of jogglers,
    - A dataframe of events in which multiple jogglers participated
    '''

    jogglers = list(data['Joggler'].unique())

    # Group the data by date and event and list the jogglers participating
    joggled_together = pd.DataFrame(data.groupby(['Date','Event / Venue'])['Joggler'].apply(lambda x: list(np.unique(x))).reset_index())
    joggled_together = joggled_together[~joggled_together['Event / Venue'].isin(['Time Trial','IJA, Virtual'])].reset_index(drop=True)

    # Count the number of jogglers at each event, and remove any events where the joggler has joggled alone
    joggled_together['joggler_count'] = joggled_together['Joggler'].apply(lambda x: len(x))
    joggled_together = joggled_together[joggled_together['joggler_count']>1].reset_index(drop=True)

    return jogglers, joggled_together

def build_joggler_graph(jogglers,joggled_together):
    '''
    Output:
    - Graph G. Each joggler is a node, and edges indicate that jogglers took part in the same event.
    '''
    # Initialise networkx graph
    G = nx.Graph()
    
    # Add nodes to G
    G.add_nodes_from(jogglers)
    # len(G.nodes()), G.nodes   # check nodes created

    # For each pair of jogglers in the joggled_together dataframe, count the number of occurances they have joggled together.
    # Create an edge in the graph, with weight equal to this number of occurance.

    # initialise empty array to store # occurance each pair of jogglers have joggled together
    together_count_array = np.zeros(shape=(len(jogglers),len(jogglers)))
 
    # Loop over all events in which multiple jogglers have participated
    for i in range(len(joggled_together)):
        # Retrieve the list of jogglers at the event
        event_jogglers = joggled_together['Joggler'][i]
        # Get all pairwise combinations of these jogglers
        pairs = list(combinations(event_jogglers, 2))
        # Iterate through each pair of jogglers
        for j in range(len(pairs)):
            # Add 1 to the numpy row,col corresponding to each pair
            together_count_array[jogglers.index(pairs[j][0]),jogglers.index(pairs[j][1])] += 1

    # Add edges to G
    for i in range(together_count_array.shape[0]):
        for j in range(together_count_array.shape[1]):
            if together_count_array[i,j] >= 1:
                G.add_edge(jogglers[i], jogglers[j], weight=together_count_array[i,j])
            else:
                pass

    return G

def produce_plotly_figure(G, jogglers):
    '''
    Output:
    - Plotly Figure of graph G
    '''

    # Set layout of nodes
    pos = nx.spring_layout(G)

    # Assign positions to nodes
    for node in G.nodes:
        G.nodes[node]['pos'] = pos.get(node)

    # Prepare node and edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Greens',
            reversescale=False,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # Get list of nationalities for use in the node text
    nationalities = [data[data['Joggler'] ==j]['Nationality'].unique()[0]  for j in jogglers]
    nationalities = list(map(lambda x: x.replace('0', '?'), nationalities))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'{jogglers[node]} ({nationalities[node]}): # of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # Produce Plotly Fig
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Interactive Joggling Community: Who has joggled with who?',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)),
                )

    fig.update_layout( autosize=False, width=800, height=500, )

    return fig


# Load results data
data = pd.read_csv('results.csv')    ## xlsx not supported.
# Get list of Jogglers, and df of 'multi-joggler' events
jogglers, joggled_together = prepare_data(data)
# Produce Joggler Network Graph
G = build_joggler_graph(jogglers,joggled_together)
# Prepare figure for page
fig = produce_plotly_figure(G, jogglers)

# Save figure as html file
fig.write_html('joggler_network.html')


## Now can read this into my streamlit app without it running the code each time!