var regAllContent = document.getElementById('wmi-content').innerText,
    regReplace = regAllContent.replace(/'/gi, '"'),
    regObjectJson = JSON.parse(regReplace);
    regObjectJson = {"reg": regObjectJson},
    x = new Array(),
    counter = 0,
    regAberto = '';

$.each(regObjectJson.reg, function(k, v){
    if (k != "id_reg"){
        //aplica os nomes dos grupos na tabela GRUPOS
        // x.push({text: k, handler: function(e){
            //verifica o contador
            // if (counter <= 3){
                x.push({"base_name": k});
                fields = new Array();
                columns = new Array();
                //aplica as respectivas strings no array (colocar grid e store)
                $.each(v[0], function(key, value){
                    data = v[0];
                    fields.push(key);
                    columns.push({text: key, flex: 1, minWidth: 108, dataIndex: key});
                });
                // doTable(data, fields, columns);
            //}else{
            //     alert('É permitido abrir apenas 4 tabelas simultaneamente');
            // }
        // }});
    }
});

$.each(regObjectJson.reg, function(k, v){
});

function doCombobox(x, data, fields, columns){
    //tabelas ExtJS

        // var mainMenu = Ext.create('Ext.menu.Menu', {
        //     width: 190,
        //     renderTo: 'group-table',
        //     floating: false,
        //     collapsible: true,
        //     border: true,
        //     frame: true,
        //     title: 'Home',
        //     titleAlign: 'center',
        //     items: x
        // });

            var states = Ext.create('Ext.data.Store', {
                fields: ['base_name'],
                data : x 
                    // {"abbr":"AL", "name":"Alabama"},
                    // {"abbr":"AK", "name":"Alaska"},
                    // {"abbr":"AZ", "name":"Arizona"}
                
            });

            // Create the combo box, attached to the states data store
            Ext.create('Ext.form.ComboBox', {
                listeners: {
                    'select': function(){
                        if (counter < 7){
                            doTable(data, fields, columns);
                            counter++;
                        }else{
                            alert('Só é permitido abrir 7 bases simultaneamente!')
                        }
                    }
                },
                fieldLabel: 'Escolha a Base',
                store: states,
                queryMode: 'local',
                displayField: 'base_name',
                // valueField: 'base_name',
                renderTo: 'group-table'
            });
}

doCombobox(x, data, fields, columns);

function doTable(data, fields, columns){
    Ext.require([
        'Ext.data.*',
        'Ext.grid.*'
    ]);
    
    Ext.onReady(function(){
        var store2 = Ext.create('Ext.data.Store', {
            autoLoad: true,
            data: data,
            fields: fields,
            proxy: {
                type: 'memory',
                reader: {
                    type: 'json',
                }
            }
        });



        var panel = Ext.create('Ext.grid.Panel', {
            forceFit: false,
            closable: true,
            listeners: {
                close: function(e){
                    counter--;
                }
            },
            store: store2,
            columns: columns,
            renderTo:'reg-table',
            width: 750,
            height: 85
        });
    });
}
