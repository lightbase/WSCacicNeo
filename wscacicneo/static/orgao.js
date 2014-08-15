var table = Ext.create('Ext.form.Panel', {
    renderTo: Ext.getBody(),
    title: '',
    height: 130,
    width: 280,
    style: {
            "text-align": 'left',
    },

    bodyPadding: 10,
    defaultType: 'textfield',
    items: [
        {
            fieldLabel: 'Nome',
            width:450,
            name: 'nome'
        },
        {
            fieldLabel: 'Sigla',
            width: 200,
            name: 'sigla'
        },
        {
            fieldLabel: 'Cargo / Gestor',
            width: 300,
            name: 'cargo'
        },

        {
            fieldLabel: 'Telefone',
            width: 300,
            name: 'telefone'
        },

        {
            fieldLabel: 'E-mail',
            width: 300,
            name: 'email'
        },
        {
            fieldLabel: 'Endereço',
            width: 450,
            name: 'end'
        },
        {
            xtype: 'combobox',
            name: 'checkbox1',
            fieldLabel: 'Coleta',
            boxLabel: 'coleta'
        },
        {
            xtype: 'button',
            text: 'Enviar',
            style:{
                margin: '0px 10px 0px 320px',
            }
        },
        {
            xtype: 'button',
            text: 'Limpar',
        },
        {
            xtype: 'button',
            text: 'Cadastrar',
            style:{
                margin: '50px 10px 0px 350px',
            },
        },
    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Órgão',
        width: '75%',
        height: 265,
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '0px auto 15px auto'
        },
        items: table,
});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding: '15px',
               items: [painel],
        renderTo: 'widgets'
        });

});


$('#button-1017-btnIconEl').click(function(){
    var nome = $('#textfield-1010-inputEl').val()
        sigla = $('#textfield-1011-inputEl').val()
        gestor = $('#textfield-1012-inputEl').val()
        telefone = $('#textfield-1013-inputEl').val()
        email = $('#textfield-1014-inputEl').val()
        end = $('#textfield-1015-inputEl').val()
        coleta = $('#combobox-1016-inputEl').val()
    var reg = {
        'nome' : nome,
        'sigla': sigla,
        'gestor': gestor,
        'telefone': telefone,
        'email': email,
        'end': end,
        'coleta': '15'
    }
    $.ajax({
        type: "POST",
        url: 'http://10.1.0.121/wscacicneo/orgao',
        cache: false,
        success: function(jqXHR, textStatus, errorThrown){
            alert('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert('ooooooooooooooooooooooooooooooooooooo')
        }
    });
});
