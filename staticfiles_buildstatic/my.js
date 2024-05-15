// (function() {
//     var Message;
//     Message = function(arg) {
//         this.text = arg.text, this.message_side = arg.message_side;
//         this.draw = function(_this) {
//             return function() {
//                 var $message;
//                 $message = $($('.message_template').clone().html());
//                 $message.addClass(_this.message_side).find('.text').html(_this.text);
//                 $('.messages').append($message);
//                 return setTimeout(function() {
//                     return $message.addClass('appeared');
//                 }, 0);
//             };
//         }(this);
//         return this;
//     };
//     $(function() {
//         var getMessageText, message_side, sendMessage;
//         message_side = 'right';
//         getMessageText = function() {
//             var $message_input;
//             $message_input = $('.message_input');
//             return $message_input.val();
//         };
//         sendMessage = function(text) {
//             var $messages, message;
//             if (text.trim() === '') {
//                 return;
//             }
//             $('.message_input').val('');
//             $messages = $('.messages');
//             message_side = message_side === 'left' ? 'right' : 'left';
//             message = new Message({
//                 text: text,
//                 message_side: message_side
//             });
//             message.draw();
//             return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
//         };
//         $('.send_message').click(function(e) {
//             return sendMessage(getMessageText());
//         });
//         $('.message_input').keyup(function(e) {
//             if (e.which === 13) {
//                 return sendMessage(getMessageText());
//             }
//         });
//         sendMessage('Hello Philip! :)');
//         setTimeout(function() {
//             return sendMessage('Hi Sandy! How are you?');
//         }, 1000);
//         return setTimeout(function() {
//             return sendMessage('I\'m fine, thank you!');
//         }, 2000);
//     });
// }.call(this));




let message_send_btn = document.getElementById("send-btn");
let message_input = document.getElementById("message-input");

function send_message() {
    let message = message_input.value;
    if (message === "") {
        return;
    }
    message_input.value = "";
    fetch("{% url 'chatroom-ajax' other_user.id %}", {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "Content-Type": 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(message)
    }).then(e => e.json()).then(messages => {
        for (message of messages) {
            construct_message(message);
        }
    });
}

function load_messages() {
    fetch("{% url 'chatroom-ajax' other_user.id %}")
        .then(e => e.json())
        .then(messages => {
            console.log(messages)
            for (message of messages) {
                construct_message(message);
            }
        })
}

function construct_message(message) {
    let messages_container = document.querySelector(".messages-area");
    let class_name = "left"
    if (message.sent) {
        class_name = "right"
    }
    let div = document.createElement("div");
    div.classList.add("message", class_name);
    div.innerHTML = `
        <div class="sent-by">${ message.sender }</div>
            <div class="content">${ message.message }</div>
        `
    messages_container.appendChild(div);
    div.scrollIntoView()
}
message_send_btn.addEventListener('click', send_message);
setInterval(load_messages, 2000);