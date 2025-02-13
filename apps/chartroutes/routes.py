from apps.chartroutes import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from collections import Counter
import random
import pandas as pd
import numpy as np
import itertools
from .highcharts import Chart



def get_data(base_path='BaselineData', connect_type="filesystem"):
    print('Loading Data from File System...')
    if connect_type == "filesystem" and load_subset == True:
        #data_corpus['businessdetails'] = pd.read_csv(base_path+'/Form 2/businessdetails.csv')
        #data_corpus['businessidentity'] = pd.read_csv(base_path+'/Form 2/businessidentity.csv')
        #data_corpus['manpowerengaged'] = pd.read_csv(base_path+'/Form 2/manpowerengaged.csv')
        #data_corpus['business_result'] = data_corpus['businessdetails'].merge(data_corpus['businessidentity'], how='inner')
     
        
        chunk_size = 10000  # Adjust based on memory
        chunks = pd.read_csv(base_path+'/Form 1/household.csv', dtype=str, chunksize=chunk_size)
        data_corpus['household'] = pd.concat(chunks, ignore_index=True)
        #data_corpus['household'] = pd.read_csv(base_path+'/Form 1/household.csv', dtype=str)
        print('Loading Houseful: Successful!')

        chunk_size = 10000  # Adjust based on memory
        chunks = pd.read_csv(base_path+'/Form 1/household_member.csv', dtype=str, chunksize=chunk_size)
        data_corpus['household_member'] = pd.concat(chunks, ignore_index=True)
        #data_corpus['household_member'] = pd.read_csv(base_path+'/Form 1/household_member.csv')
        print('Loading Individual Members: Successful!')


        chunk_size = 10000  # xAdjust based on memory
        chunks = pd.read_csv(base_path+'/Form 1/self_employment_seekers.csv', dtype=str, chunksize=chunk_size)
        data_corpus['self_employment_seekers'] = pd.concat(chunks, ignore_index=True)
        #data_corpus['self_employment_seekers'] = pd.read_csv(base_path+'/Form 1/self_employment_seekers.csv')
        print('Loading Self Employment Seekers: Successful!')

        chunk_size = 10000  # Adjust based on memory
        chunks = pd.read_csv(base_path+'/Form 1/unregisteredactivities.csv', dtype=str, chunksize=chunk_size)
        data_corpus['unregisteredactivities'] = pd.concat(chunks, ignore_index=True)
        print('Unregistered Activities: Successful!')
        #data_corpus['unregisteredactivities'] = pd.read_csv(base_path+'/Form 1/unregisteredactivities.csv')
        
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



        data_corpus['peur'] = data_corpus['individual_member_result'].merge(data_corpus['unregisteredactivities'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['peur'] = data_corpus['peur'][data_corpus['peur']['pecategory']=='PEUR']

        data_corpus['pee'] = data_corpus['individual_member_result'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['pee'] = data_corpus['pee'][data_corpus['pee']['pecategory']=='PEE']

        data_corpus['peu'] = data_corpus['individual_member_result'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['peu'] = data_corpus['peu'][data_corpus['peu']['pecategory']=='PEU']
        
        #print(data_corpus['peur'].shape[0],data_corpus['pee'].shape[0], data_corpus['peu'].shape[0] )
        print('Loading Data: Successful!')
    elif connect_type == "filesystem" and load_subset == False:

        print('Loading new dtaset')
        #/ chunk_size = 10000  # Adjust based on memory
        #/ chunks = pd.read_csv(base_path+'/hoh_result.csv', dtype=str, chunksize=chunk_size)
        #/ data_corpus['hoh_result'] = pd.concat(chunks, ignore_index=True)
        #/ #data_corpus['household_member'] = pd.read_csv(base_path+'/Form 1/household_member.csv')
        #/ print('Loading Household Members: Successful!')



        # chunk_size = 10000  # Adjust based on memory
        # chunks = pd.read_csv(base_path+'/individual_member_result.csv', dtype=str, chunksize=chunk_size)
        # data_corpus['individual_member_result'] = pd.concat(chunks, ignore_index=True)
        # #data_corpus['household_member'] = pd.read_csv(base_path+'/Form 1/household_member.csv')
        # print('Loading Individual Members: Successful!')

        # chunk_size = 10000  # Adjust based on memory
        # chunks = pd.read_csv(base_path+'/peur_data.csv', dtype=str, chunksize=chunk_size)
        # data_corpus['peur'] = pd.concat(chunks, ignore_index=True)
        # #data_corpus['household_member'] = pd.read_csv(base_path+'/Form 1/household_member.csv')
        # print('Loading PEUR Members: Successful!')


        # chunk_size = 10000  # Adjust based on memory
        # chunks = pd.read_csv(base_path+'/pee_data.csv', dtype=str, chunksize=chunk_size)
        # data_corpus['pee'] = pd.concat(chunks, ignore_index=True)
        # #data_corpus['household_member'] = pd.read_csv(base_path+'/Form 1/household_member.csv')
        # print('Loading PEE Members: Successful!')

        # chunk_size = 10000  # Adjust based on memory
        # chunks = pd.read_csv(base_path+'/peu_data.csv', dtype=str, chunksize=chunk_size)
        # data_corpus['peu'] = pd.concat(chunks, ignore_index=True)
        # #data_corpus['household_member'] = pd.read_csv(base_path+'/Form 1/household_member.csv')
        # print('Loading PEU Members: Successful!')
        
        # data_corpus['hoh_result'] = data_corpus['individual_member_result'][data_corpus['individual_member_result']['relationwithhoh'] == 'Self']
        
        
        
        data_corpus['individual_member_result'] = pd.read_csv(base_path+'/individual_member_result_cleaned.csv')
        print('Loading Individual Members: Successful!')


        data_corpus['peur'] = pd.read_csv(base_path+'/peur_data_cleaned.csv')
        print('Loading PEUR Members: Successful!')


        data_corpus['pee'] = pd.read_csv(base_path+'/pee_data_cleaned.csv')
        print('Loading PEE Members: Successful!')

       
        data_corpus['peu'] = pd.read_csv(base_path+'/peu_data_cleaned.csv')
        print('Loading PEU Members: Successful!')
        
        data_corpus['hoh_result'] = data_corpus['individual_member_result'][data_corpus['individual_member_result']['relationwithhoh'] == 'Self']
        
        print('Loading Data: Successful!')


data_corpus = dict()

load_subset = False
if load_subset == True:
    base_path = 'dataset/BaselineDataTest'
else:
    base_path = 'dataset/BaselineDataNew2'  

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


household_numbers = len(data_corpus['hoh_result']['uniqueidofmember'].unique())
#household_numbers_f = f"{household_numbers:,}"
individual_numbers = len(data_corpus['individual_member_result']['uniqueidofmember'].unique())
#individual_numbers_f = f"{individual_numbers:,}"
peur_numbers = len(data_corpus['peur'][data_corpus['peur']['pecategory']=='PEUR']['uniqueidofmember'].unique())
peu_numbers = len(data_corpus['peu'][data_corpus['peu']['pecategory']=='PEU']['uniqueidofmember'].unique())
#peu_numbers_f = f"{peu_numbers:,}"
pee_numbers = len(data_corpus['pee'][data_corpus['pee']['pecategory']=='PEE']['uniqueidofmember'].unique())
#pee_numbers_f = f"{pee_numbers:,}"
##### FOR NUMBERS ENDING   ####





def get_filtered_numbers(df_hoh_filtered, df_ilp_filtered, df_peur_filtered, df_pee_filtered, df_peu_filtered):
    district_stats_filtered = dict()
    for d in ['Anantnag', 'Baramulla', 'Budgam', 'Rajouri', 'Kupwara', 'Pulwama','Shopian', 'Poonch', 'Srinagar', 'Doda', 'Kulgam', 'Jammu', 'Kathua','Ganderbal', 'Bandipora', 'Reasi', 'Udhampur', 'Ramban', 'Kishtwar','Samba']:
        district_stats_filtered[d] = {"peu":"0", "peur":"0", "pee":"0", "individual_members":"0", "households":"0"}

    households_districts_filtered = pd.DataFrame(df_hoh_filtered['district'].value_counts())
    individual_member_districts_filtered = pd.DataFrame(df_ilp_filtered['district'].value_counts())
    peu_districts_filtered = pd.DataFrame(df_peu_filtered['district'].value_counts())
    pee_districts_filtered = pd.DataFrame(df_pee_filtered['district'].value_counts())
    peur_districts_filtered = pd.DataFrame(df_peur_filtered['district'].value_counts())



    #needs to check
    household_numbers_filtered = len(list(df_hoh_filtered['uniqueidofmember'].unique()))
    #df_hoh_filtered.shape[0]
    #household_numbers_f = f"{household_numbers:,}"
    individual_numbers_filtered = len(list(df_ilp_filtered['uniqueidofmember'].unique()))
    #individual_numbers_f = f"{individual_numbers:,}"
    peur_numbers_filtered = len(list(df_peur_filtered['uniqueidofmember'].unique()))
    peu_numbers_filtered = len(list(df_peu_filtered['uniqueidofmember'].unique()))
    #peu_numbers_f = f"{peu_numbers:,}"
    pee_numbers_filtered = len(list(df_pee_filtered['uniqueidofmember'].unique()))
    #pee_numbers_f = f"{pee_numbers:,}"
    

    for i in range (households_districts_filtered.shape[0]):
        #print(peu_districts.index[i], peu_districts['count'].iloc[i])
        district_stats_filtered[households_districts_filtered.index[i]]['households'] = str(int(district_stats_filtered[households_districts_filtered.index[i]]['households']) + households_districts_filtered['count'].iloc[i])
    
    for i in range (individual_member_districts_filtered.shape[0]):
        #print(peu_districts.index[i], peu_districts['count'].iloc[i])
        district_stats_filtered[individual_member_districts.index[i]]['individual_members'] = str(int(district_stats_filtered[individual_member_districts_filtered.index[i]]['individual_members']) + individual_member_districts_filtered['count'].iloc[i])
    
    for i in range (peur_districts_filtered.shape[0]):
        #print(peu_districts.index[i], peu_districts['count'].iloc[i])
        district_stats_filtered[peur_districts_filtered.index[i]]['peur'] = str(int(district_stats_filtered[peur_districts_filtered.index[i]]['peur'])+ peur_districts_filtered['count'].iloc[i])

    for i in range (pee_districts_filtered.shape[0]):
        #print(peu_districts.index[i], peu_districts['count'].iloc[i])
        district_stats_filtered[pee_districts_filtered.index[i]]['pee'] = str(int(district_stats_filtered[pee_districts_filtered.index[i]]['pee'])+ pee_districts_filtered['count'].iloc[i])

    for i in range (peu_districts_filtered.shape[0]):
        #print(peu_districts.index[i], peu_districts['count'].iloc[i])
        district_stats_filtered[peu_districts_filtered.index[i]]['peu'] =  str(int(district_stats_filtered[peu_districts_filtered.index[i]]['peu']) + peu_districts_filtered['count'].iloc[i])

    
    hoh_details_filtered = {'number':household_numbers_filtered,'from':'','to':''}
    ilp_details_filtered = {'number':individual_numbers_filtered,'from':'','to':''}
    peur_details_filtered = {'number':56855,'from':'','to':''}
    peu_details_filtered = {'number':343871,'from':'','to':''}
    pee_details_filtered = {'number':148035,'from':'','to':''}
    district_wise_details_filtered = {'number':district_stats_filtered,'from':'','to':''}


    
    #data_corpus['peur'] = data_corpus['hoh_member'].merge(data_corpus['household'], how='inner', left_on='trimmed_uniqueid', right_on='uniqueidofhousehold'0
    #return jsonify({'hoh':household_numbers_f, 'individual_members':individual_numbers_f, 'peur':peur_numbers_f, 'pee':pee_numbers_f, 'peu':peu_numbers_f})
    return {'hoh':hoh_details_filtered, 'individual_members':ilp_details_filtered, 'peur':peur_details_filtered, 'pee':pee_details_filtered,  'peu':peu_details_filtered, 'district_wise_details': district_wise_details_filtered }

    
   

# def get_filtered_numbers(df_hoh_filtered, df_ilp_filtered, df_peur_filtered, df_pee_filtered, df_peu_filtered):
#     district_stats_filtered = dict()
#     for d in ['Anantnag', 'Baramulla', 'Budgam', 'Rajouri', 'Kupwara', 'Pulwama','Shopian', 'Poonch', 'Srinagar', 'Doda', 'Kulgam', 'Jammu', 'Kathua','Ganderbal', 'Bandipora', 'Reasi', 'Udhampur', 'Ramban', 'Kishtwar','Samba']:
#         district_stats_filtered[d] = {"peu":"0", "peur":"0", "pee":"0", "individual_members":"0", "households":"0"}

#     households_districts_filtered = pd.DataFrame(df_hoh_filtered['district'].value_counts())
#     individual_member_districts_filtered = pd.DataFrame(df_ilp_filtered['district'].value_counts())
#     peu_districts_filtered = pd.DataFrame(df_peu_filtered['district'].value_counts())
#     pee_districts_filtered = pd.DataFrame(df_pee_filtered['district'].value_counts())
#     peur_districts_filtered = pd.DataFrame(df_peur_filtered['district'].value_counts())

#     household_numbers_filtered = df_hoh_filtered.shape[0]
#     #household_numbers_f = f"{household_numbers:,}"
#     individual_numbers_filtered = df_ilp_filtered.shape[0]
#     #individual_numbers_f = f"{individual_numbers:,}"
#     peur_numbers_filtered = df_peur_filtered.shape[0]
#     peu_numbers_filtered = df_peu_filtered.shape[0]
#     #peu_numbers_f = f"{peu_numbers:,}"
#     pee_numbers_filtered = df_pee_filtered.shape[0]
#     #pee_numbers_f = f"{pee_numbers:,}"
    

#     for i in range (households_districts_filtered.shape[0]):
#         #print(peu_districts.index[i], peu_districts['count'].iloc[i])
#         district_stats_filtered[households_districts_filtered.index[i]]['households'] = str(int(district_stats_filtered[households_districts_filtered.index[i]]['households']))
    
#     for i in range (individual_member_districts_filtered.shape[0]):
#         #print(peu_districts.index[i], peu_districts['count'].iloc[i])
#         district_stats_filtered[individual_member_districts.index[i]]['individual_members'] = str(int(district_stats_filtered[individual_member_districts_filtered.index[i]]['individual_members']))
    
#     for i in range (peur_districts_filtered.shape[0]):
#         #print(peu_districts.index[i], peu_districts['count'].iloc[i])
#         district_stats_filtered[peur_districts_filtered.index[i]]['peur'] = str(int(district_stats_filtered[peur_districts_filtered.index[i]]['peur']))

#     for i in range (pee_districts_filtered.shape[0]):
#         #print(peu_districts.index[i], peu_districts['count'].iloc[i])
#         district_stats_filtered[pee_districts_filtered.index[i]]['pee'] = str(int(district_stats_filtered[pee_districts_filtered.index[i]]['pee']))

#     for i in range (peu_districts_filtered.shape[0]):
#         #print(peu_districts.index[i], peu_districts['count'].iloc[i])
#         district_stats_filtered[peu_districts_filtered.index[i]]['peu'] =  str(int(district_stats_filtered[peu_districts_filtered.index[i]]['peu']))

    
#     hoh_details_filtered = {'number':household_numbers_filtered,'from':'','to':''}
#     ilp_details_filtered = {'number':individual_numbers_filtered,'from':'','to':''}
#     peur_details_filtered = {'number':peur_numbers_filtered,'from':'','to':''}
#     peu_details_filtered = {'number':peu_numbers_filtered,'from':'','to':''}
#     pee_details_filtered = {'number':pee_numbers_filtered,'from':'','to':''}
#     district_wise_details_filtered = {'number':district_stats_filtered,'from':'','to':''}
    
#     #data_corpus['peur'] = data_corpus['hoh_member'].merge(data_corpus['household'], how='inner', left_on='trimmed_uniqueid', right_on='uniqueidofhousehold'0
#     #return jsonify({'hoh':household_numbers_f, 'individual_members':individual_numbers_f, 'peur':peur_numbers_f, 'pee':pee_numbers_f, 'peu':peu_numbers_f})
#     return {'hoh':hoh_details_filtered, 'individual_members':ilp_details_filtered, 'peur':peur_details_filtered, 'pee':pee_details_filtered,  'peu':peu_details_filtered, 'district_wise_details': district_wise_details_filtered }





###### OPTIONS ########
@blueprint.route('/api/v2/fetch_numbers')
# **@login_required
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
#@login_required
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
        if True: #changed from type_of_data in set_of_type_of_data:
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
                    options = sorted(list(filtered_data[parameter].unique()))
                    #print(options)
                    
                # elif parameter == 'gender':
                #     residentialtype = request.args.get("residentialtype")
                #     district = request.args.get("district")
                #     blockmunicipality = request.args.get("cdblockulbmc")
                #     panchayatward = request.args.get("panchayatward")
                    

                #     if not residentialtype == "All":
                #         filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                #         #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                #     if not district == "All":
                #         filtered_data = filtered_data[filtered_data['district']==district]
                #         #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                #     if not blockmunicipality == "All":
                #         filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                #         #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                #     if not panchayatward == "All":
                #         filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                #         #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                #     options = sorted(list(filtered_data[parameter].unique()))
                #     #print(options)

                    
                elif parameter == 'annualhouseholdincome':
                    options = sorted(list(filtered_data[parameter].unique()))

                
                # elif parameter == 'annualhouseholdincome':
                #     residentialtype = request.args.get("residentialtype")
                #     district = request.args.get("district")
                #     blockmunicipality = request.args.get("cdblockulbmc")
                #     panchayatward = request.args.get("panchayatward")
                #     gender = request.args.get("gender")

                #     if not residentialtype == "All":
                #         filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                #         #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                #     if not district == "All":
                #         filtered_data = filtered_data[filtered_data['district']==district]
                #         #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                #     if not blockmunicipality == "All":
                #         filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                #         #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                #     if not panchayatward == "All":
                #         filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                #         #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                #     if not gender == "All":
                #         filtered_data = filtered_data[filtered_data['gender']==gender]
                #         #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                #     options = sorted(list(filtered_data[parameter].unique()))
                #     #options = list(data_corpus[type_of_data][parameter].unique())
                # else:
                #     abort(404, f"Invalid area_type '{parameter}'")
            
            
            
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
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    age_options = sorted(list(filtered_data[parameter].unique()))
                    options = classify_age_groups(age_options)
                    #options = sorted(list(filtered_data[parameter].unique()))
                    #print(options)
                
                elif parameter == 'gender':
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'employmentstatus':
                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'annualincome':
                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                elif parameter == 'changepresentwork':
                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'pursuinghighereducation':
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
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # #options = sorted(list(filtered_data[parameter].unique()))
                    
                    age_options = sorted(list(filtered_data[parameter].unique()))
                    
                    options = classify_age_groups(age_options)
                    
                    #print(options)
                
                elif parameter == 'gender':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'sectorofenterprise':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'natureofbusiness':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofenterprise = request.args.get("sectorofenterprise")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofenterprise == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'sourceofrawmaterial':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofenterprise = request.args.get("sectorofenterprise")
                    # natureofbusiness = request.args.get("natureofbusiness")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofenterprise == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not natureofbusiness == "All":
                    #     filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    rawmaterial_options = list(filtered_data['rawmaterialsource'].unique())
                    options =  classify_raw_material_sources(rawmaterial_options)
                    #print(options)
                

                elif parameter == 'enterprisefinancialstatus':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofenterprise = request.args.get("sectorofenterprise")
                    # natureofbusiness = request.args.get("natureofbusiness")
                    # sourceofrawmaterial = request.args.get("sourceofrawmaterial")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofenterprise == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not natureofbusiness == "All":
                    #     filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sourceofrawmaterial == "All":
                    #     filtered_data = filtered_data[filtered_data['rawmaterialsource']==sourceofrawmaterial]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data['statusofenterprise'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'currentmarketreach':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofenterprise = request.args.get("sectorofenterprise")
                    # natureofbusiness = request.args.get("natureofbusiness")
                    # sourceofrawmaterial = request.args.get("sourceofrawmaterial")
                    # enterprisefinancialstatus = request.args.get("enterprisefinancialstatus")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofenterprise == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not natureofbusiness == "All":
                    #     filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sourceofrawmaterial == "All":
                    #     filtered_data = filtered_data[filtered_data['rawmaterialsource']==sourceofrawmaterial]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not enterprisefinancialstatus == "All":
                    #     filtered_data = filtered_data[filtered_data['statusofenterprise']==enterprisefinancialstatus]

                    cmr_options = list(filtered_data[parameter].unique())
                    options = classify_currentMarketReach(cmr_options)
                
                elif parameter == 'assistancerequiredyuva':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofenterprise = request.args.get("sectorofenterprise")
                    # natureofbusiness = request.args.get("natureofbusiness")
                    # sourceofrawmaterial = request.args.get("sourceofrawmaterial")
                    # enterprisefinancialstatus = request.args.get("enterprisefinancialstatus")
                    # currentmarketreach = request.args.get("currentmarketreach")
                    
                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofenterprise == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofenterprise']==sectorofenterprise]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not natureofbusiness == "All":
                    #     filtered_data = filtered_data[filtered_data['natureofbusiness']==natureofbusiness]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sourceofrawmaterial == "All":
                    #     filtered_data = filtered_data[filtered_data['rawmaterialsource']==sourceofrawmaterial]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not enterprisefinancialstatus == "All":
                    #     filtered_data = filtered_data[filtered_data['statusofenterprise']==enterprisefinancialstatus]
                    
                    options = list(filtered_data['interestedinyuvaforupgrading'].unique())
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
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    #options = sorted(list(filtered_data[parameter].unique()))
                    age_options = sorted(list(filtered_data[parameter].unique()))
                    options = classify_age_groups(age_options)
                    
                    #print(options)
                
                elif parameter == 'gender':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'sectorofinterest':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'expectedscaleofbusiness':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofinterest = request.args.get("sectorofinterest")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofinterest == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data['scaleofbusiness'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'assistancerequiredyuva':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofinterest = request.args.get("sectorofinterest")
                    # expectedscaleofbusiness = request.args.get("expectedscaleofbusiness")
                    
                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    
                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofinterest == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not expectedscaleofbusiness == "All":
                    #     filtered_data = filtered_data[filtered_data['scaleofbusiness']==expectedscaleofbusiness]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    
                     
                    options = list(filtered_data['interestedinyuva'].unique())
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
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # #options = sorted(list(filtered_data[parameter].unique()))
                    age_options = sorted(list(filtered_data[parameter].unique()))
                    options = classify_age_groups(age_options)
                    
                    #print(options)
                
                elif parameter == 'gender':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    options = sorted(list(filtered_data[parameter].unique()))
                    
                   
                    #print(options)

                elif parameter == 'educationlevel':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)

                elif parameter == 'sectorofinterest':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                
                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data[parameter].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])

                    #print(options)

                elif parameter == 'expectedscaleofbusiness':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofinterest = request.args.get("sectorofinterest")
                    

                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofinterest == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    options = list(filtered_data['scaleofbusiness'].unique())
                    options = sorted(["NA" if isinstance(x, float) and np.isnan(x) else x for x in options])
                    #print(options)
                
                elif parameter == 'assistancerequiredyuva':
                    # residentialtype = request.args.get("residentialtype")
                    # district = request.args.get("district")
                    # blockmunicipality = request.args.get("cdblockulbmc")
                    # panchayatward = request.args.get("panchayatward")
                    # age = request.args.get("age")
                    # gender = request.args.get("gender")
                    # educationlevel = request.args.get("educationlevel")
                    # sectorofinterest = request.args.get("sectorofinterest")
                    # expectedscaleofbusiness = request.args.get("expectedscaleofbusiness")
                    
                    # if not residentialtype == "All":
                    #     filtered_data = filtered_data[filtered_data['residentialtype']==residentialtype]
                    #     #print('After filtering Residential type ', residentialtype ,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not district == "All":
                    #     filtered_data = filtered_data[filtered_data['district']==district]
                    #     #print('After filtering district type ', district,',Genders remain', list(filtered_data[parameter].unique()))
                        
                    # if not blockmunicipality == "All":
                    #     filtered_data = filtered_data[filtered_data['cdblockulbmc']==blockmunicipality]
                    #     #print('After filtering block municipality type ', blockmunicipality,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not panchayatward == "All":
                    #     filtered_data = filtered_data[filtered_data['panchayatward']==panchayatward]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not age== "All":
                    #     #print('INSIDE AGE FILTER')
                    #     min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
                    #     if max_age == "onwards":
                    #         max_age == 1000
                    #     else:
                    #         max_age = int(max_age)
                    #     #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
                    #     filtered_data['years'] = ""
                    #     filtered_data['years'] = filtered_data['age'].str.extract(r'(\d+)Y').astype(int)
                    #     #print('Shape of dataset', filtered_data.shape[0])
                    #     #print(filtered_data['years'])
                    #     #print("*******", min_age, max_age, min_age==0, max_age==18)
                        
                    #     if min_age == 0 and max_age == 17:
                    #         #print('Yes! under 18')
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print("Filtered data", filtered_data)
                    #     elif min_age == 18 and max_age == 39:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #     elif min_age == 40 and max_age == 59:
                    #         #print(filtered_data['years'])
                    #         filtered_data = filtered_data[(filtered_data['years'] >= min_age) & (filtered_data['years'] <= max_age)]
                    #         #print(filtered_data)
                    #     elif min_age == 60:
                    #         filtered_data = filtered_data[filtered_data['years'] >= min_age]
                    #     #filtered_data = filtered_data[filtered_data['age']==age]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))


                    # if not gender == "All":
                    #     filtered_data = filtered_data[filtered_data['gender']==gender]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not educationlevel == "All":
                    #     filtered_data = filtered_data[filtered_data['educationlevel']==educationlevel]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    # if not sectorofinterest == "All":
                    #     filtered_data = filtered_data[filtered_data['sectorofinterest']==sectorofinterest]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))

                    # if not expectedscaleofbusiness == "All":
                    #     filtered_data = filtered_data[filtered_data['scaleofbusiness']==expectedscaleofbusiness]
                    #     #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
                    
                    
                     
                    options = list(filtered_data['interestedinyuva'].unique())
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
# **@login_required
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
    
    if residentialtype != 'All':
        df = df[df['residentialtype'] == residentialtype]

    if district != 'All':
        df = df[df['district'] == district]

    if cdblockulbmc != 'All':
        df = df[df['cdblockulbmc'] == cdblockulbmc]

    if panchayatward != 'All':
        df = df[df['panchayatward'] == panchayatward]

    if gender != 'All':
        df = df[df['gender'] == gender]

    if annualhouseholdincome != 'All':
        df = df[df['annualhouseholdincome'] == annualhouseholdincome]

    filtered_df = df.copy()
    #print("*******Conditions ****** ",conditions)
    #print("*******Filtered ****** ",filtered_df.shape[0])


    
    
    
    df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid']) & data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]


    #Uncomment if you just want to know about HOH
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peur']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['pee']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peu']['uniqueid'].isin(filtered_df['uniqueid'])]
    
    
    filtered_numbers = get_filtered_numbers(df_hoh_filtered, df_ilp_filtered, df_peur_filtered, df_pee_filtered, df_peu_filtered)
    data = charts_object.all_households_charts(filtered_df, residentialtype, filtered_numbers)
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
    #print('Age gotten', age)
    gender = request.args.get("gender")
    educationlevel = request.args.get("educationlevel")
    employmentstatus = request.args.get("employmentstatus")
    annualincome = request.args.get("annualincome")
    changepresentwork = request.args.get("changepresentwork")
    pursuinghighereducation= request.args.get("pursuinghighereducation")
                    

    if not residentialtype == "All":
        df = df[df['residentialtype']==residentialtype]
                       
    if not district == "All":
        df = df[df['district']==district]
    
    if not cdblockulbmc == "All":
        df = df[df['cdblockulbmc']==cdblockulbmc]
    
    if not panchayatward == "All":
        df = df[df['panchayatward']==panchayatward]
    
    if not age== "All":
        #print('INSIDE AGE FILTER')
        min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
        if max_age == "onwards":
            max_age == 1000
        else:
             max_age = int(max_age)
        #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
        df['years'] = ""
        df['years'] = df['age'].str.extract(r'(\d+)Y').astype(int)
        #print('Shape of dataset', df.shape[0])
        #print(df['years'])
        #print("*******", min_age, max_age, min_age==0, max_age==18)
        
        if min_age == 0 and max_age == 17:
            #print('Yes! under 18')
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print("Filtered data", df)
        elif min_age == 18 and max_age == 39:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
        elif min_age == 40 and max_age == 59:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print(df)
        elif min_age == 60:
            df = df[df['years'] >= min_age]
        #df = df[df['age']==age]
        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(filtered_data[parameter].unique()))
        

                    
    if not gender == "All":
        df = df[df['gender']==gender]
    
    if not educationlevel == "All":
        df = df[df['educationlevel']==educationlevel]
                    
    if not employmentstatus == "All":
        df = df[df['employmentstatus']==employmentstatus]
    
    if not annualincome == "All":
        df = df[df['annualincome']==annualincome]
    
    if not changepresentwork == "All":
        df = df[df['changepresentwork']==changepresentwork]

    if not pursuinghighereducation == "All":
        df = df[df['pursuinghighereducation']==pursuinghighereducation]
        
        
    filtered_df = df.copy()
    
    df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid']) & data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]

    #strict
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueid'].isin(filtered_df['uniqueid'])]
    

    #stricter
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peur']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['pee']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peu']['uniqueid'].isin(filtered_df['uniqueid'])]
    
    filtered_numbers = get_filtered_numbers(df_hoh_filtered, df_ilp_filtered, df_peur_filtered, df_pee_filtered, df_peu_filtered)
    data = charts_object.all_ilp_charts(filtered_df, filtered_numbers)

    return jsonify(data)




###### CHARTS HOUSEHOLDS FILTERED ########
@blueprint.route('/api/v2/charts-filtered/pee')
def get_pee_charts_filtered():
    dataset_name = 'pee'
    
    df = data_corpus[dataset_name]
    #print(df.columns)
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
        #print('INSIDE AGE FILTER')
        min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
        if max_age == "onwards":
            max_age == 1000
        else:
             max_age = int(max_age)
        #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
        df['years'] = ""
        df['years'] = df['age'].str.extract(r'(\d+)Y').astype(int)
        #print('Shape of dataset', df.shape[0])
        #print(df['years'])
        #print("*******", min_age, max_age, min_age==0, max_age==18)
        
        if min_age == 0 and max_age == 17:
            #print('Yes! under 18')
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print("Filtered data", df)
        elif min_age == 18 and max_age == 39:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
        elif min_age == 40 and max_age == 59:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print(df)
        elif min_age == 60:
            df = df[df['years'] >= min_age]
        #df = df[df['age']==age]
        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(df[parameter].unique()))
     
                    
    if not gender == "All":
        df = df[df['gender']==gender]
    
    if not educationlevel == "All":
        df = df[df['educationlevel']==educationlevel]
                    
    if not sectorofinterest == "All":
        df = df[df['sectorofinterest']==sectorofinterest]
    
    if not expectedscaleofbusiness == "All":
        df = df[df['scaleofbusiness']==expectedscaleofbusiness]

    if not assistancerequiredyuva == "All":
        df = df[df['interestedinyuva']==assistancerequiredyuva]
    
        
    filtered_df = df.copy()

    df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid']) & data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]


    #strict
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peur']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['pee']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peu']['uniqueid'].isin(filtered_df['uniqueid'])]
    
    filtered_numbers = get_filtered_numbers(df_hoh_filtered, df_ilp_filtered, df_peur_filtered, df_pee_filtered, df_peu_filtered)
    
    data = charts_object.all_pee_charts(filtered_df, filtered_numbers)

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
        #print('INSIDE AGE FILTER')

    
        min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
        if max_age == "onwards":
            max_age == 1000
        else:
             max_age = int(max_age)
        
        #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
        df['years'] = ""
        df['years'] = df['age'].str.extract(r'(\d+)Y').astype(int)
        #print('Shape of dataset', df.shape[0])
        #print(df['years'])
        #print("*******", min_age, max_age, min_age==0, max_age==18)
        
        if min_age == 0 and max_age == 17:
            #print('Yes! under 18')
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print("Filtered data", df)
        elif min_age == 18 and max_age == 39:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
        elif min_age == 40 and max_age == 59:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print(df)
        elif min_age == 60:
            df = df[df['years'] >= min_age]
        #df = df[df['age']==age]
        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(df[parameter].unique()))
     
                    
    if not gender == "All":
        df = df[df['gender']==gender]
    
    if not educationlevel == "All":
        df = df[df['educationlevel']==educationlevel]
                    
    if not sectorofinterest == "All":
        df = df[df['sectorofinterest']==sectorofinterest]
    
    if not expectedscaleofbusiness == "All":
        df = df[df['scaleofbusiness']==expectedscaleofbusiness]

    if not assistancerequiredyuva == "All":
        df = df[df['interestedinyuva']==assistancerequiredyuva]
    
        
    filtered_df = df.copy()
    



    df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid']) & data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]

    ##strict
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    
    #stricterf
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peur']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['pee']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peu']['uniqueid'].isin(filtered_df['uniqueid'])]
    
    filtered_numbers = get_filtered_numbers(df_hoh_filtered, df_ilp_filtered, df_peur_filtered, df_pee_filtered, df_peu_filtered)
    data = charts_object.all_peu_charts(filtered_df, filtered_numbers)
    return jsonify(data)


@blueprint.route('/api/v2/charts-filtered/peur')
def get_peur_charts_filtered():
    dataset_name = 'peur'
    df = data_corpus[dataset_name]
    #print(df.shape[0])
    residentialtype = request.args.get("residentialtype")
    district = request.args.get("district")
    cdblockulbmc = request.args.get("cdblockulbmc")
    panchayatward = request.args.get("panchayatward")
    age = request.args.get("age")
    gender = request.args.get("gender")
    educationlevel = request.args.get("educationlevel")
    sectorofenterprise = request.args.get("sectorofenterprise")
    natureofbusiness = request.args.get("natureofbusiness")
    sourceofrawmaterial = request.args.get("sourceofrawmaterial")
    enterprisefinancialstatus = request.args.get("enterprisefinancialstatus")
    currentmarketreach = request.args.get("currentmarketreach")
    #expectedscaleofbusiness = request.args.get("expectedscaleofbusiness")
    assistancerequiredyuva = request.args.get("assistancerequiredforyuva")
    print(df.shape[0])
    if not residentialtype == "All":
        df = df[df['residentialtype']==residentialtype]

    if not district == "All":
        df = df[df['district']==district]
        
    if not cdblockulbmc == "All":
        df = df[df['cdblockulbmc']==cdblockulbmc]
        
    if not panchayatward == "All":
        df = df[df['panchayatward']==panchayatward]
        
    if not age== "All":
        #print('INSIDE AGE FILTER')
        min_age, max_age = int(age.split("-")[0]),  age.split("-")[1]
        
        if max_age == "onwards":
            max_age == 1000
        else:
             max_age = int(max_age)
        #print('*****MIN AGE, MAX AGE= ', min_age, max_age)
        df['years'] = ""
        df['years'] = df['age'].str.extract(r'(\d+)Y').astype(int)
        #print('Shape of dataset', df.shape[0])
        #print(df['years'])
        #print("*******", min_age, max_age, min_age==0, max_age==18)
        
        if min_age == 0 and max_age == 17:
            #print('Yes! under 18')
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print("Filtered data", df)
        elif min_age == 18 and max_age == 39:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
        elif min_age == 40 and max_age == 59:
            #print(df['years'])
            df = df[(df['years'] >= min_age) & (df['years'] <= max_age)]
            #print(df)
        elif min_age == 60:
            df = df[df['years'] >= min_age]
        #df = df[df['age']==age]
        #print('After filtering panchayatward type ', panchayatward,',Genders remain', list(df[parameter].unique()))
     
          
    if not gender == "All":
        df = df[df['gender']==gender]
    
    if not educationlevel == "All":
        df = df[df['educationlevel']==educationlevel]

    if not sectorofenterprise == "All":
        df = df[df['sectorofenterprise']==sectorofenterprise]

    if not natureofbusiness == "All":
        df = df[df['natureofbusiness']==natureofbusiness]
        
    if not sourceofrawmaterial == "All":
        if not sourceofrawmaterial == "Others":
            df = df[df['rawmaterialsource']==sourceofrawmaterial]
        else:
            df = df[df['rawmaterialsource']!="Internationally (imported)"]
            df = df[df['rawmaterialsource']!="Locally(within the same district)"]
            df = df[df['rawmaterialsource']!="Nationally(outside J&K)"]
            df = df[df['rawmaterialsource']!="Regionally(within J&K)"]
            df = df[df['rawmaterialsource']!="Self-sourced (e.g., in Agriculture )"]
            df['rawmaterialsource']= "Others"
    if not enterprisefinancialstatus == "All":
        df = df[df['statusofenterprise']==enterprisefinancialstatus]
        
    if not currentmarketreach == "All":
        if not currentmarketreach == "Others":
            df = df[df['currentmarketreach']==currentmarketreach]
        else:
            df = df[df['currentmarketreach']!="International (export markets)"]
            df = df[df['currentmarketreach']!="Local (within district)"]
            df = df[df['currentmarketreach']!="National (outside J&K)"]
            df = df[df['currentmarketreach']!="Regional (within J&K)"]
            df['currentmarketreach']= "Others"
        df = df[df['currentmarketreach']==currentmarketreach]
       
    # if not expectedscaleofbusiness == "All":
    #     df = df[df['expectedscaleofbusiness']==expectedscaleofbusiness]
                  
    if not assistancerequiredyuva == "All":
        df = df[df['interestedinyuvaforupgrading']==assistancerequiredyuva]              
        
    filtered_df = df.copy()
    
    df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid']) & data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]
    df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueid'].isin(df_ilp_filtered['uniqueid'])]

    
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold'])]
    


    #stricters
    # df_hoh_filtered = data_corpus['hoh_result'][data_corpus['hoh_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['hoh_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_ilp_filtered = data_corpus['individual_member_result'][data_corpus['individual_member_result']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['individual_member_result']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peur_filtered = data_corpus['peur'][data_corpus['peur']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peur']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_pee_filtered = data_corpus['pee'][data_corpus['pee']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['pee']['uniqueid'].isin(filtered_df['uniqueid'])]
    # df_peu_filtered = data_corpus['peu'][data_corpus['peu']['uniqueidofhousehold'].isin(filtered_df['uniqueidofhousehold']) & data_corpus['peu']['uniqueid'].isin(filtered_df['uniqueid'])]
    
    filtered_numbers = get_filtered_numbers(df_hoh_filtered, df_ilp_filtered, df_peur_filtered, df_pee_filtered, df_peu_filtered)
    
    #print(filtered_df.shape[0])
    data = charts_object.all_peur_charts(filtered_df, filtered_numbers)
    
    return jsonify(data)

#@app.route('/api/v2/charts/refresh')
#@login_required
#def refresh_data():
#    get_data(base_path='BaselineData')
# #    return render_template('refresh.html')


# #return render_template('home/refresh.html', 
#                            segment='index', 
#                            user_id=current_user.id)


def classify_age_groups(age_list):
    # Function to extract the years and classify into predefined groups
    def get_age_group(age_str):
        years = int(age_str.split('Y')[0])  # Extract years as integer
        if years <= 17:
            return "0-17"
        elif 18 <= years <= 39:
            return "18-39"
        elif 40 <= years <= 59:
            return "40-59"
        else:
            return "60-onwards"

    # Get unique age groups
    return sorted(set(get_age_group(age) for age in age_list))

def classify_raw_material_sources(source_list):
    # Function to classify raw material sources into predefined categories
    def get_source_category(source_str):
        # Convert to string to handle non-string types
        source_str = str(source_str).strip()
        
        # Ignore blanks, nulls, and 'NA'
        if not source_str or source_str.upper() == 'NA' or source_str.lower() == 'null':
            return None
        
        # Define the predefined categories
        categories = {
            'Self-sourced (e.g., in Agriculture )',
            'Locally(within the same district)',
            'Regionally(within J&K)',
            'Nationally(outside J&K)',
            'Internationally (imported)'
        }
        
        # Return exact match if found, otherwise classify as 'Others'
        return source_str if source_str in categories else 'Others'

    # Get unique valid categories (excluding None values)
    return sorted(set(filter(None, (get_source_category(source) for source in source_list))))



def classify_currentMarketReach(source_list):
    # Function to classify raw material sources into predefined categories
    def get_source_category(source_str):
        # Convert to string to handle non-string types
        source_str = str(source_str).strip()
        
        # Ignore blanks, nulls, and 'NA'
        if not source_str or source_str.upper() == 'NA' or source_str.lower() == 'null':
            return None
        
        # Define the predefined categories
        categories = {
        'Local (within district)',
        'Regional (within J&K)',
        'National (outside J&K)',
        'International (export markets)'
        }
        
        # Return exact match if found, otherwise classify as 'Others'
        return source_str if source_str in categories else 'Others'

    # Get unique valid categories (excluding None values)
    return sorted(set(filter(None, (get_source_category(source) for source in source_list))))
