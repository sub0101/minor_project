

// $(document).on("click", ".modal", function () {
  
//     console.log('fdsfsdfs')

//     $('#area_of_law').on('click', function (e) {
    
// });

var select = document.getElementById("area_of_law");
       
laws = ['Criminal Law', 'Corruption Law', 'Environment Law', 'Education Law', 'Financial Law', 'Healthcare Law', 'Personal Law', 'Labour Law', 'Social Law', 'Property Law', 'Cyber Crime Law', 'Civil Law']


for (var i = 0; i < laws.length; i++) {

    var optn = laws[i];
    var el = document.createElement("option");
    el.textContent = optn;
    el.value = optn;
    select.appendChild(el);
}

