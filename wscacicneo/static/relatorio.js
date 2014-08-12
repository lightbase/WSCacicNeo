/*TABELA DE RELATÓRIOS*/

Ext.define('User',{
    extend: 'Ext.data.Model',
    fields: [ 'marca', 'modelo', 'fabricacao', 'quantidade' ],
});

var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: [
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'AMD', modelo: 'AMD 3.2GHZ', fabricacao: '08/22/2008', quantidade: '26' },

                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'INTEL', modelo: 'CORE I7 3.2GHZ', fabricacao: '12/12/2014', quantidade: '32' },
                { marca: 'AMD', modelo: 'AMD 3.2GHZ', fabricacao: '08/22/2008', quantidade: '26' },
    ],
    autoLoad: false,

    id:'simpsonsStore',
});

table = Ext.create('Ext.grid.Panel', {
    store: userStore,
    width: 400,
    height: 300,
 //   title: 'Application Users',
    columns: [
        {
            text: 'MARCA',
            width: 75,
            sortable: true,
            hideable: false,
            dataIndex: 'marca'
        },
        {
            text: 'MODELO',
            width: 300,
            dataIndex: 'modelo',
            hidden: false,
        },
        {
            text: 'FABRICAÇÃO',
            sortable: false,
            width:80,
            renderer: Ext.util.Format.dateRenderer('d/m/Y'),
            flex: 1,
            dataIndex: 'fabricacao'
        },
        {
            text: 'QUANTIDADE',
            sortable: false,
            width:80,
            dataIndex: 'quantidade'
        },
    ],
    tbar:[


        'Exportar PDF',
        { xtype: 'tbfill'},
        'Imprimir',
        { xtype: 'tbfill'},
        'Favorito',
        { xtype: 'tbfill'},
        'CSV',

        ]
});

/*COMEÇANDO PAGINAÇÃO - LEMBRANDO QUE TODA A PAGINAÇÃO NÃO ESTÁ COMPLETAMENTE FUNCIONANDO.
APENAS PARA QUESTÃO DE DOCUMENTAÇÃO.*/


var itemsPerPage = 2;   // set the number of items you want per page

var store = Ext.create('Ext.data.Store', {
    id:'simpsonsStore',
    autoLoad: false,
    fields:['name', 'email', 'phone'],
    pageSize: itemsPerPage, // items per page
    proxy: {
        type: 'ajax',
        url: 'pagingstore.js',  // url that will load data with respect to start and limit params
        reader: {
            type: 'json',
            root: 'items',
            totalProperty: 'total'
        }
    }
});




// specify segment of data you want to load using params
store.load({
    params:{
        start:0,
        limit: itemsPerPage
    }
});

tabela = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Relatorio de coletas por PROCESSADOR',
        width: '75%',
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '0px auto 15px auto'
        },
        items: table,

        dockedItems: [{
        xtype: 'pagingtoolbar',
        store: userStore,   // same store GridPanel is using
        dock: 'bottom',
        displayInfo: true
    }],

});

Ext.onReady(function(){
        Ext.create('Ext.Container', {
               padding: '15px',
               items: [tabela],
        renderTo: 'widgets'
        });

});


//CRIANDO GRAFICO


var store = Ext.create('Ext.data.JsonStore', {
    fields: ['name', 'data'],
    data: [
        { 'name': 'INTEL 55%', 'data': 32 },
        { 'name': 'AMD 45%', 'data': 26 }
]});

var chart = Ext.create('Ext.chart.Chart', {
    layout: 'fit',
    width: 500,
    height: 350,
    animate: true,
    store: store,
    theme: 'Base:gradients',
    shadow: true,
    legend: {
        position: 'right'
    },
    series: [{
        type: 'pie',
        angleField: 'data',
        showInLegend: true,
        tips: {
            trackMouse: true,
            width: 140,
            height: 28,
            renderer: function(storeItem, item) {
                // calculate and display percentage on hover
                var total = 0;
                store.each(function(rec) {
                    total += rec.get('data');
                });
                this.setTitle(storeItem.get('name') + ': ' + Math.round(storeItem.get('data') / total * 100) + '%');
            }
        },
        highlight: {
            segment: {
                margin: 20
            }
        },
        label: {
            field: 'name',
            display: 'rotate',
            contrast: true,
            font: '18px Arial'
        }
    }]
});

widget = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Grafico de  PROCESSADORES da SECRETARIA DE LOGISTICA E TECONOLOGIA DA INFORMAÇÃO',
        width: '75%',
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '-35px auto 15px auto'
        },
        items: chart,

        tbar:[
            'Exportar PDF',
            { xtype: 'tbfill'},
            'Imprimir',
            { xtype: 'tbfill'},
            'CSV',
        ],

        bbar:[
            'Quantidade de Orgãos: 12',
            { xtype: 'tbfill'},
            'Período da Coleta: 01/2014 - 06/2014',
        ]

});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding: '15px',
               items: [widget],
        renderTo: 'widgets'
        });

});



