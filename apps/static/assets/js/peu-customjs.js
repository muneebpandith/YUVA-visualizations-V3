
// ****** PEU PART   *********//
const peu_dropdowns = ["peu-areatype", "peu-district", "peu-blockmunicipality", "peu-panchayatward"]
//"peu-age", "peu-gender", "peu-educationlevel", "peu-sectorofinterest", "peu-expectedscaleofbusiness","peu-assistancerequiredforyuva" ]

var base_url_filter_options = '/api/v2/fetch_options';
var base_url_charts = '/api/v2/charts-filtered';


async function fetchFilterOptionsPEU(url, targetDropdown) {
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




async function fetchChartsPEU(url) {
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



async function loadAreaTypePEU() {
    await fetchFilterOptionsPEU(base_url_filter_options+'/peu/residentialtype', "peu-areatype");
}


async function loadDistrictsPEU() {
    const areaType = document.getElementById("peu-areatype").value;
    if (areaType) {
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/district?residentialtype='+areaType, "peu-district");
    }
    else{
        alert('E.PEU.2: Some error occured. Reload the page.')
    }
}


async function loadBlockMunicipalityPEU() {
    const areaType = document.getElementById("peu-areatype").value;
    const district = document.getElementById("peu-district").value;

    if (areaType  && district) {
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/cdblockulbmc?residentialtype='+areaType+'&district='+district, "peu-blockmunicipality");
    }
    else{
        alert('E.PEU.3: Some error occured. Reload the page.')
    }
}



async function loadPanchayatWardPEU()  {
    const areaType = document.getElementById("peu-areatype").value;
    const district = document.getElementById("peu-district").value;
    const blockmunicipality= document.getElementById("peu-blockmunicipality").value;

    if (areaType  && district && blockmunicipality) {
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/panchayatward?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality, "peu-panchayatward");
    }
    else{
        alert('E.PEU.4: Some error occured. Reload the page.')
    }
}

async function loadAgePEU() {
    // const areaType = document.getElementById("peu-areatype").value;
    // const district = document.getElementById("peu-district").value;
    // const blockmunicipality= document.getElementById("peu-blockmunicipality").value;
    // const panchayatward = document.getElementById("peu-panchayatward").value;
    
    try  {
        //await fetchFilterOptionsPEU(base_url_filter_options+'/peu/age?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward, "peu-age");
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/age', "peu-age");
    }
    catch(error){
        alert('E.PEU.5: Some error occured. Reload the page.')
    }
}



async function loadGenderPEU() {
    // const areaType = document.getElementById("peu-areatype").value;
    // const district = document.getElementById("peu-district").value;
    // const blockmunicipality= document.getElementById("peu-blockmunicipality").value;
    // const panchayatward = document.getElementById("peu-panchayatward").value;
    // const age = document.getElementById("peu-age").value;
    // //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try{
        //await fetchFilterOptionsPEU(base_url_filter_options+'/peu/gender?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age, "peu-gender");
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/gender', "peu-gender");
    }
    catch(error) {
        alert('E.PEU.6: Some error occured. Reload the page.')
    }
}



async function loadEducationLevelPEU() {
    // const areaType = document.getElementById("peu-areatype").value;
    // const district = document.getElementById("peu-district").value;
    // const blockmunicipality= document.getElementById("peu-blockmunicipality").value;
    // const panchayatward = document.getElementById("peu-panchayatward").value;
    // const age = document.getElementById("peu-age").value;
    // const gender = document.getElementById("peu-gender").value;
    
    try{
        //await fetchFilterOptionsPEU(base_url_filter_options+'/peu/educationlevel?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender, "peu-educationlevel");
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/educationlevel', "peu-educationlevel");
    }
    catch(error){
        alert('E.PEU.7: Some error occured. Reload the page.')
    }
}


 


async function loadSectorOfInterestPEU() {
    // const areaType = document.getElementById("peu-areatype").value;
    // const district = document.getElementById("peu-district").value;
    // const blockmunicipality= document.getElementById("peu-blockmunicipality").value;
    // const panchayatward = document.getElementById("peu-panchayatward").value;
    // const age = document.getElementById("peu-age").value;
    // const gender = document.getElementById("peu-gender").value;
    // const educationlevel = document.getElementById("peu-educationlevel").value;
    


   try {
        //await fetchFilterOptionsPEU(base_url_filter_options+'/peu/sectorofinterest?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel, "peu-sectorofinterest");
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/sectorofinterest', "peu-sectorofinterest");
    }
    catch(error){
        alert('E.PEU.8: Some error occured. Reload the page.')
    }
}



async function loadExpectedScaleOfBusinessPEU() {
    // const areaType = document.getElementById("peu-areatype").value;
    // const district = document.getElementById("peu-district").value;
    // const blockmunicipality= document.getElementById("peu-blockmunicipality").value;
    // const panchayatward = document.getElementById("peu-panchayatward").value;
    // const age = document.getElementById("peu-age").value;
    // const gender = document.getElementById("peu-gender").value;
    // const educationlevel = document.getElementById("peu-educationlevel").value;
    // const sectorofinterest = document.getElementById("peu-sectorofinterest").value;
    
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

   try {
        //await fetchFilterOptionsPEU(base_url_filter_options+'/peu/expectedscaleofbusiness?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofinterest='+sectorofinterest, "peu-expectedscaleofbusiness");
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/expectedscaleofbusiness', "peu-expectedscaleofbusiness");
    }
    catch(error){
        alert('E.PEU.9: Some error occured. Reload the page.')
    }
}



async function loadAssistanceYuvaPEU() {
    // const areaType = document.getElementById("peu-areatype").value;
    // const district = document.getElementById("peu-district").value;
    // const blockmunicipality= document.getElementById("peu-blockmunicipality").value;
    // const panchayatward = document.getElementById("peu-panchayatward").value;
    // const age = document.getElementById("peu-age").value;
    // const gender = document.getElementById("peu-gender").value;
    // const educationlevel = document.getElementById("peu-educationlevel").value;
    // const sectorofinterest = document.getElementById("peu-sectorofinterest").value;
    // const expectedscaleofbusiness = document.getElementById("peu-expectedscaleofbusiness").value;
    

    try{
        //await fetchFilterOptionsPEU(base_url_filter_options+'/peu/assistancerequiredyuva?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofinterest='+sectorofinterest+'&expectedscaleofbusiness='+expectedscaleofbusiness, "peu-assistancerequiredforyuva");
        await fetchFilterOptionsPEU(base_url_filter_options+'/peu/assistancerequiredyuva', "peu-assistancerequiredforyuva");
    }
   catch(error) {
        alert('E.PEU.10: Some error occured. Reload the page.')
    }
}





/* FILTERS PORIUTION */

async function loadPEUFilters(x)
{
    resetPEUFilters(x);
    if (x==0)
        {
            if (document.getElementById('peu-areatype').value == "Urban"){
                document.getElementById('label-peu-blockmunicipality').innerHTML = 'Municipality';
                document.getElementById('label-peu-panchayatward').innerHTML = 'Ward';
            }
            else if (document.getElementById('peu-areatype').value == "Rural"){
                document.getElementById('label-peu-blockmunicipality').innerHTML = 'Block';
                document.getElementById('label-peu-panchayatward').innerHTML = 'Panchayat';
            }
            else{
                    document.getElementById('label-peu-blockmunicipality').innerHTML = 'Block/ Municipality';
                    document.getElementById('label-peu-panchayatward').innerHTML = 'Panchayat/ Ward';
                }
            await loadDistrictsPEU();
            // await loadBlockMunicipalityPEU();
            // await loadPanchayatWardPEU();
            // await loadAgePEU();
            // await loadGenderPEU();
            // await loadEducationLevelPEU();
            // await loadSectorOfInterestPEU();
            // await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();        
        }
    else if (x==1)
        {
            await loadBlockMunicipalityPEU();
            // await loadPanchayatWardPEU();
            // await loadAgePEU();
            // await loadGenderPEU();
            // await loadEducationLevelPEU();
            // await loadSectorOfInterestPEU();
            // await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();     
        }
    else if (x==2)
        {
            await loadPanchayatWardPEU();
            // await loadAgePEU();
            // await loadGenderPEU();
            // await loadEducationLevelPEU();
            // await loadSectorOfInterestPEU();
            // await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();     
        }
    else if (x==3)
        {
            //await loadAgePEU();
            // await loadGenderPEU();
            // await loadEducationLevelPEU();
            // await loadSectorOfInterestPEU();
            // await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();      
        }
    else if (x==4)
        {
            //await loadGenderPEU();
            // await loadEducationLevelPEU();
            // await loadSectorOfInterestPEU();
            // await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();     
        }
    else if (x==5)
        {
            //await loadEducationLevelPEU();
            // await loadSectorOfInterestPEU();
            // await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();
        }
    else if(x==6)
        {   
            //await loadSectorOfInterestPEU();
            // await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();
        }
    else if(x==7)
        {
            //await loadExpectedScaleOfBusinessPEU();
            // await loadAssistanceYuvaPEU();
        }
    else if(x==8)
        {
            //await loadAssistanceYuvaPEU();
            
        }
    else if(x==9)
        {
            
        }
    else{
            await loadAreaTypePEU();
            // await loadDistrictsPEU();
            // await loadBlockMunicipalityPEU();
            // await loadPanchayatWardPEU();
            await loadAgePEU();
            await loadGenderPEU();
            await loadEducationLevelPEU();
            await loadSectorOfInterestPEU();
            await loadExpectedScaleOfBusinessPEU();
            await loadAssistanceYuvaPEU();

    }

}





function enable_disable_dropdown_peu(dropdown, value=true)
{
    document.getElementById(dropdown).disabled = value;
    document.getElementById(dropdown).value="All";
}



function resetPEUFilters(currentDropdown)
{
    if (currentDropdown+1<peu_dropdowns.length){
    for (i=currentDropdown+1;i<peu_dropdowns.length;i++){
        enable_disable_dropdown_peu(peu_dropdowns[i], true);
    }
    enable_disable_dropdown_peu(peu_dropdowns[currentDropdown+1], false);
    }
    
}



async function loadPEUCharts(x)
{
    if(x==0){
        var params = "residentialtype=All&district=All&cdblockulbmc=All&panchayatward=All&age=All&gender=All&educationlevel=All&sectorofinterest=All&expectedscaleofbusiness=All&assistancerequiredforyuva=All";
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetPEU(base_url_charts+'/peu?'+params, 'peu');
        document.getElementById('loadingbar').style.display='none';
    }
    else{
        const areaType = document.getElementById("peu-areatype").value;
        const district = document.getElementById("peu-district").value;
        const blockmunicipality= document.getElementById("peu-blockmunicipality").value;
        const panchayatward = document.getElementById("peu-panchayatward").value;
        const age = document.getElementById("peu-age").value; 
        const gender = document.getElementById("peu-gender").value; 
        const educationlevel = document.getElementById("peu-educationlevel").value; 
        const sectorofinterest = document.getElementById("peu-sectorofinterest").value; 
        const expectedscaleofbusiness = document.getElementById("peu-expectedscaleofbusiness").value;
        const assistancerequiredforyuva = document.getElementById("peu-assistancerequiredforyuva").value;  
        
        var params = 'residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofinterest='+sectorofinterest+'&expectedscaleofbusiness='+expectedscaleofbusiness+'&assistancerequiredforyuva='+assistancerequiredforyuva;
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetPEU(base_url_charts+'/peu?'+params, 'peu');
        toggle_all_other_sections_peu();
        document.getElementById('loadingbar').style.display='none';
    }

    
}



async function loadChartSetPEU(url, type) {
    const data = await fetchChartsPEU(url);
    if (!data || !data[type]) return;

    const charts = data[type];
    const filtered_numbers = data['filtered_numbers'];
    await fetchGeneralNumbersFiltered(filtered_numbers);
    const mainContainer = document.getElementById('PEUChartsContainer');
    //mainContainer.style.gridTemplateColumns = `repeat(${getChartCount()}, 0.9fr)`;
    mainContainer.innerHTML = ''; // Clear previous charts
    

    var count = 0;
    charts.forEach((chart, index) => {
        
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container-highcharts';
        //chartContainer.style.flex = `1 0 calc(${100 / getChartCount()}% - 20px)`;
        //chartContainer.style.maxWidth = `calc(${100 / getChartCount()}% - 20px)`;

        const canvas = document.createElement('figure');
        canvas.id = `peu-chart-${index}`;
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



//loadPEUFilters(-1);
//loadPEUCharts(0);





function togglePEUCharts() {
    let toggleElement = document.getElementById("PEUToggle");
    let chartsElement = document.getElementById("peu_charts");

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






function toggle_all_other_sections_peu()
{
    var x = ['household_charts', 'ilp_charts', 'pee_charts', 'peur_charts']
    for(i=0; i < x.length;i++)
    {
        document.getElementById(x[i]+"_header").style.display='none';
        //console.log(x[i]);
        document.getElementById(x[i]).style.display='none';
    }
    document.getElementById("peu_charts_header").style.display='block';
    document.getElementById("peu_charts").style.display='block';

}
