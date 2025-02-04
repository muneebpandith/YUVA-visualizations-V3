import random
import pandas as pd
class Chart:
    def __init__(self):
        #print("Loaded charts")
        self.chart_config = None
    


    def generate_bar_chart(self, dataset, x_title= "", y_title = "", y_unit="Values", chart_title="", chart_subtitle="", horizontal='NO'):
        #dataset can have a array of of x's y's i.e., [[[2,3,4],[4,5,6]], [[0,1,2],[4,5,6]]], here there are two sets of x's and y's
        chart_config = {
            'type': 'column',
            'chart_title': chart_title,
            'horizontal': horizontal,
            'chart_subtitle':chart_subtitle,
            'x_axis': {'type': 'category','title': x_title}, # Districts
            'y_axis': {'title': y_title},
            'series': [{'name': y_unit, 
                        'data':dataset}]
        }
        return chart_config



    def generate_grouped_bar_chart(self, x_labels, dataset, x_title= "", y_title = "", chart_title="", chart_subtitle="", grouped="NO", multicolor="NO",  horizontal="NO"):
        #dataset can have a array of of x's y's i.e., [[[2,3,4],[4,5,6]], [[0,1,2],[4,5,6]]], here there are two sets of x's and y's
        if grouped == "NO":
            chart_config = {
                'type': 'bar',
                'multicolor': multicolor,
                'horizontal': horizontal,
                'chart_title': chart_title,
                'chart_subtitle':chart_subtitle,
                'x_axis': {'title': x_title, 'categories': [' ']}, # Districts
                'y_axis': {'title': y_title, 'data':[]},
                'series': [{'name':dataset[i]['name'], 'data':dataset[i]['data']} for i in range(len(dataset))]
            }
        else:
            #MOSTLY NOT USED as this creates Districts on X-axis and in each district, enters a bar
            chart_config = {
                'type': 'bar',
                'multicolor': multicolor,
                'horizontal': horizontal,
                'chart_title': chart_title,
                'chart_subtitle':chart_subtitle,
                'x_axis': {'title': x_title, 'categories': x_labels}, # Districts
                'y_axis': {'title': y_title, 'data':[]},
                'series': [{'name':dataset[i]['name'], 'data':dataset[i]['data']} for i in range(len(dataset))]
            }
        return chart_config

    def generate_bar_drill_chart(self):
        pass

    def generate_pie_chart(self, dataset, pie_unit="Percentage", chart_title="", chart_subtitle=""):  
        #print("*****")
        #print(dataset[0], dataset[0].keys(), dataset[0]['name'])
        #print("*****")
        #print(dataset[i] for i in range(len(dataset)))
        chart_config = {
            'type': 'pie',
            'chart_title': chart_title,
            'chart_subtitle':chart_subtitle,
            'series': [{'name':pie_unit, 
                        'data':[{'name':dataset[i]['name'],'data':dataset[i]['data']} for i in range(len(dataset))]}]
        }
        return chart_config

    def generate_pie_drill_chart(self):
        pass

    def generate_bubble_chart(self):
        pass


    def generate_custom_chart(self):
        pass

    def generate_chart(self):
        pass

    def all_households_charts(self, df, residentialtype, filtered_numbers):
        #Chart 1
        residential_proportion = df['residentialtype'].value_counts(normalize=True)
        xlabels, ydata = residential_proportion.index.tolist(), residential_proportion.values.tolist()
        data_to_visualize = [{'name':x, 'data':y} for (x,y) in zip(xlabels, ydata)]
        chartH1 = self.generate_pie_chart(data_to_visualize, chart_title="Proportion of households by residential type", chart_subtitle="")
        
        #Chart 2
        xlabels = list(df['district'].value_counts().index)
        ydata = df['district'].value_counts().values.tolist()
        data_to_visualize = [ [x,y] for (x,y) in zip(xlabels, ydata)]
        chartH2 = self.generate_bar_chart(data_to_visualize, x_title= "Districts", y_title = "Values", chart_title="Distribution of households by districts", chart_subtitle="")
 

        # # Categorize household sizes and calculate frequencies
        # categorized_sizes = df['householdsize'].dropna().loc[lambda x: x != 0].apply(lambda x: int(x) if x <= 8 else '8+')
        # size_counts = categorized_sizes.value_counts().sort_index(key=lambda x: [int(i) if isinstance(i, int) else 9 for i in x])
        # # Generate bar chart
        # chartH3 = self.generate_chart_data("bar", size_counts.index.tolist(), size_counts.values.tolist(), "Distribution of Household Sizes")

        # # Replace unmatched values with "others" and calculate counts for rural/urban households
        # categories = ["Self-employed in agriculture", "Self-employed in non-agriculture","Regular wage-salary earning", "Casual labour in agriculture","Casual labour in non- agriculture"]
        # householdtype_counts = df[df['residentialtype'] == residentialtype]['householdtype'] \
        # .apply(lambda x: x if x in categories else "others").value_counts()
        # # Generate the bar chart
        # chartHLP3 = self.generate_chart_data("bar", householdtype_counts.index.tolist(), householdtype_counts.values.tolist(), "Distribution of Household Types in "+str(residentialtype)+ " Areas")

        # # Calculate the proportion of each residential type
        # residential_proportion = df['residentialtype'].value_counts(normalize=True)
        # # Extract labels and values for the pie chart
        # xlabels, ydata = residential_proportion.index.tolist(), residential_proportion.values.tolist()
        # # Generate the pie chart data
        # chartHLP1 = self.generate_chart_data("pie", xlabels, ydata, "Proportion of households by residential type")


        # agricultureland_count = df[df['agriculturelandpossession'].notnull() & (df['agriculturelandpossession'] != '---')]['agriculturelandpossession'].value_counts()
        # xlabels, ydata = agricultureland_count.index.tolist(), agricultureland_count.values.tolist()
        # chartH5 = self.generate_chart_data("bar", xlabels, ydata, "Distribution of agriculture land possession")

        # ownership_proportion = df[df['typeoffamilyenterprise'].isin(['Yes', 'No'])]['typeoffamilyenterprise'].value_counts(normalize=True)
        # xlabels, ydata = ownership_proportion.index.tolist(), ownership_proportion.values.tolist()
        # chartH7 = self.generate_chart_data("pie", xlabels, ydata, "Proportion of households owning an enterprise")

        # response_count = df[df['responseoffamilyenterprise'].notnull() & (df['responseoffamilyenterprise'] != '---')]['responseoffamilyenterprise'].value_counts()
        # xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        # chartH8 = self.generate_chart_data("bar", xlabels, ydata, "Sector of Family Enterprise", True)
        
        # response_count = df['locationoftheenterprise'].replace('---', None).dropna().value_counts()
        # xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        # chart_location_pie = self.generate_chart_data("pie", xlabels, ydata, "Location of the Enterprise")

        # socialgroup_proportion = df[df['socialgroup'].notnull() & (df['socialgroup'] != '---')]['socialgroup'].value_counts(normalize=True)
        # xlabels, ydata = socialgroup_proportion.index.tolist(), socialgroup_proportion.values.tolist()
        # chartH4 = self.generate_chart_data("pie", xlabels, ydata, "Proportion of households by social group")


        # income_count = df[df['annualhouseholdincome'].notnull() & (df['annualhouseholdincome'] != '---')]['annualhouseholdincome'].value_counts()
        # xlabels, ydata = income_count.index.tolist(), income_count.values.tolist()
        # chartH6 = self.generate_chart_data("bar", xlabels, ydata, "Distribution of Annual Household Income")

        # # Replace unmatched values with "Others" and calculate counts for each category
        # categories = ["AAY – Antyodhya Anna Yojana", "PHH- Priority House hold", "NPHH- Non Priority Household", "No ration card", "Exclusion category"]
        # rationcard_counts = df['typeofrationcardholder'].apply(lambda x: x if x in categories else "Others").value_counts()
        # # Generate the bar chart
        # chartHLP2 = self.generate_chart_data("bar", rationcard_counts.index.tolist(), rationcard_counts.values.tolist(), "Distribution of Households by Type of Ration Card")

        # data = df[df['gender'] == 'Female']['district'].value_counts()
        # xlabels, ydata = data.index.tolist(), data.values.tolist()
        # chartDistrictWiseFemaleHoh = self.generate_chart_data("bar", xlabels, ydata, "District-wise percentage of female-headed households")

        # data = {
        # 'household': [chartHLP1,chartH0,chartH3,chartHLP3, chartH5,chartH7,chartH8,chart_location_pie,chartH4,chartH6,chartHLP2,chartDistrictWiseFemaleHoh],
        # 'business':[]
        # }
        # # Categorize household sizes and calculate frequencies
        # Define the desired order of categories
        desired_order = ['1', '2', '3', '4', '5', '6', '7', '8', '8+']

        # Convert categories to strings for consistent reindexing
        categorized_sizes = df['householdsize'].dropna().loc[lambda x: x != 0].apply(lambda x: str(int(x)) if x <= 8 else '8+')

        # Reindex the value counts
        size_counts = categorized_sizes.value_counts().reindex(desired_order, fill_value=0)

        # Generate bar chart
        data_to_visualize = [[x, y] for (x, y) in zip(size_counts.index.tolist(), size_counts.values.tolist())]
        chartH3 = self.generate_bar_chart(
            data_to_visualize,
            x_title="Household Sizes",
            y_title="Values",
            chart_title="Distribution of Household Sizes",
            chart_subtitle=""
        )
        '''# Replace unmatched values with "others" and calculate counts for rural households
        categories = ["Self-employed in agriculture", "Self-employed in non-agriculture", "Regular wage-salary earning", "Casual labour in agriculture", "Casual labour in non-agriculture"]
        householdtype_counts = df[df['residentialtype'] == 'Rural']['householdtype'] \
            .apply(lambda x: x if x in categories else "others").value_counts()

        # Generate the bar chart for rural households
        data_to_visualize = [[x, y] for (x, y) in zip(householdtype_counts.index.tolist(), householdtype_counts.values.tolist())]
        chartH4 = self.generate_bar_chart(data_to_visualize, x_title="Rural Household Types", y_title="Counts", chart_title="Distribution of Household Types in Rural Areas", chart_subtitle="")
        '''
        
        # Replace unmatched values with "others" and calculate counts for rural households
        categories = ["Self-employed in agriculture", "Self-employed in non-agriculture", "Regular wage-salary earning", "Casual labour in agriculture", "Casual labour in non- agriculture"]

        # Filter out NA, null, and blank values in 'householdtype' and select rural households
        householdtype_counts = df[
            (df['residentialtype'] == 'Rural') &  # Select rural households
            (df['householdtype'].notna()) &  # Exclude NA/null values
            (df['householdtype'].str.strip() != "")  # Exclude blank strings
        ]['householdtype'] \
            .apply(lambda x: x if x in categories else "Others").value_counts()

        # Generate the bar chart for rural households
        data_to_visualize = [[x, y] for (x, y) in zip(householdtype_counts.index.tolist(), householdtype_counts.values.tolist())]
        chartH4 = self.generate_bar_chart(data_to_visualize, x_title="Rural Household Types", y_title="Counts", chart_title="Distribution of Household Types in Rural Areas", chart_subtitle="")

                # Replace unmatched values with "others" and calculate counts for urban households
        categories = ["Self-employed", "Self-employed in non-agriculture", "Regular wage/salary earning", "Casual labour"]
        householdtype_counts = df[
            (df['residentialtype'] == 'Urban') &  # Select rural households
            (df['householdtype'].notna()) &  # Exclude NA/null values
            (df['householdtype'].str.strip() != "")  # Exclude blank strings
        ]['householdtype'] \
            .apply(lambda x: x if x in categories else "Others").value_counts()

        # Generate the bar chart for urban households
        data_to_visualize = [[x, y] for (x, y) in zip(householdtype_counts.index.tolist(), householdtype_counts.values.tolist())]
        chartH5 = self.generate_bar_chart(data_to_visualize, x_title="Urban Household Types", y_title="Counts", chart_title="Distribution of Household Types in Urban Areas", chart_subtitle="")

        # Agriculture land possession distribution
        agricultureland_count = df[df['agriculturelandpossession'].notnull() & (df['agriculturelandpossession'] != '---')]['agriculturelandpossession'].value_counts()

        # Convert to list
        data_to_visualize = [[x, y] for (x, y) in zip(agricultureland_count.index.tolist(), agricultureland_count.values.tolist())]

        # Define the desired order
        desired_order = ["No land", "less than 10 kanals", "11-20 kanals", "21-40 kanals", "41-100 kanals", "More than 100 kanals"]

        # Create an ordered version of data_to_visualize
        ordered_data = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartH6 = self.generate_bar_chart(ordered_data, x_title="Agriculture Land Possession", y_title="Counts", chart_title="Distribution of Agriculture Land Possession", chart_subtitle="")

        # Proportion of households owning an enterprise
        ownership_proportion = df[df['typeoffamilyenterprise'].isin(['Yes', 'No'])]['typeoffamilyenterprise'].value_counts(normalize=True)
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(ownership_proportion.index.tolist(), ownership_proportion.values.tolist())]
        chartH7 = self.generate_pie_chart(data_to_visualize, chart_title="Proportion of households owning an enterprise", chart_subtitle="")

        # Sector of Family Enterprise
        response_count = df[df['responseoffamilyenterprise'].notnull() & (df['responseoffamilyenterprise'] != '---')]['responseoffamilyenterprise'].value_counts()
        data_to_visualize = [[x, y] for (x, y) in zip(response_count.index.tolist(), response_count.values.tolist())]
        chartH8 = self.generate_bar_chart(data_to_visualize, x_title="Sector", y_title="Counts", chart_title="Sector of Family Enterprise (Owning Enterprise = Yes)", chart_subtitle="")

        # Location of the Enterprise
        response_count = df['locationoftheenterprise'].replace('---', None).dropna().value_counts()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(response_count.index.tolist(), response_count.values.tolist())]
        chartH9 = self.generate_pie_chart(data_to_visualize, chart_title="Location of the Enterprise (Owning Enterprise = Yes)", chart_subtitle="")

        socialgroup_proportion = df[df['socialgroup'].notnull() & (df['socialgroup'] != '---')]['socialgroup'].value_counts(normalize=True)
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(socialgroup_proportion.index.tolist(), socialgroup_proportion.values.tolist())]
        chartH10 = self.generate_pie_chart(data_to_visualize, chart_title="Proportion of households by social group", chart_subtitle="")

        # Distribution of Annual Household Income
        income_count = df[df['annualhouseholdincome'].notnull() & (df['annualhouseholdincome'] != '---')]['annualhouseholdincome'].value_counts()
        data_to_visualize = [[x, y] for (x, y) in zip(income_count.index.tolist(), income_count.values.tolist())]
        chartH11 = self.generate_bar_chart(data_to_visualize, x_title="Income Range", y_title="Counts", chart_title="Distribution of Annual Household Income", chart_subtitle="")

        # Distribution of Households by Type of Ration Card
        categories = ["AAY – Antyodhya Anna Yojana", "PHH- Priority House hold", "NPHH- Non Priority Household", "No ration card", "Exclusion category"]
        rationcard_counts = df['typeofrationcardholder'].apply(lambda x: x if x in categories else "Others").value_counts()
        data_to_visualize = [[x, y] for (x, y) in zip(rationcard_counts.index.tolist(), rationcard_counts.values.tolist())]
        chartH12 = self.generate_bar_chart(data_to_visualize, x_title="Ration Card Type", y_title="Counts", chart_title="Distribution of Households by Type of Ration Card", chart_subtitle="")


        #for the sake of numbers
        
        data = {
        'household': [chartH1,chartH2,chartH3,chartH4,chartH5, chartH6,chartH7, chartH8,chartH9, chartH10,chartH11,chartH12],           
        'filtered_numbers':filtered_numbers}

        return data
    
    def all_ilp_charts(self,df, filtered_numbers):
        
        # Age-wise Distribution of Household Members (Bar Chart)
        age_distribution = df['age'].str.extract(r'(\d+)Y')[0].astype(float).dropna()
        age_distribution = age_distribution.apply(
            lambda x: "0-17" if x <= 17 else "18-39" if x <= 39 else 
                    "40-59" if x <= 59 else "60-onwards"
        ).value_counts().sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))

        data_to_visualize = [[x, y] for x, y in zip(age_distribution.index.tolist(), age_distribution.values.tolist())]
        chartH13 = self.generate_bar_chart(data_to_visualize, x_title="Age Groups", y_title="Counts", chart_title="Age-wise Distribution of Household Members", chart_subtitle="")

        
        # Extract gender data from the 'household_member' sheet
        xlabels = list(df['gender'].value_counts().index)  # Gender values (e.g., "Male", "Female")
        ydata = df['gender'].value_counts().values.tolist()  # Count of each gender
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartH14 = self.generate_pie_chart(data_to_visualize, chart_title="Gender wise distribution of Household Members", chart_subtitle="")

        # Extract special status data from the 'household' sheet
        xlabels = list(df['specialstatus'].value_counts().index)  # Special status values (e.g., "No", "Yes")
        ydata = df['specialstatus'].value_counts().values.tolist()  # Count of each special status
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartH15 = self.generate_pie_chart(data_to_visualize, chart_title="Distribution of Special Status", chart_subtitle="")

        # Extract education level data from the 'household_member' sheet
        education_count = df['educationlevel'].value_counts()

        # Define the desired order
        desired_order = [
            "Illiterate", 
            "Literate without formal education", 
            "Below primary", 
            "Primary", 
            "Middle", 
            "Secondary", 
            "Higher secondary", 
            "Graduate", 
            "Postgraduate and above"
        ]

        # Extract xlabels and ydata in the existing format
        xlabels = list(education_count.index)  
        ydata = education_count.values.tolist()  

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartH16 = self.generate_bar_chart(data_to_visualize, x_title="Education Level", y_title="Counts", chart_title="Education Level Distribution", chart_subtitle="")

        categories = [
            "Diploma or certificate in medicine", "Diploma or certificate in other subjects", 
            "Technical degree in engineering/technology", "Learned skilled by doing without formal training", 
            "Diploma or certificate in engineering/technology", "Technical degree in medicine", 
            "Technical degree in agriculture", "Technical degree in other subjects", 
            "Diploma or certificate in crafts", "Technical degree in crafts", "Diploma or certificate in: agriculture"
        ]

        # Filter and map values
        household_member2 = df[
            df['technicaleducationskill'].notna() &  # Exclude NaN values
            (df['technicaleducationskill'].str.strip() != "") &  # Exclude empty strings
            (df['technicaleducationskill'] != "No technical education")
        ].copy()  # Use .copy() to explicitly create a copy of the DataFrame

        # Map values using .loc to avoid SettingWithCopyWarning
        household_member2.loc[:, 'technicaleducationskill'] = household_member2['technicaleducationskill'].apply(
            lambda x: x if x in categories else "Others"
        )

        # Exclude "No technical education" again (if necessary)
        household_member2 = household_member2[household_member2['technicaleducationskill'] != "No technical education"]

        # Define the desired order, placing "Others" at the end
        desired_order = [cat for cat in categories] + ["Others"]

        # Extract xlabels and ydata
        xlabels = household_member2['technicaleducationskill'].value_counts().index.tolist()
        ydata = household_member2['technicaleducationskill'].value_counts().values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order, ensuring "Others" is at the last position
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartH17 = self.generate_bar_chart(
            data_to_visualize,
            x_title="Technical Education Skills",
            y_title="Count",
            chart_title="Technical Education Skill Distribution",
            chart_subtitle=""
        )

        # Categorize data into "No Technical Education" and "Having Technical Education"
        household_member1 = df
        household_member1 = household_member1[household_member1['technicaleducationskill'].notna()]  # Remove blanks

        # Count the two categories
        education_distribution = household_member1['technicaleducationskill'].apply(
            lambda x: "No Technical Education" if x == "No technical education" else "Having Technical Education"
        ).value_counts()

        # Prepare data for the pie chart
        xlabels = education_distribution.index.tolist()  # ["No Technical Education", "Having Technical Education"]
        ydata = education_distribution.values.tolist()  # Corresponding counts
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]

        # Generate the pie chart
        chartH161 = self.generate_pie_chart(
            data_to_visualize,
            chart_title="Technical Education Skill Distribution",
            chart_subtitle=""
        )


        
        # Extract data for employment status
        response_count = df['employmentstatus'].dropna().value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartH18 = self.generate_bar_chart(data_to_visualize, x_title="Employment Status", y_title="Counts", chart_title="Employment Status Distribution", chart_subtitle="", horizontal=True)

        # Change in Present Work (Pie Chart)
        response_count = df['changepresentwork'].dropna().value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartH19 = self.generate_pie_chart(data_to_visualize, chart_title="Change in Present Work", chart_subtitle="")

        # Annual Income Distribution (Bar Chart)
        filtered_data = df['annualincome'].dropna()
        xlabels = list(filtered_data.value_counts().index)  # Unique annual income categories
        ydata = filtered_data.value_counts().values.tolist()  # Count of each category
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartH20 = self.generate_bar_chart(data_to_visualize, x_title="Annual Income", y_title="Counts", chart_title="Annual Income Distribution", chart_subtitle="")

        # Pursuing Higher Education Distribution (Pie Chart)
        filtered_data = df['pursuinghighereducation'].dropna()
        xlabels = list(filtered_data.value_counts().index)  # Unique values (e.g., "Yes", "No")
        ydata = filtered_data.value_counts().values.tolist()  # Count of each value
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartH21 = self.generate_pie_chart(data_to_visualize, chart_title="Pursuing Higher Education Distribution", chart_subtitle="")

        # Proportion of Target Group Members (Bar Chart)
        response_count = df['pecategory'].value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartH22 = self.generate_bar_chart(data_to_visualize, x_title="PECategory", y_title="Counts", chart_title="Proportion of Target Group Members (PEE, PEU, PEUR)", chart_subtitle="")

        # Gender Distribution for PEE, PEU, PEUR (Pie Chart)
        gender_count = df[df['pecategory'].isin(['PEE', 'PEU', 'PEUR']) & df['gender'].notnull()]['gender'].value_counts()
        xlabels, ydata = gender_count.index.tolist(), gender_count.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartH23 = self.generate_pie_chart(data_to_visualize, chart_title="Gender Distribution for PEE, PEU, PEUR", chart_subtitle="")

        # Education Level Distribution for PEE, PEU, PEUR (Bar Chart)
        education_count = df[df['pecategory'].isin(['PEE', 'PEU', 'PEUR']) & df['educationlevel'].notnull()]['educationlevel'].value_counts()

        # Define the desired order
        desired_order = [
            "Illiterate", 
            "Literate without formal education", 
            "Below primary", 
            "Primary", 
            "Middle", 
            "Secondary", 
            "Higher secondary", 
            "Graduate", 
            "Postgraduate and above"
        ]

        # Extract xlabels and ydata in the existing format
        xlabels, ydata = education_count.index.tolist(), education_count.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartH24 = self.generate_bar_chart(data_to_visualize, x_title="Education Level", y_title="Counts", chart_title="Education Level Distribution for PEE, PEU, PEUR", chart_subtitle="")

        # Employment Status Distribution for PEE, PEU, PEUR (Bar Chart)
        filtered_data = df[df['pecategory'].isin(['PEE', 'PEU', 'PEUR'])]
        xlabels, ydata = filtered_data['employmentstatus'].value_counts().index.tolist(), filtered_data['employmentstatus'].value_counts().values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartH25 = self.generate_bar_chart(data_to_visualize, x_title="Employment Status", y_title="Counts", chart_title="Employment Status Distribution for PEE, PEU, PEUR", chart_subtitle="")
        


        data = {
                'ilp': [chartH13,chartH14, chartH15, chartH16,chartH161,chartH17,chartH18, chartH20, chartH21, chartH22, chartH23, chartH24,chartH25],
                'filtered_numbers':filtered_numbers
        }
        return data

    def all_peur_charts(self,df, filtered_numbers):
        # Chart 1: Distribution of Sector of Unregistered Activity
        data = df['sectorofenterprise'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur1 = self.generate_bar_chart(data_to_visualize, x_title="Sector", y_title="Count", chart_title="Distribution of Sector of Unregistered Activity", chart_subtitle="")
        
        # Chart 2: Distribution of Types of Ownership (Unregistered Activities)
        specific_categories = [
            "Single Proprietorship", "Group of Family members(Partnership within the same household)",
            "Partnership", "Self Help Groups", "Corporation", "Farmers Producers Organization",
            "Society/Trust/Club/Association"
        ]
        xvalues = df['typeofownership'].apply(lambda x: x if x in specific_categories else "Others").value_counts().index.tolist()
        ydata = df['typeofownership'].apply(lambda x: x if x in specific_categories else "Others").value_counts().values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xvalues, ydata)]
        chartpeur2 = self.generate_bar_chart(data_to_visualize, x_title="Ownership Type", y_title="Count", chart_title="Distribution of Types of Ownership (Unregistered Activities)", chart_subtitle="")

        # Chart 3: PEUR- Nature of Business
        data = df['natureofbusiness'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur3 = self.generate_bar_chart(data_to_visualize, x_title="Nature of Business", y_title="Count", chart_title="PEUR- Nature of Business", chart_subtitle="")

        # Chart 13: PEUR-Location of Business
        filtered_data = df['locationofbusiness'].dropna().loc[lambda x: x != '---']
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur4 = self.generate_bar_chart(data_to_visualize, x_title="Location", y_title="Count", chart_title="PEUR-Location of Business", chart_subtitle="")

        
        # Chart 14: PEUR- Area of business unit (Location of business = Outside the home)
        data = df['areaofbusinessunit'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur5 = self.generate_bar_chart(data_to_visualize, x_title="Area", y_title="Count", chart_title="PEUR- Area of business unit (Location of business = Outside the home)", chart_subtitle="")

        # Chart 4: Initial Investment Distribution
        filtered_data = df['initialinvestment'].dropna()
        xlabels = list(filtered_data.value_counts().index)
        ydata = filtered_data.value_counts().values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur6 = self.generate_bar_chart(data_to_visualize, x_title="Initial Investment", y_title="Count", chart_title="Initial Investment Distribution", chart_subtitle="")

        
        # Chart 15: PEUR-Loan Availed
        filtered_data = df['loanavailed'].dropna().loc[lambda x: x != '---']
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeur7 = self.generate_pie_chart(data_to_visualize, chart_title="PEUR-Loan Availed", chart_subtitle="")
        
        # Chart 16: Loan Amount Availed Distribution
        loan_amount = df['amountofloanavailed'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "Less than 2 lakhs",
            "Above 2-5 lakhs",
            "Above 5-10 lakhs",
            "Above 10 lakhs"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = loan_amount.index.tolist(), loan_amount.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeur8 = self.generate_bar_chart(data_to_visualize, x_title="Loan Amount", y_title="Count", chart_title="Loan Amount Availed Distribution", chart_subtitle="")

    # Chart 17: Difficulties in Availing Loans
        categories = [
            "Difficulty in finding of collateral",
            "Lengthy duration for approval",
            "Insufficient/poor credit history",
            "High-interest rates",
            "Complex application procedures",
            "Banks inaccessible/located too far",
            "No difficulty"
        ]

        # Parse the data
        parsed_data = df['difficultyinavailingloan'].dropna().str.strip("{}").str.split(r',\s*')

        # Flatten the list, map values to "Others" where necessary, and generate a new Series
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Avoid empty rows
        )

        # Count occurrences of each value
        sorted_data = data_series.value_counts(ascending=False)

        # Define the desired order, placing "Others" at the end
        desired_order = categories + ["Others"]

        # Extract xlabels and ydata
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order, ensuring "Others" is last
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeur9 = self.generate_bar_chart(
            data_to_visualize,
            x_title="Difficulty",
            y_title="Count",
            chart_title="Difficulties in Availing Loans",
            chart_subtitle=""
        )
        
        # Chart 18: Distribution of Raw Material Source
        categories = ['Self-sourced (e.g., in Agriculture )', 'Locally(within the same district)', 'Regionally(within J&K)', 'Nationally(outside J&K)', 'Internationally(imported)', 'Others']
        rawmaterialsource_category = df['rawmaterialsource'].dropna().apply(
            lambda x: next((cat for cat in categories if cat.lower() in x.lower()), 'Others'))
        xlabels, ydata = rawmaterialsource_category.value_counts().index.tolist(), rawmaterialsource_category.value_counts().values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur10 = self.generate_bar_chart(data_to_visualize, x_title="Source", y_title="Count", chart_title="Distribution of Raw Material Source", chart_subtitle="")

        # Chart 19: Challenges in Sourcing Raw Materials
        data = df['challengesinsourcingrawmaterial'].dropna()
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
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur11 = self.generate_bar_chart(data_to_visualize, x_title="Challenge", y_title="Count", chart_title="Challenges in Sourcing Raw Materials", chart_subtitle="")

        # Chart 24: Skill Relevant to Business
        data = df['skillrelevanttobusiness'].dropna()
        response_count = data.value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeur12 = self.generate_pie_chart(data_to_visualize, chart_title="Skill Relevant to Business", chart_subtitle="")

        # Prepare data for the pie chart
        data = df['statusofenterprise'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]

        # Generate the pie chart
        chartpeur13 = self.generate_pie_chart(
            data_to_visualize,
            chart_title="PEUR-Status of Enterprise",
            chart_subtitle=""
        )

        
        # Chart 20: Current Market Reach Distribution
        data = df['currentmarketreach'].dropna()
        categories = {
            "Local (within district)": "Local (within district)",
            "Regional (within J&K)": "Regional (within J&K)",
            "National (outside J&K)": "National (outside J&K)",
            "International (export markets)": "International (export markets)"
        }

        # Map the values to categories, setting "Others" for any unmatched values
        mapped_data = data.map(lambda x: categories.get(x, "Others"))

        # Count occurrences of each value
        response_count = mapped_data.value_counts()

        # Define the desired order, placing "Others" last
        desired_order = list(categories.values()) + ["Others"]

        # Extract xlabels and ydata
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort the data based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeur14 = self.generate_bar_chart(
            data_to_visualize,
            x_title="Market Reach",
            y_title="Count",
            chart_title="Current Market Reach Distribution",
            chart_subtitle=""
        )

        
        # Chart 21: Average Time for Sales Distribution
        sales_time = df['averagetimeforsales'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "Less than 1 month",
            "Above 1-3 months",
            "Above 3-6 months",
            "Above 6 months"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = sales_time.index.tolist(), sales_time.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeur15 = self.generate_bar_chart(data_to_visualize, x_title="Average Time", y_title="Count", chart_title="Average Time for Sales Distribution", chart_subtitle="")

        # Chart 22: Lean Period in Sales Distribution
        data = df['leanperiodinsales'].dropna()
        response_count = data.value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeur16 = self.generate_pie_chart(data_to_visualize, chart_title="Lean Period in Sales Distribution", chart_subtitle="")

        # Chart 23: Lean Period Duration Distribution
        lean_period = df['leanperiodduration'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "1-2 months",
            "3-4 months",
            "5-6 months",
            "More than 6 months"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = lean_period.index.tolist(), lean_period.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeur17 = self.generate_bar_chart(data_to_visualize, x_title="Duration", y_title="Count", chart_title="Lean Period Duration Distribution", chart_subtitle="")

        
        # Chart 10: PEUR-Interested in Formal Setup
        filtered_data = df['interestedinformalsetup'].dropna().loc[lambda x: x != '---']
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeur18 = self.generate_pie_chart(data_to_visualize, chart_title="PEUR-Interested in Formal Setup", chart_subtitle="")

        # Chart 11: Reasons for Not Shifting to Formal Sector
        data = df['reasonsfornotshifting'].dropna()
        categories = ["Satisfied with the existing status", "High Interest rates on loans", "Too many Govt formalities", "Non-cooperation from government agencies"]
        mapped_data = data.apply(lambda x: next((cat for cat in categories if cat in x), "Others"))

        # Count occurrences of each value
        response_count = mapped_data.value_counts()

        # Define the desired order, placing "Others" last
        desired_order = categories + ["Others"]

        # Extract xlabels and ydata
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort the data based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeur19 = self.generate_bar_chart(
            data_to_visualize,
            x_title="Reason",
            y_title="Count",
            chart_title="Reasons for Not Shifting to Formal Sector",
            chart_subtitle=""
        )

        # Chart 5: PEUR-Awareness of Self-Employment Schemes
        filtered_data = df['awareofselfemploymentschemes'].dropna().loc[lambda x: x != '---']
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeur20 = self.generate_pie_chart(data_to_visualize, chart_title="PEUR-Awareness of Self-Employment Schemes", chart_subtitle="")

        # Chart 6: PEUR-Usage of Government Schemes
        filtered_data = df['haveyouusedgovtschemes'].dropna().loc[lambda x: x != '---']
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeur21 = self.generate_pie_chart(data_to_visualize, chart_title="PEUR-Usage of Government Schemes", chart_subtitle="")

        # Chart 7: PEUR - Name of Used Schemes
        categories = [
            "Prime Minister's Employment Generation Program(PMEGP)",
            "Credit Guarantee Fund for micro and Small Businesses (CGTMSE)",
            "J&K Rural Employment Generation Program (JKREGP)",
            "Pradhan Mantri Formalization of Micro Food Processing Businesses",
            "National Urban Livelihood Mission (NULM)",
            "National Rural Livelihood Mission (NRLM)",
            "Dairy Business Development Scheme",
            "Kisan Credit Card Scheme",
            "Pradhan Mantri Weaver Mudra Yojna",
            "Poultry Venture Capital Fund",
            "National Agriculture Infrastructure Fund (AIF)",
            "Animal Husbandry Infrastructure Fund (AHIDF)",
            "PM-SVANidhi Scheme",
            "Pradhan Mantri MUDRA Yojana (PMMY)",
            "STAND UP India-Loans for MSMEs",
            "Holistic Agriculture Development Program",
            "Women Entrepreneurship Program(WEP)",
            "Micro finance Loan Scheme",
            "Virasat Scheme",
            "Mumkin-Mission Youth",
            "TEJASWINI-The Radiant",
            "Spurring Entrepreneurship Initiative",
            "Youth Startup Loan Scheme",
            "Integrated Dairy Development Scheme",
            "Artisan Credit Card Scheme",
            "Rise Together-Mission Youth",
            "J&K IT/ITeS Policy",
            "New Central Government Scheme",
            "J&K Affordable Housing, Slum Rehabilitation and Township Policy",
            "J&K Wool Processing, Handloom, and Handicrafts Policy",
            "J&K Poultry Policy",
            "J&K Industrial Policy",
            "J&K Film Policy",
            "J&K Tourism Policy",
            "Rashtriya Krishi Vikas Yojana (RKVY)-RAFTAAR"
        ]
        parsed_data = df['usedgovtschemes'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]
        )
        sorted_data = data_series.value_counts(ascending=False)
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur22 = self.generate_bar_chart(data_to_visualize, x_title="Scheme", y_title="Count", chart_title="PEUR - Name of Used Schemes", chart_subtitle="")

        # Prepare data for the bar chart
        filtered_data = df['loanrepaymentstatus'].dropna()  # Filter non-null values
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()  # Get counts
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Generate the bar chart
        chartpeur23 = self.generate_bar_chart(
            data_to_visualize,
            x_title="Loan Repayment Status",
            y_title="Count",
            chart_title="PEUR-Loan Repayment Status",
            chart_subtitle=""
        )

        

        # Chart 8: PEUR-Reasons for Not Availing Schemes
        filtered_data = df['reasonsfornotavailingscheme'].dropna().loc[lambda x: x != '---']
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeur24 = self.generate_bar_chart(data_to_visualize, x_title="Reason", y_title="Count", chart_title="PEUR-Reasons for Not Availing Schemes", chart_subtitle="")

    
        # Chart 12: PEUR-Interested in YUVA for Upgrading
        filtered_data = df['interestedinyuvaforupgrading'].dropna().loc[lambda x: x != '---']
        xlabels, ydata = filtered_data.value_counts().index.tolist(), filtered_data.value_counts().values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeur25 = self.generate_pie_chart(data_to_visualize, chart_title="PEUR-Interested in YUVA for Upgrading", chart_subtitle="")

        categories = [
        "Financial support",
        "Market accesses ",
        "Technological support",
        "Relaxation in Regulatory Barriers (Licenses/registration) ",
        "Providing Mentorship/Hand holding",
        "Providing Transportation/Logistics accessibility ",
        "Providing trainings to upgrade skill "
        ]

        # Parse and clean the data
        parsed_data = df['assistanceareyoulooking'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows (`{}`)
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Prepare data for the bar chart
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Generate the bar chart
        chartpeur26 = self.generate_bar_chart(
            data_to_visualize,
            x_title="Assistance Type",
            y_title="Count",
            chart_title="PEUR - Assistance Required in Scaling the Business",
            chart_subtitle=""
        )

        # Prepare data for the bar chart
        data = df['skillrequiredforbusinessupgrade'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Generate the bar chart
        chartpeur27 = self.generate_bar_chart(
                data_to_visualize,
                x_title="Skills",
                y_title="Count",
                chart_title="PEUR- Skills Required for Upgrading Business",
                chart_subtitle=""
            )
                    
            # Prepare data for the bar chart
        data = df['activitycoveredunderskillupgrading'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Generate the bar chart
        chartpeur28 = self.generate_bar_chart(
                data_to_visualize,
                x_title="Activity",
                y_title="Count",
                chart_title="PEUR- Activity required under Training/Skill Upgradation",
                chart_subtitle=""
            )
        
        
        # PEUR - Amount of Financial Support Needed (Bar Chart)
        financial_support = df['amountoffinancialsupport'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "Less than 2 lakhs",
            "Above 2-5 lakhs",
            "Above 5-10 lakhs",
            "Above 10 lakhs"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = financial_support.index.tolist(), financial_support.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeur29 = self.generate_bar_chart(data_to_visualize, x_title="Financial Support", y_title="Counts", chart_title="Amount of Financial Support Needed", chart_subtitle="")


        
        # Prepare data for the pie chart
        data = df['rolemodelinlocality'].dropna()
        response_count = data.value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]

        # Generate the pie chart
        chartpeur30 = self.generate_pie_chart(
            data_to_visualize,
            chart_title="Role Model in Locality",
            chart_subtitle=""
        )

        data = {
            'peur': [chartpeur1, chartpeur2, chartpeur3, chartpeur4, chartpeur5, chartpeur6, chartpeur7, chartpeur8, chartpeur9, chartpeur10, chartpeur11, chartpeur12, chartpeur13, chartpeur14, chartpeur15, chartpeur16, chartpeur17, chartpeur18, chartpeur19, chartpeur20, chartpeur21, chartpeur22, chartpeur23, chartpeur24, chartpeur25, chartpeur26, chartpeur27, chartpeur28, chartpeur29, chartpeur30],
            'filtered_numbers':filtered_numbers
        }
        return data
    
    def all_pee_charts(self,df,filtered_numbers):
        # Chart 1: PEE - Age Distribution
        xvalues = (
            df['age']
            .str.extract(r'(\d+)Y')[0]  # Extract years from the 'age' column
            .astype(float)
            .dropna()
            .apply(
                lambda x: (
                    "0-17" if x <= 17 else
                    "18-39" if x <= 39 else
                    "40-59" if x <= 59 else
                    "60-onwards"
                )
            )  # Categorize ages into the specified ranges
            .value_counts()
            .sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))  # Sort by the starting number of the range
            .index.tolist()
        )

        ydata = (
            df['age']
            .str.extract(r'(\d+)Y')[0]  # Extract years from the 'age' column
            .astype(float)
            .dropna()
            .apply(
                lambda x: (
                    "0-17" if x <= 17 else
                    "18-39" if x <= 39 else
                    "40-59" if x <= 59 else
                    "60-onwards"
                )
            )  # Categorize ages into the specified ranges
            .value_counts()
            .sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))  # Sort by the starting number of the range
            .values.tolist()
        )

        data_to_visualize = [[x, y] for (x, y) in zip(xvalues, ydata)]
        chartPEE1 = self.generate_bar_chart(data_to_visualize, x_title="Age Groups", y_title="Count", chart_title="PEE - Age Distribution", chart_subtitle="")

        # Chart 2: PEE - Gender Distribution
        data = df['gender'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartPEE2 = self.generate_pie_chart(data_to_visualize, chart_title="PEE - Gender Distribution", chart_subtitle="")

        # Chart 3: PEE - Technical Skills Possessed Across Different Sectors
        data = df['sectortechnicalskill'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartPEE3 = self.generate_bar_chart(data_to_visualize, x_title="Sectors", y_title="Count", chart_title="PEE - Technical Skills Possessed Across Different Sectors", chart_subtitle="")

        # Chart 4: PEE - Awareness of Government Initiatives for Youth Self-Employment Opportunities
        data = df['awareofgovtselfemploymentopportunity'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartPEE4 = self.generate_pie_chart(data_to_visualize, chart_title="PEE - Awareness of Government Initiatives for Youth Self-Employment Opportunities", chart_subtitle="")

        # Chart 5: PEE - Preferred Sectors for Enterprise Creation Among Youth
        data = df['sectorofinterest'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartPEE5 = self.generate_bar_chart(data_to_visualize, x_title="Sectors", y_title="Count", chart_title="PEE - Preferred Sectors for Enterprise Creation Among Youth", chart_subtitle="")

        # Chart 6: PEE - Preferred Scale of Business Investment (in Lakhs)
        business_scale = df['scaleofbusiness'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "Less than 2 lakhs",
            "Above 2-5 lakhs",
            "Above 5-10 lakhs",
            "Above 10-20 lakhs",
            "Above 20-50 lakhs",
            "More than 50 lakhs"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = business_scale.index.tolist(), business_scale.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartPEE6 = self.generate_bar_chart(data_to_visualize, x_title="Scale of Business", y_title="Count", chart_title="PEE - Preferred Scale of Business Investment", chart_subtitle="")

        # Chart 7: PEE - Awareness of Government Self-Employment Schemes
        data = df['awareofschemes'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartPEE7 = self.generate_pie_chart(data_to_visualize, chart_title="PEE - Awareness of Government Self-Employment Schemes", chart_subtitle="")

        # Chart 8: PEE - Government Self-Employment Schemes Recognized by Respondents
        categories = [
            "Prime Minister's Employment Generation Program (PMEGP)",
            "Credit Guarantee Fund for Micro and Small Businesses (CGTMSE)",
            "J&K Rural Employment Generation Program (JKREGP)",
            "Pradhan Mantri Formalization of Micro Food Processing Businesses",
            "National Urban Livelihood Mission (NULM)",
            "National Rural Livelihood Mission (NRLM)",
            "Dairy Business Development Scheme",
            "Kisan Credit Card Scheme",
            "Pradhan Mantri Weaver Mudra Yojna",
            "Poultry Venture Capital Fund",
            "Animal Husbandry Infrastructure Fund (AHIDF)",
            "PM-SVANidhi Scheme",
            "Pradhan Mantri MUDRA Yojana (PMMY)",
            "STAND UP India - Loans for MSMEs",
            "Holistic Agriculture Development Program",
            "Women Entrepreneurship Program (WEP)",
            "Microfinance Loan Scheme",
            "Virasat Scheme",
            "Mumkin - Mission Youth",
            "TEJASWINI- The Radiant",
            "Spurring Entrepreneurship Initiative",
            "Youth Start-up Loan Scheme",
            "Integrated Dairy Development Scheme",
            "Artisan Credit Card Scheme",
            "Rise Together - Mission Youth",
            "J&K IT/ITeS Policy"
        ]

        parsed_data = df['schemenames'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartPEE8 = self.generate_bar_chart(data_to_visualize, x_title="Schemes", y_title="Count", chart_title="PEE - Government Self-Employment Schemes Recognized by Respondents (Aware of govt self employment schemes: Yes)", chart_subtitle="")

        # Chart 9: PEE - Approached Authorities for Financial Assistance Under Schemes
        data = df['approachedauthorityforassistance'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartPEE9 = self.generate_pie_chart(data_to_visualize, chart_title="PEE - Approached Authorities for Financial Assistance Under Schemes (Aware of govt self employment schemes: Yes)", chart_subtitle="")

            # Chart 10: PEE - Reasons for Not Receiving Benefits Under Government Schemes
        categories = [
                "Lack of collateral security", "Lengthy duration for approval", "Insufficient/poor credit history",
                "High-interest rates", "Lack of documentation for various schemes", "Complex application procedures",
                "Banks inaccessible/located too far", "No relevant skill"
            ]

        parsed_data = df['reasonsfornotreceivingbenefit'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartPEE10 = self.generate_bar_chart(data_to_visualize, x_title="Reasons", y_title="Count", chart_title="PEE - Reasons for Not Receiving Benefits Under Government Schemes (Aware of govt self employment schemes: Yes, Approached Authority for Assistance: Yes)", chart_subtitle="")

        # Chart 11: PEE - Interest in Availing YUVA Scheme Benefits for Future Entrepreneurship
        data = df['interestedinyuva'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartPEE11 = self.generate_pie_chart(data_to_visualize, chart_title="PEE - Interest in Availing YUVA Scheme Benefits for Future Entrepreneurship", chart_subtitle="")

        # Chart 12: PEE - Types of Assistance Needed for Starting a Business
        categories = [
            "Funding or loans", "Entrepreneurship training and workshops", "Mentorship from experienced entrepreneurs",
            "Market access and industry information", "Networking opportunities", "Easier legal and regulatory processes"
        ]

        parsed_data = df['assistancelookingfor'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartPEE12 = self.generate_bar_chart(data_to_visualize, x_title="Assistance Types", y_title="Count", chart_title="PEE - Types of Assistance Needed for Starting a Business (Interested in Yuva: Yes)", chart_subtitle="")

        # Chart 13: PEE - Training & Skill Upgradation Requirements for Starting a Business
        data = df['trainingrequired'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartPEE13 = self.generate_bar_chart(data_to_visualize, x_title="Training Requirements", y_title="Count", chart_title="PEE - Training & Skill Upgradation Requirements for Starting a Business (Interested in Yuva: Yes)", chart_subtitle="")

        # Chart 14: PEU - Desired Financial Support from Government Schemes
        financial_support = df['financialsupportamount'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "Less than 2 lakhs",
            "Above 2-5 lakhs",
            "Above 05-10 lakhs",
            "Above 10-20 lakhs",
            "Above 20-50 lakhs",
            "More than 50 lakhs"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = financial_support.index.tolist(), financial_support.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartPEE14 = self.generate_bar_chart(data_to_visualize, x_title="Financial Support Amount", y_title="Count", chart_title="PEE - Desired Financial Support from Government Schemes (Interested in Yuva: Yes)", chart_subtitle="")

        # Chart 15: PEE - Anticipated Challenges in Starting a Business
        categories = ["Financial", "Legal", "Market", "Social barriers"]

        parsed_data = df['expectedchallenges'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartPEE15 = self.generate_bar_chart(data_to_visualize, x_title="Challenges", y_title="Count", chart_title="PEE - Anticipated Challenges in Starting a Business", chart_subtitle="")

        # Chart 16: PEE - Presence of Successful Entrepreneurs as Role Models in the Locality
        data = df['rolemodelentrepreneur'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartPEE16 = self.generate_pie_chart(data_to_visualize, chart_title="PEE - Presence of Successful Entrepreneurs as Role Models in the Locality", chart_subtitle="")
        
        data = {
            'pee': [chartPEE1, chartPEE2, chartPEE3, chartPEE4, chartPEE5, chartPEE6, chartPEE7,chartPEE8, chartPEE9, chartPEE10, chartPEE11, chartPEE12, chartPEE13, chartPEE14, chartPEE15,chartPEE16],
            'filtered_numbers':filtered_numbers
        }
        return data


    

    def all_peu_charts(self,df,filtered_numbers):

        # Chart 1: PEU - Age Distribution
        xvalues = (
            df['age']
            .str.extract(r'(\d+)Y')[0]  # Extract years from the 'age' column
            .astype(float)
            .dropna()
            .apply(
                lambda x: (
                    "0-17" if x <= 17 else
                    "18-39" if x <= 39 else
                    "40-59" if x <= 59 else
                    "60-onwards"
                )
            )  # Categorize ages into the specified ranges
            .value_counts()
            .sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))  # Sort by the starting number of the range
            .index.tolist()
        )

        ydata = (
            df['age']
            .str.extract(r'(\d+)Y')[0]  # Extract years from the 'age' column
            .astype(float)
            .dropna()
            .apply(
                lambda x: (
                    "0-17" if x <= 17 else
                    "18-39" if x <= 39 else
                    "40-59" if x <= 59 else
                    "60-onwards"
                )
            )  # Categorize ages into the specified ranges
            .value_counts()
            .sort_index(key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))  # Sort by the starting number of the range
            .values.tolist()
        )

        data_to_visualize = [[x, y] for (x, y) in zip(xvalues, ydata)]
        chartpeu1 = self.generate_bar_chart(data_to_visualize, x_title="Age Groups", y_title="Count", chart_title="PEU - Age Distribution", chart_subtitle="")

        
    
        # Chart 2: PEU - Gender Distribution
        data = df['gender'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeu2 = self.generate_pie_chart(data_to_visualize, chart_title="PEU - Gender Distribution", chart_subtitle="")
        
       # Chart 3: PEU - Sector of Possessed Technical Skill
        data = df['sectortechnicalskill'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeu3 = self.generate_bar_chart(data_to_visualize, x_title="Sectors", y_title="Count", chart_title="PEU - Sector of Possessed Technical Skill", chart_subtitle="")

        # Chart 4: PEU - Awareness of Government Initiatives for Youth Self-Employment Opportunities
        data = df['awareofgovtselfemploymentopportunity'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeu4 = self.generate_pie_chart(data_to_visualize, chart_title="PEU - Awareness of Government Initiatives for Youth Self-Employment Opportunities", chart_subtitle="")

        # Chart 5: PEU - Preferred Sectors for Enterprise Creation Among Youth
        data = df['sectorofinterest'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeu5 = self.generate_bar_chart(data_to_visualize, x_title="Sectors", y_title="Count", chart_title="PEU - Preferred Sectors for Enterprise Creation Among Youth", chart_subtitle="")

        # Chart 6: PEU - Preferred Scale of Business Investment (in Lakhs)
        business_scale = df['scaleofbusiness'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "Less than 2 lakhs",
            "Above 2-5 lakhs",
            "Above 5-10 lakhs",
            "Above 10-20 lakhs",
            "Above 20-50 lakhs",
            "More than 50 lakhs"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = business_scale.index.tolist(), business_scale.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeu6 = self.generate_bar_chart(data_to_visualize, x_title="Scale of Business", y_title="Count", chart_title="PEU - Preferred Scale of Business Investment", chart_subtitle="")

        # Chart 7: PEU - Awareness of Government Self-Employment Schemes
        data = df['awareofschemes'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeu7 = self.generate_pie_chart(data_to_visualize, chart_title="PEU - Awareness of Government Self-Employment Schemes", chart_subtitle="")

        # Chart 8: PEU - Government Self-Employment Schemes Recognized by Respondents
        categories = [
            "Prime Minister's Employment Generation Program (PMEGP)",
            "Credit Guarantee Fund for Micro and Small Businesses (CGTMSE)",
            "J&K Rural Employment Generation Program (JKREGP)",
            "Pradhan Mantri Formalization of Micro Food Processing Businesses",
            "National Urban Livelihood Mission (NULM)",
            "National Rural Livelihood Mission (NRLM)",
            "Dairy Business Development Scheme",
            "Kisan Credit Card Scheme",
            "Pradhan Mantri Weaver Mudra Yojna",
            "Poultry Venture Capital Fund",
            "Animal Husbandry Infrastructure Fund (AHIDF)",
            "PM-SVANidhi Scheme",
            "Pradhan Mantri MUDRA Yojana (PMMY)",
            "STAND UP India - Loans for MSMEs",
            "Holistic Agriculture Development Program",
            "Women Entrepreneurship Program (WEP)",
            "Microfinance Loan Scheme",
            "Virasat Scheme",
            "Mumkin - Mission Youth",
            "TEJASWINI- The Radiant",
            "Spurring Entrepreneurship Initiative",
            "Youth Start-up Loan Scheme",
            "Integrated Dairy Development Scheme",
            "Artisan Credit Card Scheme",
            "Rise Together - Mission Youth",
            "J&K IT/ITeS Policy"
        ]

        parsed_data = df['schemenames'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeu8 = self.generate_bar_chart(data_to_visualize, x_title="Schemes", y_title="Count", chart_title="PEU - Government Self-Employment Schemes Recognized by Respondents (Aware of govt self employment schemes: Yes)", chart_subtitle="")

        # Chart 9: PEU - Approached Authorities for Financial Assistance Under Schemes
        data = df['approachedauthorityforassistance'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeu9 = self.generate_pie_chart(data_to_visualize, chart_title="PEU - Approached Authorities for Financial Assistance Under Schemes (Aware of govt self employment schemes: Yes)", chart_subtitle="")

        # Chart 10: PEU - Reasons for Not Receiving Benefits Under Government Schemes
        categories = [
            "Lack of collateral security", "Lengthy duration for approval", "Insufficient/poor credit history",
            "High-interest rates", "Lack of documentation for various schemes", "Complex application procedures",
            "Banks inaccessible/located too far", "No relevant skill"
        ]

        parsed_data = df['reasonsfornotreceivingbenefit'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeu10 = self.generate_bar_chart(data_to_visualize, x_title="Reasons", y_title="Count", chart_title="PEU - Reasons for Not Receiving Benefits Under Government Schemes (Aware of govt self employment schemes: Yes, Approached Authority for Assistance: Yes)", chart_subtitle="")

        # Chart 11: PEU - Interest in Availing YUVA Scheme Benefits for Future Entrepreneurship
        data = df['interestedinyuva'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeu11 = self.generate_pie_chart(data_to_visualize, chart_title="PEU - Interest in Availing YUVA Scheme Benefits for Future Entrepreneurship", chart_subtitle="")

        # Chart 12: PEU - Types of Assistance Needed for Starting a Business
        categories = [
            "Funding or loans", "Entrepreneurship training and workshops", "Mentorship from experienced entrepreneurs",
            "Market access and industry information", "Networking opportunities", "Easier legal and regulatory processes"
        ]

        parsed_data = df['assistancelookingfor'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeu12 = self.generate_bar_chart(data_to_visualize, x_title="Assistance Types", y_title="Count", chart_title="PEU - Types of Assistance Needed for Starting a Business (Interested in Yuva: Yes)", chart_subtitle="")

        # Chart 13: PEU - Training & Skill Upgradation Requirements for Starting a Business
        data = df['trainingrequired'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeu13 = self.generate_bar_chart(data_to_visualize, x_title="Training Requirements", y_title="Count", chart_title="PEU - Training & Skill Upgradation Requirements for Starting a Business (Interested in Yuva: Yes)", chart_subtitle="")

        # Chart 14: PEU - Desired Financial Support from Government Schemes
        financial_support = df['financialsupportamount'].dropna().value_counts()

        # Define the desired order
        desired_order = [
            "Less than 2 lakhs",
            "Above 2-5 lakhs",
            "Above 05-10 lakhs",
            "Above 10-20 lakhs",
            "Above 20-50 lakhs",
            "More than 50 lakhs"
        ]

        # Extract xlabels and ydata
        xlabels, ydata = financial_support.index.tolist(), financial_support.values.tolist()

        # Pair the data
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]

        # Sort based on the desired order
        data_to_visualize = sorted(data_to_visualize, key=lambda x: desired_order.index(x[0]) if x[0] in desired_order else len(desired_order))

        # Generate the bar chart
        chartpeu14 = self.generate_bar_chart(data_to_visualize, x_title="Financial Support Amount", y_title="Count", chart_title="PEU - Desired Financial Support from Government Schemes (Interested in Yuva: Yes)", chart_subtitle="")

        # Chart 15: PEU - Anticipated Challenges in Starting a Business
        categories = ["Financial", "Legal", "Market", "Social barriers"]

        parsed_data = df['expectedchallenges'].dropna().str.strip("{}").str.split(r',\s*')
        data_series = pd.Series(
            category.strip('"') if category.strip('"') in categories else "Others"
            for row in parsed_data for category in row
            if row != [""]  # Skip empty rows ({})
        )

        # Count and sort in descending order
        sorted_data = data_series.value_counts(ascending=False)

        # Extract labels and values
        xlabels, ydata = sorted_data.index.tolist(), sorted_data.values.tolist()
        data_to_visualize = [[x, y] for (x, y) in zip(xlabels, ydata)]
        chartpeu15 = self.generate_bar_chart(data_to_visualize, x_title="Challenges", y_title="Count", chart_title="PEU - Anticipated Challenges in Starting a Business", chart_subtitle="")

        # Chart 16: PEU - Presence of Successful Entrepreneurs as Role Models in the Locality
        data = df['rolemodelentrepreneur'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        data_to_visualize = [{'name': x, 'data': y} for (x, y) in zip(xlabels, ydata)]
        chartpeu16 = self.generate_pie_chart(data_to_visualize, chart_title="PEU - Presence of Successful Entrepreneurs as Role Models in the Locality", chart_subtitle="")
        
        data = {
            'peu': [
                chartpeu1, chartpeu2, chartpeu3, chartpeu4, chartpeu5, chartpeu6, chartpeu7, chartpeu8, chartpeu9, chartpeu10, chartpeu11, chartpeu12, chartpeu13, chartpeu14, chartpeu15, chartpeu16],
            'filtered_numbers':filtered_numbers
            
        }
        return data
