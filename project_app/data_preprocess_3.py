"""
Swansea University Marketplace connection and visualising graph of experts
Created by: H. Matallah
Date: 29-07-2021
Modified: 12-08-2021
version: 1.0
"""
import re
import pandas as pd
from pyvis.network import Network
import networkx as nx


def read_data():
    """ Reading the related data to the project
    Inputs: None
    Returns:   profs: dataframe of professors & doctors
               experts: dataframe of expertise within the SU
               research: dataframe of research publications with authors
    """
    file_profs = './Data-from-Marcin-3/swansea_professors_db.csv'
    file_exp = './Data-from-Marcin-3/swansea_areas_of_expertise_db.csv'
    file_res = './Data-from-Marcin-3/swansea_research_highlights_db.csv'
    profs = pd.read_csv(file_profs)
    experts = pd.read_csv(file_exp)
    research = pd.read_csv(file_res)
    # print(profs.head())
    return profs, experts, research


def get_prof_from_expertise(expertise, experts1, profs1):
    """From expertise keyword returns an expert in the field
    Inputs: expertise: keyword
            experts1: dataframe of expertise and experts
            profs1: dataframe of experts with their info
        Returns: candidate: person who has the expertise:keyword
    """
    expertise = expertise.lower()
    candidates = []
    for row in experts1[['created_ID', 'area']].iterrows():
        field = row[1]['area']
        if field == 'Null':
            continue
        words = field.split(',')
        words = [w.strip() for w in words]
        words = [s.lower() for s in words]
        if any(expertise in w for w in words):
            # if len(words) > 0:
            id = row[1]['created_ID']
            candidate = profs1[profs1['created_ID'] == id]
            print('candidate', candidate['last_name'])
            candidates.append(candidate)

    return candidates


def create_profs_connection(profs, research):
    """Create a dataframe that connects each prof with others
    Inputs: profs: dataframe of experts with their info
            research: research expertise in the area column & created_ID
    Returns: df: dataframe connection of all professors and doctors in the Uni
    """

    profs['abr_auth'] = profs['last_name'].apply(lambda x: x + ', ') + \
        profs['first_name'].apply(lambda x: x[0])

    delimiters = ".,", "& ", ". ", "."
    # example = "Jenkins, C., Brown, J., Li, L., Johnstone, W., & Uttamchandani, D."
    regexPattern = '|'.join(map(re.escape, delimiters))
    # regexPattern
    # re.split(regexPattern, example)
    co_auth = []
    main_auth = []
    for auth in research['authors']:
        authors = re.split(regexPattern, auth)
        # authors = re.split(regexPattern, auth.strip())
        co_auth.append(authors)
        main_auth.append(authors[0])

    main_auth = [x.strip() for x in main_auth]
    research['main_auth'] = main_auth
    co_auth_f = [[y.strip() for y in x if y not in (None, '', ' ')] for x in co_auth]

    flat_list = [item for sublist in co_auth_f for item in sublist]
    auth_set = set(flat_list)
    ex_cols = ['cr_id']
    df = pd.DataFrame(data=0, index=auth_set, columns=list(auth_set) + ex_cols)

    for auth in auth_set:
        # profs['abr_auth'] == auth]
        # df_ex.append(profs[profs['abr_auth'] == auth]['created_ID'].values)
        abr = profs[profs['abr_auth'] == auth]['abr_auth'].values
        abr_auth = abr[0] if len(abr) > 0 else 'None'
        df.loc[auth, 'cr_id'] = abr_auth
        # df_ex.append(abr_auth)
        for auth_b in co_auth_f:
            if auth in auth_b:
                for auth1 in auth_b:
                    df.loc[auth, auth1] += 1

    return df


def create_profs_graph_data(candidate, profs, experts, research):
    """Create a dataframe that connects each prof with others
    Inputs: candidate: the person to check expertise & other things
            profs: dataframe of experts with their info
            experts: ???
            research: research expertise in the area column & created_ID
    Returns: df: dataframe connection of all professors and doctors in the Uni
    """

    # create area of expertise for the candidate prof
    first_name = profs[profs['created_ID'] == candidate]['first_name'].values[0]
    last_name = profs[profs['created_ID'] == candidate]['last_name'].values[0]
    expertise = experts[experts['created_ID'] == candidate]['area'].values
    expertise1 = [s.strip() for s in expertise[0].split(',')]

    # create research paper for the candidate prof
    papers = experts[experts['created_ID'] == candidate]['year'].values

    # create the collaboration opportunity for the candidate
    # To do: to be added later

    # create the dataframe to be visualised later
    exp_set = set(expertise1)  # use set, so we do not create duplicate
    candidate_name = last_name + ', ' + first_name[0]
    columns = [candidate_name, 'Area of Expertise'] + list(exp_set)
    df = pd.DataFrame(data=0, index=columns, columns=columns)
    # fill the dataframe connection
    df.loc[candidate_name, 'Area of Expertise'] = 3.0
    df.loc['Area of Expertise', candidate_name] = 3.0
    for area in exp_set:
        df.loc['Area of Expertise', area] = 1.0
        df.loc[area, 'Area of Expertise'] = 1.0
    '''
    profs['abr_auth'] = profs['last_name'].apply(lambda x: x + ', ') + \
                        profs['first_name'].apply(lambda x: x[0])

    delimiters = ".,", "& ", ". ", "."
    # example = "Jenkins, C., Brown, J., Li, L., Johnstone, W., & Uttamchandani, D."
    regexPattern = '|'.join(map(re.escape, delimiters))
    # regexPattern
    # re.split(regexPattern, example)
    co_auth = []
    main_auth = []
    for auth in research['authors']:
        authors = re.split(regexPattern, auth)
        # authors = re.split(regexPattern, auth.strip())
        co_auth.append(authors)
        main_auth.append(authors[0])

    main_auth = [x.strip() for x in main_auth]
    research['main_auth'] = main_auth
    co_auth_f = [[y.strip() for y in x if y not in (None, '', ' ')] for x in co_auth]

    flat_list = [item for sublist in co_auth_f for item in sublist]
    auth_set = set(flat_list)
    ex_cols = ['cr_id']
    df = pd.DataFrame(data=0, index=auth_set, columns=list(auth_set) + ex_cols)

    for auth in auth_set:
        # profs['abr_auth'] == auth]
        # df_ex.append(profs[profs['abr_auth'] == auth]['created_ID'].values)
        abr = profs[profs['abr_auth'] == auth]['abr_auth'].values
        abr_auth = abr[0] if len(abr) > 0 else 'None'
        df.loc[auth, 'cr_id'] = abr_auth
        # df_ex.append(abr_auth)
        for auth_b in co_auth_f:
            if auth in auth_b:
                for auth1 in auth_b:
                    df.loc[auth, auth1] += 1
    '''
    return df


def create_graph_viz(df_sample, profs, candidate):
    """ Create create the graph from the sampled dataframe
    Inputs: df_sample: dataframe containing connection between profs
            profs: dataframe of professors and doctors
            candidate: the expert chosen
        Returns: G: networkx Graph of candidate connections
    """
    G = nx.from_pandas_adjacency(df_sample)
    for auth, value in df_sample.iterrows():
        # print(i, auth, ' value:', type(value))
        auth_data = profs[profs['abr_auth'] == auth]  # research.iloc[i]['created_ID']
        # print(i, cr_id, profs[profs['created_ID'] == cr_id]['title'].values)
        if not auth_data.empty:
            title = auth_data['title'].values[0]
            location = auth_data['location'].values[0]
            about = auth_data['about'].values[0]
            if title == 'Professor':
                size = 20
                group = 1
            elif title == 'Dr':
                size = 15
                group = 2
            else:
                size = 10
                group = 3
        else:
            title = 'None'
            location = 'None'
            about = 'None'
            size = 5
            group = 10
        G.nodes[auth]['title'] = title
        G.nodes[auth]['location'] = location
        G.nodes[auth]['about'] = about
        G.nodes[auth]['size'] = size
        G.nodes[auth]['group'] = group
    G.nodes[candidate]['size'] = 30
    return G


def visualise_net():
    """Visualise the networkx graph in an html format
    Inputs: G: Networkx graph
    """
    # Create the pyvis network to visualise
    nt = Network('800px', '1000px')
    # populates the nodes and edges data structures
    nt.from_nx(G)
    nt.show('nx.html')


def main(expertise, experts, profs, research, df):
    """ Process and return the expert person"""
    if expertise == None:
        print('No expertise field ig given')
        return -1

    candidates = get_prof_from_expertise(expertise, experts, profs)

    # sample from dataframe df
    entry_name = 'Lavery, N'
    # entry_name = candidates[0]['last_name'].values[0] + ', ' + candidates[0]['first_name'].values[0][0]
    # entry_name_list = [x for x in df.index if entry_name in x]
    df_sample = df.drop('cr_id', axis=1)
    df_sample = df_sample[df_sample.loc[entry_name] > 0]
    df_sample = df_sample[df_sample.index]

    # Create the network graph
    G = create_graph_viz(df_sample, profs, entry_name)
    # Visualise the graph
    visualise_net(G)


if __name__ == "__main__":
    # expertise = 'Computational'
    expertise = 'In-silico'
    profs, experts, research = read_data()
    # Get the profs connection dataframe
    df = create_profs_connection(profs, research)
    # search for experts in the field "expertise" and visualise
    main(expertise, experts, profs, research, df)
