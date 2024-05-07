/*   TODOS LOS RECURSOS JS PARA LOS REPORTES  */


function ConsultarRepo(num) {
	// body...

	
	var fd1 = document.getElementById('fecha_desde1').value;
	var fh1 = document.getElementById('fecha_hasta1').value;

	if( document.getElementById('sel_equipo') ){
		var equ = document.getElementById('sel_equipo').value;
	}
	if( document.getElementById('cod_col') ){
		var col = document.getElementById('cod_col').value;
	}


	var f1 = new Date(fd1);
	var f2 = new Date(fh1);

	if(f1 == 'Invalid Date' || f2 == 'Invalid Date' ){
	    alert("Ingrese rango de fechas correcto.");
	}
	else{
		if (f1 > f2) {
			var ft = fecha_desde1;
			fecha_desde1 = fecha_hasta1;
			fecha_hasta1 = ft;
		}

		if (num == 5) {
			// Clientes
			var cad = "/rep005/?equ="+equ+"&&fd1='"+fd1+"'&&fh1='"+fh1+"'";
		}
		if (num == 6) {
			// Clientes
			var cad = "/rep006/?equ="+equ+"&&fd1='"+fd1+"'&&fh1='"+fh1+"'";
		}
		if (num == 7) {
			// Reporte semanal
			var cad = "/rep007/?idu="+col+"&&fd1='"+fd1+"'&&fh1='"+fh1+"'";
		}
		// Call sp
		window.location.href = cad;
	}
}