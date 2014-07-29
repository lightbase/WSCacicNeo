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
            fieldLabel: 'Quantidade',
            width:450,
            name: 'nome'
        },
        {
            fieldLabel: 'Marca',
            width: 250,
            name: 'matricula'
        },
        {
            fieldLabel: 'Tipo',
            width: 300,
            name: 'email'
        },
        {
            fieldLabel: 'Idade',
            name: 'telefone'
        },
        {
            xtype: 'button',
            text: 'Enviar',
            style : {
                margin : " 0px 10px 0px 0px"
            }
        },
        {
            xtype: 'button',
            text: 'Limpar',
        },

    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'HD',
        width: '75%',
        height: 200,
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

