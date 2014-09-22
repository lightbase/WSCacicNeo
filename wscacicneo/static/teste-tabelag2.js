
w = document.getElementById('data');
t = w.textContent;
var regex = new RegExp("'", 'g');
t.replace(regex,'"');
t = t.replace(regex,'"');
JSON.parse(t);
t = JSON.parse(t);

w = document.getElementById('data2');
q = w.textContent;
var regex = new RegExp("'", 'g');
q.replace(regex,'"');
q = q.replace(regex,'"'); 
JSON.parse(q);
q = JSON.parse(q);


Ext.create('Ext.data.Store', {
    storeId:'simpsonsStore',
    fields:['te_node_address', 'id_so', 'id_software_inventariado'],
    data: t,
    proxy: {
        type: 'memory',
        reader: {
            type: 'json',
            root: 'items'
        }
    }
});

Ext.create('Ext.grid.Panel', {
    title: 'tabela',
    store: Ext.data.StoreManager.lookup('simpsonsStore'),
    columns: [
        { text: 'Numero',  dataIndex: 'te_node_address' },
        { text: "SO's", dataIndex: 'id_so' },
        { text: 'Apelido', dataIndex: 'id_software_inventariado' },
    ],
    height: 400,
    width: 600,
    renderTo: 'centro' 
});

Ext.create('Ext.Button', {
    text: 'Clique para gerar grafico da tabela',
    renderTo: 'centro',
    handler: function() {
        
         

var store1 = Ext.create('Ext.data.Store', {
    storeId:'Simpsons',
    fields:['countera', 'counterb'],
    data: q,
    proxy: {
        type: 'memory',
        reader: {
            type: 'json',
            root: 'items'
        }
    }
}); 

Ext.require('Ext.chart.*');
Ext.require(['Ext.layout.container.Fit', 'Ext.window.MessageBox']);

Ext.onReady(function () {

    var chart = Ext.create('Ext.chart.Chart', {
            animate: true,
            shadow: true,
            store: store1,
            axes: [{
                type: 'Numeric',
                position: 'left',
                fields: ['data1'],
                title: 'Quantidade',
                grid: true,
                minimum: 0,
                maximum: 60
            }, {
                type: 'Category',
                position: 'bottom',
                fields: [''],
                title: 'Valor',
                label: {
                }
            }],
            series: [{
                type: 'column',
                axis: 'left',
                gutter: 80,
                xField: '',
                yField: ['countera', 'counterb'],
                tips: {
                    trackMouse: true,
                    width: 74,
                    height: 38,
                    renderer: function(storeItem, item) {
                        this.setTitle(storeItem.get('name'));
                        this.update(storeItem.get('data1'));
                    }
                },
                style: {
                    fill: '#38B8BF'
                }
            }]
        });


    var panel1 = Ext.create('widget.panel', {
        width: 800,
        height: 400,
        title: 'Column Chart with Reload - Hits per Month',
        renderTo: 'centro',
        layout: 'fit',
        tbar: [{
            text: 'Save Chart',
            handler: function() {
                Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(choice){
                    if(choice == 'yes'){
                        chart.save({
                            type: 'image/png'
                        });
                    }
                });
            }
        }, {
            text: 'Reload Data',
            handler: function() {
                // Add a short delay to prevent fast sequential clicks
                window.loadTask.delay(100, function() {
                    store1.loadData(generateData());
                });
            }
        }],
        items: chart
    });
});


    }
});