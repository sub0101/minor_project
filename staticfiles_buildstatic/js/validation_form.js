function validateForm() {

    var valid=true
    var name =  document.getElementById('name').value;
    if (name == "") {
            
        document.getElementById('name').style.borderBottomColor="red";
        
        valid=false;
    }
    var email =  document.getElementById('email').value;
    if (email == "") {
       
        document.getElementById('email').style.borderBottomColor="red";
       valid=false;
    } else {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(!re.test(email)){
            document.getElementById('email').style.borderBottomColor="red";
          
            document.querySelector('.status').innerHTML = "Email format invalid";
           valid=false;
        }
    }
    var city =  document.getElementById('mobile').value;
    if (city == "") {
        document.getElementById('city').style.borderBottomColor="red";
        document.querySelector('.status').innerHTML = "city cannot be empty";
     
    }
    var mobile =  document.getElementById('mobile').value;
    if (mobile == "") {
        document.getElementById('mobile').style.borderBottomColor="red";
        document.querySelector('.status').innerHTML = "mobile cannot be empty";
     
    }
    var password1 =  document.getElementById('password1').value;
    if (password1 == "") {
        document.getElementById('password1').style.borderBottomColor="red";
        document.querySelector('.status').innerHTML = "password cannot be empty";
     
    }
    var password2 =  document.getElementById('password2').value;
    if (password2 == "") {
        document.getElementById('password2').style.borderBottomColor="red";
        document.querySelector('.status').innerHTML = "password cannot be empty";
       
    }
    if(password1 != password2)
    {
        document.querySelector('.status').innerHTML = " password does not match ";
    }
    if(valid == false)
    {
        return false;
    }
    document.querySelector('.status').innerHTML = "Sending...";
    document.getElementById('signup-form').submit();
  }