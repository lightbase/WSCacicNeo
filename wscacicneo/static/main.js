Ext.onReady(function() {
 
         var mainMenu = Ext.create('Ext.menu.Menu', {
                 renderTo: 'menu-principal',
                 floating: false,
         collapsible: true,
                 border: true,
                 frame: true,
                 title: 'Home',
        titleAlign: 'center',
                items: [
                        {text: 'Item 1' },
                        {text: 'Item 2' },
                        {text: 'Item 3' },
                        {text: 'Item 4' },
                        {text: 'Item 5' },
                        {text: 'Item 6' },
                        {text: 'Item 7' },
                        {text: 'Item 8' },
                        {text: 'Item 9' },
                        {text: 'Item 10'}
                                ]
        });

        fav_html = '<div id="favoriteItems">'+
                '<div class="fav"><a><img src="static/icons/estatisticas.png">EstatÃ­sticas</a></div>'+
                '<div class="fav"><a><img src="static/icons/busca.png">Busca</a></div>'+
                '<div class="fav"><a><img src="static/icons/downloads.png">Downloads</a></div>'+
                '<div class="fav"><a href="reports"><img src="static/icons/relatorios.png">RelatÃ³rios</a></div>'+
                '<div class="fav"><a><img src="static/icons/mensagens.png">Mensagens</a></div>'+
                '<div class="fav"><a><img src="static/icons/ajuda.png">Ajuda</a></div>'+
                '<div class="fav"><a><img src="static/icons/usuario.png">UsuÃ¡rio</a></div>'+
                '<div class="fav"><a><img src="static/icons/ferramentas.png">Ferramentas de sistema</a></div>'+
        '</div>';

        var favoriteMenu = Ext.create('Ext.panel.Panel', {
                layout: 'fit',
                renderTo: 'menu-favoritos',
                collapsible: true,
                border: true,
                frame: true,
                heigth: "100%",
                width: "100%",
                title: 'Favoritos',
                titleAlign: 'center',
                html: fav_html
        });
});
