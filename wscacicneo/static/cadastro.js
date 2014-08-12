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
            fieldLabel: 'Username',
            width: 250,
            name: 'matricula'
        },
        {
            fieldLabel: 'Senha',
            width: 300,
            name: 'email'
        },
        {
            fieldLabel: 'Confirmar senha',
            width: 300,
            name: 'email'
        },

        {
            fieldLabel: 'E-mail',
            name: 'telefone'
        },
        {
            xtype: 'combobox',
            name: 'checkbox1',
            fieldLabel: 'Orgão',
            boxLabel: 'Orgão'
        },
        {
            fieldLabel: 'Unidade',
            width:450,
            name: 'cargo'
        },
        {
            fieldLabel: 'Telefone',
            width:450,
            name: 'setor'
        },
        {
            fieldLabel: 'SIAPE',
            width:450,
            name: 'setor'
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
