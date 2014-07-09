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
            fieldLabel: 'Orgão',
            width: 450,
            name: 'orgao'
        },
        {
            fieldLabel: 'Cargo',
            width:450,
            name: 'cargo'
        },
        {
            fieldLabel: 'Setor',
            width:450,
            name: 'setor'
        },
        {
            fieldLabel: 'Permissão',
            width: 200,
            name: 'permissao'
        },
        {
            xtype: 'button',
            text: 'Editar',
            style:{
                margin: '0px 10px 0px 400px',
            }
        },
        {
            xtype: 'button',
            text: 'Alterar Senha',
        },
    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Meu Perfil',
        width: '75%',
        height: 300,
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

