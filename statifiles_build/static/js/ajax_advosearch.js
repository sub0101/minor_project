// $('#filter_law').on('change', function (e) {
//     e.preventDefault();
//     var csrf = document.getElementsByName('csrfmiddlewaretoken')


//     var filter_law = document.getElementById('filter_law')
//    console.log(filter_law.value)
//     $.ajax({

//         type: 'POST',
//         url: 'advo_search',

//         data: {

//             'csrfmiddlewaretoken': csrf[0].value,


//         },
//         success: function (data) {
//             var obj = []
//             obj = data.msg

//             console.log('sffdfdf')
//             console.log(data.msg)
//             var msg = JSON.parse(data.msg)
//            field = msg[0]['fields']
//            console.log(field['name'])
//             console.log(msg)
//             console.log(field['name'])
//             $('#filter_law').val("")
//         },
//     });
// });