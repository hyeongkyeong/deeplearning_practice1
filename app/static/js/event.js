//<![CDATA[
$(document).ready(function(){

    $('#action_menu_btn').click(function(){
        $('.action_menu').toggle();
    });
    $('#send-message').click(function(){
        message_input();
    });
    $('#send-message').keypress(function(e){
        if(e.keyCode==13){
            message_input();
        }
    });
});

function message_input(){
    var msg = $('#user-message').val();
        set_user_msg_component(msg)
        $('#user-message').val('');
        console.log('send message:',msg)
        $.getJSON('/predict',{user_msg: msg} ,function(data){
            console.log('JSON get: ',data);
            if(data.answer=='Positive'){    
                console.log('Positive');
                set_host_msg_component('제가 비슷한 영화를 추천 드릴게요!!');
            }else if(data.answer=='Negative'){
                console.log('Negative');
                set_host_msg_component('그럼 다른 영화를 추천 드릴게요!!');
            }else{
                console.log('Unkown Answer');
            }
        });
}

function set_host_msg_component(msg){
    var host_avatar='https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg'

    var host_msg_component='<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="'+host_avatar+'" class="rounded-circle user_img_msg"/></div><div class="msg_cotainer">' + 
    msg + 
    '<span class="msg_time">8:40 AM, Today</span></div></div>'
    $('#chat-box').append(host_msg_component);
}
function set_user_msg_component(msg){
    var user_avatar='https://avatars0.githubusercontent.com/u/43701043?s=460&v=4'
    var user_msg_component='<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">'+
    msg+
    '<span class="msg_time_send">8:55 AM, Today</span></div>'+
    '<div class="img_cont_msg"><img src="' + user_avatar +
    '" class="rounded-circle user_img_msg"/></div></div>'
    $('#chat-box').append(user_msg_component);
}

//]]>