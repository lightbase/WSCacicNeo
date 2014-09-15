/*GRAFICO DE ORGÃOS*/


Ext.define('User',{
    extend: 'Ext.data.Model',
    fields: [ 'codigo', 'orgao', 'date' ]
});

var userStore = Ext.create('Ext.data.Store', {
    model: 'User',
    data: [
                { codigo: 'Gráficos'},
                { codigo: 'Favoritos'},
                { codigo: 'Pesquisa Rápida'},
                { codigo: 'Notificações'},
                { codigo: 'Base de Dados'},
          ]
});

table = Ext.create('Ext.grid.Panel', {
    store: userStore,
    width: 400,
    height: 200,
 //   title: 'Application Users',
    columns: [
        {
            text: 'Opções',
            width: 550,
            sortable: true,
            hideable: false,
            dataIndex: 'codigo'
        },
    ]
});

tabela = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Configurações da Aplicação',
        width: '75%',
        height: 165,
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
                { item: 'Relatórios'},
                { item: 'Meu Perfil'},
          ]
});

table1 = Ext.create('Ext.grid.Panel', {
    store: userStore1,
    width: 400,
    height: 200,
 //   title: 'Application Users',
    columns: [
        {
            text: 'Pesquisar',
            width: 500,
            sortable: true,
            hideable: false,
            dataIndex: 'item'
        },
        {
            text: 'Remover',
            width: 100,
            sortable: true,
            hideable: false,
            dataIndex: 'excluir'
        },

    ]
});

tabela1 = Ext.create('Ext.panel.Panel', {
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
        items: table1,
});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding:'15px',
               items: [tabela1],
        renderTo: 'widgets'
        });

});

