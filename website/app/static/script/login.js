function validate() {
    name = $('#name').val()
    voter_id = $('#voter_id').val()
    password = $('#password').val()
    warning = $('#warning')
    if(name == '' || voter_id == '' || password == ''){
        warning.html("Please fill all the fields")
        glowWarning()
        return false
    }
    var voter_id_regex = /^[1-9]{1}[0-9]{11}$/
    if(voter_id_regex.test(voter_id)){
        return true
    }
    warning.html("Invalid Voter ID")
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