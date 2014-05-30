var recur = 0;
function xmlhttpPost(strURL) {
	if (recur == 0)
		limpiar()
    var xmlHttpReq = false;
    var self = this;
    // Mozilla/Safari
    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
    }
    // IE
    else if (window.ActiveXObject) {
        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    }
    self.xmlHttpReq.open('POST', strURL, true);
    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    self.xmlHttpReq.onreadystatechange = function() {
        if (self.xmlHttpReq.readyState == 4) {
            updatepage(self.xmlHttpReq.responseText);
            var img = document.getElementById('imgc');
    		img.style.visibility = "hidden";    		
    		xmlhttpPostApis('searchApis.py');   			
        }
    }
    
    self.xmlHttpReq.send(getquerystring());
}

function getquerystring() {
    var form     = document.forms['fInV'];
    var word = form.search.value;
    qstr = 'search=' + escape(word);  // NOTE: no '?' before querystring
    var img = document.getElementById('imgc');
    img.style.visibility = "visible";
    return qstr;
}

function updatepage(str){
    document.getElementById("result").innerHTML = str;
}
function updatepageAdd(str){
    document.getElementById("result").innerHTML += str;
}
function limpiar(){
	document.getElementById("result").innerHTML = "";
}

function xmlhttpPostApis(strURL) {
    var xmlHttpReq = false;
    var self = this;
    // Mozilla/Safari
    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
    }
    // IE
    else if (window.ActiveXObject) {
        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    }
    self.xmlHttpReq.open('POST', strURL, true);
    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    self.xmlHttpReq.onreadystatechange = function() {
        if (self.xmlHttpReq.readyState == 4) {
            updatepageAdd(self.xmlHttpReq.responseText);
            var img = document.getElementById('imgc');
    		img.style.visibility = "hidden";
        }
    }
    self.xmlHttpReq.send(getquerystring());
}

function xmlhttpPostSensibility(strURL) {
	var form     = document.forms['fInV'];
    var word = form.search.value;
    if (word.length >=3){
		limpiar()
	    var xmlHttpReq = false;
	    var self = this;
	    // Mozilla/Safari
	    if (window.XMLHttpRequest) {
	        self.xmlHttpReq = new XMLHttpRequest();
	    }
	    // IE
	    else if (window.ActiveXObject) {
	        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
	    }
	    self.xmlHttpReq.open('POST', strURL, true);
	    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	    self.xmlHttpReq.onreadystatechange = function() {
	        if (self.xmlHttpReq.readyState == 4) {
	            updatepage(self.xmlHttpReq.responseText);
	            var img = document.getElementById('imgc');
	    		img.style.visibility = "hidden";	
	        }
	    }
	    self.xmlHttpReq.send(getquerystring());
	  }
}

function gup(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if (results == null)
        return "";
    else
        return results[1];
} 

//Crear las relaciones entre el Usuario y Datos
function xmlhttpPostRelations(strURL) {

    var xmlHttpReq = false;
    var self = this;
    // Mozilla/Safari
    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
    }
    // IE
    else if (window.ActiveXObject) {
        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    }
    self.xmlHttpReq.open('POST', strURL, true);
    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    self.xmlHttpReq.onreadystatechange = function() {
        if (self.xmlHttpReq.readyState == 4) {
        	var img = document.getElementById('imgc');
	    	img.style.visibility = "hidden";	
        }
    }
    self.xmlHttpReq.send(getquerystring());
}

//Función para generar las recomendaciones
//Crear las relaciones entre el Usuario y Datos
function xmlhttpPostRecomendations(strURL) {

    var xmlHttpReq = false;
    var self = this;
    // Mozilla/Safari
    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
    }
    // IE
    else if (window.ActiveXObject) {
        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    }
    self.xmlHttpReq.open('POST', strURL, true);
    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    self.xmlHttpReq.onreadystatechange = function() {
        if (self.xmlHttpReq.readyState == 4) {
        	document.getElementById('data_recom_ol').innerHTML += self.xmlHttpReq.responseText;
        	var img = document.getElementById('imgr');
	    	img.style.visibility = "hidden";
        }
    }
    self.xmlHttpReq.send();
}
function doRelation(link){
	var id = link.getAttribute('alt');
	xmlhttpPostRelations("ajax.py?method=relUserItem&id="+id);
	
}