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

// **** GRAFICO DE PIZZA ****

var store = Ext.create('Ext.data.JsonStore', {
    fields: ['name', 'data'],
    data: [
        { 'name': 'dado1', 'data':  2 },
        { 'name': 'dado2', 'data':  2 },
        { 'name': 'dado3', 'data':  4 },
        { 'name': 'dado4', 'data': 10 },
        { 'name': 'dado5', 'data': 20 }
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
        title: 'Relatório',
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


