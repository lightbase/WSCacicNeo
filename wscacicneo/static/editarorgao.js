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
            width: 300,
            name: 'Sigla'
        },
        {
            fieldLabel: 'E-mail',
            name: 'email'
        },
        {
            fieldLabel: 'Telefone',
            name: 'telefone'
        },

        {
            xtype: 'button',
            text: 'Editar',
            style:{
                margin: '50px 10px 0px 350px',
            },
        },
    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Editar Orgão',
        width: '75%',
        height: 250,
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

