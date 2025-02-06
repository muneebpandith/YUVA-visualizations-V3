var base_url_general_elements = '/api/v2/fetch_numbers';

async function fetchGeneralNumbers(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        document.getElementById("hoh-number-total-1").innerHTML = data.hoh.number.toLocaleString('en-IN');
        document.getElementById("hoh-number-total-2").innerHTML = data.hoh.number.toLocaleString('en-IN');
        document.getElementById("individual-members-total-1").innerHTML = data.individual_members.number.toLocaleString('en-IN');
        document.getElementById("individual-members-total-2").innerHTML = data.individual_members.number.toLocaleString('en-IN');
        document.getElementById("peur-number-total-1").innerHTML = data.peur.number.toLocaleString('en-IN');
        document.getElementById("peur-number-total-2").innerHTML = data.peur.number.toLocaleString('en-IN');
        document.getElementById("pee-number-total-1").innerHTML = data.pee.number.toLocaleString('en-IN');
        document.getElementById("pee-number-total-2").innerHTML = data.pee.number.toLocaleString('en-IN');
        document.getElementById("peu-number-total-1").innerHTML = data.peu.number.toLocaleString('en-IN');
        document.getElementById("peu-number-total-2").innerHTML = data.peu.number.toLocaleString('en-IN');

        return data.district_wise_details;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}





async function fetchGeneralNumbersFiltered(data, t="") {
    try {

        if(t=="household"){
            document.getElementById("individualmembersheader-1").innerHTML = "Number of Heads of households<br>&nbsp;";
            document.getElementById("individualmembersheader-2").innerHTML = "Number of Heads of households<br>&nbsp;"
        }
        else{
            document.getElementById("individualmembersheader-1").innerHTML = "Individual Members<br>&nbsp;";
            document.getElementById("individualmembersheader-2").innerHTML = "Individual Members<br>&nbsp;";
        }
        document.getElementById("hoh-number-total-1").innerHTML = data.hoh.number.toLocaleString('en-IN');
        document.getElementById("hoh-number-total-2").innerHTML = data.hoh.number.toLocaleString('en-IN');
        document.getElementById("individual-members-total-1").innerHTML = data.individual_members.number.toLocaleString('en-IN');
        document.getElementById("individual-members-total-2").innerHTML = data.individual_members.number.toLocaleString('en-IN');
        document.getElementById("peur-number-total-1").innerHTML = data.peur.number.toLocaleString('en-IN');
        document.getElementById("peur-number-total-2").innerHTML = data.peur.number.toLocaleString('en-IN');
        document.getElementById("pee-number-total-1").innerHTML = data.pee.number.toLocaleString('en-IN');
        document.getElementById("pee-number-total-2").innerHTML = data.pee.number.toLocaleString('en-IN');
        document.getElementById("peu-number-total-1").innerHTML = data.peu.number.toLocaleString('en-IN');
        document.getElementById("peu-number-total-2").innerHTML = data.peu.number.toLocaleString('en-IN');
        //console.log(data.hoh.number.toLocaleString('en-IN'));
        //console.log(data.district_wise_details);
        district_wise_details= data.district_wise_details;
        //console.log(district_wise_details);

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}


async function loadGeneralElements() {    
    district_wise_details = await fetchGeneralNumbers(base_url_general_elements);
    //console.log(district_wise_details.number);
    //return district_wise_details.number;
}

var district_wise_details;
loadGeneralElements();



