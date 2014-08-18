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
            fieldLabel: 'instalação',
            width: 250,
            name: 'data instalação'
        },
        {
            fieldLabel: 'Nome',
            width: 300,
            name: 'email'
        },
        {
            fieldLabel: 'Versão',
            width: 250,
            name: 'email'
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
        title: 'Sistemas Operacionais',
        width: '75%',
        height: 200,
        title: 'Processador',
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

