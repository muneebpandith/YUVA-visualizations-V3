


// ****** PEUR PART   *********//
const peur_dropdowns = ["peur-areatype", "peur-district", "peur-blockmunicipality", "peur-panchayatward"];
    
//"peur-age", "peur-gender", "peur-educationlevel", "peur-sectorofenterprise", "peur-natureofbusiness","peur-sourceofrawmaterial","peur-enterprisefinancialstatus","peur-currentmarketreach","peur-assistancerequiredforyuva" ]

var base_url_filter_options = '/api/v2/fetch_options';
var base_url_charts = '/api/v2/charts-filtered';

async function fetchFilterOptionsPEUR(url, targetDropdown) {
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

// Load districts based on selected area type




xx = []
async function fetchChartsPEUR(url) {
    var count = 0;
    try {
        const response = await fetch(url);
        const data = await response.json();
        xx = data;
        //await loadChartSet(data, 'household')

        //console.log(data);
        //dropdown.disabled = false; // Enable dropdown after data is loaded
        //xd = data;
        return data;
        


    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

async function loadAreaTypePEUR() {
    await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/residentialtype', "peur-areatype");
}


async function loadDistrictsPEUR() {
    const areaType = document.getElementById("peur-areatype").value;
    if (areaType) {
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/district?residentialtype='+areaType, "peur-district");
    }
    else{
        alert('E.PEUR.2: Some error occured. Reload the page.')
    }
}


async function loadBlockMunicipalityPEUR() {
    const areaType = document.getElementById("peur-areatype").value;
    const district = document.getElementById("peur-district").value;

    if (areaType  && district) {
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/cdblockulbmc?residentialtype='+areaType+'&district='+district, "peur-blockmunicipality");
    }
    else{
        alert('E.PEUR.3: Some error occured. Reload the page.')
    }
}



async function loadPanchayatWardPEUR()  {
    const areaType = document.getElementById("peur-areatype").value;
    const district = document.getElementById("peur-district").value;
    const blockmunicipality= document.getElementById("peur-blockmunicipality").value;

    if (areaType  && district && blockmunicipality) {
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/panchayatward?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality, "peur-panchayatward");
    }
    else{
        alert('E.PEUR.4: Some error occured. Reload the page.')
    }
}

async function loadAgePEUR() {
    //alert('Inside called function to find classes of age')
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    
    try {
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/age?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward, "peur-age");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/age', "peur-age");
    }
    catch(error){
        alert('E.PEUR.5: Some error occured. Reload the page.')
    }
}



async function loadGenderPEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try {
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/gender?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age, "peur-gender");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/gender', "peur-gender");
        
    }
    catch(error){
        alert('E.PEUR.6: Some error occured. Reload the page.')
    }
}



async function loadEducationLevelPEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // const gender = document.getElementById("peur-gender").value;
    
    try  {
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/educationlevel?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender, "peur-educationlevel");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/educationlevel', "peur-educationlevel");
    }
    catch (error) {
        alert('E.PEUR.7: Some error occured. Reload the page.')
    }
}


 


async function loadSectorOfEnterprisePEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // const gender = document.getElementById("peur-gender").value;
    // const educationlevel = document.getElementById("peur-educationlevel").value;
    
    
    //alert(' Education level' + educationlevel);

    try {
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/sectorofenterprise?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel, "peur-sectorofenterprise");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/sectorofenterprise', "peur-sectorofenterprise");
    }
    catch(error){
        alert('E.PEUR.8: Some error occured. Reload the page.')
    }
}




async function loadNatureOfBusinessPEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // const gender = document.getElementById("peur-gender").value;
    // const educationlevel = document.getElementById("peur-educationlevel").value;
    // const sectorofenterprise = document.getElementById("peur-sectorofenterprise").value;
    
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try {
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/natureofbusiness?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofenterprise='+sectorofenterprise, "peur-natureofbusiness");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/natureofbusiness', "peur-natureofbusiness");
    }
    catch (error) {
        alert('E.PEUR.9: Some error occured. Reload the page.')
    }
}


async function loadSourceOfRawMaterialPEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // const gender = document.getElementById("peur-gender").value;
    // const educationlevel = document.getElementById("peur-educationlevel").value;
    // const sectorofenterprise = document.getElementById("peur-sectorofenterprise").value;
    // const natureofbusiness = document.getElementById("peur-natureofbusiness").value;
    
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try {
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/sourceofrawmaterial?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofenterprise='+sectorofenterprise+'&natureofbusiness='+natureofbusiness, "peur-sourceofrawmaterial");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/sourceofrawmaterial', "peur-sourceofrawmaterial");
    
    }
    catch(error) {
        alert('E.PEUR.10: Some error occured. Reload the page.')
    }
}

async function loadEnterpriseFinancialStatusPEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // const gender = document.getElementById("peur-gender").value;
    // const educationlevel = document.getElementById("peur-educationlevel").value;
    // const sectorofenterprise = document.getElementById("peur-sectorofenterprise").value;
    // const natureofbusiness = document.getElementById("peur-natureofbusiness").value;
    // const sourceofrawmaterial = document.getElementById("peur-sourceofrawmaterial").value;
    
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try{
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/enterprisefinancialstatus?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofenterprise='+sectorofenterprise+'&natureofbusiness='+natureofbusiness+'&sourceofrawmaterial='+sourceofrawmaterial, "peur-enterprisefinancialstatus");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/enterprisefinancialstatus', "peur-enterprisefinancialstatus");
    }
    catch(error) {
        alert('E.PEUR.11: Some error occured. Reload the page.')
    }
}

async function loadCurrentMarketReachPEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // const gender = document.getElementById("peur-gender").value;
    // const educationlevel = document.getElementById("peur-educationlevel").value;
    // const sectorofenterprise = document.getElementById("peur-sectorofenterprise").value;
    // const natureofbusiness = document.getElementById("peur-natureofbusiness").value;
    // const sourceofrawmaterial = document.getElementById("peur-sourceofrawmaterial").value;
    // const enterprisefinancialstatus = document.getElementById("peur-enterprisefinancialstatus").value;
    
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try{
       //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/currentmarketreach?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofenterprise='+sectorofenterprise+'&natureofbusiness='+natureofbusiness+'&sourceofrawmaterial='+sourceofrawmaterial+'&enterprisefinancialstatus='+enterprisefinancialstatus, "peur-currentmarketreach");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/currentmarketreach', "peur-currentmarketreach");
    }
    catch(error) {
        alert('E.PEUR.12: Some error occured. Reload the page.')
    }
}


async function loadAssistanceYuvaPEUR() {
    // const areaType = document.getElementById("peur-areatype").value;
    // const district = document.getElementById("peur-district").value;
    // const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
    // const panchayatward = document.getElementById("peur-panchayatward").value;
    // const age = document.getElementById("peur-age").value;
    // const gender = document.getElementById("peur-gender").value;
    // const educationlevel = document.getElementById("peur-educationlevel").value;
    // const sectorofenterprise = document.getElementById("peur-sectorofenterprise").value;
    // const natureofbusiness = document.getElementById("peur-natureofbusiness").value;
    // const sourceofrawmaterial = document.getElementById("peur-sourceofrawmaterial").value;
    // const enterprisefinancialstatus = document.getElementById("peur-enterprisefinancialstatus").value;
    // const currentmarketreach = document.getElementById("peur-currentmarketreach").value;
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try  {
        //await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/assistancerequiredyuva?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofenterprise='+sectorofenterprise+'&natureofbusiness='+natureofbusiness+'&sourceofrawmaterial='+sourceofrawmaterial+'&enterprisefinancialstatus='+enterprisefinancialstatus+'&currentmarketreach='+currentmarketreach, "peur-assistancerequiredforyuva");
        await fetchFilterOptionsPEUR(base_url_filter_options+'/peur/assistancerequiredyuva', "peur-assistancerequiredforyuva");
    }
    catch(error) {
        alert('E.PEUR.13: Some error occured. Reload the page.')
    }
}





/* FILTERS PORIUTION */



async function loadPEURFilters(x)
{
    resetPEURFilters(x);
    if (x==0)
        {
            if (document.getElementById('peur-areatype').value == "Urban"){
                document.getElementById('label-peur-blockmunicipality').innerHTML = 'Municipality';
                document.getElementById('label-peur-panchayatward').innerHTML = 'Ward';
            }
            else if (document.getElementById('peur-areatype').value == "Rural"){
                document.getElementById('label-peur-blockmunicipality').innerHTML = 'Block';
                document.getElementById('label-peur-panchayatward').innerHTML = 'Panchayat';
            }
            else{
                    document.getElementById('label-peur-blockmunicipality').innerHTML = 'Block/ Municipality';
                    document.getElementById('label-peur-panchayatward').innerHTML = 'Panchayat/ Ward';
                }
            await loadDistrictsPEUR();
            // await loadBlockMunicipalityPEUR();
            // await loadPanchayatWardPEUR();
            // await loadAgePEUR();
            // await loadGenderPEUR();
            // await loadEducationLevelPEUR();
            // await loadSectorOfEnterprisePEUR();
            // await loadNatureOfBusinessPEUR();
            // await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR();        
        }
    else if (x==1)
        {
            await loadBlockMunicipalityPEUR();
            // await loadPanchayatWardPEUR();
            // await loadAgePEUR();
            // await loadGenderPEUR();
            // await loadEducationLevelPEUR();
            // await loadSectorOfEnterprisePEUR();
            // await loadNatureOfBusinessPEUR();
            // await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if (x==2)
        {
            await loadPanchayatWardPEUR();
            // await loadAgePEUR();
            // await loadGenderPEUR();
            // await loadEducationLevelPEUR();
            // await loadSectorOfEnterprisePEUR();
            // await loadNatureOfBusinessPEUR();
            // await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if (x==3)
        {
            //alert('Calling to find classes of age');
            //await loadAgePEUR();
            // await loadGenderPEUR();
            // await loadEducationLevelPEUR();
            // await loadSectorOfEnterprisePEUR();
            // await loadNatureOfBusinessPEUR();
            // await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if (x==4)
        {
            //await loadGenderPEUR();
            // await loadEducationLevelPEUR();
            // await loadSectorOfEnterprisePEUR();
            // await loadNatureOfBusinessPEUR();
            // await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if (x==5)
        {
            //await loadEducationLevelPEUR();
            // await loadSectorOfEnterprisePEUR();
            // await loadNatureOfBusinessPEUR();
            // await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if(x==6)
        {   
            //await loadSectorOfEnterprisePEUR();
            // await loadNatureOfBusinessPEUR();
            // await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if(x==7)
        {
            //await loadNatureOfBusinessPEUR();
        //     await loadSourceOfRawMaterialPEUR();
        //     await loadEnterpriseFinancialStatusPEUR();
        //     await loadCurrentMarketReachPEUR();
        //     await loadAssistanceYuvaPEUR(); 
        }
    else if(x==8)
        {
            //await loadSourceOfRawMaterialPEUR();
            // await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
            
        }
    else if(x==9)
        {
            //await loadEnterpriseFinancialStatusPEUR();
            // await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if(x==10)
        {
            //await loadCurrentMarketReachPEUR();
            // await loadAssistanceYuvaPEUR(); 
        }
    else if(x==11)
        {
            //await loadAssistanceYuvaPEUR(); 
        }
    else if(x==12)
            {
                //await loadAssistanceYuvaPEUR(); 
            }
   
    else if(x==13)
        {

        }
    else{
            await loadAreaTypePEUR();
            // await loadDistrictsPEUR();
            // await loadBlockMunicipalityPEUR();
            // await loadPanchayatWardPEUR();
            await loadAgePEUR();
            await loadGenderPEUR();
            await loadEducationLevelPEUR();
            await loadSectorOfEnterprisePEUR();
            await loadNatureOfBusinessPEUR();
            await loadSourceOfRawMaterialPEUR();
            await loadEnterpriseFinancialStatusPEUR();
            await loadCurrentMarketReachPEUR();
            await loadAssistanceYuvaPEUR(); 

    }

}


function enable_disable_dropdown_peur(dropdown, value=true)
{
    document.getElementById(dropdown).disabled = value;
    document.getElementById(dropdown).value="All";
}

function resetPEURFilters(currentDropdown)
{
    if (currentDropdown+1<peur_dropdowns.length){
    for (i=currentDropdown+1;i<peur_dropdowns.length;i++){
        enable_disable_dropdown_peur(peur_dropdowns[i], true);
    }
    enable_disable_dropdown_peur(peur_dropdowns[currentDropdown+1], false);
    }
    
}



async function loadPEURCharts(x)
{
    if(x==0){
        var params = "residentialtype=All&district=All&cdblockulbmc=All&panchayatward=All&age=All&gender=All&educationlevel=All&sectorofenterprise=All&natureofbusiness=All&sourceofrawmaterial=All&enterprisefinancialstatus=All&currentmarketreach=All&assistancerequiredforyuva=All";
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetPEUR(base_url_charts+'/peur?'+params, 'peur');
        document.getElementById('loadingbar').style.display='none';
    }
    else{
        const areaType = document.getElementById("peur-areatype").value;
        const district = document.getElementById("peur-district").value;
        const blockmunicipality= document.getElementById("peur-blockmunicipality").value;
        const panchayatward = document.getElementById("peur-panchayatward").value;
        const age = document.getElementById("peur-age").value;
        const gender = document.getElementById("peur-gender").value;
        const educationlevel = document.getElementById("peur-educationlevel").value;
        const sectorofenterprise = document.getElementById("peur-sectorofenterprise").value;
        const natureofbusiness = document.getElementById("peur-natureofbusiness").value;
        const sourceofrawmaterial = encodeURIComponent(document.getElementById("peur-sourceofrawmaterial").value);
        //alert(sourceofrawmaterial);
        const enterprisefinancialstatus = document.getElementById("peur-enterprisefinancialstatus").value;
        const currentmarketreach = encodeURIComponent(document.getElementById("peur-currentmarketreach").value); 
        //const expectedscaleofbusiness = document.getElementById("peur-expectedscaleofbusiness").value;
        const assistancerequiredforyuva = document.getElementById("peur-assistancerequiredforyuva").value;  
        
        var params = 'residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&sectorofenterprise='+sectorofenterprise+'&natureofbusiness='+natureofbusiness+'&sourceofrawmaterial='+sourceofrawmaterial+'&enterprisefinancialstatus='+enterprisefinancialstatus+'&currentmarketreach='+currentmarketreach+'&assistancerequiredforyuva='+assistancerequiredforyuva;
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetPEUR(base_url_charts+'/peur?'+params, 'peur');
        toggle_all_other_sections_peur();
        document.getElementById('loadingbar').style.display='none';
    }

    
}


async function loadChartSetPEUR(url, type) {
    const data = await fetchChartsPEUR(url);
    if (!data || !data[type]) return;

    const charts = data[type];
    const filtered_numbers = data['filtered_numbers'];
    await fetchGeneralNumbersFiltered(filtered_numbers);
    const mainContainer = document.getElementById('PEURChartsContainer');
    
    //mainContainer.style.gridTemplateColumns = `repeat(${getChartCount()}, 0.9fr)`;
    mainContainer.innerHTML = ''; // Clear previous charts
    var count = 0;
    charts.forEach((chart, index) => {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container-highcharts';
        //chartContainer.style.flex = `1 0 calc(${100 / getChartCount()}% - 20px)`;
        //chartContainer.style.maxWidth = `calc(${100 / getChartCount()}% - 20px)`;
        const canvas = document.createElement('figure');
        canvas.id = `peur-chart-${index}`;
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
                generatePieChart(canvas, chart);   //defined in loadchartsjs.js
            }
        else if(chart.type=='column')
            {
                generateColumnChart(canvas, chart);   //defined in loadchartsjs.js
            }
        else{}
    });
}


//loadPEURFilters(-1);
//loadPEURCharts(0);




function togglePEURCharts() {
    let toggleElement = document.getElementById("PEURToggle");
    let chartsElement = document.getElementById("peur_charts");

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



function toggle_all_other_sections_peur()
{
    var x = ['household_charts', 'ilp_charts', 'pee_charts', 'peu_charts']
    for(i=0; i < x.length;i++)
    {
        document.getElementById(x[i]+"_header").style.display='none';
        //console.log(x[i]);
        document.getElementById(x[i]).style.display='none';
    }
    document.getElementById("peur_charts_header").style.display='block';
    document.getElementById("peur_charts").style.display='block';

}
