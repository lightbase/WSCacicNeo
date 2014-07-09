 var html = "<div style='padding: 25px ; font-size: 14px; text-align: justify;'><div style='width: 29%; height: 100px; float: left;'><img src='static/caciclogo.jpg'> </div><div style='width: 70%; float: right'>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse turpis eros, accumsan in dignissim nec, rhoncus sed nunc. Integer sit amet venenatis ante, id lacinia velit. Fusce a elit purus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam aliquam lacus accumsan cursus tempus. Suspendisse ante ipsum, mollis eget ultrices eget, cursus sed quam. Fusce eget dui ut felis scelerisque sodales. Maecenas pellentesque dolor ac erat fringilla, ut vehicula mi viverra. In non turpis a massa auctor accumsan.</div></div>";


Ext.onReady(function(){

    Ext.create('Ext.Panel', {
        layout: 'fit',
        height: '220px',
        style: {margin: '15px'},
        frame: true,
        draggable: true,
        title: 'SOBRE O SUPER GERENTE',
        titleAlign: 'center',
        html: html,
        renderTo: 'g1'
    });
});
