window.addEventListener('load', function() {
    var images = $('.modal-img')
    for(image of images){
        if(!image.complete || image.naturalHeight === 0){
            image.setAttribute('src', 'static/images/party_logo/Independent.png')
        }
    }
})