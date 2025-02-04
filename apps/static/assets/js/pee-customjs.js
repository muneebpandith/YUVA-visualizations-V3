
// ****** PEE PART   *********//
const pee_dropdowns = ["pee-areatype", "pee-district", "pee-blockmunicipality", "pee-panchayatward"]
//"pee-age", "pee-gender", "pee-educationlevel", "pee-sectorofinterest", "pee-expectedscaleofbusiness","pee-assistancerequiredforyuva" ]

var base_url_filter_options = '/api/v2/fetch_options';
var base_url_charts = '/api/v2/charts-filtered';


async function fetchFilterOptionsPEE(url, targetDropdown) {
    var count = 0;
    try {
        const response = await fetch(url);
        const data = await response.json();

        const dropdown = document.getElementById(targetDropdown);
        dropdown.innerHTML = '<option value="All">All</option>'; // Reset dropdown
        //
        // console.log(data)
        data.options.forEach(item => {
            if(item!="---") {

                if(item=="Transgender") dropdown.innerHTML += `<option value="${item}">Others</option>`;
                else dropdown.innerHTML += `<option value="${item}">${item}</option>`;
            }

        });

        //dropdown.disabled = false; // Enable dropdown after data is loaded
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}




async function fetchChartsPEE(url) {
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



async function loadAreaTypePEE() {
    await fetchFilterOptionsPEE(base_url_filter_options+'/pee/residentialtype', "pee-areatype");
}


async function loadDistrictsPEE() {
    const areaType = document.getElementById("pee-areatype").value;
    if (areaType) {
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/district?residentialtype='+areaType, "pee-district");
    }
    else{
        alert('E.PEE.2: Some error occured. Reload the page.')
    }
}


async function loadBlockMunicipalityPEE() {
    const areaType = document.getElementById("pee-areatype").value;
    const district = document.getElementById("pee-district").value;

    if (areaType  && district) {
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/cdblockulbmc?residentialtype='+areaType+'&district='+district, "pee-blockmunicipality");
    }
    else{
        alert('E.PEE.3: Some error occured. Reload the page.')
    }
}



async function loadPanchayatWardPEE()  {
    const areaType = document.getElementById("pee-areatype").value;
    const district = document.getElementById("pee-district").value;
    const blockmunicipality= document.getElementById("pee-blockmunicipality").value;

    if (areaType  && district && blockmunicipality) {
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/panchayatward?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality, "pee-panchayatward");
    }
    else{
        alert('E.PEE.4: Some error occured. Reload the page.')
    }
}

async function loadAgePEE() {
    // const areaType = document.getElementById("pee-areatype").value;
    // const district = document.getElementById("pee-district").value;
    // const blockmunicipality= document.getElementById("pee-blockmunicipality").value;
    // const panchayatward = document.getElementById("pee-panchayatward").value;
    
    try  {
        //await fetchFilterOptionsPEE(base_url_filter_options+'/pee/age?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward, "pee-age");
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/age', "pee-age");
    }
    catch(error){
        alert('E.PEE.5: Some error occured. Reload the page.')
    }
}



async function loadGenderPEE() {
    // const areaType = document.getElementById("pee-areatype").value;
    // const district = document.getElementById("pee-district").value;
    // const blockmunicipality= document.getElementById("pee-blockmunicipality").value;
    // const panchayatward = document.getElementById("pee-panchayatward").value;
    // const age = document.getElementById("pee-age").value;
    // //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try{
        //await fetchFilterOptionsPEE(base_url_filter_options+'/pee/gender?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age, "pee-gender");
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/gender', "pee-gender");
    }
    catch(error) {
        alert('E.PEE.6: Some error occured. Reload the page.')
    }
}



async function loadEducationLevelPEE() {
    // const areaType = document.getElementById("pee-areatype").value;
    // const district = document.getElementById("pee-district").value;
    // const blockmunicipality= document.getElementById("pee-blockmunicipality").value;
    // const panchayatward = document.getElementById("pee-panchayatward").value;
    // const age = document.getElementById("pee-age").value;
    // const gender = document.getElementById("pee-gender").value;
    
    try{
        //await fetchFilterOptionsPEE(base_url_filter_options+'/pee/educationlevel?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender, "pee-educationlevel");
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/educationlevel', "pee-educationlevel");
    }
    catch(error){
        alert('E.PEE.7: Some error occured. Reload the page.')
    }
}


 


async function loadSectorOfInterestPEE() {
    // const areaType = document.getElementById("pee-areatype").value;
    // const district = document.getElementById("pee-district").value;
    // const blockmunicipality= document.getElementById("pee-blockmunicipality").value;
    // const panchayatward = document.getElementById("pee-panchayatward").value;
    // const age = document.getElementById("pee-age").value;
    // const gender = document.getElementById("pee-gender").value;
    // const educationlevel = document.getElementById("pee-educationlevel").value;
    


   try {
        //await fetchFilterOptionsPEE(base_url_filter_options+'/pee/sectorofinterest?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel, "pee-sectorofinterest");
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/sectorofinterest', "pee-sectorofinterest");
    }
    catch(error){
        alert('E.PEE.8: Some error occured. Reload the page.')
    }
}



async function loadExpectedScaleOfBusinessPEE() {
    // const areaType = document.getElementById("pee-areatype").value;
    // const district = document.getElementById("pee-district").value;
    // const blockmunicipality= document.getElementById("pee-blockmunicipality").value;
    // const panchayatward = document.getElementById("pee-panchayatward").value;
    // const age = document.getElementById("pee-age").value;
    // const gender = document.getElementById("pee-gender").value;
    // const educationlevel = document.getElementById("pee-educationlevel").value;
    // const sectorofinterest = document.getElementById("pee-sectorofinterest").value;
    
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

   try {
        //await fetchFilterOptionsPEE(base_url_filter_options+'/pee/expectedscaleofbusiness?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofinterest='+sectorofinterest, "pee-expectedscaleofbusiness");
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/expectedscaleofbusiness', "pee-expectedscaleofbusiness");
    }
    catch(error){
        alert('E.PEE.9: Some error occured. Reload the page.')
    }
}



async function loadAssistanceYuvaPEE() {
    // const areaType = document.getElementById("pee-areatype").value;
    // const district = document.getElementById("pee-district").value;
    // const blockmunicipality= document.getElementById("pee-blockmunicipality").value;
    // const panchayatward = document.getElementById("pee-panchayatward").value;
    // const age = document.getElementById("pee-age").value;
    // const gender = document.getElementById("pee-gender").value;
    // const educationlevel = document.getElementById("pee-educationlevel").value;
    // const sectorofinterest = document.getElementById("pee-sectorofinterest").value;
    // const expectedscaleofbusiness = document.getElementById("pee-expectedscaleofbusiness").value;
    

    try{
        //await fetchFilterOptionsPEE(base_url_filter_options+'/pee/assistancerequiredyuva?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofinterest='+sectorofinterest+'&expectedscaleofbusiness='+expectedscaleofbusiness, "pee-assistancerequiredforyuva");
        await fetchFilterOptionsPEE(base_url_filter_options+'/pee/assistancerequiredyuva', "pee-assistancerequiredforyuva");
    }
   catch(error) {
        alert('E.PEE.10: Some error occured. Reload the page.')
    }
}





/* FILTERS PORIUTION */

async function loadPEEFilters(x)
{
    resetPEEFilters(x);
    if (x==0)
        {
            if (document.getElementById('pee-areatype').value == "Urban"){
                document.getElementById('label-pee-blockmunicipality').innerHTML = 'Municipality';
                document.getElementById('label-pee-panchayatward').innerHTML = 'Ward';
            }
            else if (document.getElementById('pee-areatype').value == "Rural"){
                document.getElementById('label-pee-blockmunicipality').innerHTML = 'Block';
                document.getElementById('label-pee-panchayatward').innerHTML = 'Panchayat';
            }
            else{
                    document.getElementById('label-pee-blockmunicipality').innerHTML = 'Block/ Municipality';
                    document.getElementById('label-pee-panchayatward').innerHTML = 'Panchayat/ Ward';
                }
            await loadDistrictsPEE();
            // await loadBlockMunicipalityPEE();
            // await loadPanchayatWardPEE();
            // await loadAgePEE();
            // await loadGenderPEE();
            // await loadEducationLevelPEE();
            // await loadSectorOfInterestPEE();
            // await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();        
        }
    else if (x==1)
        {
            await loadBlockMunicipalityPEE();
            // await loadPanchayatWardPEE();
            // await loadAgePEE();
            // await loadGenderPEE();
            // await loadEducationLevelPEE();
            // await loadSectorOfInterestPEE();
            // await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();     
        }
    else if (x==2)
        {
            await loadPanchayatWardPEE();
            // await loadAgePEE();
            // await loadGenderPEE();
            // await loadEducationLevelPEE();
            // await loadSectorOfInterestPEE();
            // await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();     
        }
    else if (x==3)
        {
            //await loadAgePEE();
            // await loadGenderPEE();
            // await loadEducationLevelPEE();
            // await loadSectorOfInterestPEE();
            // await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();      
        }
    else if (x==4)
        {
            //await loadGenderPEE();
            // await loadEducationLevelPEE();
            // await loadSectorOfInterestPEE();
            // await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();     
        }
    else if (x==5)
        {
            //await loadEducationLevelPEE();
            // await loadSectorOfInterestPEE();
            // await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();
        }
    else if(x==6)
        {   
            //await loadSectorOfInterestPEE();
            // await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();
        }
    else if(x==7)
        {
            //await loadExpectedScaleOfBusinessPEE();
            // await loadAssistanceYuvaPEE();
        }
    else if(x==8)
        {
            //await loadAssistanceYuvaPEE();
            
        }
    else if(x==9)
        {
            
        }
    else{
            await loadAreaTypePEE();
            // await loadDistrictsPEE();
            // await loadBlockMunicipalityPEE();
            // await loadPanchayatWardPEE();
            await loadAgePEE();
            await loadGenderPEE();
            await loadEducationLevelPEE();
            await loadSectorOfInterestPEE();
            await loadExpectedScaleOfBusinessPEE();
            await loadAssistanceYuvaPEE();

    }

}





function enable_disable_dropdown_pee(dropdown, value=true)
{
    document.getElementById(dropdown).disabled = value;
    document.getElementById(dropdown).value="All";
}



function resetPEEFilters(currentDropdown)
{
    if (currentDropdown+1<pee_dropdowns.length){
    for (i=currentDropdown+1;i<pee_dropdowns.length;i++){
        enable_disable_dropdown_pee(pee_dropdowns[i], true);
    }
    enable_disable_dropdown_pee(pee_dropdowns[currentDropdown+1], false);
    }
    
}



async function loadPEECharts(x)
{
    if(x==0){
        var params = "residentialtype=All&district=All&cdblockulbmc=All&panchayatward=All&age=All&gender=All&educationlevel=All&sectorofinterest=All&expectedscaleofbusiness=All&assistancerequiredforyuva=All";
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetPEE(base_url_charts+'/pee?'+params, 'pee');
        document.getElementById('loadingbar').style.display='none';
    }
    else{
        const areaType = document.getElementById("pee-areatype").value;
        const district = document.getElementById("pee-district").value;
        const blockmunicipality= document.getElementById("pee-blockmunicipality").value;
        const panchayatward = document.getElementById("pee-panchayatward").value;
        const age = document.getElementById("pee-age").value; 
        const gender = document.getElementById("pee-gender").value; 
        const educationlevel = document.getElementById("pee-educationlevel").value; 
        const sectorofinterest = document.getElementById("pee-sectorofinterest").value; 
        const expectedscaleofbusiness = document.getElementById("pee-expectedscaleofbusiness").value;
        const assistancerequiredforyuva = document.getElementById("pee-assistancerequiredforyuva").value;  
        
        var params = 'residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofinterest='+sectorofinterest+'&expectedscaleofbusiness='+expectedscaleofbusiness+'&assistancerequiredforyuva='+assistancerequiredforyuva;
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetPEE(base_url_charts+'/pee?'+params, 'pee');
        toggle_all_other_sections_pee();
        document.getElementById('loadingbar').style.display='none';
    }

    
}



async function loadChartSetPEE(url, type) {
    const data = await fetchChartsPEE(url);
    if (!data || !data[type]) return;

    const charts = data[type];
    const filtered_numbers = data['filtered_numbers'];
    await fetchGeneralNumbersFiltered(filtered_numbers);
    const mainContainer = document.getElementById('PEEChartsContainer');
    //mainContainer.style.gridTemplateColumns = `repeat(${getChartCount()}, 0.9fr)`;
    mainContainer.innerHTML = ''; // Clear previous charts
    

    var count = 0;
    charts.forEach((chart, index) => {
        
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container-highcharts';
        //chartContainer.style.flex = `1 0 calc(${100 / getChartCount()}% - 20px)`;
        //chartContainer.style.maxWidth = `calc(${100 / getChartCount()}% - 20px)`;

        const canvas = document.createElement('figure');
        canvas.id = `pee-chart-${index}`;
        chartContainer.appendChild(canvas);
        
        mainContainer.appendChild(chartContainer);
        if(chart.type=='pie')
            {
                generatePieChart(canvas, chart);   //defined in loadchartsjs.js
            }
    
            if(chart.type=='bar')
                {
                    generatePieChart(canvas, chart);   //defined in loadchartsjs.js
                }
            else if(chart.type=='column')
                {
                    generateColumnChart(canvas, chart);   //defined in loadchartsjs.js
                }
            else{}
        });
}



//loadPEEFilters(-1);
//loadPEECharts(0);





function togglePEECharts() {
    let toggleElement = document.getElementById("PEEToggle");
    let chartsElement = document.getElementById("pee_charts");

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






function toggle_all_other_sections_pee()
{
    var x = ['household_charts', 'ilp_charts', 'peu_charts', 'peur_charts']
    for(i=0; i < x.length;i++)
    {
        document.getElementById(x[i]+"_header").style.display='none';
        //console.log(x[i]);
        document.getElementById(x[i]).style.display='none';
    }
    document.getElementById("pee_charts_header").style.display='block';
    document.getElementById("pee_charts").style.display='block';

}
