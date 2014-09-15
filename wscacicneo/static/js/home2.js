Ext.require([
    'Ext.data.*',
    'Ext.grid.*'
]);

Ext.onReady(function(){

    Ext.create('Ext.data.JsonPStore', {
        storeId:'baseboard',
        fields:['Win32_BaseBoard.Product', 'Win32_BaseBoard.Manufacturer', 'Win32_BaseBoard.Version', 'Win32_BaseBoard.SerialNumber'],
        autoLoad: true,
        model: 'User',
        proxy: {
            type: 'jsonp',
            url : 'http://10.209.8.39/wscserver/rest/coleta',
            callbackKey: 'callback',
            reader: {
                type: 'json',
                root: 'results',
                totalProperty: 'result_count',
            }
        }
    });

    Ext.create('Ext.grid.Panel', {
        title: 'BaseBoard',
        store: Ext.data.StoreManager.lookup('baseboard'),
        columns: [
            { header: 'Product',  dataIndex: 'Win32_BaseBoard.Product', flex: 1 },
            { header: 'Manufacturer', dataIndex: 'Win32_BaseBoard.Manufacturer', flex: 1 },
            { header: 'Version', dataIndex: 'Win32_BaseBoard.Version', flex: 1 },
            { header: 'SerialNumber', dataIndex: 'Win32_BaseBoard.SerialNumber', flex: 1 }
        ],
        width: "50%",
        draggable: true,
        renderTo: Ext.getBody()
    });
});
