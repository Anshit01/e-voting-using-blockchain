
function showUpdateModal() {
    $('#password').val('')
    $('#update-modal').modal()
}

function hideUpdateModal() {
    $('#update-modal').modal('hide')
    $("#password").val('')
}

function updateKey() {
    var voter_id = $('#voter-id').html()
    var password = $('#password').val()
    hideUpdateModal()
    $(window).bind('beforeunload', function() {return 'Please wait.'})
    $('#status-modal').modal({backdrop: 'static', keyboard: false})
    $.post('/api/update_key',
        {
            'voter_id': voter_id,
            'password': password
        },
        function(data) {
            if(data == ''){
                $('.info-text , .key').css('display', 'none')
                $('.error')
                .css('display', 'block')
                .html("Incorrect Password. Please try again.")
            }else{
                $('.info-text').css('display', 'block')
                $('.key')
                .css('display', 'block')
                .html(data)
                $('.error').css('display', 'none')
            }
            $('#status-modal').modal('hide')
            $('#success-modal').modal()
            $(window).unbind('beforeunload')
        }
    )
}

function hideSuccessModal() {
    $('#success-modal').modal('hide')
}