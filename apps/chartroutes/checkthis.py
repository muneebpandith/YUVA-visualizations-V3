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



        data_corpus['peur_result_new'] = data_corpus['individual_member_result'].merge(data_corpus['unregisteredactivities'], how='inner', left_on='uniqueid_x', right_on='memberid')
        data_corpus['peur_result_new'] = data_corpus['peur_result_new'][data_corpus['peur_result_new']['pecategory']=='PEUR']

        data_corpus['pee_result_new'] = data_corpus['individual_member_result'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid_x', right_on='memberid')
        data_corpus['pee_result_new'] = data_corpus['pee_result_new'][data_corpus['pee_result_new']['pecategory']=='PEE']

        data_corpus['pee_result_new'] = data_corpus['individual_member_result'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid_x', right_on='memberid')
        data_corpus['pee_result_new'] = data_corpus['pee_result_new'][data_corpus['pee_result_new']['pecategory']=='PEE']
        

