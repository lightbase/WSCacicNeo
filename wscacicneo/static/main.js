Ext.onReady(function() {
 
         var mainMenu = Ext.create('Ext.menu.Menu',{
                renderTo: 'menu-principal',
                floating: false,
                collapsible: true,
                border: true,
                frame: true,
                title: 'Home',
                titleAlign: 'center',
                items: [
                        {text: 'Meu Perfil' },
                        {text: 'Gestor de Orgãos' },
                        {text: 'Notificações' },
                        {text: 'Relatórios' },
                        {text: 'Acesso Rápido' },
                        {text: 'Sobre' },
                       ]
        });

        fav_html = '<div id="favoriteItems">'+
                '<div class="fav"><a><img src="static/icons/estatisticas.png">Estatisticas</a></div>'+
                '<div class="fav"><a><img src="static/icons/busca.png">Busca</a></div>'+
                '<div class="fav"><a><img src="static/icons/downloads.png">Downloads</a></div>'+
                '<div class="fav"><a href="reports"><img src="static/icons/relatorios.png">Relat&oacuterios</a></div>'+
                '<div class="fav"><a><img src="static/icons/ajuda.png">Ajuda</a></div>'+
                '<div class="fav"><a><img src="static/icons/usuario.png">Usu&aacuterio</a></div>'+
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
