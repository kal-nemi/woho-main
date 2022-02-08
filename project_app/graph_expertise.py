"""
Swansea University Marketplace connection and visualising graph of experts
Created by: H. Matallah
Date: 29-07-2021
Modified: 12-08-2021
version: 1.0
"""
from pymongo import MongoClient
import re
import pandas as pd
from pyvis.network import Network
import networkx as nx
from django import template

register = template.Library()


def get_db_handle(db_name, host, port):
    client = MongoClient(host=host,
                         port=int(port),
                         )
    db_handle = client[db_name]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]


# todo:
# Connection to server. You will need to change this to your server.
db_handle, mongo_client = get_db_handle('db_swansea',
                                        'mongodb+srv://admin:admin@cluster0.zotwq.mongodb.net/db_swansea?retryWrites=true&w=majority',
                                        27017, )
expertise_collection_handle = get_collection_handle(db_handle, 'api_basic_areasofexpertise')
research_highlights_collection_handle = get_collection_handle(db_handle, 'api_basic_researchhighlights')
professors_collection_handle = get_collection_handle(db_handle, 'api_basic_professors')


class Prof_vis_expertise(object):
    def __init__(self, last_name, first_name, topic):
        self.last_name = last_name
        self.first_name = first_name
        self.G = None
        self.df = None
        self.expertise = topic;

        # Read related data
        self.profs, self.experts, self.research = self.read_data()
        # Get candidate id
        self.candidate_id = self.get_candidate_id(self.last_name, self.first_name, self.profs)

    def get_final_graph(self):
        if self.candidate_id:
            self.df = self.create_profs_connection(self.profs, self.research)
            self.main_exp(self.expertise, self.experts, self.profs, self.research, self.df)

    def create_profs_connection(self, profs, research):
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
        ex_cols = ['created_ID']
        df = pd.DataFrame(data=0, index=auth_set, columns=list(auth_set) + ex_cols)

        for auth in auth_set:
            # profs['abr_auth'] == auth]
            # df_ex.append(profs[profs['abr_auth'] == auth]['created_ID'].values)
            abr = profs[profs['abr_auth'] == auth]['abr_auth'].values
            abr_auth = abr[0] if len(abr) > 0 else 'None'
            df.loc[auth, 'created_ID'] = abr_auth
            # df_ex.append(abr_auth)
            for auth_b in co_auth_f:
                if auth in auth_b:
                    for auth1 in auth_b:
                        df.loc[auth, auth1] += 1

        return df

    def read_data(self):
        """ Reading the related data to the project
        Inputs: None
        Returns:   profs: dataframe of professors & doctors
                   experts: dataframe of expertise within the SU
                   research: dataframe of research publications with authors
        """
        profs = professors_collection_handle.find()
        experts = expertise_collection_handle.find()
        research = research_highlights_collection_handle.find()

        profs = pd.DataFrame(list(profs))
        experts = pd.DataFrame(list(experts))
        research = pd.DataFrame(list(research))

        return profs, experts, research

    def get_prof_from_expertise(self, expertise, experts1, profs1):
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

    def create_profs_connection(self, profs, research):
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

    def create_profs_graph_data(self, candidate, profs, experts, research):
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
        papers = research[research['created_ID'] == candidate]['year'].values.shape[0]

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
        # papers
        df.loc['papers', :] = 0
        df.loc[:, 'papers'] = 0
        df.loc['papers', candidate_name] = papers
        df.loc[candidate_name, 'papers'] = papers
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
        return df, list(exp_set)

    def from_expertise_to_profs(self, candidate_id, df1, expertise, i, experts, profs):
        df = df1.copy()
        ex1 = expertise
        ex = experts['area'].apply(lambda x: x.split(','))
        ex = ex.apply(lambda x: [x1.strip().lower() for x1 in x])
        exx = ex.apply(lambda x: 1 if ex1.lower() in x else 0)
        # exx[exx == 1].index
        new_candidates_id = experts['created_ID'].iloc[exx[exx == 1].index].values
        print('new_candidate_id', new_candidates_id)
        # new_candidates = profs[profs['created_ID'] == new_candidates_id[0]]
        '''
        if (len(new_candidates_id) == 1 and new_candidates_id[0] != candidate_id) \
                or len(new_candidates_id) > 1:
            # Add the new candidate to the dataframe graph df
            area_string = 'Area of Expertise_' + str(i)
            df[area_string] = 0
            df.loc[area_string] = 0
            df.loc[area_string, ex1] = 1
            df.loc[ex1, area_string] = 1 '''

        for new_cd in new_candidates_id:
            new_candidates = profs[profs['created_ID'] == new_cd]

            # if new_candidates_id[0] != candidate_id:
            if new_cd != candidate_id:
                new_candidate = new_candidates['last_name'].values[0] + ', ' + new_candidates['first_name'].values[0][0]
                print('new_candidate:', new_candidate)

                df[new_candidate] = 0
                df.loc[new_candidate] = 0
                # df.loc[area_string, new_candidate] = 1
                # df.loc[new_candidate, area_string] = 1
                df.loc[ex1, new_candidate] = 1
                df.loc[new_candidate, ex1] = 1

        return df

    def create_graph_viz(self, df_sample, profs, candidate):
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

    def visualise_net(self):
        """Visualise the networkx graph in an html format
        Inputs: G: Networkx graph
        """
        # Create the pyvis network to visualise
        nt = Network('600px', '1000px')
        # populates the nodes and edges data structures
        nt.from_nx(self.G)
        nt.save_graph(r'C:\Users\User\OneDrive\Other\Desktop\Shared\su-collaboration-hub\project_app\templates\pages\graph_expertise.html')
        # nt.show(r'C:\Users\User\OneDrive\Other\Desktop\Shared\su-collaboration-hub\project_app\templates\pages\nx.html')

    def save_graph(self):
        pass

    def main_exp(self, expertise, experts, profs, research, df):
        """ Process and return the expert person"""
        if expertise == None:
            print('No expertise field is given')
            return -1

        candidates = self.get_prof_from_expertise(expertise, experts, profs)

        # sample from dataframe df
        entry_name = 'Lavery, N'
        # entry_name = candidates[0]['last_name'].values[0] + ', ' + candidates[0]['first_name'].values[0][0]
        # entry_name_list = [x for x in df.index if entry_name in x]
        df_sample = df.drop('cr_id', axis=1)
        # df_sample = df_sample[df_sample.loc[entry_name] > 0]
        df_sample = df_sample[df_sample.index]

        # Create the network graph
        self.G = self.create_graph_viz(df_sample, profs, entry_name)
        # Visualise the graph
        self.visualise_net()

    def main_candidate(self, candidate, experts, profs, research):
        """ Process and return the expert person"""
        if candidate == None:
            print('No Candidate person is given')
            return -1

        df, exp_list = self.create_profs_graph_data(candidate, profs, experts, research)

        # Check expertise with other profs
        # expertise = exp_list[-1]  # .lower()
        for i, expertise in enumerate(exp_list, start=1):
            # expertise = exp_list[4].lower()
            # expertise = expertise.lower()
            print('Exp: ', expertise)
            df = self.from_expertise_to_profs(candidate, df, expertise, i, experts, profs)

        '''# sample from dataframe df
        df_sample = df.drop('cr_id', axis=1)
        df_sample = df_sample[df_sample.loc[entry_name] > 0]
        df_sample = df_sample[df_sample.index] '''
        self.df = df

        # Create the network graph
        prof_name = profs[profs['created_ID'] == candidate]
        entry_name = prof_name['last_name'].values[0] + ', ' + prof_name['first_name'].values[0][0]
        self.G = self.create_graph_viz(df, profs, entry_name, exp_list)
        # Visualise the graph
        self.visualise_net()

    def get_candidate_id(self, last_name, first_name, profs):
        candidate = profs[(profs['first_name'] == first_name) & (profs['last_name'] == last_name)]
        return candidate['created_ID'].values[0]

# if __name__ == "__main__":
#     # Given the first_name and last_name of a person
#     # search for expertise in the field and visualise
#     # Some examples
#     last_names = ['Croft', 'Gethin', 'Hassan']
#     first_names = ['Nick', 'David', 'Oubay']
#     # When i == 1, the area is 'Null', which needs to be addressed as Gethin has a lot of expertise
#     i = 0
#     last_name = last_names[i]
#     first_name = first_names[i]
#
#     prof = Prof_vis(last_name, first_name)
#     # visualise the networkx plot in html
#     prof.get_final_graph()
