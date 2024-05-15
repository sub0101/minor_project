

$('.login_input').blur(function()
{
    
    
  var  input_email  = document.getElementById('login_email').value;
  var  input_password1 = document.getElementById('login_password').value;
 
    if(input_email != ""  )
    {
        
        $('#login_email_label').addClass('form-label')
        
    }
    else
    {
        $('#login_email_label').removeClass('form-label')
       
        
    }
 
    if(input_password1 != ""  )
    {
     
        $('#login_password_label').addClass('form-label')
    }
    else
    {
        $('#login_password_label').removeClass('form-label')
    }

})

