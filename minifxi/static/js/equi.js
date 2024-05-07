/*    RECURSOS DE EQUIPO Y SUS DETALLE  */

 
function OpenModalEqui(equi_id) {

	//Set Id 
	
	document.getElementById('id_equ').value = equi_id;

	//#ModalEquipoDetalle
	var modal_carg = '<tr><td style="text-align:center;">'+
		'<span><img src="/static/img/cargando.gif"></span> </td></tr>';

	// Activamos el modal con el gif
	var tab_modal = document.getElementById('tab_modal'); 
	tab_modal.innerHTML = modal_carg;

	// Obtenemos el Tr con los datos del equipo
	var tr_equi = document.getElementById(('tr_'+equi_id));

	// h3_tit SET TITLE
	document.getElementById('h3_tit').innerHTML =(tr_equi.cells[1].innerHTML+" : "+tr_equi.cells[2].innerHTML);

	// Get detail
	var cad = "/equ_det_lis/?ide="+equi_id;  

	//alert(cad);
	AjxSrvr(cad,PrintMdl);
}



// Imprimimos el detalle en el modal
function PrintMdl(jsn){
	//alert(jsn[0]);
	var tbody = '';
	var tab_modal = document.getElementById('tab_modal');


	if (jsn[0] != 'Ok') {

/*      Nee : No existe equipo
		Ned : No existe detalle     */
		switch (jsn[0]) {
			case 'Nee': alert('Equipo no encontrado');break;
			case 'Ned': alert('Sin cliente asignados');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
    	tab_modal.innerHTML = '';
	}
	else{

		// Set thead
		tbody += '<thead style="background:#90BFF3;font-weight: bold;"><tr><td>Código</td> <td>Cliente</td> ';
		tbody += '<td>País</td> <td>Alta</td> <td>Por</td> <td>estado</td> <td></td></tr></thead>';
		tbody += '<tbody id="id_tbody">';

		for (var i in jsn) { if (i > 0) {
        	var lstDet 	= jsn[i].split(',');
        	// Set TR
        	tbody += '<tr id="tr_de_'+lstDet[0]+'"> <td>'+lstDet[1]+'</td>'
        	tbody += '<td>'+lstDet[2]+'</td> <td>'+lstDet[3]+'</td> <td>'+lstDet[4]+'</td> '
        	tbody += '<td>'+lstDet[5]+'</td>'
        	tbody += '<td>'+lstDet[6]+'</td>'
        	tbody += '<td><button type="button" class="btn btn-sm btn-warning" onclick="RemoverCliente(this.id)" id="'+lstDet[0]+'">'
        	tbody += '<i class="fa fa-trash"></i></button></td> </tr>'
    	}}
		tbody += '</tbody>';

    	// imprimir
    	tab_modal.innerHTML = tbody;
	}
}







/*   Asociar */
function AgregarCliente() {
	// body...
	var sel_cli = document.getElementById('sel_cli');
	var id_equ = document.getElementById('id_equ').value;
	//alert('sel_cli : '+sel_cli.value+' del eq:'+id_equ);

	// Get detail
	var cad = "/equ_det_cre/?ide="+id_equ+'&idc='+sel_cli.value; 
	// ESTADO del requerimiento
	AjxSrvr(cad,AddRowDetEquipo);
}




/* agregar a la tabla el nuevo registro */
function AddRowDetEquipo(jsn){

	if (jsn[0] != 'Ok') {
/*      Nec : No existe cliente					
		Nee : No existe equipo	     */
		switch (jsn[0]) {
			case 'Nec': alert('No existe cliente');break;
			case 'Nee': alert('No existe equipo');break;
			case 'Yex': alert('Ya pertenece al equipo');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
	else{
		//alert(jsn[2]);
		var Det = jsn[2].split(',');
		var trn = '';

		if (document.getElementById('id_tbody')) { 

			var tbody = document.getElementById('id_tbody');
		    trn = '<tr id="tr_de_'+Det[0]+'"> <td>'+Det[1]+'</td>'
	    	trn += '<td>'+Det[2]+'</td> <td>'+Det[3]+'</td> <td>'+Det[4]+'</td> '
	    	trn += '<td>'+Det[5]+'</td>'
	    	trn += '<td>'+Det[6]+'</td>'
	    	trn += '<td><button type="button" class="btn btn-sm btn-warning" onclick="RemoverCliente(this.id)" id="'+Det[0]+'">'
	    	trn += '<i class="fa fa-trash"></i></button></td> </tr>'
	        tbody.innerHTML += trn;
		}
		else{
			var tab_modal = document.getElementById('tab_modal');
			tab_modal.innerHTML += '<thead style="background:#90BFF3;font-weight: bold;"><tr><td>Código</td> <td>Cliente</td> <td>País</td> <td>Alta</td> <td>Por</td> <td>estado</td> <td></td></tr></thead>';
		    tab_modal.innerHTML += '<tbody id="id_tbody"></tbody>';

			var tbody = document.getElementById('id_tbody');
		    trn = '<tr id="tr_de_'+Det[0]+'"> <td>'+Det[1]+'</td>'
	    	trn += '<td>'+Det[2]+'</td> <td>'+Det[3]+'</td> <td>'+Det[4]+'</td> '
	    	trn += '<td>'+Det[5]+'</td>'
	    	trn += '<td>'+Det[6]+'</td>'
	    	trn += '<td><button type="button" class="btn btn-sm btn-warning" onclick="RemoverCliente(this.id)" id="'+Det[0]+'">'
	    	trn += '<i class="fa fa-trash"></i></button></td> </tr>'
	        tbody.innerHTML += trn;
		}

			
	}
}




/* Eliminar detalle de Equipo/Cliente */
function RemoverCliente(idec) {

	if( confirm('¿Desea desasociar el cliente al equipo?')){
		var cad = "/equ_det_eli/?idec="+idec; 
		// ESTADO del requerimiento
		AjxSrvr(cad,RmvHtml);
	}
}

function RmvHtml(jsn) {
	if (jsn[0] != 'Ok') {
/*      Ned : No existe el detalle	  */
		switch (jsn[0]) {
			case 'Ned': alert('No se encontró en la ddbb');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
	else{
		//alert(jsn[2]);
		document.getElementById(('tr_de_'+jsn[2]+'')).remove();
	}
}