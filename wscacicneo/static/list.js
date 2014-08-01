/*GRAFICO DE ORGÃOS*/


Ext.define('User',{
    extend: 'Ext.data.Model',
    fields: [ 'codigo', 'orgao']
});

var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: [
                { orgao: 'Minist&eacuterio da Fazenda', date: 'Editar  Excluir' },
                { orgao: 'Minist&eacuterio da Fazenda', date: 'Editar  Excluir' },
                { orgao: 'Minist&eacuterio da Fazenda', date: 'Editar  Excluir' },
                { orgao: 'Minist&eacuterio da Fazenda', date: 'Editar  Excluir' },
          ]
});

table = Ext.create('Ext.grid.Panel', {
    store: userStore,
    width: 400,
    height: 200,
 // title: 'Application Users',
    columns: [
        {
            text: 'Orgão',
            width: 390,
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
                    icon:'static/icons/delete.png',
                    tooltip: 'Excluir'
                },
       ]},
   ]
});

tabela = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Orgãos',
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

