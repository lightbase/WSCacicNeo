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
                        {text: 'Sobre' },
                       ]
        });

        fav_html = '<div id="favoriteItems">'+
                '<div class="fav"><a href="reports"><img src="static/icons/relatorios.png">Relat&oacuterios</a></div>'+
                '<div class="fav"><a><img src="static/icons/usuario.png">Meu Perfil</a></div>'+
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
