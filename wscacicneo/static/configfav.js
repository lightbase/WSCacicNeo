// **** FILTRO DE ITENS ****

Ext.define('User1',{
    extend: 'Ext.data.Model',
    fields: ['chbox', 'item' ]
});

var userStore1 = Ext.create('Ext.data.Store', {
    model: 'User1',
    data: [
                { item: 'Relatórios'},
                { item: 'Gestão de Orgãos'},
                { item: 'Notificações'},
                { item: 'Meu Perfil'},
                { item: 'Configurar API'}, 
    ]
});

table1 = Ext.create('Ext.grid.Panel', {
    store: userStore1,
    width: 400,
    height: 200,
 //   title: 'Application Users',
    columns: [
        {
            text: 'Item',
            width: 500,
            sortable: true,
            hideable: false,
            dataIndex: 'item'
        },
    ]
});

tabela1 = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Lista de Funcionalidade',
        width: '75%',
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '0px auto 15px auto'
        },
        items: table1,
});


        Ext.create('Ext.Container', {
               padding:'15px',
               items: [tabela1],
        renderTo: 'widgets'
        });



//------------------------------------


Ext.define('User2',{
    extend: 'Ext.data.Model',
    fields: ['chbox', 'item' ]
});

var userStore2 = Ext.create('Ext.data.Store', {
    model: 'User2',
    data: [
                { item: 'Relatório'},
                { item: 'Meu Perfil'},

    ]
});

table2 = Ext.create('Ext.grid.Panel', {
    store: userStore2,
    width: 400,
 //   title: 'Application Users',
    columns: [
        {
            text: 'Item',
            width: 490,
            sortable: true,
            hideable: false,
            dataIndex: 'item'
        },
    ],
    bbar:[ 
          {
            xtype: 'button',
            text: 'Confirmar',
            style:{
                margin: '0px 10px 0px 320px',
            }
        },
        ,{
            xtype: 'button',
            text: 'Cancelar',
        },
        ]
});

tabela2 =Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Favoritos',
        width: '75%',
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '0px auto 15px auto'
        },
        items: table2,
});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding:'15px',
               items: [tabela2],
        renderTo: 'widgets'
        });

});


