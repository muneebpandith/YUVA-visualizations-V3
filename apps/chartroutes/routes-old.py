from apps.chartroutes import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from collections import Counter
import random
import pandas as pd
import numpy as np
import itertools
from .chart import Chart
#from flask import Flask, render_template



def get_data(base_path='BaselineData', connect_type="filesystem"):
    if connect_type == "filesystem":
        print('Loading Data from File System...')
        data_corpus['businessdetails'] = pd.read_csv(base_path+'/Form 2/businessdetails.csv')
        data_corpus['businessidentity'] = pd.read_csv(base_path+'/Form 2/businessidentity.csv')
        data_corpus['manpowerengaged'] = pd.read_csv(base_path+'/Form 2/manpowerengaged.csv')
        data_corpus['business_result'] = data_corpus['businessdetails'].merge(data_corpus['businessidentity'], how='inner')
        
        data_corpus['household'] = pd.read_csv(base_path+'/Form 1/household.csv', low_memory=False)
        data_corpus['household_member'] = pd.read_csv(base_path+'/Form 1/household_member.csv')
        data_corpus['self_employment_seekers'] = pd.read_csv(base_path+'/Form 1/self_employment_seekers.csv')
        data_corpus['unregisteredactivities'] = pd.read_csv(base_path+'/Form 1/unregisteredactivities.csv')
        
        #data_corpus['peur_result'] = data_corpus['household_member'].merge(data_corpus['unregisteredactivities'], how='inner', left_on='uniqueid', right_on='memberid')
        #data_corpus['peu_result'] = data_corpus['household_member'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        #data_corpus['pee_result'] = data_corpus['household_member'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        #data_corpus['pee_result'] = data_corpus['pee_result'][data_corpus['pee_result']['pecategory']=='PEE']
        #data_corpus['peu_result'] = data_corpus['peu_result'][data_corpus['peu_result']['pecategory']=='PEU']
        #data_corpus['peur_result'] = data_corpus['peur_result'][data_corpus['peur_result']['pecategory']=='PEUR']

        data_corpus['hoh_member'] = data_corpus['household_member'][data_corpus['household_member']['relationwithhoh'] == 'Self'].copy()
        data_corpus['hoh_member']['trimmed_uniqueid'] = data_corpus['hoh_member']['uniqueidofmember'].str[:13] 
        data_corpus['hoh_result'] = data_corpus['hoh_member'].merge(data_corpus['household'], how='inner', left_on='trimmed_uniqueid', right_on='uniqueidofhousehold')


        #the datasheets finally used
        data_corpus['individual_member'] = data_corpus['household_member'].copy()
        data_corpus['individual_member']['trimmed_uniqueid'] = data_corpus['individual_member']['uniqueidofmember'].str[:13] 
        data_corpus['individual_member_result'] = data_corpus['individual_member'].merge(data_corpus['household'], how='inner', left_on='trimmed_uniqueid', right_on='uniqueidofhousehold')



        data_corpus['peur'] = data_corpus['individual_member_result'].merge(data_corpus['unregisteredactivities'], how='inner', left_on='uniqueid_x', right_on='memberid')
        data_corpus['peur'] = data_corpus['peur'][data_corpus['peur']['pecategory']=='PEUR']

        data_corpus['pee'] = data_corpus['individual_member_result'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid_x', right_on='memberid')
        data_corpus['pee'] = data_corpus['pee'][data_corpus['pee']['pecategory']=='PEE']

        data_corpus['peu'] = data_corpus['individual_member_result'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid_x', right_on='memberid')
        data_corpus['peu'] = data_corpus['peu'][data_corpus['peu']['pecategory']=='PEU']
        
        print(data_corpus['peur'].shape[0],data_corpus['pee'].shape[0], data_corpus['peu'].shape[0] )


        print('Loading Data: Successful!')
    elif connect_type == "google-drive":
        print('Loading Data from Google Drive!')
        data_corpus['gid_businessidentity'] = '1Fvrds513yknjDtqizSfk60JB_W1G1yjd'
        data_corpus['gid_businessdetails'] = '1ilaexFPOYPHXYNdXRppQh2VEVI9qZv4N'
        data_corpus['gid_manpowerengaged'] = '1rBzz6kNzpBQwvWAj93NXm1h4kaUgXPOd'

        data_corpus['url_businessidentity'] = f"https://drive.google.com/uc?id={data_corpus['gid_businessidentity']}&export=download"
        data_corpus['url_businessdetails'] = f"https://drive.google.com/uc?id={data_corpus['gid_businessdetails']}&export=download"
        data_corpus['url_manpowerengaged'] = f"https://drive.google.com/uc?id={data_corpus['gid_manpowerengaged']}&export=download"

        data_corpus['businessdetails'] = pd.read_csv(data_corpus['url_businessdetails'])
        data_corpus['businessidentity'] = pd.read_csv(data_corpus['url_businessidentity'])  #https://drive.google.com/file/d/1Fvrds513yknjDtqizSfk60JB_W1G1yjd/view?usp=sharing
        data_corpus['manpowerengaged'] = pd.read_csv(data_corpus['url_manpowerengaged'])

        #household
        data_corpus['gid_household'] = '1lD5OvSg9rAvPJR-kas_vn-wn1OatDr_L'
        data_corpus['gid_householdmember'] = '1zA5LjofLFsTsaKJbBKsVhyY8bYs3Pou9'
        data_corpus['gid_self_employment_seekers'] = '1AB8hDJYZy7wQdRX_AKZdZIgiePtkd0d_'
        data_corpus['gid_unregisteredactivities'] = '1Art08hVQ78krap0AWt32RKt37P6tymmX'

        data_corpus['url_household'] = f"https://drive.google.com/uc?id={data_corpus['gid_household']}&export=download"
        data_corpus['url_householdmember'] = f"https://drive.google.com/uc?id={data_corpus['gid_householdmember']}&export=download"
        data_corpus['url_self_employment_seekers'] = f"https://drive.google.com/uc?id={data_corpus['gid_self_employment_seekers']}&export=download"
        data_corpus['url_unregisteredactivities'] = f"https://drive.google.com/uc?id={data_corpus['gid_unregisteredactivities']}&export=download"



        data_corpus['household'] = pd.read_csv(data_corpus['url_household'])
        data_corpus['household_member'] = pd.read_csv(data_corpus['url_householdmember'])  #https://drive.google.com/file/d/1Fvrds513yknjDtqizSfk60JB_W1G1yjd/view?usp=sharing
        data_corpus['self_employment_seekers'] = pd.read_csv(data_corpus['url_self_employment_seekers'])
        data_corpus['unregisteredactivities'] = pd.read_csv(data_corpus['url_unregisteredactivities'])
       
        data_corpus['business_result'] = data_corpus['businessdetails'].merge(data_corpus['businessidentity'], how='inner')
        data_corpus['peur_result'] = data_corpus['household_member'].merge(data_corpus['unregisteredactivities'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['peu_result'] = data_corpus['household_member'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['pee_result'] = data_corpus['household_member'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['pee_result'] = data_corpus['pee_result'][data_corpus['pee_result']['pecategory']=='PEE']
        data_corpus['peu_result'] = data_corpus['peu_result'][data_corpus['peu_result']['pecategory']=='PEU']
        data_corpus['peur_result'] = data_corpus['peur_result'][data_corpus['peur_result']['pecategory']=='PEUR']
        print('Loading Data: Successful!')

        ### BUSINESS IDENTITY = https://drive.google.com/file/d/1Fvrds513yknjDtqizSfk60JB_W1G1yjd/view?usp=sharing
        ### MANPOWERENGAGED = https://drive.google.com/file/d/1rBzz6kNzpBQwvWAj93NXm1h4kaUgXPOd/view?usp=sharing
        ### BUSINESS DETAILS = https://drive.google.com/file/d/1ilaexFPOYPHXYNdXRppQh2VEVI9qZv4N/view?usp=sharing
        ###HOUSEHOLD = https://drive.google.com/file/d/1lD5OvSg9rAvPJR-kas_vn-wn1OatDr_L/view?usp=sharing
        ### HOUSEHOLD MEMBER = https://drive.google.com/file/d/1zA5LjofLFsTsaKJbBKsVhyY8bYs3Pou9/view?usp=sharing
        ### SELFWMPLOYEMENT SEEKERS = https://drive.google.com/file/d/1AB8hDJYZy7wQdRX_AKZdZIgiePtkd0d_/view?usp=sharing
        ### UNREGISTERED_ACTIVITIES = https://drive.google.com/file/d/1Art08hVQ78krap0AWt32RKt37P6tymmX/view?usp=sharing


data_corpus = dict()

load_subset = True

if load_subset == True:
    base_path = 'dataset/BaselineDataTest'
else:
    base_path = 'dataset/BaselineData'  

get_data(base_path=base_path)

#print(data_corpus['hoh_result'].columns)


#FOR SVG MAP
district_stats = dict()
for d in ['Anantnag', 'Baramulla', 'Budgam', 'Rajouri', 'Kupwara', 'Pulwama','Shopian', 'Poonch', 'Srinagar', 'Doda', 'Kulgam', 'Jammu', 'Kathua','Ganderbal', 'Bandipora', 'Reasi', 'Udhampur', 'Ramban', 'Kishtwar','Samba']:
    district_stats [d] = {"peu":"0", "peur":"0", "pee":"0", "individual_members":"0", "households":"0"}

households_districts = pd.DataFrame(data_corpus['hoh_result']['district'].value_counts())
individual_member_districts = pd.DataFrame(data_corpus['individual_member_result']['district'].value_counts())
peu_districts = pd.DataFrame(data_corpus['peu']['district'].value_counts())
pee_districts = pd.DataFrame(data_corpus['pee']['district'].value_counts())
peur_districts = pd.DataFrame(data_corpus['peur']['district'].value_counts())

for i in range (peu_districts.shape[0]):
    #print(peu_districts.index[i], peu_districts['count'].iloc[i])
    district_stats[peu_districts.index[i]]['peu'] =  str(int(district_stats[peu_districts.index[i]]['peu']) + peu_districts['count'].iloc[i])

for i in range (pee_districts.shape[0]):
    #print(peu_districts.index[i], peu_districts['count'].iloc[i])
    district_stats[pee_districts.index[i]]['pee'] = str(int(district_stats[pee_districts.index[i]]['pee'])+ pee_districts['count'].iloc[i])

for i in range (peur_districts.shape[0]):
    #print(peu_districts.index[i], peu_districts['count'].iloc[i])
    district_stats[peur_districts.index[i]]['peur'] = str(int(district_stats[peur_districts.index[i]]['peur'])+ peur_districts['count'].iloc[i])

for i in range (individual_member_districts.shape[0]):
    #print(peu_districts.index[i], peu_districts['count'].iloc[i])
    district_stats[individual_member_districts.index[i]]['individual_members'] = str(int(district_stats[individual_member_districts.index[i]]['individual_members']) + individual_member_districts['count'].iloc[i])

for i in range (households_districts.shape[0]):
    #print(peu_districts.index[i], peu_districts['count'].iloc[i])
    district_stats[households_districts.index[i]]['households'] = str(int(district_stats[households_districts.index[i]]['households']) + households_districts['count'].iloc[i])

household_numbers = data_corpus['hoh_member'].shape[0]
#household_numbers_f = f"{household_numbers:,}"

individual_numbers = data_corpus['individual_member_result'].shape[0]
#individual_numbers_f = f"{individual_numbers:,}"

peur_numbers = data_corpus['peur'].shape[0]


peu_numbers = data_corpus['peu'].shape[0]
#peu_numbers_f = f"{peu_numbers:,}"

pee_numbers = data_corpus['pee'].shape[0]
#pee_numbers_f = f"{pee_numbers:,}"

##### FOR NUMBERS ENDING   ####









###### OPTIONS ########
@blueprint.route('/api/v2/fetch_numbers')
# ** @login_required
def get_numbers():
    # household_numbers = data_corpus['hoh_member'].shape[0]
    # #household_numbers_f = f"{household_numbers:,}"

    # individual_numbers = data_corpus['individual_member_result'].shape[0]
    # #individual_numbers_f = f"{individual_numbers:,}"

    hoh_details = {'number':household_numbers,'from':'','to':''}
    ilp_details = {'number':individual_numbers,'from':'','to':''}
    peur_details = {'number':peur_numbers,'from':'','to':''}
    peu_details = {'number':peu_numbers,'from':'','to':''}
    pee_details = {'number':pee_numbers,'from':'','to':''}
    district_wise_details = {'number':district_stats,'from':'','to':''}
    

    #return jsonify({'hoh':household_numbers_f, 'individual_members':individual_numbers_f, 'peur':peur_numbers_f, 'pee':pee_numbers_f, 'peu':peu_numbers_f})
    return jsonify({'hoh':hoh_details, 'individual_members':ilp_details, 'peur':peur_details, 'pee':pee_details,  'peu':peu_details, 'district_wise_details': district_wise_details })


        



###### OPTIONS ########
@blueprint.route('/api/v2/fetch_options/<type_of_data>/<parameter>')
# ** @login_required
def get_options(type_of_data, parameter):
    """
    Fetches options based on the type of data and parameter.

    Args:
        type_of_data: The type of data to fetch options for (e.g., 'country', 'city').
        parameter: The parameter to filter options by (e.g., 'country_code').

    Returns:
        A JSON response containing the fetched options.
    """

    set_of_type_of_data = list(data_corpus.keys())
    try:
        # Replace this with your actual logic to fetch options 
        # based on type_of_data and parameter
        if type_of_data in set_of_type_of_data:
            #HOUSEHOLD PART
            if type_of_data == 'household':
                dataset_name = 'hoh_result'
                
                filtered_data = data_corpus[dataset_name]
                #print(list(filtered_data.columns))
                if parameter == 'residentialtype':
                    options = sorted(list(filtered_data['residentialtype'].unique()))
                
                elif parameter == 'district':
                    residentialtype = request.args.get("residentialtype")
                    #print(residentialtype)
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    options = list(filtered_data[parameter].unique())
                
                elif parameter == 'cdblockulbmc':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                    options = sorted(list(filtered_data[parameter].unique()))
                
                elif parameter == 'panchayatward':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    #print(residentialtype, district, blockmunicipality)
                    #options = []
                    if residentialtype == "All" and district == "All" and blockmunicipality == "All":
                        #print("Yesss")
                        options = []   
                    else:
                        if not residentialtype == "All":
                            filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = []  #not able to load due to issue with large corpus
                        else:
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = [] #not able to load due to issue with large corpus
                            
                
                elif parameter == 'gender':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    options = sorted(list(filtered_data[parameter].unique()))
                    #print(options)

                    

                
                elif parameter == 'annualhouseholdincome':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    gender = request.args.get("gender")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    options = sorted(list(filtered_data[parameter].unique()))
                    #options = list(data_corpus[type_of_data][parameter].unique())
                else:
                    abort(404, f"Invalid area_type '{parameter}'")
            
            
            
            elif type_of_data == 'individual_member':
                #ILP PART
                dataset_name = 'individual_member_result'
                filtered_data = data_corpus[dataset_name]
                #print(list(filtered_data.columns))
                if parameter == 'residentialtype':
                    options = sorted(list(filtered_data['residentialtype'].unique()))
                
                elif parameter == 'district':
                    residentialtype = request.args.get("residentialtype")
                    #print(residentialtype)
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    options = list(filtered_data[parameter].unique())
                
                elif parameter == 'cdblockulbmc':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                    options = sorted(list(filtered_data[parameter].unique()))
                
                elif parameter == 'panchayatward':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    #print(residentialtype, district, blockmunicipality)
                    #options = []
                    if residentialtype == "All" and district == "All" and blockmunicipality == "All":
                        #print("Yesss")
                        options = []   
                    else:
                        if not residentialtype == "All":
                            filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = []  #not able to load due to issue with large corpus
                        else:
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = [] #not able to load due to issue with large corpus
                            
                
                elif parameter == 'age':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    options = sorted(list(filtered_data[parameter].unique()))
                    #print(options)
                
                elif parameter == 'gender':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==age]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'employmentstatus':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'annualincome':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    employmentstatus = request.args.get("employmentstatus")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not employmentstatus == "All":
                        filtered_data = filtered_data[filtered_data['employmentstatus']==employmentstatus]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                else:
                    abort(404, f"Invalid area_type '{parameter}'")
            
            elif type_of_data == 'peur':
                #ILP PART
                dataset_name = 'peur'
                filtered_data = data_corpus[dataset_name]
                #print("********", filtered_data.shape)
                #print(list(filtered_data.columns))
                if parameter == 'residentialtype':
                    options = sorted(list(filtered_data['residentialtype'].unique()))
                
                elif parameter == 'district':
                    residentialtype = request.args.get("residentialtype")
                    #print(residentialtype)
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    options = list(filtered_data[parameter].unique())
                
                elif parameter == 'cdblockulbmc':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                    options = sorted(list(filtered_data[parameter].unique()))
                
                elif parameter == 'panchayatward':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    #print(residentialtype, district, blockmunicipality)
                    #options = []
                    if residentialtype == "All" and district == "All" and blockmunicipality == "All":
                        #print("Yesss")
                        options = []   
                    else:
                        if not residentialtype == "All":
                            filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = []  #not able to load due to issue with large corpus
                        else:
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = [] #not able to load due to issue with large corpus
                            
                
                elif parameter == 'age':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    options = sorted(list(filtered_data[parameter].unique()))
                    #print(options)
                
                elif parameter == 'gender':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==age]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'sectorofenterprise':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'natureofbusiness':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofenterprise = request.args.get("sectorofenterprise")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofenterprise == "All":
                        filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'sourceofrawmaterial':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofenterprise = request.args.get("sectorofenterprise")
                    natureofbusiness = request.args.get("natureofbusiness")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofenterprise == "All":
                        filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not natureofbusiness == "All":
                        filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data['rawmaterialsource'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                

                elif parameter == 'enterprisefinancialstatus':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofenterprise = request.args.get("sectorofenterprise")
                    natureofbusiness = request.args.get("natureofbusiness")
                    sourceofrawmaterial = request.args.get("sourceofrawmaterial")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofenterprise == "All":
                        filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not natureofbusiness == "All":
                        filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sourceofrawmaterial == "All":
                        filtered_data = filtered_data[filtered_data['rawmaterialsource']==sourceofrawmaterial]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data['statusofenterprise'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'currentmarketreach':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofenterprise = request.args.get("sectorofenterprise")
                    natureofbusiness = request.args.get("natureofbusiness")
                    sourceofrawmaterial = request.args.get("sourceofrawmaterial")
                    enterprisefinancialstatus = request.args.get("enterprisefinancialstatus")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofenterprise == "All":
                        filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not natureofbusiness == "All":
                        filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sourceofrawmaterial == "All":
                        filtered_data = filtered_data[filtered_data['rawmaterialsource']==sourceofrawmaterial]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not enterprisefinancialstatus == "All":
                        filtered_data = filtered_data[filtered_data['statusofenterprise']==enterprisefinancialstatusxxw]

                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'assistancerequiredyuva':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofenterprise = request.args.get("sectorofenterprise")
                    natureofbusiness = request.args.get("natureofbusiness")
                    sourceofrawmaterial = request.args.get("sourceofrawmaterial")
                    enterprisefinancialstatus = request.args.get("enterprisefinancialstatus")
                    currentmarketreach = request.args.get("currentmarketreach")
                    
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofenterprise == "All":
                        filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not natureofbusiness == "All":
                        filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sourceofrawmaterial == "All":
                        filtered_data = filtered_data[filtered_data['sourceofrawmaterial']==sourceofrawmaterial]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not enterprisefinancialstatus == "All":
                        filtered_data = filtered_data[filtered_data['statusofenterprise']==enterprisefinancialstatus]
                    
                    
                     
                    options = list(filtered_data['assistanceareyoulooking'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                else:
                    abort(404, f"Invalid area_type '{parameter}'")
            
            elif type_of_data == 'pee':
                #PEE PART
                dataset_name = 'pee'
                filtered_data = data_corpus[dataset_name]
                #print("********", filtered_data.shape)
                #print(list(filtered_data.columns))
                if parameter == 'residentialtype':
                    options = sorted(list(filtered_data['residentialtype'].unique()))
                
                elif parameter == 'district':
                    residentialtype = request.args.get("residentialtype")
                    #print(residentialtype)
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    options = list(filtered_data[parameter].unique())
                
                elif parameter == 'cdblockulbmc':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                    options = sorted(list(filtered_data[parameter].unique()))
                
                elif parameter == 'panchayatward':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    #print(residentialtype, district, blockmunicipality)
                    #options = []
                    if residentialtype == "All" and district == "All" and blockmunicipality == "All":
                        #print("Yesss")
                        options = []   
                    else:
                        if not residentialtype == "All":
                            filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = []  #not able to load due to issue with large corpus
                        else:
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = [] #not able to load due to issue with large corpus
                            
                
                elif parameter == 'age':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    options = sorted(list(filtered_data[parameter].unique()))
                    #print(options)
                
                elif parameter == 'gender':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==age]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'sectorofinterest':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'expectedscaleofbusiness':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofinterest = request.args.get("sectorofinterest")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofinterest == "All":
                        filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data['scaleofbusiness'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'assistancerequiredyuva':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofinterest = request.args.get("sectorofinterest")
                    expectedscaleofbusiness = request.args.get("expectedscaleofbusiness")
                    
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofinterest == "All":
                        filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not expectedscaleofbusiness == "All":
                        filtered_data = filtered_data[filtered_data['scaleofbusiness']==expectedscaleofbusiness]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    
                     
                    options = list(filtered_data['assistancelookingfor'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                else:
                    abort(404, f"Invalid area_type '{parameter}'")
            
            
            elif type_of_data == 'peu':
                #PEE PART
                dataset_name = 'peu'
                filtered_data = data_corpus[dataset_name]
                #print("********", filtered_data.shape)
                #print(list(filtered_data.columns))
                if parameter == 'residentialtype':
                    options = sorted(list(filtered_data['residentialtype'].unique()))
                
                elif parameter == 'district':
                    residentialtype = request.args.get("residentialtype")
                    #print(residentialtype)
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    options = list(filtered_data[parameter].unique())
                
                elif parameter == 'cdblockulbmc':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                    options = sorted(list(filtered_data[parameter].unique()))
                
                elif parameter == 'panchayatward':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    #print(residentialtype, district, blockmunicipality)
                    #options = []
                    if residentialtype == "All" and district == "All" and blockmunicipality == "All":
                        #print("Yesss")
                        options = []   
                    else:
                        if not residentialtype == "All":
                            filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = []  #not able to load due to issue with large corpus
                        else:
                            if not district == "All":
                                filtered_data = filtered_data[filtered_data['district']==district]
                                if not blockmunicipality == "All":
                                    filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                                    options = sorted(list(filtered_data[parameter].unique()))
                                else:
                                    options = sorted(list(filtered_data[parameter].unique()))
                            else:
                                options = [] #not able to load due to issue with large corpus
                            
                
                elif parameter == 'age':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    options = sorted(list(filtered_data[parameter].unique()))
                    #print(options)
                
                elif parameter == 'gender':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==age]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'sectorofinterest':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'expectedscaleofbusiness':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofinterest = request.args.get("sectorofinterest")
                    

                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofinterest == "All":
                        filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data['scaleofbusiness'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'assistancerequiredyuva':
                    residentialtype = request.args.get("residentialtype")
                    district = request.args.get("district")
                    blockmunicipality = request.args.get("cdblockulbmc")
                    panchayatward = request.args.get("panchayatward")
                    age = request.args.get("age")
                    gender = request.args.get("gender")
                    educationlevel = request.args.get("educationlevel")
                    sectorofinterest = request.args.get("sectorofinterest")
                    expectedscaleofbusiness = request.args.get("expectedscaleofbusiness")
                    
                    if not residentialtype == "All":
                        filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                        #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not district == "All":
                        filtered_data = filtered_data[filtered_data['district']==district]
                        #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    if not blockmunicipality == "All":
                        filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                        #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    if not panchayatward == "All":
                        filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not age== "All":
                        filtered_data = filtered_data[filtered_data['age']==panchayatward]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not gender == "All":
                        filtered_data = filtered_data[filtered_data['gender']==gender]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not educationlevel == "All":
                        filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    if not sectorofinterest == "All":
                        filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    if not expectedscaleofbusiness == "All":
                        filtered_data = filtered_data[filtered_data['scaleofbusiness']==expectedscaleofbusiness]
                        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    
                     
                    options = list(filtered_data['assistancelookingfor'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                else:
                    abort(404, f"Invalid area_type '{parameter}'")
                



        
        else:
            abort(404, f"Invalid type_of_data '{type_of_data}'")
        #return jsonify({'options': options, 'cols':list(data_corpus[type_of_data].columns)})
        return jsonify({'options': options})

        # if type_of_data in set_of_type_of_data:
        #     if type_of_data == 'household':

        #         options = ['area_type':['Rural','Urban']]

        # else:
        #     abort(404, f"Invalid type_of_data '{type_of_data}'")
        # return jsonify({'options': options, 'cols':list(data_corpus[type_of_data].columns)})


    except Exception as e:
        abort(500, f"An error occurred: {str(e)}")





charts_object = Chart()



###### CHARTS HOUSEHOLDS ########
@blueprint.route('/api/v2/charts/household')
# ** @login_required
def get_households_charts():
    return jsonify({"Hi":"Household charts"})


###### CHARTS HOUSEHOLDS FILTERED ########
@blueprint.route('/api/v2/charts-filtered/household')
def get_households_charts_filtered():
    dataset_name = 'hoh_result'
    #filtered_data = data_corpus[dataset_name]

    residentialtype = request.args.get("residentialtype")
    district = request.args.get("district")
    cdblockulbmc = request.args.get("cdblockulbmc")
    panchayatward = request.args.get("panchayatward")
    gender = request.args.get("gender")
    annualhouseholdincome = request.args.get("annualhouseholdincome")
    
    df = data_corpus[dataset_name]
    
    #print("*******ORIGINAL ****** ",df.shape[0])
    
    if not residentialtype == 'All':
    	df = df[df['residentialtype']==residentialtype]

    if not district == 'All':
    	df = df[df['district']==district]

    
    if not cdblockulbmc == 'All':
    	df = df[df['cdblockulbmc']==cdblockulbmc]
    
    if not panchayatward == 'All':
    	df = df[df['panchayatward']==panchayatward]
    
    if not gender == 'All':
    	df = df[df['gender']==gender]
    
    if not annualhouseholdincome == 'All':
    	df = df[df['annualhouseholdincome']==annualhouseholdincome]
    
    filtered_df = df.copy() 
    #print("*******Conditions ****** ",conditions)
    #print("*******Filtered ****** ",filtered_df.shape[0])
    
    data = charts_object.all_households_charts(filtered_df, residentialtype)
    return jsonify(data)



###### CHARTS HOUSEHOLDS FILTERED ########
@blueprint.route('/api/v2/charts-filtered/individual_member')
def get_ilp_charts_filtered():
    dataset_name = 'individual_member_result'
    
    df = data_corpus[dataset_name]

    residentialtype = request.args.get("residentialtype")
    district = request.args.get("district")
    cdblockulbmc = request.args.get("cdblockulbmc")
    panchayatward = request.args.get("panchayatward")
    age = request.args.get("age")
    gender = request.args.get("gender")
    educationlevel = request.args.get("educationlevel")
    employmentstatus = request.args.get("employmentstatus")
    annualincome = request.args.get("annualincome")
                    

    if not residentialtype == "All":
        df = df[df['residentialtype']==residentialtype]
                       
    if not district == "All":
        df = df[df['district']==district]
    
    if not cdblockulbmc == "All":
        df = df[df['cdblockulbmc']==cdblockulbmc]
    
    if not panchayatward == "All":
        df = df[df['panchayatward']==panchayatward]
    
    if not age== "All":
        df = df[df['age']==panchayatward]
                    
    if not gender == "All":
        df = df[df['gender']==gender]
    
    if not educationlevel == "All":
        df = df[df['educationlevel']==educationlevel]
                    
    if not employmentstatus == "All":
        df = df[df['employmentstatus']==employmentstatus]
    
    if not annualincome == "All":
        df = df[df['annualincome']==annualincome]
        
        
    filtered_df = df.copy()
    
    data = charts_object.all_ilp_charts(filtered_df)

    return jsonify(data)




###### CHARTS HOUSEHOLDS FILTERED ########
@blueprint.route('/api/v2/charts-filtered/pee')
def get_pee_charts_filtered():
    dataset_name = 'pee'
    
    df = data_corpus[dataset_name]

    residentialtype = request.args.get("residentialtype")
    district = request.args.get("district")
    cdblockulbmc = request.args.get("cdblockulbmc")
    panchayatward = request.args.get("panchayatward")
    age = request.args.get("age")
    gender = request.args.get("gender")
    educationlevel = request.args.get("educationlevel")
    sectorofinterest = request.args.get("sectorofinterest")
    expectedscaleofbusiness = request.args.get("expectedscaleofbusiness")
    assistancerequiredyuva = request.args.get("assistancerequiredforyuva")
    
    if not residentialtype == "All":
        df = df[df['residentialtype']==residentialtype]
                       
    if not district == "All":
        df = df[df['district']==district]
    
    if not cdblockulbmc == "All":
        df = df[df['cdblockulbmc']==cdblockulbmc]
    
    if not panchayatward == "All":
        df = df[df['panchayatward']==panchayatward]
    
    if not age== "All":
        df = df[df['age']==panchayatward]
                    
    if not gender == "All":
        df = df[df['gender']==gender]
    
    if not educationlevel == "All":
        df = df[df['educationlevel']==educationlevel]
                    
    if not sectorofinterest == "All":
        df = df[df['sectorofinterest']==sectorofinterest]
    
    if not expectedscaleofbusiness == "All":
        df = df[df['scaleofbusiness']==expectedscaleofbusiness]

    if not assistancerequiredyuva == "All":
        df = df[df['assistancelookingfor']==assistancerequiredyuva]
    
        
    filtered_df = df.copy()
    
    data = charts_object.all_pee_charts(filtered_df)

    return jsonify(data)



@blueprint.route('/api/v2/charts-filtered/peu')
def get_peu_charts_filtered():
    dataset_name = 'peu'
    df = data_corpus[dataset_name]
    residentialtype = request.args.get("residentialtype")
    district = request.args.get("district")
    cdblockulbmc = request.args.get("cdblockulbmc")
    panchayatward = request.args.get("panchayatward")
    age = request.args.get("age")
    gender = request.args.get("gender")
    educationlevel = request.args.get("educationlevel")
    sectorofinterest = request.args.get("sectorofinterest")
    expectedscaleofbusiness = request.args.get("expectedscaleofbusiness")
    assistancerequiredyuva = request.args.get("assistancerequiredforyuva")
    
    if not residentialtype == "All":
        df = df[df['residentialtype']==residentialtype]
                       
    if not district == "All":
        df = df[df['district']==district]
    
    if not cdblockulbmc == "All":
        df = df[df['cdblockulbmc']==cdblockulbmc]
    
    if not panchayatward == "All":
        df = df[df['panchayatward']==panchayatward]
    
    if not age== "All":
        df = df[df['age']==panchayatward]
                    
    if not gender == "All":
        df = df[df['gender']==gender]
    
    if not educationlevel == "All":
        df = df[df['educationlevel']==educationlevel]
                    
    if not sectorofinterest == "All":
        df = df[df['sectorofinterest']==sectorofinterest]
    
    if not expectedscaleofbusiness == "All":
        df = df[df['scaleofbusiness']==expectedscaleofbusiness]

    if not assistancerequiredyuva == "All":
        df = df[df['assistancelookingfor']==assistancerequiredyuva]
    
        
    filtered_df = df.copy()
    
    data = charts_object.all_peu_charts(filtered_df)

    return jsonify(data)





#@app.route('/api/v2/charts/refresh')
#@login_required
#def refresh_data():
#    get_data(base_path='BaselineData')
# #    return render_template('refresh.html')

# #return render_template('home/refresh.html', 
#                            segment='index', 
#                            user_id=current_user.id)