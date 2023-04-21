$(document).ready( function (){
    $("#header_profileimage").dblclick( function (){
        $(this).hide();
    });
})

$(document).ready( function (){
    $("#user-click-img").click ( function (){
       $("#header_profileimage").toggle();
    });
})

function esconder_mostrar(){
    let list = document.getElementById('question-list');
    let btn = document.getElementById('hide-show-quest');
    if (list.style.display == 'none'){
        list.style.display = 'block';
        btn.textContent = 'Esconder lista de questões';
    } else {
        list.style.display = 'none';
        btn = 'Mostrar lista de questões';
    }
}

function validate(){

}

