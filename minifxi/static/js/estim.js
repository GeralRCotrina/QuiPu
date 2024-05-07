
/*   TODOS LOS RECURSOS JS PARA LA ESTIMACIÓN  */

 
function OpenModal(req_id) {
	
	// Get row from Req....
	var pk_tr = 'tr_req'+req_id+'';
	var tr_req = document.getElementById(pk_tr);


	// SET TITLE TO MODAL
	var tit = tr_req.cells[10].innerHTML + ' : ' + tr_req.cells[11].innerHTML;
	document.getElementById('mdl_tit').innerHTML = tit;
	document.getElementById('req_id').value = req_id;


	// Set url
	var url  = document.getElementById('id_url').value;
	var btn_dwn = document.getElementById('id_href');
	btn_dwn.setAttribute('href',(''+url+'?req='+req_id+''));


	// TRAER ESTIMACIONES PREVIAS
	CargandoGif(1);
		var cad = "/etimdet_lis/?req="+req_id+"";

		var xhr = new XMLHttpRequest();
		xhr.open('GET',cad,true); 
		xhr.onreadystatechange = function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				// Err = Error en el servidor
				// sde = Sin estimaciones
				if( xhr.response == 'Err' || 
					xhr.response == 'sde' ){
					switch (xhr.response) {
						case 'Err': alert('Error en el server: ' + xhr.response );break;
						case 'ndf': alert('Sin estimaciones' );break;
					}
					CargandoGif(2);
				} 
				else{
					// 
					var tbody = document.getElementById('id_estim_tbody');
					var tr0 = '';
					var json = xhr.response
					var result = JSON.parse(json) || {};
					var cont = 0;
					var lstJS ;
					document.getElementById('sel_tipo').value=result.req.idtipo_peticion;
					document.getElementById('sel_tipo_descripcion').value=result.req.tipo;
					document.getElementById('sel_estimacion_aprobada').value=result.req.estimacion_aprobada;
					document.getElementById('id_aprobar').style.visibility=result.req.estimacion_aprobada?'hidden':'visible';
					for (var i in result.detalle) {
						// console.log("  >> i:"+i+"    lstTmp[i]:"+lstTmp[i])
				        lstJS = result.detalle[i];

						// Values
						 tr0 += '<tr id="tr_estim_'+ lstJS[0] +'"><td style="text-transform:uppercase">' + lstJS[1] + '</td>'
								 +'<td style="text-transform:uppercase">' + lstJS[2] + '</td>'
								 +'<td style="text-transform:uppercase">' + lstJS[3] + '</td>'
								 +'<td >' + lstJS[11] + '</td>'//ecarpiod
								 +'<td id="td_esf_'+ lstJS[0] +'">' + lstJS[4] + '</td>'
						        + '<td width="10px"  ondblclick="AgregarAjuste(this.id)" id="ajst0_'+lstJS[0]+'" style="background: #F9F9F9;">'+lstJS[7]+'</td>'
						        + '<td width="190px;"  ondblclick="AgregarAjuste(this.id)" id="ajst1_'+lstJS[0]+'" style="background: #F9F9F9;">'+lstJS[8]+'</td>'
						        + '<td> <div class="dropdown"><div class="btn-group" role="group" aria-label="Basic example">'
						        + '<button class="btn btn-sm btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"'
								+ ' aria-haspopup="true" aria-expanded="false"> <i class="fa fa-eye"></i> </button>'
								+ '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton" '
								+    'style="background:#D3E9FD;color:#707BA8; font-size:1.0em;font-weight:normal;">'
								+    '<p class="dropdown-item">Creado por  '+ lstJS[5] +' , el ' + lstJS[6] + '</p>';
						//alert("  lstJS[9] = "+ String(lstJS[9]) );
						if ( lstJS[7] > 0) {
							tr0 +='<p class="dropdown-item">Se ajustó por '+ lstJS[9] +' , el ' + lstJS[10] + '</p>';
						}  
						
						tr0 +=  '</div><button type="button" class="btn btn-sm btn-warning" onclick="BtnEliminarEstim(this.id)" id="'+ lstJS[0] +'" >'
							+ '<i class="fa fa-trash"></i></button></div></div></td></tr>';

				    }
					// Set value
					tbody.innerHTML = tbody.innerHTML + tr0;

					// Recalcular acumulado
					RecalcularTotal();

					CargandoGif(2);
				}
			}
		}
		xhr.send();


}







/*   ==============  AL USAR LOS SELECT  ==================== */
function ChngEstim(){
	//  ...
	var tip = document.getElementById('sel_tipo').value;
	var sub = document.getElementById('sel_subtipo').value;
	var dif = document.getElementById('sel_dificultad').value;
	var btn  = document.getElementById('id_agregar');
	var pes  = document.getElementById('esfuerzo');

	//
	if (tip > 0 && sub > 0 && dif > 0) {

		// Traer pero 
		CargandoGif(1);
		var cad = "/etimdet_peso/?tip="+tip+"&&sub="+sub+"&&dif="+dif+"&&cli=30";

		var xhr = new XMLHttpRequest();
		xhr.open('GET',cad,true); 
		xhr.onreadystatechange = function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				if( xhr.response == 'ne'){
					alert('Peso no configurado.');
					CargandoGif(2);
				} 
				else if ( xhr.response == 'm2'){
					alert('Varios pesos para dicha configuración, revisar con el líder.');
					CargandoGif(2);
				}
				else{
					// Set Peso
					pes.value = parseFloat( xhr.response );
					// Enables buttom
					btn.removeAttribute('disabled');
					CargandoGif(2);
				}
			}
		}
		xhr.send();

	}else{
		// Disabled buttom
		btn.setAttribute('disabled','disabled');
	}
}




/*   ==============  AL APROBAR ESTIMACIÓN: ECARPIOD  ==================== */

function BtnAprobeEstim(){
	var req_id = document.getElementById('req_id').value;
	CargandoGif(1);
	$.ajax({
		type:'GET',
		url:`/etimdet_apro/?req=${req_id}`,
		dataType:'json',
		success:function(data,textStatus,jqXHR){
			CargandoGif(2);
			if(data.result){
				document.getElementById('id_aprobar').style.visibility='hidden';
				// var url  = document.getElementById('id_url').value;
				// window.location.replace(`${url}?req='${req_id}'`);
			}else{
				alert(`${data.message}`);
			}
		},
		error:function(){
			CargandoGif(2);
			alert('Error en el server');
		}
	})
}


/*   ==============  AL AGREGAR ESTIMACIÓN  ==================== */
function BtnAddEstim(){

	// Variables
	var tr0 = '';
	var alias = '';
	var fecha = '';
	var idest = '';
	var tbody = document.getElementById('id_estim_tbody');

	var req = document.getElementById('req_id');
	var tip = document.getElementById('sel_tipo');
	var tip_des = document.getElementById('sel_tipo_descripcion');
	var sub = document.getElementById('sel_subtipo');
	var dif = document.getElementById('sel_dificultad');
	var esf = document.getElementById('esfuerzo').value;

	// CREAR EN EL SERVIDOR //
	CargandoGif(1);
	var cad = "/etimdet_cre/?req="+req.value+"&&tip="+tip.value+"&&sub="+sub.value;
	var cad = cad +"&&dif="+dif.value+"&&esf="+esf;

	var xhr = new XMLHttpRequest();
	xhr.open('GET',cad,true); 
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			if( xhr.response == 'Err' ||
			     xhr.response == 'ndf' ||
			     xhr.response == 'nsb' ||
			     xhr.response == 'nti' ||
			     xhr.response == 'nrq' ){
				/*
				Err = Error en el servidor
				ndf = Dificultad no encontrada
				nsb = Subtipo no encontrado
				nti = Tipo no encontrado
				nrq = Requerimiento no encontrado.
				*/
				switch (xhr.response) {
					case 'Err': alert('Error en el server: '+xhr.response );break;
					case 'ndf': alert('Dificultad no encontrada' );break;
					case 'nsb': alert('Subtipo no encontrado' );break;
					case 'nti': alert('Tipo no encontrado');break;
					case 'nrq': alert('Requerimiento no encontrado');break;
				}
				CargandoGif(2);

			}else{
				var rpta = xhr.response
				var myObj = JSON.parse(rpta);
				alias   = myObj['alias']; 
				fecha 	= myObj['fecha']; 
				idest 	= myObj['idest']; 
				CargandoGif(2);


				// Values
				tr0 = '<tr id="tr_estim_'+idest+'"><td style="text-transform:uppercase">' + tip_des.value + '</td>'
						+'<td style="text-transform:uppercase">' + sub.options[sub.selectedIndex].text + '</td>'
						+'<td style="text-transform:uppercase">' + dif.options[dif.selectedIndex].text + '</td>'
						+'<td>' + esf + '</td>'//+ecarpiod
						+'<td id="td_esf_'+ idest +'">' + esf + '</td>'
				        + '<td width="10px"  ondblclick="AgregarAjuste(this.id)" id="ajst0_'+idest+'" style="background: #F9F9F9;"></td>'
				        + '<td width="190px;"  ondblclick="AgregarAjuste(this.id)" id="ajst1_'+idest+'" style="background: #F9F9F9;"></td>'
				        + '<td> <div class="dropdown"><div class="btn-group" role="group" aria-label="Basic example">'
				        + '<button class="btn btn-sm btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"'
						+ ' aria-haspopup="true" aria-expanded="false"> <i class="fa fa-eye"></i> </button>'
						+ '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton" '
						+    'style="background:#D3E9FD;color:#707BA8; font-size:1.0em;font-weight:normal;">'
						+    '<p class="dropdown-item">Creado por ' + alias + ', el '+ fecha + '</p></div>'
						+  '<button type="button" class="btn btn-sm btn-warning" onclick="BtnEliminarEstim(this.id)" id="'+ idest +'" >'
						+ '<i class="fa fa-trash"></i></button></div></div></td></tr>';

				// Set value
				tbody.innerHTML = tbody.innerHTML + tr0;

				// Recalcular acumulado
				 RecalcularTotal();

			}
		}
	}
	xhr.send();



}


/*
	// Values
	tr0 = '<tr><td style="text-transform:uppercase">' + tipo.options[tipo.selectedIndex].text + '</td>'
			 +'<td style="text-transform:uppercase">' + subt.options[subt.selectedIndex].text + '</td>'
			 +'<td style="text-transform:uppercase">' + difi.options[difi.selectedIndex].text + '</td>'
			 +'<td>' + esfu + '</td>'
	        + '<td width="10px"><input type="number" step="0.5" style="width: 50px;"></td>'
	        + '<td width="170px;">Corrección de código previo no estimado inicialmente.</td>'

	        + '<td> <div class="dropdown"><div class="btn-group" role="group" aria-label="Basic example">'
	        + '<button class="btn btn-sm btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"'
			+ ' aria-haspopup="true" aria-expanded="false"> <i class="fa fa-eye"></i> </button>'
			+ '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton" '
			+    'style="background:#D3E9FD;color:#707BA8; font-size:1.0em;font-weight:normal;">'
			+    '<p class="dropdown-item">Creado por Geral Cotrina, el 11.04.2021</p>'
			+    '<p class="dropdown-item">Ajuste por Geral Cotrina, el 11.04.2021</p>  </div>'
			+  '<button type="button" class="btn btn-sm btn-warning"><i class="fa fa-trash"></i></button>'
			+ '</div></div></td></tr>';
*/






// Clear before information in MODAL
/*   ============== LIMPIAR EL MODAL  ==================== */
function ClearMDL(action = '0'){

	// Delete title
	document.getElementById('mdl_tit').innerHTML = '';
	if (action === '0'){
		// Delete values
		document.getElementById('sel_tipo').value = 0;
		document.getElementById('sel_tipo_descripcion').value = '';
		document.getElementById('sel_estimacion_aprobada').value=null;
		document.getElementById('id_aprobar').style.visibility='hidden';
		document.getElementById('sel_subtipo').value = 0;
		document.getElementById('sel_dificultad').value = 0;
		document.getElementById('esfuerzo').value = 0;

		// Delete body of table
		document.getElementById('id_estim_tbody').innerHTML = '';

		// Delete total
		document.getElementById('id_estim_total').innerHTML = '0h';
	}

	// Remove link
	document.getElementById('id_href').removeAttribute('href');
	window.location.replace('')

}









/*   ==============  ELIMINAR TAREA DE ESRTIMACIÓN  ==================== */
function BtnEliminarEstim(detest_id){

	// Confirmación 
	if( confirm('¿Desea eliminar la tarea?')){

		CargandoGif(1);
		var cad = "/etimdet_eli/?detest="+detest_id+"";

		var xhr = new XMLHttpRequest();
		xhr.open('GET',cad,true); 
		xhr.onreadystatechange = function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				if( xhr.response == 'Ok'){
					// Se eliminó con éxito

					// tr_estim_
					var id_tr = '#tr_estim_' + detest_id + '';
					$(id_tr).remove();
					// Recalcular total
					 RecalcularTotal();

					CargandoGif(2);
				}
				else{
					switch (xhr.response) {
							case 'nde': alert('No se encontró el datalle de la estimación');break;
							default: alert('Error no mapeado');break;
						}
					CargandoGif(2);
				}
			}
		}
		xhr.send();
	}
}






/*   ==============  	RECALCULAR EL TOTAL DE LA ESTIMACIÓN  ==================== */
function RecalcularTotal(){
	// Recalcualr acumulado
	var total_col1 = 0;
	$('#id_estim_tbody').find('tr').each(function (i, el){
		total_col1 += parseFloat($(this).find('td').eq(4).text());//+ecarpiod 4
	});
	document.getElementById('id_estim_total').innerHTML = total_col1 + 'h';
	if(total_col1 === 0){
		document.getElementById('id_aprobar').style.visibility='hidden';
		document.getElementById('id_href').style.visibility='hidden';
	}else{

		document.getElementById('id_aprobar').style.visibility=parseInt(document.getElementById('sel_estimacion_aprobada').value,10)?'hidden':'visible';
		document.getElementById('id_href').style.visibility='visible';
	}
	

}







/*   ==============  	AGREGAR AJUSTE - A J U S T E   ==================== */
function AgregarAjuste(detest_id){
	//" id="ajst0_'+ lstJS[1] +'"
	var id0 = detest_id.substring(6);

	var td00 = document.getElementById(('ajst0_'+id0+''));
	td00.innerHTML = '<input type="number" step="0.25" id="ajst_inpt1_'+id0+'" style="width:60px;" value="'+td00.innerHTML+'">';

	var td01 = document.getElementById(('ajst1_'+id0+''));
	td01.innerHTML = `
		<div class="row">
			<div class="col-sm-8" style="padding:0">
			<textarea type="text" maxlength="100" id="ajst_inpt2_${id0}">${td01.innerHTML}</textarea>
			</div>
			<div class="col-sm-4" style="padding:0">
				<a class="btn btn-sm  active" onclick="AjusteGuardar(${id0})"><i class="fa fa-save"></i></a>
			</div>
		</div>
	`;

	// Quitamos el evento doble click

	td00.removeAttribute('ondblclick');
	td01.removeAttribute('ondblclick');

}





/*   ==============  	AL ESCRIBIR EN EL AJUSTE - A J U S T E   ==================== */
function AjusteGuardar(ids){
	//alert("OK");

	var ip1 = document.getElementById(('ajst_inpt1_'+ids+'')).value;
	var ip2 = document.getElementById(('ajst_inpt2_'+ids+'')).value;

	if( ip1 == 0 || ip2.length == 0 ){
		alert("Completar ambos campos");
	}else{
		//
  		if( confirm('¿Desea ajustar el peso de la tarea con ('+ip1+'), por el motivo "'+ip2+'"?')){

			var td_esf = document.getElementById(('td_esf_'+ids+''))			
			/***-------------------------------------------------------------***/
			CargandoGif(1);
			var cad = "/etimdet_ajs/?det="+ids+"&&ajs="+ip1+"&&des="+ip2+"";
			var xhr = new XMLHttpRequest();
			xhr.open('GET',cad,true); 
			xhr.onreadystatechange = function(){
				if(xhr.readyState == 4 && xhr.status == 200){
					switch(xhr.response){
						case 'sde': alert('No se encontró el datalle de la estimación');break;
						case 'dne': alert('Detalle no encontrado');break;
						case 'var': alert('Varios pesos conficurado para la msima convinació');break;
						default: td_esf.innerHTML = ''+ xhr.response + ''; break;
					}
					// Reclarcualr total
					RecalcularTotal();
				}
			}
			xhr.send();
			CargandoGif(2);

			/***-------------------------------------------------------------***/

			
  		}
	}
}

								/*
								sde = No se encontró el datalle de la estimación
								dne = Detalle no encontrado
								var = Varios pesos conficurado para la msima convinació*/