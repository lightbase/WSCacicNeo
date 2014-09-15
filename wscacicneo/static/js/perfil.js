 table = Ext.create('Ext.form.Panel', {
    renderTo: Ext.getBody(),
    title: '',
    height: 130,
    width: 280,
    style: {
            "text-align": 'left',
    },

    bodyPadding: 10,
    items: [
        {
            xtype: 'displayfield',
            name: 'name',
            fieldLabel: 'Nome',
            value: 'João da Silva'
        },
        {
            xtype: 'displayfield',
            name: 'matricula',
            fieldLabel: 'Matricula',
            value: '00326'
        },
        {
            xtype: 'displayfield',
            name: 'E-mail',
            fieldLabel: 'E-mail',
            value: 'joão@email.com'
        },
        {
            xtype: 'displayfield',
            name: 'telefone',
            fieldLabel: 'Telefone',
            value: '(61)3669-6548'
        },
        {
            xtype: 'displayfield',
            name: 'orgao',
            fieldLabel: 'Orgão',
            value: 'Ministerio do Desenvolvimento'
        },
        {
            xtype: 'displayfield',
            name: 'cargo',
            fieldLabel: 'Cargo',
            value: 'Analísta'
        },
        {
            xtype: 'displayfield',
            name: 'setor',
            fieldLabel: 'Setor',
            value: 'Setor Sul'
        },
{
            xtype: 'displayfield',
            name: 'name',
            fieldLabel: 'Permissão',
            value: 'Usuário'
        },


        {
            xtype: 'button',
            text: 'Editar',
            style:{
                margin: '0px 10px 0px 320px',
            }
        },
        {
            xtype: 'button',
            text: 'Alterar Senha',
            style:{
                margin: '0px 10px 0px 0px',
            }
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

