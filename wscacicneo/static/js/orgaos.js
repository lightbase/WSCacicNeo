/**
 * Created by eduardo on 05/06/15.
 */
function validaOrgao(orgao, url, method) {
    var response = true;
    $.ajax({
        type: method,
        url: url,
        data: JSON.stringify( orgao ),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: false,
        beforeSend: function(){
            // Esconde todas as mensagens de erro
            $( '.label-danger').hide();
        },
        success: function(result){
            if (result.result == false) {
                // Dá mensagem de erro no elemento
                var error_html = '&nbsp;<span class="label label-danger">' +
                    result.message +
                '</span>';

                var elm = $( '#'+result.element );
                elm.after(error_html);

                noty({
                    text: 'Erro no envio! Verifique as mensagens de erro no formulário',
                    layout:'topRight',
                    type:'error',
                    timeout:3000
                });

                // Cancel the request
                response = false;
                //return false;
            }
        },
        error: function(result){
            if (result.result == false) {
                // Dá mensagem de erro no elemento
                var error_html = '&nbsp;<span class="label label-danger">' +
                    result.message +
                '</span>';

                var elm = $( '#'+result.element );
                elm.after(error_html);

                noty({
                    text: 'Erro no envio! Verifique as mensagens de erro no formulário',
                    layout:'topRight',
                    type:'error',
                    timeout:3000
                });

                // Cancel the request
                response = false;
            }
        }
    });

    return response;
}

