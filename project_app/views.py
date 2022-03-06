from django.core import paginator
from django.db.models import query
from typing import ContextManager, Counter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from numpy import integer
from traitlets.traitlets import default
from project_app.experts import get_experts
from project_app.startup_data import companies_data
# from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
# from .forms import UserUpdateForm
import requests
import base64
from decouple import config
from urllib.parse import urlencode
from math import ceil
from .graph_expertise import Prof_vis_expertise
from .graph_professors import Prof_vis_professors
from pyvis.network import Network
from django.views.decorators.clickjacking import xframe_options_exempt

from .suppliers import read_data_csv
from .tenders import read_data_csv2
from .pagination import pagination
import plotly.graph_objects as go
import pandas as pd
import re
from .forms import AddSpace
from .models import Space
from json import dumps

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
@xframe_options_exempt
def ok_to_load(request, index=0):
    return render(request, f"pages/graphs/graph_professors_{index}.html")


@xframe_options_exempt
def expertise_graph(request):
    return render(request, f'pages/graphs/{request.user}-expertise_graph.html')


@xframe_options_exempt
def graph_frame(request, index=0):
    return render(request, f'pages/graphs/{request.user}-graph_professors_{index}.html')



@login_required
def homepage(request):
    topic_result = ""
    experts = []
    threshold = 0.35
    topic = request.GET.get('topicquery')
    if topic:
        request.session['topicquery'] = topic
        response = requests.get(f"https://su-semantic-api.herokuapp.com/get_expert?topic={topic}&filter={threshold}")
        if response.status_code == 204:
            topic_result = []
        else:
            topic_result = response.json()

            for topic in topic_result:
                net_map = Prof_vis_professors(topic['LastName'], topic['FirstName'], topic['id'])
                net_map.get_final_graph()
    context = {
        'topic_query': topic,
        'topics': topic_result,
    }
    return render(request, 'pages/search.html', context)


@login_required
def network_map(request):
    topic_result = ""
    experts = []
    threshold = 0.35
    topic = request.GET.get('mapquery')
    if topic:
        request.session['mapquery'] = topic
        response = requests.get(f"https://su-semantic-api.herokuapp.com/get_expert?topic={topic}&filter={threshold}")
        if response.status_code == 204:
            topic_result = []
        else:
            topic_result = response.json()

            net_map = Prof_vis_professors(topic_result[0]['LastName'], topic_result[0]['FirstName'])

            net_map.get_final_graph()
    context = {
        'topic_query': topic,
        'topics': topic_result,
    }
    return render(request, 'pages/search_graph_professors.html', context)


@login_required
def search_professors(request):
    topic_result = ""
    experts = []
    threshold = 0.35
    topic = request.GET.get('professors_site')
    if topic:
        request.session['professors_site'] = topic
        response = requests.get(f"https://su-semantic-api.herokuapp.com/get_expert?topic={topic}&filter={threshold}")
        if response.status_code == 204:
            topic_result = []
        else:
            topic_result = response.json()

            net_map = Prof_vis_professors(topic_result[0]['LastName'], topic_result[0]['FirstName'])

            net_map.get_final_graph()
    context = {
        'topic_query': topic,
        'topics': topic_result,
    }
    return render(request, 'pages/search_graph_professors.html', context)


@login_required
def search_expertise(request):
    topic_result = ""
    experts = []
    threshold = 0.35
    topic = request.GET.get('expertise_site')
    if topic:
        request.session['expertise_site'] = topic
        response = requests.get(f"https://su-semantic-api.herokuapp.com/get_expert?topic={topic}&filter={threshold}")
        if response.status_code == 204:
            topic_result = []
        else:
            topic_result = response.json()

            net_map = Prof_vis_expertise(topic_result[0]['LastName'], topic_result[0]['FirstName'], topic)

            net_map.get_final_graph()
    context = {
        'topic_query': topic,
        'topics': topic_result,
    }
    return render(request, 'pages/search_graph_expertise.html', context)


@login_required
def expertise_map(request):

    topic_query = request.GET.get('topicquery')

    if topic_query:
        topics = topic_query.split(',')
        topics = [topic.strip() for topic in topics]
        threshold = 0.35
        net = Network(width="100%")

        for topic in topics:
            response = requests.get(f"https://su-semantic-api.herokuapp.com/get_expert?topic={topic}&filter={threshold}")
            if response.status_code == 204:
                topic_result = []
            else:
                topic_result = response.json()
            net.add_node(topic, label=topic, title=topic, color='#00ff1e', size=32)

            for expert in topic_result:
                expert_name = f"{expert['FirstName']} {expert['LastName']}"
                net.add_node(expert_name, expert_name, title=expert_name, color='#dd4b39', size=24)
                net.add_edge(topic, expert_name)

                # Professor expertise

                # for expertise in expert['AreaOfExpertise']:
                #     net.add_node(f"{expert_name} {expertise}", expertise, title=expertise, color='#162347', size=16)
                #     net.add_edge(expert_name, f"{expert_name} {expertise}")
        net.save_graph(f'project_app/templates/pages/graphs/{request.user}-expertise_graph.html')
        context = {
            'show': True
        }
        return render(request, f'pages/expertise.html', context)

    return render(request, 'pages/expertise.html')


'''
@login_required
def expertise_map_new(request):

    topic_query = request.GET.get('topicquery')

    if topic_query:
        topics = topic_query.split(',')
        topics = [topic.strip() for topic in topics]
        net = Network(width="100%")

        for topic in topics:
            topic_result = get_experts(topic)
            # if response.status_code == 204:
            #     topic_result = []
            # else:
            #     topic_result = response.json()
            net.add_node(topic, label=topic, title=topic, color='#00ff1e', size=32)

            for expert in topic_result:
                expert_name = f"{expert['first_name']} {expert['last_name']}"
                net.add_node(expert_name, expert_name, title=expert_name, color='#dd4b39', size=24)
                net.add_edge(topic, expert_name)

                # Professor expertise

                # for expertise in expert['AreaOfExpertise']:
                #     net.add_node(f"{expert_name} {expertise}", expertise, title=expertise, color='#162347', size=16)
                #     net.add_edge(expert_name, f"{expert_name} {expertise}")
        net.save_graph(f'project_app/templates/pages/graphs/{request.user}-expertise_graph.html')
        context = {
            'show': True
        }
        return render(request, f'pages/expertise.html', context)

    return render(request, 'pages/expertise.html')
'''


@login_required
def expertise_map_new(request):
    topic_query = request.GET.get('topicquery')
    if topic_query:
        topics = topic_query.split(',')
        topics = [topic.strip() for topic in topics]
        net = Network(width="100%")
        for topic in topics:
            data = companies_data(topic)
            # print(data)
            net.add_node(topic, label=topic, title=topic, color='#00ff1e', size=32)

            for company in data:
                company_name = f"{company['Company Name']}"
                net.add_node(company_name, company_name, title=company_name, color='#162347', size=16)
                net.add_edge(topic, company_name)

        net.save_graph(f'project_app/templates/pages/graphs/{request.user}-expertise_graph.html')
        context = {
            'show': True
        }
        return render(request, f'pages/expertise.html', context)

    return render(request, 'pages/expertise.html')


'''
@login_required
def search_new(request):
    experts = []
    topic_query = request.GET.get('topicquery')

    if topic_query:
        topic_result = get_experts(topic_query.strip())
        counter = 0
        for expert in topic_result:
            expert_info = {
                'id': counter,
                'Relevance': 'NA',
                'FirstName': expert['first_name'],
                'LastName': expert['last_name'],
                'title': expert['title'],
                'AreaOfExpertise': expert['area'].split(","),
                # 'About': df_supplierData['about'][supplier[0]],
            }
            experts.append(expert_info)
            net = Network(width="100%")
            expert_name = f"{expert['first_name']} {expert['last_name']}"
            net.add_node(expert_name, expert_name, title=expert_name, color='#00ff1e', size=40)
            net.add_node('Area of Expertise', 'Area of Expertise', color='#E1578A', size=32)
            net.add_edge(expert_name, 'Area of Expertise')
            areasOfExpertise = expert['area'].split(',')
            areasOfExpertise = [area.strip() for area in areasOfExpertise]
            for area in areasOfExpertise:
                net.add_node(area, area, title=area, color='#1E3163', size=24)
                net.add_edge(area, 'Area of Expertise')
                expertise_result = get_experts(area)
                for prof in expertise_result:
                    prof_name = f"{prof['first_name']} {prof['last_name']}"
                    if prof_name != expert_name:
                        net.add_node(prof_name, prof_name, title=prof_name, color='#dd4b39', size=16)
                        net.add_edge(area, prof_name)

            net.save_graph(f'project_app/templates/pages/graphs/{request.user}-graph_professors_{counter}.html')
            counter += 1

        context = {
            'topic_query': topic_query,
            'topics': experts,
        }
        return render(request, 'pages/search_new.html', context)

    return render(request, 'pages/search_new.html')
'''


@login_required
def search_new(request):
    topic_query = request.GET.get('topicquery')
    
    if topic_query:
        data = companies_data(topic_query.strip())
        # print(data)
        counter = 0
        startup = []
        for company in data:
            company_info = {
                'id': counter,
                'CompanyName': company['Company Name'],
                'Industry': company['Industry'].split("/"),
            }

            startup.append(company_info)
            net = Network(width="100%")
            company_name = f"{company['Company Name']}"
            net.add_node(company_name, company_name, title=company_name, color='#00ff1e', size=40)
            net.add_node('Industry', 'Industry', color='  # E1578A', size=32)
            net.add_edge(company_name, 'Industry')
            industry = company['Industry'].split("/")
            industry = [Industry.strip() for Industry in industry]

            for Industry in industry:

                net.add_node(Industry, Industry, title=Industry, color='#1E3163', size=24)
                net.add_edge(Industry, 'Industry')
                industries_data = companies_data(Industry)

                for type in industries_data:
                    if company_name:
                        net.add_node(company_name, company_name, title=company_name, color='#dd4b39', size=16)
                        net.add_edge(Industry, company_name)

            net.save_graph(f'project_app/templates/pages/graphs/{request.user}-graph_professors_{counter}.html')  # changing name leads to template error and display wrong graph
            counter += 1

        context = {
            'topic_query': topic_query,
            'startup': startup,
        }
        return render(request, 'pages/search_new.html', context)

    return render(request, 'pages/search_new.html')

@login_required
def add_new_tender(request):
    return render(request, 'pages/add_tender_form.html')


@login_required
def tender_search(request):
    topic_query=""
    topic_query = request.GET.get('topicquery')
    counter = 0
    #filer logic for tender contract value
    filtered=[]
    if topic_query:
        result=read_data_csv2(topic_query)

        # if filters are applied
        if (request.GET.get('tvalue')):
            tvalue = float(request.GET.get('tvalue'))
            for tender in result:
                if tender['contract_value']<=tvalue:
                    filtered.append(tender)
            #print(filtered)
            result=filtered
        if request.GET.get('sort'):
            if (int(request.GET.get('sort'))==1):
                result = sorted(result,key=lambda i: i['contract_value'],reverse=True)
            elif (int(request.GET.get('sort'))==0):
                result = sorted(result,key=lambda i: i['contract_value'],reverse=False)

        
        for company in result:
            company['id']=counter
            counter+=1

        #calling pagination function to get page object 
        page_obj=pagination(request,result)
        
        
        #datajson=dumps(result)
        context={'tenders':page_obj, 'keyword':topic_query,'count':counter}
        return render(request, 'pages/tender_search.html',context)

    return render(request, 'pages/tender_search.html',{'count':counter},)



@login_required
def home(request):
    return render(request, 'pages/home.html')

@login_required
def partner_search(request):

    #processes list to be shown in dropdown
    context={'processes': [  'Agriculture', 'Forestry', 'Assembly' ,'Fabrication' , 'Business Processes', 'Casting', 'Moulding', 'Forming', 'Forging',
            'Construction','Craft and Trade Processes','Design','Electrical','Electronics','Eroding ','ICT Process','Industrial Furnaces','Machining'
            ,'Metal Forming','Presswork','Printing','Photography','Ink Stamps','Prototyping','Quality','Statistics','Measurement','Renewable Energy','Renewable Materials'
            ,'Research','Development','Services','Sintering','Supply Chain','Surface treatment and coating','Tooling','Welding', 'brazing and soldering']}
    #get processes selected
    topic_query=request.GET.getlist("process")
    

    result=[]  #will contain final result list
    if(topic_query):
        result=read_data_csv(topic_query)
        
            
        # apply filters here    
        filtered=[]
        # if request.GET.get("standard"):
        #     standard=request.GET.get("standard")
        #     for supplier in result:
        #         if supplier['standards']==standard:
        #             filtered.append(supplier)
        #     print(filtered)
        #     result=filtered
        if request.GET.get("num"):
            n=float(request.GET.get("num"))
            for supplier in result:
                print(type(supplier['noOfEmployees']))
                if supplier['noOfEmployees']>=n:
                    filtered.append(supplier)
            print(filtered)
            result=filtered

     #after results are fetched assign ids to fetched results
    counter=0
    for company in result:
        company['id']=counter
        counter+=1

    page_obj=pagination(request,result)
    context['standards']=["ADS SC21 Signatory","AS9100", "BS 25999-1:2006 - Business Continuity","GTMA World Class","IMDS","Investors in Excellence","Investors in People","ISO 13485:2001","ISO 14001 - Environmental Management","ISO 15489-1:2001 - Records Management","ISO 9001:2000 - QMS Requirements","ISO 9001:2008 QMS Requirements","ISO/IEC 17799:2005 - Information Security Code of Practice","ISO/IEC 27001:2005 - IT Security Requirements","ISO/IEC/EN 17025","ISO/TS 16949:2002","ITIL Certified","Microsoft Certified Partner","Novell Business Partner","Oracle Certified Partner","PAS 124","Q1 (Ford Quality Standard)","QS 9000:1994","SHIFT","Sun Authorised Java Center","Technology Means Business","TS 16949 Updated","UKITA Quality Mark","UL508A","UL94"]
    context['suppliers']=page_obj
    context['count']=counter
    return render(request, 'pages/partner_search.html',context)

@login_required
def directory(request):
    mapbox_access_token = config('MAPBOX_ACCESS_TOKEN')
    topic_query=""
    topic_query = request.GET.get('topicquery')
    # print("dropdown : ",odering)
    # print(type(topic_query),topic_query)
    counter = 0
    filtered=[]
    context={}
    if topic_query:
        result=read_data_csv(topic_query)
        processes=[  'Agriculture & Forestry', 'Assembly & Fabrication' , 'Business Processes', 'Casting, Moulding, Forming, & Forging',
                'Construction','Craft and Trade Processes','Design','Electrical & Electronics','Eroding (EDM)','ICT Process','Industrial Furnaces','Machining'
                ,'Metal Forming & Press-work','Printing','Photography & Ink Stamps','Prototyping','Quality, Statistics & Measurement','Renewable Energy','Renewable Materials'
                ,'Research & Development','Services','Sintering','Supply Chain','Surface treatment & coating','Tooling','Welding', 'brazing & soldering']
        context['processes']=processes
        context['count']=counter

        if request.GET.get('process'):
            process=request.GET.get('process')
            context['process']=process
            #print(context['process'])
            for company in result:
                if process in company['profile']:
                    filtered.append(company)

            result=filtered
            
        if result:
            latitude=[]
            longitude=[]
            description=[]
            #longitude latitude and description from result
            for company in result:
                latitude.append(company['latitude'])
                longitude.append(company['longitude'])
                description.append(company['companyName'])

            # map
            fig = go.Figure(
                    go.Scattermapbox(
                    lat=latitude,
                    lon=longitude,
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=9
                    ),
                    text=description,
                    hovertemplate ="<b>%{text} </b>",
                )) 

            fig.update_layout(
                autosize=True,
                hovermode='closest',
                #hovermode=False,
                #hoverinfo="text",
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=latitude[0],
                        lon=longitude[0]
                    ),
                    pitch=0,
                    zoom=10
                ),
            )
            map=fig.to_html(full_html=False,default_height=500, default_width=1000)
            #fig.show()#map should come
            
            
            for company in result:
                company['id']=counter
                counter+=1
            
            page_obj=pagination(request,result)

            context['suppliers']=page_obj
            context['keyword']=topic_query
            context['map']=map
            context['count']=counter
            
    
        return render(request, 'pages/directory.html',context)

    return render(request,'pages/directory.html',{'count': counter} )

@login_required
def projects(request):
    return render(request, 'pages/projects.html')

@login_required
def clusters(request):
    return render(request, 'pages/clusters.html')

def woho_base(request):
    return render(request, 'pages/woho_base.html')
    
def woho_home(request):
    return render(request, 'pages/woho_home.html')

def woho_addspace(request):
    form=AddSpace()
    if request and request.method=='POST':
        if len(request.FILES)!=0:
            file=request.FILES.get("img")
        capacity=request.POST.get("capacity")
        address=request.POST.get("address")
        comments=request.POST.get("comments")
        s=Space(img=file,email=request.user.email,capacity=capacity,address=address,comments=comments)
        s.save()
        # form=AddSpace(request.POST,request.FILES)
        # if form.is_valid():
        #     form.save()
        
    context={
        'form':form,
    }    
    return render(request, 'pages/woho_addspace.html',context)
    