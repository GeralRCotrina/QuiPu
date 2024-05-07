
/*   TODOS LOS RECURSOS JS PARA LAS TASK  */
var aTaskList = [];
var req_id1 = 0;
var editFaseActividad;

function OpenModalTask(req_id, action = '0') {
	// Get row from Req....
	req_id1 = req_id;
	var pk_tr = 'tr_req'+req_id+'';
	var tr_req = document.getElementById(pk_tr);


	// SET TITLE TO MODAL
	var tit = (action ===  '1') ? tr_req.cells[6].innerHTML + ' : ' + tr_req.cells[7].innerHTML : tr_req.cells[10].innerHTML + ' : ' + tr_req.cells[11].innerHTML;
	document.getElementById('mdl_tit').innerHTML = tit;
	document.getElementById('req_id').value = req_id;


	// Set url
	var url  = document.getElementById('id_url').value;
	var btn_dwn = document.getElementById('id_href');
	btn_dwn.setAttribute('href',(''+url+'?req='+req_id+''));


	document.getElementById("titleReqModalTask").innerHTML = tit;
	document.getElementById("t_IdRequerimiento").value = req_id;
 
	let fechaHoy = new Date();
	//Seteo de fecha del sistema
	let year = fechaHoy.getFullYear();
	let month = fechaHoy.getMonth() + 1;
	if(month < 10) month= "0"+month;
	let day = fechaHoy.getDate();
	if(day < 10) day= "0"+day;
	let formatedDate = year + "-" + month + "-" + day; 

	document.getElementById("t_FechaInicio").value = formatedDate;
	document.getElementById("t_FechaFin").value = formatedDate;

	document.getElementById("t_EsfuerzoEjecutado").value = 0;

	// TRAER TAREAS EXISTENTES
	var cad = "/tsk_lst_ext/?idr="+req_id+"";
	AjxSrvr(cad,AgregarLista);


	


}

// Agregamos las tareas ya existentes a la lista
function AgregarLista(jsn){

	if (jsn[0] == 'ok') {

		LstTsk = {};
		for (var i in jsn) {
			if (i != '0') {
		        LstTsk = jsn[i].split('~');
			    var task = {
			    	idtsk_local : i,
			    	idtsk : LstTsk[0],
					codigo: LstTsk[1],
					idRequerimiento: req_id1,
			        subTarea: LstTsk[2],
			        faseActividad: LstTsk[3],
			        id_faseActividad: LstTsk[10], 
			        fechaInicio: LstTsk[4],
			        fechaFin: LstTsk[5],
			        esfuerzoTotEstandar: LstTsk[6],
					esfuerzoEjecutado: LstTsk[7], // amjo esfuerzo ejecutado 18/06/2021
					idEmpleado: LstTsk[9],
					Empleado: LstTsk[8],
					nombreEmpleado: LstTsk[8]
			    };
	    		aTaskList.push(task);
		    }
		}

		//task.nombreEmpleado = lst_usrs.find(user => user.id = task.idEmpleado);
		$('#id_addTask').show();
		$('#id_updateTask').hide();
	    ActualizarTabla();
		$('#msj_task_all').text('Task cargadas');
	}
	else{
		/*		ERRORES 
		Vac  = 'Sin task creadas'  */
		switch (jsn[0]) {
			case 'Vac': $('#msj_task_all').text('Aún sin task creadas');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}




// Creamos un id local para las task aún no guardadas.  // grcl4
function CrearIdLocal(cont){
    var idlcl = ('id_tsk_local_'+cont);
	if ( document.getElementById(idlcl) ){ idlcl = CrearIdLocal((cont + 1));  }
	return idlcl; 
}


function AgregarTask(){

	$('#msj_task_all').text('...');

	//Validación de inputs
	if (validateRequired()){
		//Variables
		var len_lst = aTaskList.length;
		var id_opt_usu = 'id_inp_usr_'+document.getElementById('t_idEmpleado').value;
		var idlcl =  CrearIdLocal(len_lst);
		var cmbFaseActividad = document.getElementById('t_FaseActividad');
		var task = {
			idtsk_local : idlcl,
			idtsk : 0,
			idRequerimiento: req_id1,
			subTarea: document.getElementById('t_Subtarea').value,
			faseActividad: cmbFaseActividad.selectedOptions[0].text,
			id_faseActividad: document.getElementById('t_FaseActividad').value ,
			fechaInicio:document.getElementById('t_FechaInicio').value,
			fechaFin: document.getElementById('t_FechaFin').value,
			esfuerzoTotEstandar:document.getElementById('t_EsfuerzTotalEstandar').value,
			esfuerzoEjecutado:document.getElementById('t_EsfuerzoEjecutado').value, //amjo esfuerzo ejecutado 18/06/2021
			idEmpleado: document.getElementById('t_idEmpleado').value,
			Empleado: document.getElementById(id_opt_usu).value, // grcl4
		};
		//task.nombreEmpleado = lst_usrs.find(user => user.id = task.idEmpleado);
		$('#id_addTask').show();
		$('#id_updateTask').hide();
		aTaskList.push(task);
		ActualizarTabla();
		CleanInput();

		document.getElementById("t_EsfuerzoEjecutado").value = 0;

	}else{
		alert("Por favor, llene todos los campos para agregar una tarea");
	}

}
function validateRequired(){
	if(document.getElementById('t_Subtarea').value === "") return false;
    else if(document.getElementById('t_FaseActividad').value === "") return false;
    else if(document.getElementById('t_FechaInicio').value === "") return false;
    else if(document.getElementById('t_FechaFin').value === "") return false;
    else if(document.getElementById('t_EsfuerzTotalEstandar').value === "") return false;
    else if(document.getElementById('t_EsfuerzoEjecutado').value === "") return false; //amjo esfuerzo ejecutado 18/06/2021
	else if(document.getElementById('t_idEmpleado').value === "") return false;
	else return true;
}
function CleanInput(){
	document.getElementById('t_Subtarea').value = "";
    document.getElementById('t_FaseActividad').value = "";
    document.getElementById('t_FechaInicio').value = "";
    document.getElementById('t_FechaFin').value = "";
    document.getElementById('t_EsfuerzTotalEstandar').value = "";
    document.getElementById('t_EsfuerzoEjecutado').value = ""; //amjo esfuerzo ejecutado 18/06/2021
	document.getElementById('aTaskList_poss').value = "";
	document.getElementById('t_idEmpleado').value = "";
}

function SetValuesToInput(poss){
	document.getElementById('t_Subtarea').value = aTaskList[poss].subTarea;
    document.getElementById('t_FaseActividad').value = aTaskList[poss].id_faseActividad;
    editFaseActividad = aTaskList[poss].faseActividad;
    document.getElementById('t_FechaInicio').value = aTaskList[poss].fechaInicio;
    document.getElementById('t_FechaFin').value = aTaskList[poss].fechaFin;
    document.getElementById('t_EsfuerzTotalEstandar').value = aTaskList[poss].esfuerzoTotEstandar;
	document.getElementById('t_EsfuerzoEjecutado').value = aTaskList[poss].esfuerzoEjecutado; //amjo esfuerzo ejecutado 18/06/2021
	document.getElementById('t_idEmpleado').value = aTaskList[poss].idEmpleado;
	document.getElementById('aTaskList_poss').value = poss;
	$('#id_addTask').hide();
	$('#id_updateTask').show();
}

function UpdateTask(){
	if(validateRequired()){
		var cmbFaseActividad = document.getElementById('t_FaseActividad');
		var poss = document.getElementById('aTaskList_poss').value;
		aTaskList[poss].subTarea= document.getElementById('t_Subtarea').value;
		aTaskList[poss].id_faseActividad = document.getElementById('t_FaseActividad').value;
		aTaskList[poss].faseActividad = cmbFaseActividad.selectedOptions[0].text;
		aTaskList[poss].fechaInicio = document.getElementById('t_FechaInicio').value;
		aTaskList[poss].fechaFin = document.getElementById('t_FechaFin').value;
		aTaskList[poss].esfuerzoTotEstandar = document.getElementById('t_EsfuerzTotalEstandar').value ;
		aTaskList[poss].esfuerzoEjecutado = document.getElementById('t_EsfuerzoEjecutado').value ; //amjo esfuerzo ejecutado 18/06/2021
		aTaskList[poss].idEmpleado = document.getElementById('t_idEmpleado').value;

		editFaseActividad = "";
		$('#id_addTask').show();
		$('#id_updateTask').hide();
		ActualizarTabla();
		CleanInput();
	}else{
		alert("No se puede registrar ningún campo vacío, por favor, llene todos los campos");
	}

}
function DeleteTask(pos){
	aTaskList.splice(pos,1);
	ActualizarTabla();
	CleanInput();
	$('#id_addTask').show();
	$('#id_updateTask').hide();
	$('#msj_task_all').text('...');

}

function ActualizarTabla(){
    //Eliminar datos de tabla
	$("#m_taskAdded").empty();
    // Cargar matriz actualizada 
	for (var i = 0; i < aTaskList.length; i++) {
				$("#m_taskAdded").append('<tr id="' + aTaskList[i].idtsk_local + '"><td>' + aTaskList[i].codigo + "</td>"
										 +"<td>" + aTaskList[i].subTarea + "</td>"
										 +"<td>" + aTaskList[i].faseActividad + "</td>"
										 +"<td>" + aTaskList[i].fechaInicio + "</td>"
										 +"<td>" + aTaskList[i].fechaFin + "</td>"
										 +"<td>" + aTaskList[i].esfuerzoTotEstandar + "</td>"
										 +"<td>" + aTaskList[i].esfuerzoEjecutado + "</td>" //amjo esfuerzo ejecutado 18/06/2021
										// +"<td>" + aTaskList[i].Empleado + "</td>" grcl4
										 +"<td>" + aTaskList[i].Empleado + "</td>"
										 +'<td><button class="btn btn-sm btn-warning" onClick=SetValuesToInput('+i+')><i class="fa fa-edit"></i></button>'
										 +'<button class="btn btn-sm btn-danger" onClick=DeleteTask('+i+')><i class="fa fa-trash"></i></button></td></tr>');			
			
	
	}
    
}

function validarFecha(){
	var fechaInicio =  document.getElementById('t_FechaInicio').value;
	var fechaFin= document.getElementById('t_FechaFin').value;

	if(fechaFin < fechaInicio){
		alert("La fecha de fin no puede ser menor que la fecha de inicio");
		document.getElementById('t_FechaFin').value = "";
	}
}


function SaveTasks(){
	$('#msj_task_all').text("...");
	var texto = "";
	var idr = document.getElementById('req_id').value;
	for(i=0;i<aTaskList.length;i++){
		if ( texto != '' ) { texto = texto + '~';  }  // grcl ++  Agrego separador para hacer el .plit() en el back
		texto = texto + JSON.stringify(aTaskList[i]); 
	}
	var cad = '/tsk_cre_lst/?idr='+idr+'&&jsn='+texto+' ' ;
	//alert(cad);
	AjxSrvr(cad,reloadPage);
}

// Recibimos el request y lo pintamos en el Dom
function reloadPage(jsn){
	if (jsn[0] == 'ok') {
		// Todo bien
		// Y actualizamos los códigos de las acc
		var lst = []
		for (var i in jsn) {
			if (jsn[i] != 'ok') {

	       		lst = jsn[i].split('~');

	       		if(document.getElementById(i)){
	       			// Obtebnemos la fila de la tabla para reescribir el código
	       			document.getElementById(i).cells[0].innerHTML = '<b>'+lst[1]+'</b>';
	       		}
			}
	    }
		$('#msj_task_all').text("Tareas actualizadas");
	}else{
		/*		ERRORES 
		ok  = 'Proceso finalizado correctamente'
		nrq = 'No existe requerimiento'  */
		document.getElementById(('td_sel_resp_'+idr)).style.background = '#FF99A0';
		switch (jsn[0]) {
			case 'nrq': alert('Requerimiento no encontrado');break;
			default: 	alert('Error en el servidor:'+jsn[0] );break;
		}
	}
}