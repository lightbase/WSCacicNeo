/*GRAFICO DE ORGÃOS*/


Ext.define('User',{
    extend: 'Ext.data.Model',
    fields: [ 'codigo', 'orgao']
});

var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: [
                { codigo: 'Pedro', orgao: 'Minist&eacuterio da Fazenda'},
                { codigo: 'Carlos', orgao: 'Minist&eacuterio da Fazenda'},
                { codigo: 'Thiago', orgao: 'Minist&eacuterio da Fazenda'},
                { codigo: 'Helder', orgao: 'Minist&eacuterio da Fazenda'},
          ]
});

table = Ext.create('Ext.grid.Panel', {
    store: userStore,
    width: 400,
    height: 200,
 // title: 'Application Users',
    columns: [
        {
            text: 'Nome',
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
            xtype: 'actioncolumn',
            width: 100,
            align: 'center',
                items:[{
                    icon:'static/icons/edit.png',
                    tooltip: 'Editar'
                },
                {
                    icon:''
                },
                {
                    icon:'static/icons/delete.gif',
                    tooltip: 'Excluir'
                }
            ]
        },
    ]
});

tabela = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Usuários',
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

