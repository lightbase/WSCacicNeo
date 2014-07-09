var painelContent=
    Ext.create('Ext.tree.Panel', {
        renderTo: Ext.getBody(),
        title: '',
        root: {
            text: 'Gestor',
            expanded: true,
            children: [
                {
                    text: 'Coleta automática',
                    leaf: true
                },
                {
                    text: 'Coleta manual',
                    leaf: true
                },
                {
                    text: 'Questionar coleta',
                    leaf: true
                },
            ]
        }
    });

admin = Ext.create('Ext.panel.Panel', {
		title: 'Gestor de Orgãos',
	 	width: '75%',
		frame: true,
		layout: 'fit',
		collapsible: true,
		draggable: true,
		border : true,
		style: {
			margin: '0px auto 15px auto'
				},
		items: painelContent
	});

Ext.onReady(function(){

		Ext.create('Ext.Container', {
			padding: '15px',
			items: [admin],
	    	renderTo: 'widgets'
		});		
		
});
