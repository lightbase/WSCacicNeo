Ext.create('Ext.button.Button', {
	    text: 'Abrir texto',
    renderTo: 'centro',
    handler: function () {


	if (window.XMLHttpRequest){

	  xmlhttp=new XMLHttpRequest();

  	}

	xmlhttp.onreadystatechange=function(){

	  if (xmlhttp.readyState==4 && xmlhttp.status==200)

	 {

    		document.getElementById("centro").innerHTML=xmlhttp.responseText;

    	}

  	}

	xmlhttp.open("GET",'static/cartoon.xml',true);
	xmlhttp.send();









	}





    	
});
