var name, party, candidate_id, imgSrc




function showConfirmModal(i) {
    var candidate_div = $("#candidate-div-" + i)
    name = candidate_div.children('.name').html()
    party = candidate_div.children('.party').html()
    candidate_id = candidate_div.children('.candidate-id').html()
    imgSrc = candidate_div.children('.img').attr('src')
    var confirmModal = $('#confirm-modal')
    $('#confirm-name').html(name)
    $('#confirm-party').html(party)
    $('#confirm-candidate-id').html(candidate_id)
    $('#confirm-ing').attr('src', imgSrc)
    confirmModal.modal()
}

function showKeyModal() {
    $('#confirm-modal').modal('hide')
    var keyModal = $('#key-modal')
    $('#key-name').html(name)
    $('#key-party').html(party)
    $('#key-candidate-id').html(candidate_id)
    $('#key-ing').attr('src', imgSrc)
    keyModal.modal({backdrop: 'static', keyboard: false})
}

function cancelConfirmModal() {
    $("#confirm-modal").modal('hide')
}

function cancelKeyModal() {
    $("#key-modal").modal('hide')
}

function castVote() {
    var voter_id = $('#voter_id').html()
    var key = $('#key').val()
    
}

