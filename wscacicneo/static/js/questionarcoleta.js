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
            xtype:'displayfield',
            fieldLabel: 'Nome do responsavel',
            name: 'nome',
            value: 'João da Silva'
        },
        {
            xtype:'displayfield',
            fieldLabel: 'Orgão da coleta:',
            name: 'orgao',
            value: 'Ministerio do Planejamento',
        },{
            xtype:'displayfield',
            fieldLabel: 'Codigo da coleta:',
            name: 'orgao',
            value: '1231654',
        },

        {   
            xtype:'displayfield',
            fieldLabel: 'Data',
            name: 'data',
            value:'12/12/2012',
        },
        {
            xtype:'textfield',
            fieldLabel: 'Descrição',
            name: 'Descrição',
            width: 450,
            height: 100,
        },

        {
            xtype: 'button',
            text: 'Enviar',
            style:{
                margin: '20px 10px 0px 300px',
            },
        },
        {
            xtype: 'button',
            text: 'Cancelar',
            style:{
                margin: '20px 10px 0px 0px',
            },

        },
    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Questionar Coleta',
        width: '75%',
        height: 350,
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

