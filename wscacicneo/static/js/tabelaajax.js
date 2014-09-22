function carregamentoTabela()
{
var xmlhttp;
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }

xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    document.getElementById("centro").innerHTML=xmlhttp.responseXML;
    }
  }
xmlhttp.open("GET","cartoon.xml",true);
xmlhttp.send();
}
