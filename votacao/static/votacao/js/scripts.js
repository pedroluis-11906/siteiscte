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

$(document).ready(
    function (){
        $('#showprofile .profileimg').hover(
            function (){
                $('#user-info').show();
            },
            function (){
                $('#user-info').hide();
            }
            )
})

$(document).ready(function() {
  $('input[type="radio"]').click(function() {
      $('div[id^="num-votos"]').hide();
      // Obter o ID do botão selecionado
      let btn_id = $(this).attr('id');
      // Extrair o número do ID (usando uma expressão regular)
      let num = parseInt(btn_id.replace(/\D/g,''));
      let div_id = 'num-votos' + num;

      if ($(this).is(':checked')) {
        $('#' + div_id).show();
      } else {
        $('#' + div_id).hide();
      }
  });
});



function esconder_mostrar(){
    let list = document.getElementById('question-list');
    let btn = document.getElementById('hide-show-quest');
    if (list.style.display === 'none'){
        list.style.display = 'block';
        btn.textContent = 'Esconder lista de questões';
    } else {
        list.style.display = 'none';
        btn.textContent = 'Mostrar lista de questões';
    }
}

function validateComment() {
    let comment = document.getElementById('comment');
    let commentValue = comment.value;
    let result = document.getElementById('comment-result');
    const badWords = ["abécula", "abentesma", "achavascado", "estólido", "pechenga", "somítico"];
    let hasBadWords = false;

    if (commentValue !== "") {
        console.log('not null');

        for (let i = 0; i <= badWords.length; i++) {
            if (commentValue.includes(badWords[i])) {
                hasBadWords = true;
                console.log('true');
                break;
            }
        }

        if (hasBadWords) {
            result.textContent = 'Comentário não aceite.';
            result.style.display = "block";
            comment.value = '';
        } else {
            result.textContent = 'Comentário aceite.';
            result.style.display = "block";
        }

    }
}



