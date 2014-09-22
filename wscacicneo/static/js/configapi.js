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
            xtype:'combobox',
            fieldLabel: 'Fonte',
            width:300,
            name: 'fonte'
        },
        {
            xtype:'combobox',
            fieldLabel: 'Estilo de cores',
            width: 250,
            name: 'matricula'
        },
        {
            xtype: 'button',
            text: 'Confirmar',
            style:{
                margin: '0px 10px 0px 300px',
            }
        },
        {
            xtype: 'button',
            text: 'Cancelar',
        },

    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Configuração da Aplicação',
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

