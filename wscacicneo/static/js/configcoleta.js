// **** FILTRO DE ITENS ****

Ext.define('User1',{
    extend: 'Ext.data.Model',
    fields: ['chbox', 'item' ]
});

var userStore1 = Ext.create('Ext.data.Store', {
    model: 'User1',
    data: [
                { item: 'Computador'},
                { item: 'Processador'},
                { item: 'Memórias'},
                { item: 'Hard Disk (HD)'},
                { item: 'Sistemas Operacionais'}, 
                { item: 'Suítes de Escritórios'},
                { item: 'Ativos de Redes'}, 
                { item: 'Softwares Básicos'},
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
        title: 'Campos da Coleta',
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
                { item: 'Computador'},
                { item: 'Processador'},
                { item: 'memórias'},
                { item: 'memórias'},

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
            text: 'Gerar Relatório',
            style:{
                margin: '0px 10px 0px 200px',
            }
        },
        {
            xtype: 'button',
            text: 'Limpar Campos',
        },{
            xtype: 'button',
            text: 'Cancelar',
        },
        ]
});

tabela2 =Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Campos Selecionados',
        width: '75%',
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '0px auto 15px auto'
        },
        items: [table2,
         {
            xtype: 'button',
            text: 'Gerar Relatório',
            style:{
                margin: '0px 10px 0px 0px',
            }
        },
        {
            xtype: 'button',
            text: 'Limpar Campos',
        },{
            xtype: 'button',
            text: 'Cancelar',
        },
]

});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding:'15px',
               items: [tabela2],
        renderTo: 'widgets'
        });

});


