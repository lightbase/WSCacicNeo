function crossDomainPost() {
  // Add the iframe with a unique name
  var iframe = document.createElement("iframe");
  var uniqueString = "nome";
  document.body.appendChild(iframe);
  iframe.style.display = "none";
  iframe.contentWindow.name = uniqueString;

  // construct a form with hidden inputs, targeting the iframe
  var form = document.createElement("form");
  form.target = uniqueString;
  form.action = "http://http://10.1.0.95/Cacic/so";
  form.method = "POST";

  form.submit();
}