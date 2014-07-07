var painelContent= 
    Ext.create('Ext.tree.Panel', {
        renderTo: Ext.getBody(),
        title: '',
        root: {
            text: 'Administração',
            expanded: true,
            children: [
                {
                    text: 'Administração de Órgãos',
                    expanded: true,
                    children: [
                        {
                            text: 'Cadastrar Órgão',
                            leaf: true
                        },
                        {
                            text: 'Lista de Órgãos',
                            leaf: true
                        },
                    ]
                },
                {
                    text: 'Administrção de Usuário',
                    expanded: true,
                    children: [
                        {
                            text: 'Cadastro de Usuário',
                            leaf: true
                        },
                        {
                            text: 'Gestão de Usuário',
                            leaf: true
                        },
                    ]
                },
                {
                    text: 'Configurções do sistema',
                    expanded: true,
                    children: [
                        {
                            text: 'Configurações das Bases de dados',
                            leaf: true
                        },
                        {
                            text: 'Confirgurações da aplicação',
                            leaf: true
                        },
                    ]
                },

            ]
        }
    });

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
		items: painelContent
	});

Ext.onReady(function(){

		Ext.create('Ext.Container', {
			padding: '15px',
			items: [admin],
	    	renderTo: 'widgets'
		});		
		
});
