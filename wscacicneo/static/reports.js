/*GRAFICO DE ORGÃOS*/



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
            xtype: 'checkcolumn',
            allowBlank: false,
            dataIndex: 'active',
            width: 60,
            editor:{
                xtype: 'checkbox',
                cls: 'item'
                },
        },
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
        title: 'Gerar Relatório',
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

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding:'15px',
               items: [tabela1],
        renderTo: 'widgets'
        });

});


