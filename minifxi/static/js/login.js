
window.onload = function() {
	
}
 
/*     login */
 var guia = document.getElementById("guia");
 var guia1 = document.getElementById("guia1");
 var guia2 = document.getElementById("guia2");
  
  // this handler will be executed only once when the cursor moves over the unordered list
  guia.addEventListener("mouseenter", function( event ) { 
  	if (guia.classList.contains( "p_uno")) {
  		guia.classList.remove("p_uno");
	  	guia.classList.add("p_uno_h");
	  } else{
	  	guia.classList.remove("p_uno_h");
	  	guia.classList.add("p_uno");
	  }	  	
  }, false); 

  guia1.addEventListener("mouseenter", function( event ) {  
  	if (guia1.classList.contains( "p_dos")) {
	  	guia1.classList.remove("p_dos");
	  	guia1.classList.add("p_dos_h");
	  }else{
	  	guia1.classList.remove("p_dos_h");
	  	guia1.classList.add("p_dos");
	  }
  }, false); 

  guia2.addEventListener("mouseenter", function( event ) { 
	  if (guia2.classList.contains( "p_tres")) {  
		  	guia2.classList.remove("p_tres");
		  	guia2.classList.add("p_tres_h");
		 }else{
		 	guia2.classList.remove("p_tres_h");
		  	guia2.classList.add("p_tres");
		 }
  }, false);  
  
  /* this handler will be executed every time the cursor is moved over a different list item
  guia.addEventListener("mouseover", function( event ) {   
  	console.log("aler_2");
  }, false);*/