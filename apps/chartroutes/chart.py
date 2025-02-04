import random

class Chart:
    def __init__(self):
        #print("Loaded charts")
        self.chart_config = None
    def generate_line_chart(self):
        pass
    def generate_bar_chart(self):
        pass

    def generate_bar_drill_chart(self):
        pass

    def generate_pie_chart(self):
        pass

    def generate_pie_drill_chart(self):
        pass

    def generate_bubble_chart(self):
        pass


    def generate_custom_chart(self):
        pass

    def generate_chart(self):
        pass

    def all_households_charts(self, df, residentialtype):
        type_charts = ["bar", "line", "pie"]
        #breaker_hlp = generate_break('======= Household Level Profile =======')
        # Generate the xlabels (district names) and ydata (count of entries per district)
        xlabels = list(df['district'].value_counts().index)
        ydata = df['district'].value_counts().values.tolist()
        # Generate the chart
        chartH0 = self.generate_chart_data("bar", xlabels, ydata, "Distribution of households by districts")

        # Categorize household sizes and calculate frequencies
        categorized_sizes = df['householdsize'].dropna().loc[lambda x: x != 0].apply(lambda x: int(x) if x <= 8 else '8+')
        size_counts = categorized_sizes.value_counts().sort_index(key=lambda x: [int(i) if isinstance(i, int) else 9 for i in x])
        # Generate bar chart
        chartH3 = self.generate_chart_data("bar", size_counts.index.tolist(), size_counts.values.tolist(), "Distribution of Household Sizes")

        # Replace unmatched values with "others" and calculate counts for rural/urban households
        categories = ["Self-employed in agriculture", "Self-employed in non-agriculture","Regular wage-salary earning", "Casual labour in agriculture","Casual labour in non- agriculture"]
        householdtype_counts = df[df['residentialtype'] == residentialtype]['householdtype'] \
        .apply(lambda x: x if x in categories else "others").value_counts()
        # Generate the bar chart
        chartHLP3 = self.generate_chart_data("bar", householdtype_counts.index.tolist(), householdtype_counts.values.tolist(), "Distribution of Household Types in "+str(residentialtype)+ " Areas")

        # Calculate the proportion of each residential type
        residential_proportion = df['residentialtype'].value_counts(normalize=True)
        # Extract labels and values for the pie chart
        xlabels, ydata = residential_proportion.index.tolist(), residential_proportion.values.tolist()
        # Generate the pie chart data
        chartHLP1 = self.generate_chart_data("pie", xlabels, ydata, "Proportion of households by residential type")


        agricultureland_count = df[df['agriculturelandpossession'].notnull() & (df['agriculturelandpossession'] != '---')]['agriculturelandpossession'].value_counts()
        xlabels, ydata = agricultureland_count.index.tolist(), agricultureland_count.values.tolist()
        chartH5 = self.generate_chart_data("bar", xlabels, ydata, "Distribution of agriculture land possession")

        ownership_proportion = df[df['typeoffamilyenterprise'].isin(['Yes', 'No'])]['typeoffamilyenterprise'].value_counts(normalize=True)
        xlabels, ydata = ownership_proportion.index.tolist(), ownership_proportion.values.tolist()
        chartH7 = self.generate_chart_data("pie", xlabels, ydata, "Proportion of households owning an enterprise")

        response_count = df[df['responseoffamilyenterprise'].notnull() & (df['responseoffamilyenterprise'] != '---')]['responseoffamilyenterprise'].value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        chartH8 = self.generate_chart_data("bar", xlabels, ydata, "Sector of Family Enterprise", True)
        
        response_count = df['locationoftheenterprise'].replace('---', None).dropna().value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        chart_location_pie = self.generate_chart_data("pie", xlabels, ydata, "Location of the Enterprise")

        socialgroup_proportion = df[df['socialgroup'].notnull() & (df['socialgroup'] != '---')]['socialgroup'].value_counts(normalize=True)
        xlabels, ydata = socialgroup_proportion.index.tolist(), socialgroup_proportion.values.tolist()
        chartH4 = self.generate_chart_data("pie", xlabels, ydata, "Proportion of households by social group")


        income_count = df[df['annualhouseholdincome'].notnull() & (df['annualhouseholdincome'] != '---')]['annualhouseholdincome'].value_counts()
        xlabels, ydata = income_count.index.tolist(), income_count.values.tolist()
        chartH6 = self.generate_chart_data("bar", xlabels, ydata, "Distribution of Annual Household Income")

        # Replace unmatched values with "Others" and calculate counts for each category
        categories = ["AAY – Antyodhya Anna Yojana", "PHH- Priority House hold", "NPHH- Non Priority Household", "No ration card", "Exclusion category"]
        rationcard_counts = df['typeofrationcardholder'].apply(lambda x: x if x in categories else "Others").value_counts()
        # Generate the bar chart
        chartHLP2 = self.generate_chart_data("bar", rationcard_counts.index.tolist(), rationcard_counts.values.tolist(), "Distribution of Households by Type of Ration Card")

        data = df[df['gender'] == 'Female']['district'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartDistrictWiseFemaleHoh = self.generate_chart_data("bar", xlabels, ydata, "District-wise percentage of female-headed households")

        data = {
        'household': [chartHLP1,chartH0,chartH3,chartHLP3, chartH5,chartH7,chartH8,chart_location_pie,chartH4,chartH6,chartHLP2,chartDistrictWiseFemaleHoh],
        'business':[]
        }

        return data
    
    def all_ilp_charts(self,df):
        xvalues = (
        df['age']
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
            df['age']
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

        chartAgeWiseDistribution = self.generate_chart_data(
            "bar", xvalues, ydata, "Age-wise Distribution of Household Members"
        )

        # Extract gender data from the 'household_member' sheet
        xlabels = list(df['gender'].value_counts().index)  # Gender values (e.g., "Male", "Female")
        ydata = df['gender'].value_counts().values.tolist()  # Count of each gender
        # Generate the pie chart
        chart_gender_distribution = self.generate_chart_data("pie", xlabels, ydata, "Gender wise distribution of Household Members")

        # Extract special status data from the 'household' sheet
        xlabels = list(df['specialstatus'].value_counts().index)  # Special status values (e.g., "No", "Yes")
        ydata = df['specialstatus'].value_counts().values.tolist()  # Count of each special status
        # Generate the pie chart
        chart_specialstatus = self.generate_chart_data("pie", xlabels, ydata, "Distribution of Special Status")

        # Extract education level data from the 'household_member' sheet
        xlabels = list(df['educationlevel'].value_counts().index)  # Education levels (e.g., "Secondary", "Higher secondary")
        ydata = df['educationlevel'].value_counts().values.tolist()  # Count of each education level
        # Generate the bar chart
        chart_educationlevel = self.generate_chart_data("bar", xlabels, ydata, "Education Level Distribution")

        # Define categories and map unmatched values to "others"
        categories = ["No technical education", "Diploma or certificate in medicine", "Diploma or certificate in other subjects", 
                "Technical degree in engineering/ technology", "Learned skilled by doing without formal training", 
                "Diploma or certificate in engineering/technology", "Technical degree in medicine", 
                "Technical degree in agriculture", "Technical degree in other subjects", 
                "Diploma or certificate in crafts", "Technical degree in crafts", "Diploma or certificate in: agriculture"]
        
        household_member = df
        household_member['technicaleducationskill'] = household_member['technicaleducationskill'].apply(lambda x: x if x in categories else "others")

        # Generate bar chart
        chart_technicaleducation = self.generate_chart_data(
        "bar", 
        household_member['technicaleducationskill'].value_counts().index.tolist(), 
        household_member['technicaleducationskill'].value_counts().values.tolist(), 
        "Technical Education Skill Distribution"
        )

        # Extract data for employment status
        response_count = df['employmentstatus'].dropna().value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        # Generate bar chart
        chart_employment_status = self.generate_chart_data("bar", xlabels, ydata, "Employment Status Distribution", True)



        response_count = df['changepresentwork'].dropna().value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        chart_change_work_pie = self.generate_chart_data("pie", xlabels, ydata, "Change in Present Work")



        # Filter non-blank annual income data and calculate counts
        filtered_data = df['annualincome'].dropna()
        xlabels = list(filtered_data.value_counts().index)  # Unique annual income categories
        ydata = filtered_data.value_counts().values.tolist()  # Count of each category
        # Generate the bar chart
        chart_annualincome = self.generate_chart_data("bar", xlabels, ydata, "Annual Income Distribution")

        # Filter non-blank pursuing higher education data and calculate counts
        filtered_data = df['pursuinghighereducation'].dropna()
        xlabels = list(filtered_data.value_counts().index)  # Unique values (e.g., "Yes", "No")
        ydata = filtered_data.value_counts().values.tolist()  # Count of each value

        # Generate the pie chart
        chart_higher_education = self.generate_chart_data("pie", xlabels, ydata, "Pursuing Higher Education Distribution")




        response_count = df['pecategory'].value_counts()
        xlabels, ydata = response_count.index.tolist(), response_count.values.tolist()
        chart_pecategory = self.generate_chart_data("bar", xlabels, ydata, "Proportion of Target Group Members- Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) among the households")


        gender_count = df[df['pecategory'].isin(['PEE', 'PEU', 'PEUR']) & df['gender'].notnull()]['gender'].value_counts()
        xlabels, ydata = gender_count.index.tolist(), gender_count.values.tolist()
        chartH9 = self.generate_chart_data("pie", xlabels, ydata, "Gender Distribution for Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) Categories")

        education_count = df[df['pecategory'].isin(['PEE', 'PEU', 'PEUR']) & df['educationlevel'].notnull()]['educationlevel'].value_counts()
        xlabels, ydata = education_count.index.tolist(), education_count.values.tolist()
        chartH10 = self.generate_chart_data("bar", xlabels, ydata, "Education Level Distribution for Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) Categories")

        filtered_data = df[df['pecategory'].isin(['PEE', 'PEU', 'PEUR'])]
        xlabels, ydata = filtered_data['employmentstatus'].value_counts().index.tolist(), filtered_data['employmentstatus'].value_counts().values.tolist()
        chartH11 = self.generate_chart_data("bar", xlabels, ydata, "Employment Status Distribution for Potential Entrepreneur Employed(PEE), Potential Entrepreneur Unemployed(PEU) and Potential Entrepreneur Unregistered Activity(PEUR) Categories")


        data = {
            'ilp': [chartAgeWiseDistribution,chart_gender_distribution,chart_specialstatus,chart_educationlevel,chart_technicaleducation,chart_employment_status,chart_annualincome,chart_higher_education,chart_pecategory,chartH9,chartH10,chartH11],
            'business':[]
        }
        return data

    def all_peur_charts(self,data):
        pass
    
    
    def all_pee_charts(self,df):
        data = df['employmentstatus'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH23 = self.generate_chart_data("bar", xlabels, ydata, "PEE- Employment Status Distribution")

        data = df['age'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH24 = self.generate_chart_data("bar", xlabels, ydata, "PEE- Agewise Distribution")

        data = df['gender'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH25 = self.generate_chart_data("pie", xlabels, ydata, "PEE- Gender Distribution")

        data = df['financialsupportamount'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH26 = self.generate_chart_data("bar", xlabels, ydata, "PEE- Financial Support Amount Needed Distribution")

        data = df['sectorofinterest'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH27 = self.generate_chart_data("bar", xlabels, ydata, "PEE- Sector of Interest")

        income_counts = df['annualincome'].value_counts()
        # Prepare data for the chart
        xvalues = income_counts.index.tolist()
        ydata = income_counts.values.tolist()
        chartAnnualIncomeDistribution = self.generate_chart_data(
        "bar", xvalues, ydata, "Annual Income Distribution in PEE Category"
        )

        data = {
            'pee': [chartH23,chartH24,chartH25,chartH26,chartH27,chartAnnualIncomeDistribution],
            'business':[]
            }
        return data

    def all_peu_charts(self,df):
        data = df['age'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH28 = self.generate_chart_data("bar", xlabels, ydata, "PEU- Agewise Distribution")

        data = df['gender'].dropna().value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH29 = self.generate_chart_data("pie", xlabels, ydata, "PEU- Gender Distribution")

        data = df['financialsupportamount'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH30 = self.generate_chart_data("bar", xlabels, ydata, "PEU- Financial Support Amount Needed Distribution")

        data = df['sectorofinterest'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH31 = self.generate_chart_data("bar", xlabels, ydata, "PEU- Sector of Interest")
        
           
        data = df['financialsupportamount'].value_counts()
        xlabels, ydata = data.index.tolist(), data.values.tolist()
        chartH32 = self.generate_chart_data("bar", xlabels, ydata, "PEU- Financial Support Amount Needed Distribution")
        
        data = {
            'peu': [chartH28,chartH29,chartH30,chartH31,chartH32],
            'business':[]
            }
        return data
    
    def generate_chart_data(self, chart_type, xlabels, ydata, title_of_chart, datasets=[], horizontal=False):
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
            self.chart_config = {
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
        return self.chart_config



