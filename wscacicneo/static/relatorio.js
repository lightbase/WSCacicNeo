Ext.define('User',{
    extend: 'Ext.data.Model',
    fields: [ 'codigo', 'orgao', 'date' ]
});

var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: [
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
                { codigo: '27236', orgao: 'Minist&eacuterio da Fazenda', date: '12/12/2014' },
    ]
});

table = Ext.create('Ext.grid.Panel', {
    store: userStore,
    width: 400,
    height: 200,
 //   title: 'Application Users',
    columns: [
        {
            text: 'Codigo',
            width: 75,
            sortable: true,
            hideable: false,
            dataIndex: 'codigo'
        },
        {
            text: 'Orgao',
            width: 300,
            dataIndex: 'orgao',
            hidden: false,
        },
        {
            text: 'Data',
            sortable: false,
            width:80,
            renderer: Ext.util.Format.dateRenderer('m/d/Y'),
            flex: 1,
            dataIndex: 'date'
        },
      
    ]
});

tabela = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Relatorios de Coletas',
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
});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding: '15px',
               items: [tabela],
        renderTo: 'widgets'
        });

});


// **** GRAFICO DE COLUNA ****

var store = Ext.create('Ext.data.JsonStore', {
    fields: ['name', 'data'],
    data: [
        { 'name': 'dado1', 'data':  200 },
        { 'name': 'dado2', 'data':  20 },
        { 'name': 'dado3', 'data':  500 },
        { 'name': 'dado4', 'data':  600 },
        { 'name': 'dado5', 'data':  700 },
        { 'name': 'dado6', 'data':  1000 },
        { 'name': 'dado7', 'data':  50 },
        { 'name': 'dado8', 'data':  200 },
        { 'name': 'dado9', 'data':  400 },
]});

var chart = Ext.create('Ext.chart.Chart', {
    layout: 'fit',
    width: 500,
    height: 350,
    animate: true,
    store: store,
    theme: 'Base:gradients',
    shadow: true,
    axes: [
        {
            type: 'Numeric',
            position: 'left',
            fields: ['data'],
            label: {
                renderer: Ext.util.Format.numberRenderer('0,0')
            },
            title: 'Eixo X',
            grid: true,
            minimum: 0
        },
        {
            type: 'Category',
            position: 'bottom',
            fields: ['name'],
            title: 'Eixo Y'
        }
    ],
    series: [
        {
            type: 'column',
            axis: 'left',
            highlight: true,
            tips: {
              trackMouse: true,
              width: 140,
              height: 28,
              renderer: function(storeItem, item) {
                this.setTitle(storeItem.get('name') + ': ' + storeItem.get('data'));
              }
            },
            label: {
              display: 'insideEnd',
              'text-anchor': 'middle',
                field: 'data',
                renderer: Ext.util.Format.numberRenderer('0'),
                orientation: 'vertical',
                color: '#333'
            },
            xField: 'name',
            yField: 'data'
        }
    ]
});

widget = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Grafico de dados',
        width: '75%',
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '-35px auto 15px auto'
        },
        items: chart
});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding: '15px',
               items: [widget],
        renderTo: 'widgets'
        });

});
