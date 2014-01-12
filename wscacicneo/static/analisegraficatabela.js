w = document.getElementById('widgets');
t = w.textContent;
var regex = new RegExp("'", 'g');
t.replace(regex,'"');
t = t.replace(regex,'"'); 
JSON.parse(t);
t = JSON.parse(t);

var store1 = Ext.create('Ext.data.Store', {
    storeId:'Simpsons',
    fields:['wcount', 'ucount', 'dcount', 'a', 'b', 'c'],
    data: t,
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
                maximum: 16
            }, {
                type: 'Category',
                position: 'bottom',
                fields: ['a', 'b', 'c'],
                title: 'Sistemas Operacionais',
                label: {
                }
            }],
            series: [{
                type: 'column',
                axis: 'left',
                gutter: 80,
                xField: '',
                yField: ['wcount', 'ucount', 'dcount'],
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