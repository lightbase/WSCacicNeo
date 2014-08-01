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
            fieldLabel: 'Matricula',
            width: 250,
            name: 'matricula'
        },
        {
            fieldLabel: 'E-mail',
            width: 300,
            name: 'email'
        },
        {
            fieldLabel: 'Telefone',
            name: 'telefone'
        },
        {
            xtype: 'combobox',
            name: 'checkbox1',
            fieldLabel: 'Orgão',
            boxLabel: 'Orgão'
        },
        {
            xtype:'combobox',
            fieldLabel: 'Cargo',
            width:450,
            name: 'cargo'
        },
        {
            xtype:'combobox',
            fieldLabel: 'Setor',
            width:450,
            name: 'setor'
        },
        {
            xtype: 'radiofield',
            name: 'radio1',
            value: 'radiovalue1',
            fieldLabel: 'Permissão',
            boxLabel: 'Gestor',
        },
        {
            xtype: 'radiofield',
            name: 'radio1',
            value: 'radiovalue2',
            fieldLabel: '',
            labelSeparator: '',
            hideEmptyLabel: false,
            boxLabel: 'Administrador'
        },
        {
            xtype: 'button',
            text: 'Enviar',
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
        title: 'Cadastro Usuário',
        width: '75%',
        height: 320,
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
