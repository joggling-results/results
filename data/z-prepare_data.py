import pandas as pd
import numpy as np
from itertools import combinations
import math

import networkx as nx
import plotly.graph_objects as go

## Load the Initial Data
data = pd.read_csv('data/results.csv')    ## xlsx not supported.
print('Data Loaded')

## Create Joggler Level Pivot and save to csv.
def make_joggler_pivot(data = pd.read_csv('data/results.csv')) -> pd.DataFrame:
    '''
    Load the result data, group by joggler to record #results, earliest and latest etc.

    Separately, pivot the result data to find each jogglers fastest times over a set of common distances.

    Merge these datasets together.

    Returns:
        joggler_df: pd.DataFrame
    '''

    # Filter out relays
    data = data[~data['Distance'].isin(['3b 4x100m','3b 4x200m','3b 4x400m'])]

    # Create table at joggler level: nationality, years active
    joggler_df = (data.groupby(['Joggler','Nationality','Gender'])
                    .agg({'Year':['min','max'],'Event / Venue':'count'})
                    .reset_index()
                    .replace({'0':'Unknown'})
    )
    joggler_df.columns = ['Joggler','Nationality','Gender','First Active','Last Active','Entry Count']
    joggler_df['Years Active'] = 1 + joggler_df['Last Active'] - joggler_df['First Active']
    joggler_df = joggler_df[['Joggler','Nationality','Gender','Years Active','First Active','Last Active','Entry Count']]

    # Create personal best times for common events for each joggler
    pivot_df = pd.pivot_table(data,
                            values='Finish Time',
                            index='Joggler', 
                            columns='Distance', 
                            aggfunc='min')
    pivot_df = pivot_df[['3b 100m', 
                        '3b 400m',
                        '3b Mile',
                        '3b 5km',
                        '3b 10km',
                        '3b Half Marathon',
                        '3b Marathon',
                        '5b 100m',
                        '5b Mile',
                        '5b 5km']].reset_index().fillna('-')

    # Merge to produce single joggler_df
    joggler_df = joggler_df.merge(pivot_df,on='Joggler')

    return joggler_df
 
joggler_df = make_joggler_pivot(data)
joggler_df.to_csv('data/joggler_pivot.csv',index=False)
print('Joggler Pivot Complete')

## Create Pivot of jogglers by country by year for Joggler Map
def make_country_year_pivot(data = pd.read_csv('data/results.csv')) -> pd.DataFrame:
    '''
    Source the results data, group by joggler to get the year of their latest result, and pivot by nationality

    Return:
        pivot_df: pd.DataFrame
    '''

    ## Remove relay events from the data - nationality not well defined.
    data = data[~data['Distance'].isin(['3b 4x100m','3b 4x200m','3b 4x400m'])]

    grouped_df = (data[['Joggler','Nationality','Year']].groupby('Joggler')
                                                        .max()
                                                        .reset_index())
    grouped_df['Nationality'].replace({'0':'Unknown'}, 
                                      inplace=True)
    
    pivot_df = (pd.pivot_table(grouped_df,
                              values='Joggler',
                              index='Year',
                              columns='Nationality',
                              aggfunc='count')
                  .fillna(0)
                  .reset_index())
    
    return pivot_df

map_pivot_df = make_country_year_pivot(data)
map_pivot_df.to_csv('data/map_pivot.csv',index=False)
print('Joggler Map Data Complete')

## Produce Ranking Lists by Event and Gender
def make_all_time_list(gender, distance, data = pd.read_csv('data/results.csv')) -> pd.DataFrame:
    '''
    Source the results data, filter to distance and gender, and group by joggler to find their fastest time. Rank fastest to slowest.

    Return:
        fastest_times: pd.DataFrame
    '''
    # Filter to gender
    data = data[data['Gender'] == gender]
    
    # Get the fastest time by joggler for the distance
    fastest_times = data[data['Distance'] == distance][['Joggler','Finish Time']].groupby(['Joggler']).min().reset_index()
    
    # Merge back on the joggler nationality
    fastest_times = fastest_times.merge(data,how='left',left_on=['Joggler','Finish Time'],right_on=['Joggler','Finish Time'])
    
    # Add a ranking column (rank 1  = fastest)
    fastest_times['Ranking'] = pd.to_numeric(fastest_times['Finish Time'].rank(method="min")).astype(int)
    
    # Filling Unknown Nationalities
    fastest_times['Nationality'] = fastest_times['Nationality'].replace({'0':'Unknown'})  # 0 loaded in as a string
    
    # Column selection
    fastest_times = fastest_times[['Ranking','Finish Time', 'Joggler','Gender','Nationality','Date','Event / Venue','Notes / Result Links']].sort_values('Ranking').reset_index(drop=True)
    
    return fastest_times

distance_list = ["3b 5km", "3b 10km", '3b Half Marathon', '3b Marathon', '5b 5km','5b Marathon',
                 "3b 800m", "3b 1500m", "3b Mile", "5b Mile",
                 "3b 100m", "5b 100m", "7b 100m", "3b 200m", "3b 400m", "5b 400m","3b 4x100m","3b 4x400m",]

for gender in ['M','F']:
    for distance in distance_list:
        # Prepare file name based on gender and distance
        file_string = 'ranking_' + gender + '_' + distance.replace(' ','_')
        # Produce dataframe of rankings
        fastest_times = make_all_time_list(gender,distance,data)
        # Save to csv file
        fastest_times.to_csv(f'data/{file_string}.csv',index=False)
print('All Time Lists Complete')


## Produce Joggler Network dataframes (Giduz Number) and Plotly Viz 
def prepare_data(data = pd.read_csv('data/results.csv')):
    '''
    Output:
    - A list of jogglers,
    - A dataframe of events in which multiple jogglers participated
    '''

    ## Remove relay events from the data - nationality not well defined.
    data = data[~data['Distance'].isin(['3b 4x100m','3b 4x200m','3b 4x400m'])]

    jogglers = list(data['Joggler'].unique())

    # Group the data by date and event and list the jogglers participating
    joggled_together = pd.DataFrame(data.groupby(['Date','Event / Venue'])['Joggler'].apply(lambda x: list(np.unique(x))).reset_index())
    # Remove Time Trials and Virtual IJA's - the jogglers did not joggle in person
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

# Get list of Jogglers, and df of 'multi-joggler' events
jogglers, joggled_together = prepare_data(data)
# Produce Joggler Network Graph
G = build_joggler_graph(jogglers,joggled_together)
# Prepare figure for page
fig = produce_plotly_figure(G, jogglers)

# Save figure as html file
fig.write_html('data/joggler_network.html')
print('Joggler Network Plot Complete')

# Create dataframe of giduz_number
sp_dict = nx.shortest_path(G, source='Bill Giduz', target=None, weight=None, method='dijkstra')
giduz_df = pd.DataFrame({'Joggler':jogglers})

def calculate_giduz_path(joggler):
    try:
        bg_path = sp_dict[joggler]
    except:
        bg_path = 'No Connection to Bill Giduz'

    return bg_path

def calculate_giduz_number(bg_path):
    if  bg_path == 'No Connection to Bill Giduz':
        giduz_number = math.inf
    else:
        giduz_number = len(bg_path) - 1
    return giduz_number

giduz_df['Giduz_Path'] = giduz_df['Joggler'].apply(lambda x: calculate_giduz_path(x))
giduz_df['Giduz_Number'] = giduz_df['Giduz_Path'].apply(lambda x: calculate_giduz_number(x))
giduz_df = (giduz_df.sort_values('Giduz_Number')
                    .reset_index(drop=True)
                    .merge(data[['Joggler','Nationality','Gender']].drop_duplicates(),
                           how='left',
                           on='Joggler')
)
giduz_df['Nationality'] = giduz_df['Nationality'].replace({'0':'Unknown'})

giduz_df.to_csv('data/giduz_df.csv',index=False)
