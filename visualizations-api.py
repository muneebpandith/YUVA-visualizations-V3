from flask import Flask, render_template, jsonify
from collections import Counter
import random
import pandas as pd
import numpy as np
import itertools



debug = True
app = Flask(__name__)



data_corpus = dict()


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
        
        data_corpus['peur_result'] = data_corpus['household_member'].merge(data_corpus['unregisteredactivities'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['peu_result'] = data_corpus['household_member'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['pee_result'] = data_corpus['household_member'].merge(data_corpus['self_employment_seekers'], how='inner', left_on='uniqueid', right_on='memberid')
        data_corpus['pee_result'] = data_corpus['pee_result'][data_corpus['pee_result']['pecategory']=='PEE']
        data_corpus['peu_result'] = data_corpus['peu_result'][data_corpus['peu_result']['pecategory']=='PEU']
        data_corpus['peur_result'] = data_corpus['peur_result'][data_corpus['peur_result']['pecategory']=='PEUR']

        data_corpus['hoh_member'] = data_corpus['household_member'][data_corpus['household_member']['relationwithhoh'] == 'Self'].copy()
        data_corpus['hoh_member']['trimmed_uniqueid'] = data_corpus['hoh_member']['uniqueidofmember'].str[:13] 
        data_corpus['hoh_result'] = data_corpus['hoh_member'].merge(data_corpus['household'], how='inner', left_on='trimmed_uniqueid', right_on='uniqueidofhousehold')

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



if debug == True:
    base_path = 'BaselineDataTest'
else:
    base_path = 'BaselineData'  

get_data(base_path=base_path)

def generate_break(text="", type_of_data=""):
    config = {"type_of_response":"text", "content":text,"type_of_data":type_of_data}
    return config





def generate_chart_data(chart_type, xlabels, ydata, title_of_chart, datasets=[], horizontal=False):
    labels = xlabels
    data = ydata
    colors_background = []
    colors_background_light = []
    colors_border = []
    if chart_type == "bar" or chart_type=="line":        
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # Generate random colors for the chart
        colors_background_light.append(f"rgb({r}, {g},{b},0.2)")
        colors_background.append(f"rgb({r}, {g}, {b},0.9)")
        colors_border.append(f"rgb({r}, {g}, {b})")
    for _ in data:

        if not (chart_type == "bar" or chart_type=="line"):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            # Generate random colors for the chart
            colors_background_light.append(f"rgb({r}, {g},{b},0.2)")
            colors_background.append(f"rgb({r}, {g}, {b},0.9)")
            colors_border.append(f"rgb({r}, {g}, {b})")  
        
        #if chart_type =="double-bar": 
        #    for d in datasets:
        #        datasets =[{ "label": xlabels if chart_type in ["bar", "line"] else "Data" ,
        #        "data": data,  # These will become the x-axis
        #        "borderColor": colors_border,
        #        "backgroundColor": colors_background_light if chart_type == "line" else colors_background,
        #        "fill": chart_type == "line"} for _ in range(20)]



        chart_config = {
            "type_of_response":"chart",
            "chart_title": title_of_chart,
            "type": chart_type,
            "labels": labels,  # These will become the y-axis        
            "datasets": [{
                "label": xlabels if not chart_type in ["bar", "line"] else "Data" ,
                "data": data,  # These will become the x-axis
                "borderColor": colors_border,
                "backgroundColor": colors_background_light if chart_type == "line" else colors_background,
                "fill": chart_type == "line"
            }],
            "options": {
                "indexAxis": 'x' if horizontal == False else 'y',
                "plugins": {
                    "datalabels": {
                        "anchor": "end",
                        "align": "left",  # Align to the left of the bar
                        "color": "black",
                        "font": {
                            "size": 12,
                            "weight": "bold"
                        },
                        "formatter": "value"
                    }
                },
                "scales": {
                    "x": {
                        "title": "X-axis Title",
                        "beginAtZero": True  # Ensure the X-axis starts at zero
                    },
                    "y": {
                        "title": "Y-axis Title",
                        "beginAtZero": True  # Ensure the X-axis starts at zero
                    }
                }
            }
        }
   
    
    return chart_config

#scp -i "gcp_compute_key" ABC.zip muneeb_ahmed@34.66.125.101:/home/muneeb_ahmed/YUVA-visualizations-main
#ssh -i gcp_compute_key muneeb_ahmed@34.66.125.101
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/refresh')
def refresh_data():
    get_data(base_path=base_path)
    return render_template('refresh.html')

@app.route('/sum')
def dumy_sum():
    return render_template('sum.html')


@app.route('/dummy')
def dummy_map():
    return render_template('dummymap.html')


@app.route('/jk')
def dummy_jk():
    return render_template('jk1.html')
@app.route('/jk2')
def dummy_jk2():
    return render_template('jk2.html')




@app.route('/fetch_options/<type_of_data>/<parameter>')
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
            if type_of_data == 'household':
                if parameter == 'residentialtype':
                    options = ['All']+ list(data_corpus['household']['residentialtype'].unique())
                elif parameter == 'district':
                    options = ['All'] + list(data_corpus[type_of_data][parameter].unique())
                elif parameter == 'cdblockulbmc':
                    options = ['All'] + list(data_corpus[type_of_data][parameter].unique())
                elif parameter == 'panchayatward':
                    options = ['All'] + list(data_corpus[type_of_data][parameter].unique())
                elif parameter == 'gender':
                    options = ['All']+ list(data_corpus['hoh_result'][parameter].unique())
                elif parameter == 'annualhouseholdincome':
                    options = ['All'] + list(data_corpus[type_of_data][parameter].unique())
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




@app.route('/chart-data')
def chart_data():
    type_charts = ["bar", "line", "pie"]
    breaker_hlp = generate_break('======= Household Level Profile =======')
    # Generate the xlabels (district names) and ydata (count of entries per district)
    xlabels = list(data_corpus['household']['district'].value_counts().index)
    ydata = data_corpus['household']['district'].value_counts().values.tolist()
    # Generate the chart
    chartH0 = generate_chart_data("bar", xlabels, ydata, "Distribution of households by districts")

    # Categorize household sizes and calculate frequencies
    categorized_sizes = data_corpus['household']['householdsize'].dropna().loc[lambda x: x != 0].apply(lambda x: int(x) if x <= 8 else '8+')
    size_counts = categorized_sizes.value_counts().sort_index(key=lambda x: [int(i) if isinstance(i, int) else 9 for i in x])
    # Generate bar chart
    chartH3 = generate_chart_data("bar", size_counts.index.tolist(), size_counts.values.tolist(), "Distribution of Household Sizes")

    # Replace unmatched values with "others" and calculate counts for rural households
    categories = ["Self-employed in agriculture", "Self-employed in non-agriculture","Regular wage-salary earning", "Casual labour in agriculture","Casual labour in non- agriculture"]
    householdtype_counts = data_corpus['household'][data_corpus['household']['residentialtype'] == 'Rural']['householdtype'] \
    .apply(lambda x: x if x in categories else "others").value_counts()

    # Generate the bar chart
    chartHLP3 = generate_chart_data("bar", householdtype_counts.index.tolist(), householdtype_counts.values.tolist(), "Distribution of Household Types in Rural Areas")

    # Replace unmatched values with "others" and calculate counts for Rural,Urban households
    categories = ["Self-employed", "Self-employed in non-agriculture","Regular wage/salary earning", "Casual labour"]
    householdtype_counts = data_corpus['household'][data_corpus['household']['residentialtype'] == 'Urban']['householdtype'].apply(lambda x: x if x in categories else "others").value_counts()

    # Generate the bar chart
    chartHLP4 = generate_chart_data("bar", householdtype_counts.index.tolist(), householdtype_counts.values.tolist(), "Distribution of Household Types in Urban Areas")

    # Calculate the proportion of each residential type
    residential_proportion = data_corpus['household']['residentialtype'].value_counts(normalize=True)
    # Extract labels and values for the pie chart
    xlabels, ydata = residential_proportion.index.tolist(), residential_proportion.values.tolist()
    # Generate the pie chart data
    chartHLP1 = generate_chart_data("pie", xlabels, ydata, "Proportion of households by residential type")


    agricultureland_count = data_corpus['household'][data_corpus['household']['agriculturelandpossession'].notnull() & (data_corpus['household']['agriculturelandpossession'] != '---')]['agriculturelandpossession'].value_counts()
    xlabels, ydata = agricultureland_count.index.tolist(), agricultureland_count.values.tolist()
    chartH5 = generate_chart_data("bar", xlabels, ydata, "Distribution of agriculture land possession")

    ownership_proportion = data_corpus['household'][data_corpus['household']['typeoffamilyenterprise'].isin(['Yes', 'No'])]['typeoffamilyenterprise'].value_counts(normalize=True)
    xlabels, ydata = ownership_proportion.index.tolist(), ownership_proportion.values.tolist()
    chartH7 = generate_chart_data("pie", xlabels, ydata, "Proportion of households owning an enterprise")

    response_count = data_corpus['household'][data_corpus['household']['responseoffamilyenterprise'].notnull() & (data_corpus['household']['responseoffamilyenterprise'] != '---')]['responseoffamilyenterprise'].value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chartH8 = generate_chart_data("bar", xlabels, ydata, "Sector of Family Enterprise", True)
    
    response_count = data_corpus['household']['locationoftheenterprise'].replace('---', None).dropna().value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_location_pie = generate_chart_data("pie", xlabels, ydata, "Location of the Enterprise")

    socialgroup_proportion = data_corpus['household'][data_corpus['household']['socialgroup'].notnull() & (data_corpus['household']['socialgroup'] != '---')]['socialgroup'].value_counts(normalize=True)
    xlabels, ydata = socialgroup_proportion.index.tolist(), socialgroup_proportion.values.tolist()
    chartH4 = generate_chart_data("pie", xlabels, ydata, "Proportion of households by social group")


    income_count = data_corpus['household'][data_corpus['household']['annualhouseholdincome'].notnull() & (data_corpus['household']['annualhouseholdincome'] != '---')]['annualhouseholdincome'].value_counts()
    xlabels, ydata = income_count.index.tolist(), income_count.values.tolist()
    chartH6 = generate_chart_data("bar", xlabels, ydata, "Distribution of Annual Household Income")

    # Replace unmatched values with "Others" and calculate counts for each category
    categories = ["AAY – Antyodhya Anna Yojana", "PHH- Priority House hold", "NPHH- Non Priority Household", "No ration card", "Exclusion category"]
    rationcard_counts = data_corpus['household']['typeofrationcardholder'].apply(lambda x: x if x in categories else "Others").value_counts()
    # Generate the bar chart
    chartHLP2 = generate_chart_data("bar", rationcard_counts.index.tolist(), rationcard_counts.values.tolist(), "Distribution of Households by Type of Ration Card")








    breaker_ilp = generate_break('======= Individuals Level Profile =======')

    xvalues = (
    data_corpus['household_member']['age']
    .str.extract(r'(\d+)Y')[0]  # Extract years from the 'age' column
    .astype(float)
    .dropna()
    .apply(
        lambda x: (
            "0-18" if x <= 18 else
            "19-25" if x <= 25 else
            "26-45" if x <= 45 else
            "46-60" if x <= 60 else
            "60+"
        )
    )  # Categorize ages into the specified ranges
    .value_counts()
    .sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))  # Sort by the starting number of the range
    .index.tolist()
    )

    ydata = (
        data_corpus['household_member']['age']
        .str.extract(r'(\d+)Y')[0]  # Extract years from the 'age' column
        .astype(float)
        .dropna()
        .apply(
            lambda x: (
                "0-18" if x <= 18 else
                "19-25" if x <= 25 else
                "26-45" if x <= 45 else
                "46-60" if x <= 60 else
                "60+"
            )
        )  # Categorize ages into the specified ranges
        .value_counts()
        .sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))  # Sort by the starting number of the range
        .values.tolist())

    chartAgeWiseDistribution = generate_chart_data(
        "bar", xvalues, ydata, "Age-wise Distribution of Household Members"
    )

    # Extract gender data from the 'household_member' sheet
    xlabels = list(data_corpus['household_member']['gender'].value_counts().index)  # Gender values (e.g., "Male", "Female")
    ydata = data_corpus['household_member']['gender'].value_counts().values.tolist()  # Count of each gender
    # Generate the pie chart
    chart_gender_distribution = generate_chart_data("pie", xlabels, ydata, "Gender wise distribution of Household Members")

    # Extract special status data from the 'household' sheet
    xlabels = list(data_corpus['household_member']['specialstatus'].value_counts().index)  # Special status values (e.g., "No", "Yes")
    ydata = data_corpus['household_member']['specialstatus'].value_counts().values.tolist()  # Count of each special status
    # Generate the pie chart
    chart_specialstatus = generate_chart_data("pie", xlabels, ydata, "Distribution of Special Status")

    # Extract education level data from the 'household_member' sheet
    xlabels = list(data_corpus['household_member']['educationlevel'].value_counts().index)  # Education levels (e.g., "Secondary", "Higher secondary")
    ydata = data_corpus['household_member']['educationlevel'].value_counts().values.tolist()  # Count of each education level
    # Generate the bar chart
    chart_educationlevel = generate_chart_data("bar", xlabels, ydata, "Education Level Distribution")

    # Define categories and map unmatched values to "others"
    categories = ["No technical education", "Diploma or certificate in medicine", "Diploma or certificate in other subjects", 
              "Technical degree in engineering/ technology", "Learned skilled by doing without formal training", 
              "Diploma or certificate in engineering/technology", "Technical degree in medicine", 
              "Technical degree in agriculture", "Technical degree in other subjects", 
              "Diploma or certificate in crafts", "Technical degree in crafts", "Diploma or certificate in: agriculture"]
    household_member = data_corpus['household_member']
    household_member['technicaleducationskill'] = household_member['technicaleducationskill'].apply(lambda x: x if x in categories else "others")

    # Generate bar chart
    chart_technicaleducation = generate_chart_data(
    "bar", 
    household_member['technicaleducationskill'].value_counts().index.tolist(), 
    household_member['technicaleducationskill'].value_counts().values.tolist(), 
    "Technical Education Skill Distribution"
    )

    # Extract data for employment status
    response_count = data_corpus['household_member']['employmentstatus'].dropna().value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    # Generate bar chart
    chart_employment_status = generate_chart_data("bar", xlabels, ydata, "Employment Status Distribution", True)



    response_count = data_corpus['household_member']['changepresentwork'].dropna().value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_change_work_pie = generate_chart_data("pie", xlabels, ydata, "Change in Present Work")



    # Filter non-blank annual income data and calculate counts
    filtered_data = data_corpus['household_member']['annualincome'].dropna()
    xlabels = list(filtered_data.value_counts().index)  # Unique annual income categories
    ydata = filtered_data.value_counts().values.tolist()  # Count of each category
    # Generate the bar chart
    chart_annualincome = generate_chart_data("bar", xlabels, ydata, "Annual Income Distribution")

    # Filter non-blank pursuing higher education data and calculate counts
    filtered_data = data_corpus['household_member']['pursuinghighereducation'].dropna()
    xlabels = list(filtered_data.value_counts().index)  # Unique values (e.g., "Yes", "No")
    ydata = filtered_data.value_counts().values.tolist()  # Count of each value

    # Generate the pie chart
    chart_higher_education = generate_chart_data("pie", xlabels, ydata, "Pursuing Higher Education Distribution")




    response_count = data_corpus['household_member']['pecategory'].value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_pecategory = generate_chart_data("bar", xlabels, ydata, "Proportion of Target Group Members- Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) among the households")


    gender_count = data_corpus['household_member'][data_corpus['household_member']['pecategory'].isin(['PEE', 'PEU', 'PEUR']) & data_corpus['household_member']['gender'].notnull()]['gender'].value_counts()
    xlabels, ydata = gender_count.index.tolist(), gender_count.values.tolist()
    chartH9 = generate_chart_data("pie", xlabels, ydata, "Gender Distribution for Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) Categories")

    education_count = data_corpus['household_member'][data_corpus['household_member']['pecategory'].isin(['PEE', 'PEU', 'PEUR']) & data_corpus['household_member']['educationlevel'].notnull()]['educationlevel'].value_counts()
    xlabels, ydata = education_count.index.tolist(), education_count.values.tolist()
    chartH10 = generate_chart_data("bar", xlabels, ydata, "Education Level Distribution for Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) Categories")

    filtered_data = data_corpus['household_member'][data_corpus['household_member']['pecategory'].isin(['PEE', 'PEU', 'PEUR'])]
    xlabels, ydata = filtered_data['employmentstatus'].value_counts().index.tolist(), filtered_data['employmentstatus'].value_counts().values.tolist()
    chartH11 = generate_chart_data("bar", xlabels, ydata, "Employment Status Distribution for Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) Categories")

    breaker_peur = generate_break('======= Details about Potential Entrepreneur Unregistered Activity(PEUR) =======')

    data = data_corpus['unregisteredactivities']['sectorofenterprise'].dropna().value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chart_sectorofenterprise = generate_chart_data("bar", xlabels, ydata, "Distribution of Sector of Unregistered Activity", True)

    
    specific_categories = [
    "Single Proprietorship", "Group of Family members(Partnership within the same household)",
    "Partnership", "Self Help Groups", "Corporation", "Farmers Producers Organization",
    "Society/Trust/Club/Association"
    ]
    xvalues = data_corpus['unregisteredactivities']['typeofownership'].apply(
    lambda x: x if x in specific_categories else "Others").value_counts().index.tolist()
    ydata = data_corpus['unregisteredactivities']['typeofownership'].apply(
    lambda x: x if x in specific_categories else "Others").value_counts().values.tolist()
    chartOwnershipDistribution = generate_chart_data(
    "bar", xvalues, ydata, "Distribution of Types of Ownership (Unregistered Activities)"
    )   

    data = data_corpus['unregisteredactivities']['natureofbusiness'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH20 = generate_chart_data("bar", xlabels, ydata, "PEUR- Nature of Business")


    # Filter data for 'initialinvestment' and ignore blanks
    filtered_data = data_corpus['unregisteredactivities']['initialinvestment'].dropna()
    # Count occurrences of each category
    xlabels = list(filtered_data.value_counts().index)  # Investment categories
    ydata = filtered_data.value_counts().values.tolist()  # Count of each category
    # Generate the bar chart
    chart_initial_investment = generate_chart_data("bar", xlabels, ydata, "Initial Investment Distribution")


    filtered_data = data_corpus['unregisteredactivities']['awareofselfemploymentschemes'].dropna().loc[lambda x: x != '---']
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
    chartH12 = generate_chart_data("pie", xlabels, ydata, "PEUR-Awareness of Self-Employment Schemes")

    filtered_data = data_corpus['unregisteredactivities']['haveyouusedgovtschemes'].dropna().loc[lambda x: x != '---']
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
    chartH13 = generate_chart_data("pie", xlabels, ydata, "PEUR-Usage of Government Schemes")

    filtered_data = data_corpus['unregisteredactivities']['reasonsfornotavailingscheme'].dropna().loc[lambda x: x != '---']
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
    chartH14 = generate_chart_data("bar", xlabels, ydata, "PEUR-Reasons for Not Availing Schemes")


    # Flatten and clean data
    data = data_corpus['unregisteredactivities']['usedgovtschemes'].dropna()
    flattened = [val.strip().strip('{}"') for row in data for val in row.split(',')]
    # Count occurrences
    counts = {scheme: flattened.count(scheme) for scheme in set(flattened)}
    # Prepare x-labels and y-data
    xlabels, ydata = list(counts.keys()), list(counts.values())
    # Generate the bar chart
    chart_usd = generate_chart_data("bar", xlabels, ydata, "Used Government Schemes Distribution",True)


    filtered_data = data_corpus['unregisteredactivities']['interestedinformalsetup'].dropna().loc[lambda x: x != '---']
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
    chartH15 = generate_chart_data("pie", xlabels, ydata, "PEUR-Interested in Formal Setup")

    data = data_corpus['unregisteredactivities']['reasonsfornotshifting'].dropna()
    categories = ["Satisfied with the existing status", "High Interest rates on loans", "Too many Govt formalities", "Non-cooperation from government agencies"]
    mapped_data = data.apply(lambda x: next((cat for cat in categories if cat in x), "Others"))
    xlabels, ydata = mapped_data.value_counts().index.tolist(), mapped_data.value_counts().values.tolist()
    chart_reasons_for_not_shifting = generate_chart_data("bar", xlabels, ydata, "Reasons for Not Shifting Distribution")


    filtered_data = data_corpus['unregisteredactivities']['interestedinyuvaforupgrading'].dropna().loc[lambda x: x != '---']
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
    chartH16 = generate_chart_data("pie", xlabels, ydata, "PEUR-Interested in YUVA for Upgrading")

    filtered_data = data_corpus['unregisteredactivities']['locationofbusiness'].dropna().loc[lambda x: x != '---']
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
    chartH17 = generate_chart_data("bar", xlabels, ydata, "PEUR-Location of Business")


    filtered_data = data_corpus['unregisteredactivities']['loanavailed'].dropna().loc[lambda x: x != '---']
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
    chartH18 = generate_chart_data("pie", xlabels, ydata, "PEUR-Loan Availed")


    # Filter non-blank loan amount data and calculate counts
    filtered_data = data_corpus['unregisteredactivities']['amountofloanavailed'].dropna()
    xlabels = list(filtered_data.value_counts().index)  # Unique loan amount categories
    ydata = filtered_data.value_counts().values.tolist()  # Count of each category
    # Generate the bar chart
    chart_loan_amount = generate_chart_data("bar", xlabels, ydata, "Loan Amount Availed Distribution")

    categories = [
    "Difficulty in finding of collateral",
    "Lengthy duration for approval",
    "Insufficient/poor credit history",
    "High-interest rates",
    "Complex application procedures",
    "Banks inaccessible/located too far",
    "No difficulty"
    ]

    parsed_data = data_corpus['unregisteredactivities']['difficultyinavailingloan'].dropna().str.strip("{}").str.split(r',\s*')
    data = Counter(
        category.strip('"') if category.strip('"') in categories else "Others"
        for row in parsed_data for category in row
        if row != [""]  # Skip empty rows (`{}`)
    )

    xlabels, ydata = list(data.keys()), list(data.values())
    chart_difficulty_in_availing_loan = generate_chart_data("bar", xlabels, ydata, "Difficulties in Availing Loans")

    categories = ['Self-sourced (e.g., in Agriculture )', 'Locally(within the same district)', 'Regionally(within J&K)', 'Nationally(outside J&K)', 'Internationally(imported)', 'Others']
    rawmaterialsource_category = data_corpus['unregisteredactivities']['rawmaterialsource'].dropna().apply(
        lambda x: next((cat for cat in categories if cat.lower() in x.lower()), 'Others'))
    xlabels, ydata = rawmaterialsource_category.value_counts().index.tolist(), rawmaterialsource_category.value_counts().values.tolist()
    chart_rawmaterialsource = generate_chart_data("bar", xlabels, ydata, "Distribution of Raw Material Source")


    data = data_corpus['unregisteredactivities']['challengesinsourcingrawmaterial'].dropna()
    categories = {
        "High transportation costs": "High transportation costs",
        "Poor availability or quality of raw materials": "Poor availability or quality of raw materials",
        "Unstable supply or delays": "Unstable supply or delays",
        "High procurement costs": "High procurement costs",
        "Lack of reliable suppliers": "Lack of reliable suppliers",
        "Regulatory issues": "Regulatory issues",
        "No Challenge": "No Challenge",
    }
    response_count = (
        data.str.strip('{}').str.split(',').explode().str.strip('" ')
        .apply(lambda x: categories.get(x, "Others")).value_counts()
    )
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_challenges_sourcing = generate_chart_data("bar", xlabels, ydata, "Challenges in Sourcing Raw Materials")

    data = data_corpus['unregisteredactivities']['currentmarketreach'].dropna()
    categories = {
        "Local (within district)": "Local (within district)",
        "Regional (within J&K)": "Regional (within J&K)",
        "National (outside J&K)": "National (outside J&K)",
        "International (export markets)": "International (export markets)"
    }
    mapped_data = data.map(lambda x: categories.get(x, "Others"))
    response_count = mapped_data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_market_reach = generate_chart_data("bar", xlabels, ydata, "Current Market Reach Distribution")

    data = data_corpus['unregisteredactivities']['averagetimeforsales'].dropna()
    response_count = data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_avg_time_for_sales = generate_chart_data("bar", xlabels, ydata, "Average Time for Sales Distribution")

    data = data_corpus['unregisteredactivities']['leanperiodinsales'].dropna()
    response_count = data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_lean_period_sales = generate_chart_data("pie", xlabels, ydata, "Lean Period in Sales Distribution")



    data = data_corpus['unregisteredactivities']['leanperiodduration'].dropna()
    response_count = data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_lean_period_duration = generate_chart_data("bar", xlabels, ydata, "Lean Period Duration Distribution")



    data = data_corpus['unregisteredactivities']['skillrelevanttobusiness'].dropna()
    response_count = data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_skill_relevance = generate_chart_data("pie", xlabels, ydata, "Skill Relevant to Business")



    filtered_data  = data_corpus['unregisteredactivities']['loanrepaymentstatus'].dropna()  # Filter non-null values
    xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()  # Get counts
    chartH19 = generate_chart_data("bar", xlabels, ydata, "PEUR-Loan Repayment Status")  # Generate chart 


    data = data_corpus['unregisteredactivities']['expectedchallengesinupgrading'].dropna()
    categories = {
        "High Competition": "High Competition",
        "Taxation system": "Taxation system",
        "Lack of technological support": "Lack of technological support",
        "Regulatory Barriers(Licenses/registration etc)": "Regulatory Barriers(Licenses/registration etc)",
        "Lack of guidance/Mentorship": "Lack of guidance/Mentorship",
        "Transportation/Logistics Issues": "Transportation/Logistics Issues",
        "Language or cultural barriers": "Language or cultural barriers",
        "Lack of finance": "Lack of finance"
    }
    mapped_data = data.map(lambda x: categories.get(x, "Others"))
    response_count = mapped_data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_challenges = generate_chart_data("bar", xlabels, ydata, "Expected Challenges in Upgrading Business")


    data = data_corpus['unregisteredactivities']['amountoffinancialsupport'].dropna()
    response_count = data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_financial_support = generate_chart_data("bar", xlabels, ydata, "Amount of Financial Support Needed Distribution")




    data = data_corpus['unregisteredactivities']['skillrequiredforbusinessupgrade'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH21 = generate_chart_data("bar", xlabels, ydata, "PEUR- Skills Required for Upgrading Business")

    data = data_corpus['unregisteredactivities']['statusofenterprise'].dropna().value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH22 = generate_chart_data  ("pie", xlabels, ydata, "PEUR-Status of Enterprise")


    data = data_corpus['unregisteredactivities']['rolemodelinlocality'].dropna()
    response_count = data.value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_role_model = generate_chart_data("pie", xlabels, ydata, "Role Model in Locality")


    breaker_pee = generate_break('======= Potential Entrepreneur Employed(PEE) =======')

    data = data_corpus['pee_result']['employmentstatus'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH23 = generate_chart_data("bar", xlabels, ydata, "PEE- Employment Status Distribution")

    data = data_corpus['pee_result']['age'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH24 = generate_chart_data("bar", xlabels, ydata, "PEE- Agewise Distribution")

    data = data_corpus['pee_result']['gender'].dropna().value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH25 = generate_chart_data("pie", xlabels, ydata, "PEE- Gender Distribution")

    data = data_corpus['pee_result']['financialsupportamount'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH26 = generate_chart_data("bar", xlabels, ydata, "PEE- Financial Support Amount Needed Distribution")

    data = data_corpus['pee_result']['sectorofinterest'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH27 = generate_chart_data("bar", xlabels, ydata, "PEE- Sector of Interest")

    breaker_peu = generate_break('======= Potential Entrepreneur Unemployed(PEU)=======')

    data = data_corpus['peu_result']['age'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH28 = generate_chart_data("bar", xlabels, ydata, "PEU- Agewise Distribution")

    data = data_corpus['peu_result']['gender'].dropna().value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH29 = generate_chart_data("pie", xlabels, ydata, "PEU- Gender Distribution")

    data = data_corpus['peu_result']['financialsupportamount'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH30 = generate_chart_data("bar", xlabels, ydata, "PEU- Financial Support Amount Needed Distribution")

    data = data_corpus['pee_result']['sectorofinterest'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH31 = generate_chart_data("bar", xlabels, ydata, "PEU- Sector of Interest")
        
    xlabels = list(data_corpus['business_result']['annualprofitloss2022_23'].value_counts().index)
    ydata = data_corpus['business_result']['annualprofitloss2022_23'].value_counts().values.tolist()
    # Generate the chart
    chartB0 = generate_chart_data("bar", xlabels, ydata, "Distribution of Businesses by Profits (2022-23)")

    xlabels = list(data_corpus['business_result']['annualprofitloss2023_24'].value_counts().index)
    ydata = data_corpus['business_result']['annualprofitloss2023_24'].value_counts().values.tolist()
    # Generate the chart
    chartB1 = generate_chart_data("bar", xlabels, ydata, "Distribution of Businesses by Profits (2023-24)")


    xlabels = list(data_corpus['business_result']['annualturnover2022_23'].value_counts().index)
    ydata = data_corpus['business_result']['annualturnover2022_23'].value_counts().values.tolist()
    # Generate the chart
    chartB2 = generate_chart_data("bar", xlabels, ydata, "Distribution of Businesses by Turnover (2022-23)", True)

    xlabels = list(data_corpus['business_result']['annualturnover2023_24'].value_counts().index)
    ydata = data_corpus['business_result']['annualturnover2022_23'].value_counts().values.tolist()
    # Generate the chart
    chartB3 = generate_chart_data("bar", xlabels, ydata, "Distribution of Businesses by Turnover (2022-23)", True)


    data = data_corpus['hoh_result'][data_corpus['hoh_result']['gender'] == 'Female']['district'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartDistrictWiseFemaleHoh = generate_chart_data("bar", xlabels, ydata, "District-wise percentage of female-headed households")

    filtered_data = data_corpus['household'][(data_corpus['household']['agriculturelandpossession'] != 'No land') &(data_corpus['household']['agriculturelandpossession'] != '---')]
    data = filtered_data['district'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartDistrictWiseAgricultureLand = generate_chart_data("bar", xlabels, ydata, "District-wise distribution of households with agriculture land possession")

   
    data = data_corpus['peu_result']['financialsupportamount'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartH32 = generate_chart_data("bar", xlabels, ydata, "PEU- Financial Support Amount Needed Distribution")


    # Count occurrences of each annual income category
    income_counts = data_corpus['pee_result']['annualincome'].value_counts()

    # Prepare data for the chart
    xvalues = income_counts.index.tolist()
    ydata = income_counts.values.tolist()

    # Generate the bar chart
    chartAnnualIncomeDistribution = generate_chart_data(
    "bar", xvalues, ydata, "Annual Income Distribution in PEE Category"
    )

    #random_number[random.randint(0,2)  chartDistrictWiseAgricultureLand   chart_change_work_pie   chart_usd
    # Generate data for two different chart sets (line and bar)
    data = {
       'household': [breaker_hlp,chartHLP1,chartH0,chartH3,chartHLP3,chartHLP4,chartH5,chartH7,chartH8,chart_location_pie,chartH4,chartH6,chartHLP2,chartDistrictWiseFemaleHoh,breaker_ilp,chartAgeWiseDistribution,chart_gender_distribution,chart_specialstatus,chart_educationlevel,chart_technicaleducation,chart_employment_status,chart_annualincome,chart_higher_education,
        chart_pecategory,chartH9,chartH10,chartH11,breaker_peur,chart_sectorofenterprise,chartOwnershipDistribution,chartH20,chartH17,chart_initial_investment,chartH18,chart_loan_amount,chart_difficulty_in_availing_loan,chart_rawmaterialsource,chart_challenges_sourcing,chart_skill_relevance,chartH22,chart_market_reach,chart_avg_time_for_sales,chart_lean_period_sales,chart_lean_period_duration,chartH15,chart_reasons_for_not_shifting,chartH12,chartH13,chartH14,chartH19,chartH16,chart_challenges,chartH21,chart_financial_support,chart_role_model,breaker_pee,chartH23,chartH24,chartH25,chartH26,chartH27,chartAnnualIncomeDistribution,breaker_peu,chartH28,chartH29,chartH30,chartH31,chartH32],
        'business':[chartB0, chartB1, chartB2, chartB3]
    }

    
    return jsonify(data)


@app.route('/chart-data-filtered/<type_of_data>/<residentialtype>/<district>/<cdblockulbmc>/<panchayatward>/<gender>/<annualhouseholdincome>')
def chart_data_filtered(type_of_data, residentialtype, district, cdblockulbmc, panchayatward, gender, annualhouseholdincome):
    if type_of_data == 'household':
        data_to_return = filter_data(data_corpus, 'hoh_result', residentialtype, district, cdblockulbmc, panchayatward, gender, annualhouseholdincome)
        #print(data_to_return)
        data = update_charts_household(data_to_return, residentialtype)
        
        return jsonify(data)

def update_charts_household(df, residentialtype):
    type_charts = ["bar", "line", "pie"]
    breaker_hlp = generate_break('======= Household Level Profile =======')
    # Generate the xlabels (district names) and ydata (count of entries per district)
    xlabels = list(df['district'].value_counts().index)
    ydata = df['district'].value_counts().values.tolist()
    # Generate the chart
    chartH0 = generate_chart_data("bar", xlabels, ydata, "Distribution of households by districts")

    # Categorize household sizes and calculate frequencies
    categorized_sizes = df['householdsize'].dropna().loc[lambda x: x != 0].apply(lambda x: int(x) if x <= 8 else '8+')
    size_counts = categorized_sizes.value_counts().sort_index(key=lambda x: [int(i) if isinstance(i, int) else 9 for i in x])
    # Generate bar chart
    chartH3 = generate_chart_data("bar", size_counts.index.tolist(), size_counts.values.tolist(), "Distribution of Household Sizes")

    # Replace unmatched values with "others" and calculate counts for rural/urban households
    categories = ["Self-employed in agriculture", "Self-employed in non-agriculture","Regular wage-salary earning", "Casual labour in agriculture","Casual labour in non- agriculture"]
    householdtype_counts = df[df['residentialtype'] == residentialtype]['householdtype'] \
    .apply(lambda x: x if x in categories else "others").value_counts()
    # Generate the bar chart
    chartHLP3 = generate_chart_data("bar", householdtype_counts.index.tolist(), householdtype_counts.values.tolist(), "Distribution of Household Types in "+residentialtype+ " Areas")

    # Calculate the proportion of each residential type
    residential_proportion = df['residentialtype'].value_counts(normalize=True)
    # Extract labels and values for the pie chart
    xlabels, ydata = residential_proportion.index.tolist(), residential_proportion.values.tolist()
    # Generate the pie chart data
    chartHLP1 = generate_chart_data("pie", xlabels, ydata, "Proportion of households by residential type")


    agricultureland_count = df[df['agriculturelandpossession'].notnull() & (df['agriculturelandpossession'] != '---')]['agriculturelandpossession'].value_counts()
    xlabels, ydata = agricultureland_count.index.tolist(), agricultureland_count.values.tolist()
    chartH5 = generate_chart_data("bar", xlabels, ydata, "Distribution of agriculture land possession")

    ownership_proportion = df[df['typeoffamilyenterprise'].isin(['Yes', 'No'])]['typeoffamilyenterprise'].value_counts(normalize=True)
    xlabels, ydata = ownership_proportion.index.tolist(), ownership_proportion.values.tolist()
    chartH7 = generate_chart_data("pie", xlabels, ydata, "Proportion of households owning an enterprise")

    response_count = df[df['responseoffamilyenterprise'].notnull() & (df['responseoffamilyenterprise'] != '---')]['responseoffamilyenterprise'].value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chartH8 = generate_chart_data("bar", xlabels, ydata, "Sector of Family Enterprise", True)
    
    response_count = df['locationoftheenterprise'].replace('---', None).dropna().value_counts()
    xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
    chart_location_pie = generate_chart_data("pie", xlabels, ydata, "Location of the Enterprise")

    socialgroup_proportion = df[df['socialgroup'].notnull() & (df['socialgroup'] != '---')]['socialgroup'].value_counts(normalize=True)
    xlabels, ydata = socialgroup_proportion.index.tolist(), socialgroup_proportion.values.tolist()
    chartH4 = generate_chart_data("pie", xlabels, ydata, "Proportion of households by social group")


    income_count = df[df['annualhouseholdincome'].notnull() & (df['annualhouseholdincome'] != '---')]['annualhouseholdincome'].value_counts()
    xlabels, ydata = income_count.index.tolist(), income_count.values.tolist()
    chartH6 = generate_chart_data("bar", xlabels, ydata, "Distribution of Annual Household Income")

    # Replace unmatched values with "Others" and calculate counts for each category
    categories = ["AAY – Antyodhya Anna Yojana", "PHH- Priority House hold", "NPHH- Non Priority Household", "No ration card", "Exclusion category"]
    rationcard_counts = df['typeofrationcardholder'].apply(lambda x: x if x in categories else "Others").value_counts()
    # Generate the bar chart
    chartHLP2 = generate_chart_data("bar", rationcard_counts.index.tolist(), rationcard_counts.values.tolist(), "Distribution of Households by Type of Ration Card")

    data = data_corpus['hoh_result'][data_corpus['hoh_result']['gender'] == 'Female']['district'].value_counts()
    xlabels, ydata = data.index.tolist(), data.values.tolist()
    chartDistrictWiseFemaleHoh = generate_chart_data("bar", xlabels, ydata, "District-wise percentage of female-headed households")

    data = {
       'household': [breaker_hlp,chartHLP1,chartH0,chartH3,chartHLP3, chartH5,chartH7,chartH8,chart_location_pie,chartH4,chartH6,chartHLP2,chartDistrictWiseFemaleHoh],
       'business':[]
    }

    
    return data



def filter_data(df, type_of_data, residentialtype, district, cdblockulbmc, panchayatward, gender, annualhouseholdincome):
    conditions = []
    df = data_corpus[type_of_data]

    if residentialtype != 'All':
    	conditions.append(df['residentialtype'] == residentialtype)
    
    if district != 'All':
    	conditions.append(df['district'] == district)
    
    if cdblockulbmc != 'All':
    	conditions.append(df['cdblockulbmc'] == cdblockulbmc)
    
    if panchayatward != 'All':
    	conditions.append(df['panchayatward'] == panchayatward)
    
    if gender != 'All':
    	conditions.append(df['gender'] == gender)
    
    if annualhouseholdincome != 'All':
    	conditions.append(df['annualhouseholdincome'] == annualhouseholdincome)
    
    if conditions:
    	filtered_df = df[pd.concat(conditions, axis=1).all(axis=1)] 
    
    else:
    	filtered_df = df.copy() 
    return pd.DataFrame(filtered_df)



    # # Example Usage:
    # # Assuming 'df' is your pandas DataFrame
    # filtered_data = filter_data(
    # 	data_corpus, 
    #     type_of_data ='hoh_result',
    # 	residentialtype='Urban', 
    # 	district='All', 
    # 	cdblockulbmc='All', 
    # 	panchayatward='All', 
    # 	gender='All', 
    # 	annualhouseholdincome='All'
    # )

 



if __name__ == '__main__':
    app.run("0.0.0.0", debug=debug, port=8080)


