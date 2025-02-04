function loaddefaultmapJK()
{
    document.querySelectorAll("#JKmapMain path").forEach(path => {
        path.addEventListener("click", function(event) {
        event.preventDefault(); 
        //alert("Path ID: " + this.id);
        if(district_wise_details){

            box = document.getElementById("map-hover-box")
            
            
            box.innerHTML = "<div align=center style='color: #addaff;font-size: 14px;'><b style='text-align:center;'>"+this.id+"</b></div>"+ "<hr style='margin:2px;'>Households : <b>"+district_wise_details.number[this.id].households+"</b><br>Members : <b>"+district_wise_details.number[this.id].individual_members+"</b><br>PEUR : <b>"+district_wise_details.number[this.id].peur+"</b><br>PEE : <b>"+district_wise_details.number[this.id].pee+"</b><br>PEU : <b>"+district_wise_details.number[this.id].peu+"</b>";
            box.style.display='block';
            box.style.left = event.clientX - 200 + "px";
            box.style.top = event.clientY -100+ "px";
        }
        
        });
    });

}

loaddefaultmapJK();