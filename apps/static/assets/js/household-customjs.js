

// ****** HOUSEHOLD PART   *********//
const household_dropdowns = ["household-areatype", "household-district", "household-blockmunicipality", "household-panchayatward"]

    
var base_url_filter_options = '/api/v2/fetch_options';
var base_url_charts = '/api/v2/charts-filtered';



async function fetchFilterOptionsHousehold(url, targetDropdown) {
    var count = 0;
    try {
        
        
        const response = await fetch(url);
        const data = await response.json();

        const dropdown = document.getElementById(targetDropdown);
        dropdown.innerHTML = '<option value="All">All</option>'; // Reset dropdown
        
        //
        // console.log(data)
        data.options.forEach(item => {
            if(item!="---" && item!="NA") {
                if(item=="Transgender") dropdown.innerHTML += `<option value="${item}">Others</option>`;
               else dropdown.innerHTML += `<option value="${item}">${item}</option>`;
            }

        });

        //dropdown.disabled = false; // Enable dropdown after data is loaded
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}




async function fetchChartsHousehold(url) {
    var count = 0;
    try {
        const response = await fetch(url);
        const data = await response.json();
        //await loadChartSet(data, 'household')

        //console.log(data);
        //dropdown.disabled = false; // Enable dropdown after data is loaded
        //xd = data;
        return data;
        


    } catch (error) {
        console.error("Error fetching data:", error);
    }
}


// Load districts based on selected area type

async function loadAreaTypeHousehold() {
    
    await fetchFilterOptionsHousehold(base_url_filter_options+'/household/residentialtype', "household-areatype");
    
}


async function loadDistrictsHousehold() {
    const areaType = document.getElementById("household-areatype").value;
    if (areaType) {
        await fetchFilterOptionsHousehold(base_url_filter_options+'/household/district?residentialtype='+areaType, "household-district");
    }
    else{
        alert('EH2: Some error occured. Reload the page.')
    }
}


async function loadBlockMunicipalityHousehold() {
    const areaType = document.getElementById("household-areatype").value;
    const district = document.getElementById("household-district").value;

    if (areaType  && district) {
        await fetchFilterOptionsHousehold(base_url_filter_options+'/household/cdblockulbmc?residentialtype='+areaType+'&district='+district, "household-blockmunicipality");
    }
    else{
        alert('EH3: Some error occured. Reload the page.')
    }
}



async function loadPanchayatWardHousehold()  {
    const areaType = document.getElementById("household-areatype").value;
    const district = document.getElementById("household-district").value;
    const blockmunicipality= document.getElementById("household-blockmunicipality").value;

    if (areaType  && district && blockmunicipality) {
        await fetchFilterOptionsHousehold(base_url_filter_options+'/household/panchayatward?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality, "household-panchayatward");
    }
    else{
        alert('EH4: Some error occured. Reload the page.')
    }
}

async function loadGenderHousehold() {
    // const areaType = document.getElementById("household-areatype").value;
    // const district = document.getElementById("household-district").value;
    // const blockmunicipality= document.getElementById("household-blockmunicipality").value;
    // const panchayatward = document.getElementById("household-panchayatward").value;
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try {
        //await fetchFilterOptionsHousehold(base_url_filter_options+'/household/gender?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward, "household-headgender");
        await fetchFilterOptionsHousehold(base_url_filter_options+'/household/gender', "household-headgender");
    }
    catch (error){
        alert('EH5: Some error occured. Reload the page.')
    }
}


async function loadAnnualIncomeHousehold() {
    // const areaType = document.getElementById("household-areatype").value;
    // const district = document.getElementById("household-district").value;
    // const blockmunicipality= document.getElementById("household-blockmunicipality").value;
    // const panchayatward = document.getElementById("household-panchayatward").value;
    // const gender = document.getElementById("household-headgender").value;

    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try {
        //await fetchFilterOptionsHousehold(base_url_filter_options+'/household/annualhouseholdincome?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&gender='+gender, "household-annualincome");
        await fetchFilterOptionsHousehold(base_url_filter_options+'/household/annualhouseholdincome',"household-annualincome" );
    }
    catch (error) {
        alert('EH6: Some error occured. Reload the page.')
    }
}



async function loadHouseholdFilters(x)
{

    resetHouseholdFilters(x);
    
    if (x==0)
        {
            if (document.getElementById('household-areatype').value == "Urban"){
                document.getElementById('label-household-blockmunicipality').innerHTML = 'Municipality';
                document.getElementById('label-household-panchayatward').innerHTML = 'Ward';
            }
            else if (document.getElementById('household-areatype').value == "Rural"){
                document.getElementById('label-household-blockmunicipality').innerHTML = 'Block';
                document.getElementById('label-household-panchayatward').innerHTML = 'Panchayat';
            }
            else{
                    document.getElementById('label-household-blockmunicipality').innerHTML = 'Block/ Municipality';
                    document.getElementById('label-household-panchayatward').innerHTML = 'Panchayat/ Ward';
                }
            
            await loadDistrictsHousehold();
            
        }
    else if (x==1)
        {
            await loadBlockMunicipalityHousehold();
        }
    else if (x==2)
        {
            await loadPanchayatWardHousehold();
        }
    else if (x==3)
        {
            //await loadGenderHousehold();
        }
    else if (x==4)
        {
            //await loadAnnualIncomeHousehold();
        }
    else if (x==5)
            {
                
            }
    else{
            await loadAreaTypeHousehold();
            await loadGenderHousehold();
            await loadAnnualIncomeHousehold();

            

    }

}

function enable_disable_dropdown_household(dropdown, value=true)
{
    document.getElementById(dropdown).disabled = value;
    document.getElementById(dropdown).value="All";
}



function resetHouseholdFilters(currentDropdown)
{
    if (currentDropdown+1<household_dropdowns.length){
    for (i=currentDropdown+1;i<household_dropdowns.length;i++){
        enable_disable_dropdown_household(household_dropdowns[i], true);
    }
    enable_disable_dropdown_household(household_dropdowns[currentDropdown+1], false);
    }
    
}



async function loadHouseholdCharts(x)
{
    if(x==0){
        var params = "residentialtype=All&district=All&cdblockulbmc=All&panchayatward=All&gender=All&annualhouseholdincome=All";
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetHousehold(base_url_charts+'/household?'+params, 'household');
        document.getElementById('loadingbar').style.display='none';
    }
    else{

        const areaType = document.getElementById("household-areatype").value;
        const district = document.getElementById("household-district").value;
        const blockmunicipality= document.getElementById("household-blockmunicipality").value;
        const panchayatward = document.getElementById("household-panchayatward").value;
        const gender = document.getElementById("household-headgender").value; 
        const annualhouseholdincome = document.getElementById("household-annualincome").value; 
        var params = 'residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&gender='+gender+'&annualhouseholdincome='+annualhouseholdincome;
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetHousehold(base_url_charts+'/household?'+params, 'household');
        document.getElementById('loadingbar').style.display='none';
        toggle_all_other_sections_household();
        
    }

    
}


async function loadChartSetHousehold(url, type) {
    const data = await fetchChartsHousehold(url);
    if (!data || !data[type]) return;


    const charts = data[type];
    const filtered_numbers = data['filtered_numbers'];
    //console.log(filtered_numbers);
    await fetchGeneralNumbersFiltered(filtered_numbers, 'household');
    //console.log(district_wise_details);
    const mainContainer = document.getElementById('HouseholdChartsContainer');
    //mainContainer.style.gridTemplateColumns = `repeat(${getChartCount()}, 0.9fr)`;
    mainContainer.innerHTML = ''; // Clear previous charts
    var count = 0;
    
    
    charts.forEach((chart, index) => {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container-highcharts';
        //chartContainer.style.flex = `1 0 calc(${100 / getChartCount()}% - 20px)`;
        //chartContainer.style.maxWidth = `calc(${100 / getChartCount()}% - 20px)`;
        const canvas = document.createElement('figure');
        canvas.id = `household-chart-${index}`;
        chartContainer.appendChild(canvas);
        mainContainer.appendChild(chartContainer);
        //xx= chart;
        //console.log(chart.series);
        
        if(chart.type=='pie')
        {
            generatePieChart(canvas, chart);   //defined in loadchartsjs.js
        }

        if(chart.type=='bar')
            {
                generateColumnChart(canvas, chart);   //defined in loadchartsjs.js
            }
        else if(chart.type=='column')
            {
                generateColumnChart(canvas, chart);   //defined in loadchartsjs.js
            }
        else{}
    });


    //     new Chart(canvas, {
    //         type: chart.type,
    //         data: {
    //             labels: chart.labels,
    //             datasets: chart.datasets
    //         },
    //         options: {
    //             indexAxis: chart.options.indexAxis,
    //             responsive: true,
    //             maintainAspectRatio: false,
    //             plugins: {
    //                 legend: {
    //                     display: true, // Display legend
    //                     position: 'right', // Position: 'top', 'bottom', 'left', 'right'
    //                     },
                    
    //                 title: {
    //                     display: true,
    //                     text: chart.chart_title
    //                     },
    //                     datalabels: {
    //                     formatter: (value, ctx) => {
    //                         let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
    //                         let percentage = (value / sum * 100).toFixed(2) + "%";
    //                         return percentage;
    //                     },
    //                     color: '#fff',
    //                     font: {
    //                         weight: 'bold'
    //                     }
    //                 },
                    
    //                 tooltip: {
    //                     callbacks: {
    //                         label: function(context) {
    //                             let value = context.raw;
    //                             let total = context.dataset.data.reduce((a, b) => a + b, 0);
    //                             let percentage = (value / total * 100).toFixed(2) + '%';
    //                             return `${context.label}: ${percentage}`;
    //                         }
    //                     }
    //                 }                            
    //                 /*,
    //                 legend: {
    //                     display: true,
    //                     onClick: (e, legendItem) => {
    //                         const index = legendItem.datasetIndex;
    //                         const ci = e.chart;
    //                         const meta = ci.getDatasetMeta(index);
    //                         // Toggle the visibility
    //                         //meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;
                            
    //                     },
    //                     labels: {
    //                         generateLabels: function(chart) {
    //                             let dataset = chart.data.datasets[0];
    //                             return dataset.data.map((value, index) => ({
    //                                 text: chart.data.labels[index],
    //                                 fillStyle: dataset.backgroundColor[index]
    //                                 //hidden: chart.getDatasetMeta(0).data[index].hidden // Update to reflect current hidden state
                                    
    //                             }));
    //                         }
    //                     }
    //                 }*/

    //             },
    //             scales: (chart.type !== 'pie' && chart.type !== 'doughnut') ?  {
    //                     x:
    //                     {
    //                         title: {
    //                             display: true, // Enable the title
    //                             text: chart.options.scales.x.title, // Label for the X-axis
    //                             font: { size: 14,family: 'Arial',weight: 'bold',},
    //                         color: '#666', // Color of the label
    //                         padding: { top: 10, bottom: 5 }, // Padding around the label
    //                                 }
    //                     },
    //                     y:
    //                     {
    //                         title: {
    //                             display: true, // Enable the title
    //                             text: chart.options.scales.y.title, // Label for the X-axis
    //                             font: { size: 14,family: 'Arial',weight: 'bold',},
    //                         color: '#666', // Color of the label
    //                         padding: { top: 10, bottom: 5 }, // Padding around the label
    //                                 }
    //                     }


    //             }:{}
    //         }
        
    //     });
    // });
}



loadHouseholdFilters(-1);


//loadHouseholdCharts(0);







function toggleHouseholdCharts() {
    let toggleElement = document.getElementById("HLPToggle");
    let chartsElement = document.getElementById("household_charts");

    if (chartsElement.style.display === "none") {
        chartsElement.style.display = "block";
        toggleElement.classList.remove("fa-plus");
        toggleElement.classList.add("fa-minus");
    } else {
        chartsElement.style.display = "none";
        toggleElement.classList.remove("fa-minus");
        toggleElement.classList.add("fa-plus");
        
    }
}





function toggle_all_other_sections_household()
{
    var x = ['ilp_charts', 'peur_charts', 'pee_charts', 'peu_charts']
    for(i=0; i<x.length;i++)
    {
        document.getElementById(x[i]+"_header").style.display='none';
        //console.log(x[i]);
        document.getElementById(x[i]).style.display='none';
    }
    document.getElementById("household_charts_header").style.display='block';
    document.getElementById("household_charts").style.display='block';

}
