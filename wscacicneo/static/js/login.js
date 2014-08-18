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
            fieldLabel: 'Usuário',
            width:300,
            name: 'nome'
        },
        {
            fieldLabel: 'Senha',
            width: 300,
            name: 'matricula'
        },
        {
            xtype: 'button',
            text: 'Login',
            style:{
                margin: '10px 10px 0px 0px',
            }
        },
        {
            xtype: 'button',
            text: 'Recuperar Senha',
            style:{
                margin: '10px 10px 0px 0px',
            }

        },
    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Meu Perfil',
        width: 400,
        height: 150,
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '0px auto 50px 100px'
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

