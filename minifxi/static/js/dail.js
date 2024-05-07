/*   TODOS LOS RECURSOS JS PARA EL DAILY  */



/* Globals variabels */
var idr, col, val;




/*  Main Logic */


function ChngClr(zidr,zcol,zval) {

	/* Set variables */
	idr = zidr; col = zcol; val = zval;

	// 1° -> Actualizadoms la ddbb
	var cad = "/dai_upd/?idr="+idr+"&&col="+col+"&&val="+val;  // alert(cad);
	if (col == 'est') {
		// ESTADO del requerimiento
		AjxSrvr(cad,UpdDomEst);

	}else if(col == 'prio') {
		// PRIORIDAD del requerimiento
		AjxSrvr(cad,UpdDomPrio);

	}else if(col == 'f_ini') {
		// FECHA INICIO del requerimiento
		AjxSrvr(cad,UpdDomF_Ini);

	}else if(col == 'cont') {
		// CONTACTO del requerimiento
		AjxSrvr(cad,UpdDomCont);

	}else if(col == 'cld') {
		// CALIDAD DEL IMPUT del requerimiento
		AjxSrvr(cad,UpdDomCld);

	}else if(col == 'bit') {
		// BITÁCORA del requerimiento
		AjxSrvr(cad,UpdDomBit);

	}else if(col == 'resp') {
		// REAPONSABLE del requerimiento
		AjxSrvr(cad,UpdDomResp);

	};

}



// 'NUsr"'  # Usted No está asignado a ese cliente.


/*   Actualización en el DOM : BITÁCORA   */
function UpdDomResp(jsn){

	if (jsn[0] == 'ok') {
		// Todo bien
		document.getElementById(('td_sel_resp_'+idr)).style.background = '#F5FFF2';

	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		document.getElementById(('td_sel_resp_'+idr)).style.background = '#FF99A0';
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			case 'NUsr': alert('Usted actualmente no está asignado a ese cliente.');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}




/*   Actualización en el DOM : BITÁCORA   */
function UpdDomBit(jsn){

	if (jsn[0] == 'ok') {
		// Todo bien
		document.getElementById(('td_bit_'+idr)).style.background = '#F5FFF2';

	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		document.getElementById(('td_bit_'+idr)).style.background = '#FF99A0';
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			case 'NUsr': alert('Usted actualmente no está asignado a ese cliente.');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}





/*   Actualización en el DOM : CALIDAD DEL IMPUT   */
function UpdDomCld(jsn){

	// alert(" >>> "+jsn[0]);
	if (jsn[0] == 'ok') {
		// Todo bien
		document.getElementById(('td_sel_cld_'+idr)).style.background = '#F5FFF2';

	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		document.getElementById(('td_sel_cld_'+idr)).style.background = '#FF99A0';
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			case 'NUsr': alert('Usted actualmente no está asignado a ese cliente.');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}




/*   Actualización en el DOM : FECHA INICIO  */
function UpdDomCont(jsn){

	// alert(" >>> "+jsn[0]);

	if (jsn[0] == 'ok') {
		// Todo bien
		document.getElementById(('td_cont_'+idr)).style.background = '#F5FFF2';

	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		document.getElementById(('td_cont_'+idr)).style.background = '#FF99A0';
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			case 'NUsr': alert('Usted actualmente no está asignado a ese cliente.');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}



/*   Actualización en el DOM : FECHA INICIO  */
function UpdDomF_Ini(jsn){

	// alert(" >>> "+jsn[0]);

	if (jsn[0] == 'ok') {
		// Todo bien
		document.getElementById(('td_f_ini_'+idr)).style.background = '#F5FFF2';

	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		document.getElementById(('td_f_ini_'+idr)).style.background = '#FF99A0';
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			case 'NUsr': alert('Usted actualmente no está asignado a ese cliente.');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}




/*   Actualización en el DOM : PRIORIDAD  */
function UpdDomPrio(jsn){

	// alert(" >>> "+jsn[0]);

	if (jsn[0] == 'ok') {
		// Todo bien
		var color = document.getElementById(('inp_sel_prio_'+val)).value;
		document.getElementById(('td_sel_prio_'+idr)).style.background = color;

	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			case 'NUsr': alert('Usted actualmente no está asignado a ese cliente.');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}




/*   Actualización en el DOM : ESTADO  */
function UpdDomEst(jsn){

	// alert(" >>> "+jsn[0]);

	if (jsn[0] == 'ok') {
		// Todo bien
		var color = document.getElementById(('inp_sel_est_'+val)).value;
		document.getElementById(('td_sel_est_'+idr)).style.background = color;

		// Solo para el menu princopal
		if( document.getElementById(('td_sel_est_P'+idr)) )
		{
			document.getElementById(('td_sel_est_P'+idr)).style.background = color;
			document.getElementById(('td_sel_est_P'+idr)).innerHTML = ""+document.getElementById(('inp_sel_est_T'+val)).value + "";
		}

	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			case 'NUsr': alert('Usted actualmente no está asignado a ese cliente.');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}












// ========================================================================= \\

function ConsultarDaily() {
	// body...
	var url = document.getElementById('input_url').value;
	var fecha_desde1 = document.getElementById('fecha_desde1').value;
	var fecha_hasta1 = document.getElementById('fecha_hasta1').value;

	var f1 = new Date(fecha_desde1);
	var f2 = new Date(fecha_hasta1);
	    
	if(f1 == 'Invalid Date' || f2 == 'Invalid Date' ){
	    alert("Ingrese rango de fechas correcto.");
	}
	else{
		if (f1 > f2) {
			var ft = fecha_desde1;
			fecha_desde1 = fecha_hasta1;
			fecha_hasta1 = ft;
		}

		// Clientes
		var equ = document.getElementById('sel_equipo').value;

		url = "/dai_lis/?fecha_desde='"+fecha_desde1+"'&&fecha_hasta='"+fecha_hasta1+"'&&equ="+equ;		
		window.location.href = url
	}
	
}




// ==================== F I L T R O S   D E   S T A T U S ===================== \\

// Abre el modal de filtros
function CrgrFltrs(){
	//alert('Alerta');  //  ModalExcluir
	window.location.href = '#ModalExcluir';
}


// Agrega estados al filtro
function AgrgrExcl(){

	// Traer el id del estatus 
	var idx = document.getElementById('id_sel_sta_excl').value

	// Traer el id del estatus
	var idc = document.getElementById('id_cliente').value

	// Taemos el nombre del status 
	var nom = document.getElementById(('id_status_nomre_'+idx)).value

	// Taemos el color del status 
	var col = document.getElementById(('id_status_color_'+idx)).value
	col = col.slice(1)

	// Construímos los código para guardar el el hardcode
	var cad = '/hrd_svd/?app=gest&&asp=esta&&typcon=clie&&consum='+idc
	cad = cad + '&&item=excl_sta&&val01='+idx+'&&val02='+nom+'&&val03='+col+'';

	// Guardar en el server
	AjxSrvr(cad,AgrgrDom);

}


// Agregar el nuevo filtro al Dom
function AgrgrDom(jsn){
	// Agregamos a la tabla
	if (jsn[0] == 'ok') {
		// Todo bien
		var tab = document.getElementById('id_sta_excl')
		var cad = '<i style="border-radius:2px;border:solid #DAD8D8 1px; background:#'+jsn['val03']+';" id="tab_sta_excl_'+jsn['val01']+'">'
		cad = cad + jsn['val02'] + '<i class="inv">_</i><a onclick="ElimStaExc('+jsn['id']+')">'
		cad = cad + '<i class="fa fa-trash" style="color: red;"></i></a></i><i class="inv">__</i>'
		tab.innerHTML = tab.innerHTML + cad
	}else{
		/*		ERRORES   */
		alert('Error en el servidor:'+jsn[0] );
	}
}


// Elimina en el servidor el estado filtrado
function ElimStaExc(idh){
	//
	var cad = '/hrd_rmv/?idh='+idh;
	// Guardar en el server
	AjxSrvr(cad,ElimStaDom);
}



// Elimina en el Dom el esatdo filtrado
function ElimStaDom(jsn){
	if (jsn[0] == 'ok') {
		// Todo bien
		document.getElementById(('tab_sta_excl_'+jsn['val01'])).remove();
	}else{
		switch (jsn[0]) {
			case 'Noe': alert('Dato no encontrado');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}
