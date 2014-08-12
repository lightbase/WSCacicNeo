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
            width: 250,
            name: 'matricula'
        },
        {
            fieldLabel: 'Responsável',
            width: 300,
            name: 'email'
        },
        {
            fieldLabel: 'Telefone',
            width: 300,
            name: 'email'
        },

        {
            fieldLabel: 'E-mail',
            name: 'telefone'
        },
        {
            fieldLabel: 'Endereço',
            width: 450,
            name: 'orgao'
        },
        {
            xtype: 'combobox',
            name: 'checkbox1',
            fieldLabel: 'Coleta',
            boxLabel: 'Coleta'
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

    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Orgão',
        width: '75%',
        height: 270,
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

