var rate_value = 0
var post_value = 0


const one = document.getElementById('first')
const two = document.getElementById('second')

const three = document.getElementById('third')
const four = document.getElementById('fourth')
const five = document.getElementById('fifth')

const form = document.querySelector('.rate-form')

const confirBox = document.getElementById('confirm-box')
var csrf = document.getElementsByName('csrfmiddlewaretoken')




const handleStarSelect = (size) => {

    const children = form.children
    for (let i = 0; i < children.length; i++) {
        if (i <= size) {
            children[i].classList.add('checked')
        } else {
            children[i].classList.remove('checked')
        }
    }
}


const handleSelect = (selection) => {

    switch (selection) {
        case 'first':
            {

                handleStarSelect(1)
                return
            }
        case 'second':
            {

                handleStarSelect(2)
                return
            }
        case 'third':
            {

                handleStarSelect(3)
                return
            }
        case 'fourth':
            {

                handleStarSelect(4)
                return
            }
        case 'fifth':
            {

                handleStarSelect(5)
                return
            }
    }
}
const getNumericvalue = (stringValue) => {
    let numericValue;
    if (stringValue == 'first') {
        numericValue = 1
    } else if (stringValue == 'second') {
        numericValue = 2
    } else if (stringValue == 'third') {
        numericValue = 3
    } else if (stringValue == 'fourth') {
        numericValue = 4
    } else if (stringValue == 'fifth') {
        numericValue = 5
    } else {
        numericValue = 0
    }
    return numericValue
}
if (one) {
    const arr = [one, two, three, four, five]
    arr.forEach(item => item.addEventListener('mouseover', (event) => {

        handleSelect(event.target.id)



    }))

    arr.forEach(item => item.addEventListener('click', (event) => {
        const val = event.target.id


        form.addEventListener('submit', e => {
            e.preventDefault()
            const id = e.target.id
            $("#submitBtn").click(function() {
                console.log('h')

                $("#my_form").submit(); // Submit the form
            });
            rate_value = getNumericvalue(val)
            document.getElementById('temp').value = rate_value;


            // $.ajax({
            //     alert: alert('dsdsds'),
            //     type: 'POST',
            //     url: 'advocate_profile/1/',
            //     data: {

            //         'csrfmiddlewaretoken': csrf[0].value,
            //         'console': console.log(id + val_num, csrf[0].value),
            //         'id': id,
            //         'val': val_num,
            //     },
            //     success: function(response) {
            //         console.log(response)
            //         confirmBox.innerHTML = `<h1> successfully don e ${response.rate} </h1>`
            //     },
            //     error: function(error) {
            //         console.log(error)
            //         confirmBox.innerHTML = `<h1> ups something is wrong</h1>`
            //     }
            // })


        })
    }))


}