const form = document.querySelector('.professional_form')
form.addEventListener('submit', e => {

})

function func(temp, id) {
    var csrf = document.getElementsByName('csrfmiddlewaretoken')


    var value = document.getElementById(temp).value
    console

    $.ajax({

        type: 'POST',
        url: '/edit_profile/1/',

        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'value': value,
            'check': temp

        },

        success: function(data) {

            $('#' + temp).val("")

            $(id).val(function() {
                return this.value + "  " + data.msg;
            });
        },

    });
    return
}
$('#add_courts').on('change', function(e) {
    e.preventDefault();
    console.log('a')

    temp = 'add_courts'
    id = '#id_visiting_courts'
    func(temp, id)
});
$('#add_law').on('change', function(e) {
    e.preventDefault();

    temp = 'add_law'
    id = '#id_area_of_law'
    func(temp, id)
});
$('#add_cities').on('change', function(e) {
    e.preventDefault();

    temp = 'add_cities'
    id = '#id_service_cities'
    func(temp, id)
});

// $('#delete').on('click', function (e) {
//     e.preventDefault();
//     value = document.getElementById('delete')
//     $.ajax({
//         type: 'POST',
//         url: '/edit_profile/1/',

//             data: {
//                 'csrfmiddlewaretoken': csrf[0].value,
//                 'delete': value

//             },

//         success: function (data) {

//             $('#'+temp).val("")

//             $(id).val(function() {
//                 return this.value + "  "+ data.msg;
//             });
//         },

//     });
// });