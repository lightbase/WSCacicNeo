var table = Ext.create('Ext.form.Panel', {
    renderTo: Ext.getBody(),
    title: '',
    height: 1000,
    width: 280,
    style: {
            "text-align": 'left',
    },

    bodyPadding: 10,
    defaultType: 'textfield',
    items: [
        {
            xtype: 'combobox',
            name: 'checkbox1',
            fieldLabel: 'Órgão',
            boxLabel: 'Orgão'
        },
        {
            fieldLabel: 'Senha da base',
            name: 'senha',
        },
        {
            fieldLabel: 'Confirmar senha',
            name: 'email'
        },
        {
            fieldLabel: 'Nome da Base',
            name: 'telefone'
        },
        {
            xtype:'combobox',
            fieldLabel: 'Remover campo',
            name: 'cargo'
        },
        {
            fieldLabel: 'MAC',
            name: 'setor'
        },
        {
            fieldLabel: 'App a evitar',
            name: 'setor'
        },
        {
            xtype: 'button',
            text: 'Enviar',
            style:{
                margin: '0px 10px 0px 0px',
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
        title: 'Configurar Base de Dados',
        width: 500,
        height: 280,
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
