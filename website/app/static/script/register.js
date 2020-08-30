function validate() {
    var name = $('#name').val()
    var dob = $('#dob').val()
    var aadhar_id = $('#aadhar-id').val()
    var email = $('#email').val()
    var contact_no = $('#contact-no').val()
    var password = $('#password').val()
    var password_confirm = $('#password-confirm').val()
    var warning = $('#warning')

    if(name == '' || dob == '' || aadhar_id == '' || email == '' || contact_no == '' || password == '' || password_confirm == ''){
        warning.html('All fields are required.')
        // document.getElementById('warning').scrollIntoView()
        // $('html, body').animate({scrollTop: warning.offset().top}, 'slow');
        glowWarning()
        return false
    }
    var regex_name = /[a-zA-Z]/
    var regex_aadhar_id = /^[1-9]{1}[0-9]{11}$/
    var regex_email = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    var regex_contact_no = /^[1-9]{1}[0-9]{9}$/

    var msg = ''
    if(regex_name.test(name) == false){
        msg = 'Invalid name'
    }else if(isNaN(new Date(dob).getDate())){
        msg = 'Invalid date'
    }
    else if(regex_aadhar_id.test(aadhar_id) == false){
        msg = 'Invalid Aadhar ID'
    }else if(regex_email.test(email) == false){
        msg = 'Invalid email ID'
    }else if(regex_contact_no.test(contact_no) == false){
        msg = 'Invalid contact number'
    }else if(password != password_confirm){
        msg = 'Passwords does not match'
    }else{
        return true
    }
    warning.html(msg)
    // document.getElementById('warning').scrollIntoView()
    glowWarning()
    return false
}

function glowWarning() {
    var warning = $('#warning')
    warning.css(
        'text-shadow',
        '0 0 50px red, 0 0 20px red, 0 0 10px red')
    setTimeout(function() {
        warning.css('text-shadow', 'none')
    }, 300)
}