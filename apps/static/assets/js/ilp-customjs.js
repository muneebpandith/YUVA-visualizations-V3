


// ****** ILP PART   *********//
const ilp_dropdowns = ["ilp-areatype", "ilp-district", "ilp-blockmunicipality", "ilp-panchayatward"]
//"ilp-age", "ilp-gender", "ilp-educationlevel", "ilp-employmentstatus", "ilp-annualincome" 

var base_url_filter_options = '/api/v2/fetch_options';
var base_url_charts = '/api/v2/charts-filtered';

async function fetchFilterOptionsIlp(url, targetDropdown) {
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


async function fetchChartsIlp(url) {
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

async function loadAreaTypeIlp() {
    
    await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/residentialtype', "ilp-areatype");
    
}


async function loadDistrictsIlp() {
    const areaType = document.getElementById("ilp-areatype").value;
    if (areaType) {
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/district?residentialtype='+areaType, "ilp-district");
    }
    else{
        alert('E.ILP.2: Some error occured. Reload the page.')
    }
}


async function loadBlockMunicipalityIlp() {
    const areaType = document.getElementById("ilp-areatype").value;
    const district = document.getElementById("ilp-district").value;

    if (areaType  && district) {
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/cdblockulbmc?residentialtype='+areaType+'&district='+district, "ilp-blockmunicipality");
    }
    else{
        alert('E.ILP.3: Some error occured. Reload the page.')
    }
}



async function loadPanchayatWardIlp()  {
    const areaType = document.getElementById("ilp-areatype").value;
    const district = document.getElementById("ilp-district").value;
    const blockmunicipality= document.getElementById("ilp-blockmunicipality").value;

    if (areaType  && district && blockmunicipality) {
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/panchayatward?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality, "ilp-panchayatward");
    }
    else{
        alert('E.ILP.4: Some error occured. Reload the page.')
    }
}

async function loadAgeIlp() {
    // const areaType = document.getElementById("ilp-areatype").value;
    // const district = document.getElementById("ilp-district").value;
    // const blockmunicipality= document.getElementById("ilp-blockmunicipality").value;
    // const panchayatward = document.getElementById("ilp-panchayatward").value;
    
    try {
        //await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/age?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward, "ilp-age");
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/age',  "ilp-age");
    }
    catch (error){
        alert('E.ILP.5: Some error occured. Reload the page.')
    }
}



async function loadGenderIlp() {
    // const areaType = document.getElementById("ilp-areatype").value;
    // const district = document.getElementById("ilp-district").value;
    // const blockmunicipality= document.getElementById("ilp-blockmunicipality").value;
    // const panchayatward = document.getElementById("ilp-panchayatward").value;
    // const age = document.getElementById("ilp-age").value;
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try {
        //await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/gender?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age, "ilp-gender");
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/gender', "ilp-gender");
    }
    catch(error){
        alert('E.ILP.6: Some error occured. Reload the page.')
    }
}



async function loadEducationLevelIlp() {
    // const areaType = document.getElementById("ilp-areatype").value;
    // const district = document.getElementById("ilp-district").value;
    // const blockmunicipality= document.getElementById("ilp-blockmunicipality").value;
    // const panchayatward = document.getElementById("ilp-panchayatward").value;
    // const age = document.getElementById("ilp-age").value;
    // const gender = document.getElementById("ilp-gender").value;
    
    try{
        //await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/educationlevel?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender, "ilp-educationlevel");
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/educationlevel', "ilp-educationlevel");
    }
    catch(error){
        alert('E.ILP.7: Some error occured. Reload the page.')
    }
}



async function loadEmploymentStatusIlp() {
    // const areaType = document.getElementById("ilp-areatype").value;
    // const district = document.getElementById("ilp-district").value;
    // const blockmunicipality= document.getElementById("ilp-blockmunicipality").value;
    // const panchayatward = document.getElementById("ilp-panchayatward").value;
    // const age = document.getElementById("ilp-age").value;
    // const gender = document.getElementById("ilp-gender").value;
    // const educationlevel = document.getElementById("ilp-educationlevel").value;
    
    
    //alert(' Education level' + educationlevel);

   try {
        //await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/employmentstatus?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel, "ilp-employmentstatus");
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/employmentstatus', "ilp-employmentstatus");
    }
    catch(error){
        alert('E.ILP.8: Some error occured. Reload the page.')
    }
}

async function loadAnnualIncomeIlp() {
    // const areaType = document.getElementById("ilp-areatype").value;
    // const district = document.getElementById("ilp-district").value;
    // const blockmunicipality= document.getElementById("ilp-blockmunicipality").value;
    // const panchayatward = document.getElementById("ilp-panchayatward").value;
    // const age = document.getElementById("ilp-age").value;
    // const gender = document.getElementById("ilp-gender").value;
    // const educationlevel = document.getElementById("ilp-educationlevel").value;
    // const employmentstatus = document.getElementById("ilp-employmentstatus").value;
    
    //alert(areaType + ', ' + district + ', '+ blockmunicipality +' '+ panchayatward);

    try {
        //await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/annualincome?residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&employmentstatus='+employmentstatus, "ilp-annualincome");
        await fetchFilterOptionsIlp(base_url_filter_options+'/individual_member/annualincome', "ilp-annualincome");
    }
    catch (error){
        alert('E.ILP.9: Some error occured. Reload the page.')
    }
}



async function loadIlpFilters(x)
{
    resetIlpFilters(x);
    if (x==0)
        {
            if (document.getElementById('ilp-areatype').value == "Urban"){
                document.getElementById('label-ilp-blockmunicipality').innerHTML = 'Municipality';
                document.getElementById('label-ilp-panchayatward').innerHTML = 'Ward';
            }
            else if (document.getElementById('ilp-areatype').value == "Rural"){
                document.getElementById('label-ilp-blockmunicipality').innerHTML = 'Block';
                document.getElementById('label-ilp-panchayatward').innerHTML = 'Panchayat';
            }
            else{
                    document.getElementById('label-ilp-blockmunicipality').innerHTML = 'Block/ Municipality';
                    document.getElementById('label-ilp-panchayatward').innerHTML = 'Panchayat/ Ward';
            }

            await loadDistrictsIlp();
            // await loadBlockMunicipalityIlp();
            // await loadPanchayatWardIlp();
            // await loadAgeIlp();
            // await loadGenderIlp();
            // await loadEducationLevelIlp();
            // await loadEmploymentStatusIlp();
            // await loadAnnualIncomeIlp();
        }
    else if (x==1)
        {
            await loadBlockMunicipalityIlp();
            // await loadPanchayatWardIlp();
            // await loadAgeIlp();
            // await loadGenderIlp();
            // await loadEducationLevelIlp();
            // await loadEmploymentStatusIlp();
            // await loadAnnualIncomeIlp();
        }
    else if (x==2)
        {
            await loadPanchayatWardIlp();
            // await loadAgeIlp();
            // await loadGenderIlp();
            // await loadEducationLevelIlp();
            // await loadEmploymentStatusIlp();
            // await loadAnnualIncomeIlp();
        }
    else if (x==3)
        {
            //await loadAgeIlp();
            // await loadGenderIlp();
            // await loadEducationLevelIlp();
            // await loadEmploymentStatusIlp();
            // await loadAnnualIncomeIlp();
        }
    else if (x==4)
        {
            /// await loadGenderIlp();
            // await loadEducationLevelIlp();
            // await loadEmploymentStatusIlp();
            // await loadAnnualIncomeIlp();
        }
    else if (x==5)
        {
            ///await loadEducationLevelIlp();
            // await loadEmploymentStatusIlp();
            // await loadAnnualIncomeIlp();
        }
    else if(x==6)
        {   
            /// await loadEmploymentStatusIlp();
            // await loadAnnualIncomeIlp();
        }
    else if(x==7)
        {
           /// await loadAnnualIncomeIlp(); 
        }
    else if(x==8)
        {
            
        }
    else{
            await loadAreaTypeIlp();
            // await loadDistrictsIlp();
            // await loadBlockMunicipalityIlp();
            // await loadPanchayatWardIlp();
            await loadAgeIlp();
            await loadGenderIlp();
            await loadEducationLevelIlp();
            await loadEmploymentStatusIlp();
            await loadAnnualIncomeIlp();
    }
}

function enable_disable_dropdown_ilp(dropdown, value=true)
{
    document.getElementById(dropdown).disabled = value;
    document.getElementById(dropdown).value="All";
}



function resetIlpFilters(currentDropdown)
{
    if (currentDropdown+1<ilp_dropdowns.length){
    for (i=currentDropdown+1;i<ilp_dropdowns.length;i++){
        enable_disable_dropdown_ilp(ilp_dropdowns[i], true);
    }
    enable_disable_dropdown_ilp(ilp_dropdowns[currentDropdown+1], false);
    }
    
}



async function loadIlpCharts(x)
{
    if(x==0){
        //http://127.0.0.1:8080/api/v2/charts-filtered/individual_member?residentialtype=All&district=All&cdblockulbmc=All&panchayatward=All&age=All&gender=All&educationlevel=All&employmentstatus=All
        var params = "residentialtype=All&district=All&cdblockulbmc=All&panchayatward=All&age=All&gender=All&educationlevel=All&employmentstatus=All&annualincome=All";
        await loadChartSetIlp(base_url_charts+'/individual_member?'+params, 'ilp');
    }
    else{
        const areaType = document.getElementById("ilp-areatype").value;
        const district = document.getElementById("ilp-district").value;
        const blockmunicipality= document.getElementById("ilp-blockmunicipality").value;
        const panchayatward = document.getElementById("ilp-panchayatward").value;
        const age = document.getElementById("ilp-age").value; 
        const gender = document.getElementById("ilp-gender").value; 
        const educationlevel = document.getElementById("ilp-educationlevel").value; 
        const employmentstatus = document.getElementById("ilp-employmentstatus").value; 
        const annualincome = document.getElementById("ilp-annualincome").value; 
        
        var params = 'residentialtype='+areaType+'&district='+district+'&cdblockulbmc='+blockmunicipality+'&panchayatward='+panchayatward+'&age='+age+'&gender='+gender+'&educationlevel='+educationlevel+'&employmentstatus='+employmentstatus+'&annualincome='+annualincome;
        document.getElementById('loadingbar').style.display='flex';
        await loadChartSetIlp(base_url_charts+'/individual_member?'+params, 'ilp');
        toggle_all_other_sections_ilp();
        document.getElementById('loadingbar').style.display='none';

    }    
}


async function loadChartSetIlp(url, type) {
    const data = await fetchChartsIlp(url);
    if (!data || !data[type]) return;

    const charts = data[type];
    const filtered_numbers = data['filtered_numbers'];
    await fetchGeneralNumbersFiltered(filtered_numbers);
    const mainContainer = document.getElementById('IlpChartsContainer');
    //mainContainer.style.gridTemplateColumns = `repeat(${getChartCount()}, 0.9fr)`;
    mainContainer.innerHTML = ''; // Clear previous charts
    

    var count = 0;
    charts.forEach((chart, index) => {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container-highcharts';
        //chartContainer.style.flex = `1 0 calc(${100 / getChartCount()}% - 20px)`;
        //chartContainer.style.maxWidth = `calc(${100 / getChartCount()}% - 20px)`;
        const canvas = document.createElement('figure');
        canvas.id = `ilp-chart-${index}`;
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



//loadIlpFilters(-1);
//loadIlpCharts(0);








function toggleIlpCharts() {
    let toggleElement = document.getElementById("ILPToggle");
    let chartsElement = document.getElementById("ilp_charts");

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






function toggle_all_other_sections_ilp()
{
    var x = ['household_charts', 'peur_charts', 'pee_charts', 'peu_charts']
    for(i=0; i < x.length;i++)
    {
        document.getElementById(x[i]+"_header").style.display='none';
        //console.log(x[i]);
        document.getElementById(x[i]).style.display='none';
    }
    document.getElementById("ilp_charts_header").style.display='block';
    document.getElementById("ilp_charts").style.display='block';

}
