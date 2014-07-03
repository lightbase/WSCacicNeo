var painelContent=
			"Data da coleta" + "<br>" +
            "<br>" + 
			"Configurar bot" + "<br>" +
            "<br>"+
			"Consertar data da coleta" + "<br>" +
            "<br>"+
			"Agrupar dados dos orgãos";
 
admin = Ext.create('Ext.panel.Panel', {
		title: 'Painel de Administração',
	 	width: '75%',
		frame: true,
		layout: 'fit',
		collapsible: true,
		draggable: true,
		border : true,
		style: {
			margin: '0px auto 15px auto'
				},
		html: painelContent
	});

Ext.onReady(function(){

		Ext.create('Ext.Container', {
			padding: '15px',
			items: [admin],
	    	renderTo: 'widgets'
		});		
		
});
