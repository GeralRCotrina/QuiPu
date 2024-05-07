
/*&----------------------------------------------------------------------* 
*  GANT.JS          Construcción del gant en el front
*  Descripción.:    Se realiza en el front por su versatilidad.
*
*&----------------------------------------------------------------------* 
*  Author:  GRCL
*  Date:    00.00.2020
*  Company:**
*&----------------------------------------------------------------------* 
*  Modifications
*
*  Author:        GRCL        mark:  @001
*  Date:          13.08.2020
*  Description:   BUG01 :- Cuando cae fecha 1 y día de la semana sábado,
*                tiene que saltarse la primera semana.
*&----------------------------------------------------------------------* /

 
 /* window.onload = function() { }   en el JS  */

// Coloca el mes
function ColocarHora() {
	var fh = new Date();
	var mes = fh.getMonth() + 1;
	if (mes < 10) { mes = '0' + mes }
	document.getElementById('input_mes').value = "" + fh.getFullYear() + "-" + mes + "";
}




// datos del servidor ..............

var Gjson = {}		//		Registros del gant. { llave : [cod_reque, imputación]}
var lstCOL = [];		//		Lista de colaboradores
var lstIDs = [];		//		Lista de IDs de los colaboradores
var lstNlb = [];		//		Lista de días no lavorables
var id_Cli = 0;		// 		Id del cliente
var cant_dias = 0;		//		Cantidad de días del mes
var cant_rep = 0; 		// 		Cantidad de repeticiones del colaborador en la lista
var gant_html = ""; 		//		Gante en HTML.
var cant_col = 0;  		// 		Obtenemos cantidad de colaboradores
var col_span = 0;  		//		Cantidad filas que ocuparan
var cliente = "";		//		Cliente
var var_fts = "";		// 		Concepto del cliente
var mes = "";
var anio = "";
var anio_red = "";
var sem = 1;
var val_sem = true;		// 		Validación para que la sem aumente solo los sábados
var pais = "";

var fecha_desde = "";
var fecha_hasta = "";





function CargarGant() {

	// Variables Locales
	CargandoGif(1);

	// Lógica

	LimpiarVariables();		// 		Limpiamos todas las variables generales.

	input_mes = document.getElementById('input_mes').value;				// 		Cantidad de repeticiones del colaborador en la lista.
	id_Cli = document.getElementById('sel_cliente').value;				// 		Id del cliente.
	cant_rep = document.getElementById('sel_repet').value;				// 		Id del cliente.
	mes = input_mes.substring(5, 7);									//		Mes
	anio = input_mes.substring(0, 4);									//		Año.
	anio_red = input_mes.substring(2, 4);									//		Año reducido.
	cant_dias = UltimoDia(anio, mes);										//		Cantidad de días del mes.

	fecha_desde = anio + "-" + mes + "-01";
	fecha_hasta = anio + "-" + mes + "-" + cant_dias;


	// 1°
	ObtAsig(id_Cli);								// 		Trae datos del equipo y cliente.

	// 2°
	// TaerGant(id_Cli,fecha_desde,fecha_hasta);	//		Trae datos de incurrido planificado en gant

	// 3°
	// InsertarEnElDom();							//		Construye el HTML y lo inserta				
	//	3.1 -> construye cabecera
	//	3.2 -> construye cuerpo de la tabla
	//	3.3 -> construye pié de la tabla de gant
}







// último día del mes
function UltimoDia(y, m) {
	ddi = new Date();
	ddi.setFullYear(y, m, 0);
	return ddi.getDate();
}





/* 		O B T   A S I G          */
// Devuelve las asignaciones y más, para el cliente seleccionado
function ObtAsig(idc) {
	//CargandoGif(1);
	var xhr = new XMLHttpRequest();
	var cad = "/gnt_asg/?idc=" + idc + '&&anio=' + anio + '&&mes=' + mes + "&&fecha_desde=" + fecha_desde + "&&fecha_hasta=" + fecha_hasta;
	xhr.open('GET', cad, true);
	xhr.onreadystatechange = function () {
		if (xhr.readyState == 4 && xhr.status == 200) {
			rpta = xhr.response;
			var myObj = JSON.parse(rpta);
			if (myObj['msj'] == 'Ok') {
				rpta = "";
				lstCOL = myObj['lstCOL'].split(',');
				lstIDs = myObj['lstIDs'].split(',');
				cliente = myObj['Cli'];
				pais = myObj['Pai'];
				var_fts = myObj['Fte'];
				lstNlb = myObj['lstNlb'].split('~');  // 
				var StrJsn = myObj['StrJsn'];  // Traer datos del incurrido 

				cant_col = lstCOL.length;  											// 		Obtenemos cantidad de colaboradores.
				col_span = cant_col * cant_rep; 									//		Cantidad filas que ocuparan.

				// Le damos el formato de Json
				StrJsn = StrJsn.replace(/°/g, '"');
				lstTmp = JSON.parse(StrJsn);
				for (var i in lstTmp) {
					//console.log("  >> i:"+i+"    lstTmp[i]:"+lstTmp[i])
					Gjson[i] = lstTmp[i].split(',');
				}

				// Pintamos el Dom
				InsertarEnElDom();

			} else {
				alert("No se escontraron asignaciones para el cliente.");
			}
		}
	}
	xhr.send();
	//CargandoGif(2);
}










/*     R E G I S T R A R   G A N T          */

function RegHoras(ide, val) {

	var ArrE = ide.split('_');
	// 	idr ,   1   ,   25   ,   1   ,   1
	// tipo	|	id_Cli 	|	idCol 	| Posición | día
	//------------------------------
	//	idr_CLI_COL_AA_MM_SEM_DIA_POS

	if (ArrE[0] == 'idr') {
		if (val.length >= 11) {		//	Valida para registrar.
			var rpta1 = validarOtroValor(0, ide)
			if (rpta1 != 'Null') {
				ValidReq(ide, val, rpta1)
			}
		} else if (val.length == 0) {	//	Valida para eliminar.
			var rpta1 = validarOtroValor(0, ide)
			if (rpta1 == 'Null') {
				ValidBorrado(ide);
			}
		}
	} else if (ArrE[0] == 'idi') {
		if (val != '') {			//	Valida para registrar.
			var rpta1 = validarOtroValor(1, ide)
			if (rpta1 != 'Null') {
				ValidReq(ide, rpta1, val);
			}
		} else if (val.length == 0) {	//	Valida para eliminar.
			var rpta1 = validarOtroValor(1, ide)
			if (rpta1 == 'Null') {
				ValidBorrado(ide);
			}
		}
	} else { alert("Err0 id td JS"); }
}




/*   Validamos que tenga imputación o vise versa */
function validarOtroValor(tp, ide) {
	var rpta2 = 'Null';
	var cad = ide.substring(3, ide.length)
	if (tp == 0) { cad = 'idi' + cad; } else { cad = 'idr' + cad; }
	cad = document.getElementById(cad).value;
	if (cad != '') {
		rpta2 = cad;
	}
	return rpta2;
}




/*   	V A L I D A R   R E Q U E   */
function ValidReq(ide, val_1, val_2) { // Vamos a las validaciones en el servidor

	var xhr = new XMLHttpRequest();
	CargandoGif(1);
	var cad = "/gnt_c1/?ide=" + ide + "&&val_1=" + val_1 + "&&val_2=" + val_2 + "&&mes=" + mes + "&&anio=" + anio;
	xhr.open('GET', cad, true);
	xhr.onreadystatechange = function () {

		if (xhr.readyState == 4 && xhr.status == 200) {

			switch (xhr.response) {
				case 'NAsi': alert("Colaborador No está asignado a ese cliente (Solicite a un líder que lo asigne)."); break;
				case 'NUsr': alert("Usted no tiene asignación aquí, nopuede modificar.");
					document.getElementById(ide).removeAttribute('onblur');
					break;
				case 'NCli': alert("No existe el cliente."); break;
				case 'NAut': alert("No existe el Colaborador."); break;
				case 'NReq': alert("Requerimiento no encontrado, verifique el código."); break;
				case 'NRaC': alert("Requerimiento no pertenece al cliente."); break;
				case 'Much': alert("Mas de un requerimiento con ese código."); break;
				/*case 'ACT': alert("Actualizó con éxito.");break;
				case 'NAC': alert("No e snecesario actualizar, imputaciones iguales.");break;*/
				default:
					//console.log(" ok :->"+xhr.response+"      :::::::: "+ide); 
					var resp = xhr.response.split('~');
					if (resp[0] == 'ACT' || resp[0] == 'REG') {
						var idtr = 'idtr' + ide.substr(3);
						var idti = 'idti' + ide.substr(3);
						document.getElementById(idtr).style.backgroundColor = resp[1];
						document.getElementById(idti).style.backgroundColor = resp[1];
					}
					break;
			}
			return;
		}
	}
	xhr.send();
	CargandoGif(2);
}

/*  Estado
"NCli" # No existe el cliente.
"NAut" # No existe el AuthUser.
"NReq" # No existe el req.
"NRaC" # Req no pertenece al cliente.
"NAsi" # No está asignado a ese cliente.
*/



/*   	V A L I D A R   B O R A D O   */
function ValidBorrado(ide) { // Vamos a las validaciones en el servidor

	var xhr = new XMLHttpRequest();
	CargandoGif(1);
	var cad = "/gnt_vd1/?ide=" + ide; //grcl4
	xhr.open('GET', cad, true);
	xhr.onreadystatechange = function () {
		if (xhr.readyState == 4 && xhr.status == 200) {

			switch (xhr.response) {
				case 'NAsi': alert("Colaborador No está asignado a ese cliente (Solicite a un líder que lo asigne)."); break;
				case 'NUsr': alert("Usted no tiene asignación aquí, nopuede modificar.");
					document.getElementById(ide).removeAttribute('onblur');
					break;
				case 'Exi': var resp = confirm("¿Desea eliminar de forma permanente el registro?");
					if (resp) { BorraRegistro(ide); } break;
				case 'Nex':/* alert("No existe en la bd.");*/break;
				case 'Npe': alert("Solo el usuario responsable puede eliminar su imputación."); break;
				default: alert(" Err: " + xhr.response); break;
			}
		}
	}
	xhr.send();
	CargandoGif(2);
}

/*  Estados
"Nex" #	No existe nada que boorar
'Exi' #	Si existe nada que boorar
'Npe' #	No permisos para borrar.
*/



/*   	V A L I D A R   B O R A D O   */
function BorraRegistro(ide) { // Vamos a las validaciones en el servidor

	var xhr = new XMLHttpRequest();
	CargandoGif(1);
	var cad = "/gnt_d1/?ide=" + ide;
	xhr.open('GET', cad, true);
	xhr.onreadystatechange = function () {
		if (xhr.readyState == 4 && xhr.status == 200) {

			if (xhr.response == 'Ok') {
				var idtr = 'idtr' + ide.substr(3);
				var idti = 'idti' + ide.substr(3);
				document.getElementById(idtr).style.backgroundColor = '';
				document.getElementById(idti).style.backgroundColor = '';
				//alert("Se borró el registro.")
			} else if (xhr.response == 'Npe') {
				alert("Solo el usuario responsable puede eliminar su imputación.")
			} else {
				alert(" Err " + xhr.response);
			}

		}
	}
	xhr.send();
	CargandoGif(2);
}

/*  Estados
"Ok"  #	Borrado exitoso.
'Err' #	Error interno.
'Npe' #	No permisos para borrar.
*/





/*  	I M P R I M I R   V A L O R E S  O B T E N I D O S  ...  */
function Candado(llav) {
	//	idr_CLI_COL_AA_MM_SEM_DIA_POS
	var rpta = []
	if (typeof Gjson[llav] != 'undefined') {
		rpta = Gjson[llav];
		//rpta[2]="cls25";
		rpta[2] = 'style="background: ' + rpta[3] + ';"';
		//console.log(llav);

	} else {
		rpta[0] = "";
		rpta[1] = "";
		rpta[2] = "";
	}
	return rpta;
}
// Candado de totales
function CandadoSem(llav) {
	var rpta = [];
	var rpta1 = "";
	if (typeof Gjson[llav] != 'undefined') {
		rpta = Gjson[llav];
		rpta1 = rpta[1];
	}
	return rpta1;
}





/* 	D E S C R I P C I Ó N   D E L   D Í A    */
// Se le indica el día del calendario y devuelve el Nombre en la semana las el 
//  el día ue se le brindó Ejm: 'Mié-3'  , que s eusa como cabecera del gant.
function DescDia(dia) {
	var dias = ["Dom-", "Lun-", "Mar-", "Mié-", "Jue-", "Vie-", "Sáb-"];
	var dt = new Date(mes + ' ' + dia + ', ' + anio + ' 12:00:00');
	return dias[dt.getUTCDay()] + dia;
};






//  =========================== C O N S T R U C C I Ó N   D E L   G A N T   E N   H T M L ==================  \\
//  =========================== C O N S T R U C C I Ó N   D E L   G A N T   E N   H T M L ==================  \\
//  =========================== C O N S T R U C C I Ó N   D E L   G A N T   E N   H T M L ==================  \\

// Creamos las 2 primeras filas
//function CreamosEncabezado(){ 
function InsertarEnElDom() {


	//  ~-~-~-~-~-~-~-~-~-~-~-~-~-      ECABEZADO     ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\\

	var hoy = new Date()
	var cabt = " " + pais + "   -  " + cliente;
	cabt += '   -  Hoy: ' + hoy.getDate() + '.' + (hoy.getMonth() + 1) + '.' + hoy.getFullYear();
	cabt += ' - ' + hoy.getHours() + ':' + hoy.getMinutes() + ':' + hoy.getSeconds() + '';
	cabt += '    -    Rep: ' + mes + '/' + anio;

	// 1° fila de la cabecera
	var gant_html_1 = '<thead><tr class="cls04"><td colspan="7" class="cls03 fj00 cntr titl"><b>' + cabt + '</b></td>';

	for (var i = 1; i <= cant_dias; i++) {
		gant_html_1 += '<td colspan="2" class="cls05">' + DescDia(i) + '</td>';
	}

	// 2° fila de la cabecera
	gant_html_1 += '</tr><tr>' +
		'<td class="cls06 fj00" width="25px">H/d</td>' + //Personas x Día
		'<td class="cls06 fj04" width="120px">RECURSO</td>' +
		'<td class="cls06 fj06" width="40px">1° Sem</td>' +
		'<td class="cls06 fj07" width="40px">2° Sem</td>' +
		'<td class="cls06 fj08" width="40px">3° Sem</td>' +
		'<td class="cls06 fj09" width="40px">4° Sem</td>' +
		'<td class="cls06 fj10" width="45px">5° Sem</td>';

	for (var j = 1; j <= cant_dias; j++) {
		var find = DescDia(j).substring(0, 3);  // Validamos fines de semana
		if (find == "Sáb" || find == "Dom") { gant_html_1 += '<td class="cls07"></td><td class="cls07"></td>'; }
		else { gant_html_1 += '<td class="cls07">Requerim.</td><td class="cls07">Hrs.</td>'; }
	}

	gant_html_1 += '</tr></thead>';


	//  ~-~-~-~-~-~-~-~-~-~-~-~-~-       CUERPO       ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\\



	// var lstNlb = [4,11];  //  Dias no laborables   

	var cont_lst = -1; 		// Repeticiones o POSICIÓN
	var col = 0;


	var gant_html_2 = '<tbody>';

	for (var i = 1; i <= col_span; i++) {   // La cantidad de lilas que tendrá el cuerpo del gant

		cont_lst += 1;
		sem = 1;

		if (cont_lst == cant_rep) { 			// Validamos las repeticiones de los colavoradores
			cont_lst = 0;
			col += 1;
		}



		var llav_pos = id_Cli + '_' + lstIDs[col] + '_' + anio_red + '_' + mes + '_';//+dd+'_'+cont_lst;
		var llav_tr = 'idtr_' + id_Cli + '_' + lstIDs[col] + '_' + anio_red + '_' + mes + '_' + cont_lst;//  Id de cada fila del gant
		var subr = '';
		if (cont_lst == (cant_rep - 1)) { subr = 'endc'; } else { subr = ''; }  // Últim fila de cada colaborador.

		gant_html_2 += '<tr class="cls21" id="' + llav_tr + '">';
		// 1° Fila del cuerpo del gant
		if (i == 1) { gant_html_2 += '<td id="idtd_' + id_Cli + '_' + anio_red + '_' + mes + '" rowspan="' + col_span + '" class="cls22 fj00 cntr"><p class="txt_vertical">' + var_fts + '</p></td>' }

		gant_html_2 += '<td class="cls22 fj04 ' + subr + '">' + lstCOL[col] + '</td>' +
			'<td class="cls22 fj06 ' + subr + ' cntr">' + CandadoSem(llav_pos + '1_rs_' + cont_lst) + '</td>' +
			'<td class="cls22 fj07 ' + subr + ' cntr">' + CandadoSem(llav_pos + '2_rs_' + cont_lst) + '</td>' +
			'<td class="cls22 fj08 ' + subr + ' cntr">' + CandadoSem(llav_pos + '3_rs_' + cont_lst) + '</td>' +
			'<td class="cls22 fj09 ' + subr + ' cntr">' + CandadoSem(llav_pos + '4_rs_' + cont_lst) + '</td>' +
			'<td class="cls22 fj10 ' + subr + ' cntr">' + CandadoSem(llav_pos + '5_rs_' + cont_lst) + '</td>';

		val_sem = true; //  Corrige el día 1° de cada mes que cae domingo para la 1° fila (daba error)

		// *° demás Fila del cuerpo del gant
		for (var dd = 1; dd <= cant_dias; dd++) {			// llena los td diarios editable


			var find = DescDia(dd).substring(0, 3);
			if (find == "Sáb" || find == "Dom") {		// valida fines de semánas 
				//Agregamos en día no incurrible.
				gant_html_2 += '<td class="cls24 ' + subr + '"></td><td class="cls24 ' + subr + '"></td>';

				// Incrementamos la semana  <i class="fa fa-trash"></i>
				if (val_sem) {
					if (dd == 1 && find == "Sáb") { } else { sem += 1; } //  +  @001
					val_sem = false;
				}

			} else {
				val_sem = true;
				// idr_CLI_COL_AA_MM_SEM_DIA_POS
				//var llav_dd = id_Cli+'_'+lstIDs[col]+'_'+anio_red+'_'+mes+'_'+sem+'_'+dd+'_'+cont_lst;
				var llav_dd = llav_pos + sem + '_' + dd + '_' + cont_lst;
				var Rpta = Candado(llav_dd);

				// Pintar dias no laborables
				if (lstNlb.includes(dd.toString())) {
					gant_html_2 += '<td class="cls26 ' + subr + ' no_lab" ></td><td class="cls23 ' + subr + ' no_lab" ></td>';
				} else {  /*   ondblclick   por     onblur     */
					gant_html_2 += 
					'<td class="cls26 ' + subr + '" ' + Rpta[2] + ' id="idtr_' + llav_dd + '" >'
					+   '<input id="idr_' + llav_dd + '" type="text"   ondblclick="DetGant(this.id,this.value)" onblur="RegHoras(this.id,this.value)" value="' + Rpta[0] + '" />'
					+'</td>'
					+'<td class="cls23 ' + subr + '" ' + Rpta[2] + ' id="idti_' + llav_dd + '" >'
					+   '<input id="idi_' + llav_dd + '" type="number" ondblclick="DetGant(this.id,this.value)" onblur="RegHoras(this.id,this.value)" value="' + Rpta[1] + '" />'
					+'</td>';
				};
			}
		}
		gant_html_2 += '</tr>';
	}


	//  ~-~-~-~-~-~-~-~-~-~-~-~-~-          PIÉ       ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\\


	var llav_pos = id_Cli + '_au_' + anio_red + '_' + mes + '_';//+dd+'_'+cont_lst; 1_au_20_06_1_ha_1



	//  ----- Crear 1° línea del pié de tabla-------------------
	sem = 1;
	var gant_html_3 = '<tr class="cls21">' +
		'<td class="cls22 fj00"></td>' +
		'<td class="cls42 fj04">Hrs. Acuerdo</td>' +
		'<td class="cls42 fj06">' + CandadoSem(llav_pos + '1_ha_1') + '</td>' +
		'<td class="cls42 fj07">' + CandadoSem(llav_pos + '2_ha_2') + '</td>' +
		'<td class="cls42 fj08">' + CandadoSem(llav_pos + '3_ha_3') + '</td>' +
		'<td class="cls42 fj09">' + CandadoSem(llav_pos + '4_ha_4') + '</td>' +
		'<td class="cls42 fj10">' + CandadoSem(llav_pos + '5_ha_5') + '</td>';

	for (var dd = 1; dd <= cant_dias; dd++) {			// llena los td diarios editable
		var find = DescDia(dd).substring(0, 3);
		if (find == "Sáb" || find == "Dom") {		// valida fines de semánas 
			gant_html_3 += '<td class="cls24"></td><td class="cls24"></td>';
			if (val_sem) {
				if (dd == 1 && find == "Sáb") { } else { sem += 1; } //  +  @001 : 
				val_sem = false;
			}
		} else {
			val_sem = true;
			// idr_CLI_COL_AA_MM_SEM_DIA_RD   :: RD => Resumen diario
			// idi_34_01_21_04_1_1_za
			var llav_dd = id_Cli + '_1_' + anio_red + '_' + mes + '_' + sem + '_' + dd + '_za';
			var Rpta = Candado(llav_dd)

			// Verificamos si tiene ajuste para cambiar color de celda
			var clr_ajs = '#D7F7FD';
			var llv2 = id_Cli + '_1_' + anio_red + '_' + mes + '_' + sem + '_' + dd + '_zj';
			var rp_jsn = Candado(llv2);
			if (rp_jsn[1] != 0) {
				clr_ajs = '#9CF0FF';
			}

			// Pintar dias no laborables
			if (lstNlb.includes(dd.toString())) {
				gant_html_3 += '<td class="cls26 no_lab"></td><td class="cls23 no_lab"></td>';
			} else {
				gant_html_3 += '<td class="cls26" style="background:#E6FBFF;"></td>' +
					'<td class="cls23" style="background:' + clr_ajs + '; text-align:center;font-weight:bold;" ' +
					' id="' + llav_dd + '"  ondblclick="MdlConfig(this.id)" >' + Rpta[1] + '</td>';
			};
		}
	}
	gant_html_3 += '</tr>';



	//  ----- Crear 2° línea del pié de tabla-------------------
	sem = 1;
	gant_html_3 += '<tr class="cls21">' +
		'<td class="cls22 fj00"></td>' +
		'<td class="cls42 fj04">Incurrido</td>' +
		'<td class="cls43 fj06">' + CandadoSem(llav_pos + '1_in_1') + '</td>' +
		'<td class="cls43 fj07">' + CandadoSem(llav_pos + '2_in_2') + '</td>' +
		'<td class="cls43 fj08">' + CandadoSem(llav_pos + '3_in_3') + '</td>' +
		'<td class="cls43 fj09">' + CandadoSem(llav_pos + '4_in_4') + '</td>' +
		'<td class="cls43 fj10">' + CandadoSem(llav_pos + '5_in_5') + '</td>';

	for (var dd = 1; dd <= cant_dias; dd++) {			// llena los td diarios editable
		var find = DescDia(dd).substring(0, 3);
		if (find == "Sáb" || find == "Dom") {		// valida fines de semánas 
			gant_html_3 += '<td class="cls24"></td><td class="cls24"></td>';
			if (val_sem) {
				if (dd == 1 && find == "Sáb") { } else { sem += 1; } //  +  @001 : 
				val_sem = false;
			}
		} else {
			val_sem = true;
			// idr_CLI_COL_AA_MM_SEM_DIA_RD   :: RD => Resumen diario
			// idi_34_01_21_04_1_1_zi
			var llav_dd = id_Cli + '_1_' + anio_red + '_' + mes + '_' + sem + '_' + dd + '_zi';
			var Rpta = Candado(llav_dd);


			// Pintar dias no laborables
			if (lstNlb.includes(dd.toString())) {
				gant_html_3 += '<td class="cls26 no_lab"></td><td class="cls23 no_lab"></td>';
			} else {
				gant_html_3 += '<td class="cls26" style="background: #E4FFE5;"></td>' +
					'<td class="cls23" style="background: #D7FDD9;text-align:center;font-weight:bold;">' + Rpta[1] + '</td>';
			};

		}
	}
	gant_html_3 += '</tr>';




	//  ----- Crear 3° línea del pié de tabla-------------------
	sem = 1;
	gant_html_3 += '<tr class="cls21"><td class="cls22 fj00 endc"></td>' +
		'<td class="cls42 fj04 endc">Disponibilidad</td>' +
		'<td class="cls44 fj06 endc">' + CandadoSem(llav_pos + '1_di_1') + '</td>' +
		'<td class="cls44 fj07 endc">' + CandadoSem(llav_pos + '2_di_2') + '</td>' +
		'<td class="cls44 fj08 endc">' + CandadoSem(llav_pos + '3_di_3') + '</td>' +
		'<td class="cls44 fj09 endc">' + CandadoSem(llav_pos + '4_di_4') + '</td>' +
		'<td class="cls44 fj10 endc">' + CandadoSem(llav_pos + '5_di_5') + '</td>';

	for (var dd = 1; dd <= cant_dias; dd++) {			// llena los td diarios editable
		var find = DescDia(dd).substring(0, 3);
		if (find == "Sáb" || find == "Dom") {		// valida fines de semánas 
			gant_html_3 += '<td class="cls24 endc"></td><td class="cls24 endc"></td>';
			if (val_sem) {
				if (dd == 1 && find == "Sáb") { } else { sem += 1; } //  +  @001 : 
				val_sem = false;
			}
		} else {
			val_sem = true;
			// idr_CLI_COL_AA_MM_SEM_DIA_RD   :: RD => Resumen diario
			var llav_dd = id_Cli + '_1_' + anio_red + '_' + mes + '_' + sem + '_' + dd + '_zd';
			var Rpta = Candado(llav_dd);


			// Pintar dias no laborables
			if (lstNlb.includes(dd.toString())) {
				gant_html_3 += '<td class="cls26 endc no_lab"></td><td class="cls23 endc no_lab"></td>';
			} else {
				gant_html_3 += '<td class="cls26 endc" style="background: #FECCCC;"></td>' +
					'<td class="cls23 endc" style="background: #FFA6A6;text-align:center;font-weight:bold;" id="idi_' + llav_dd + '" >' + Rpta[1] + '</td>';
			};

		}
	}
	gant_html_3 += '</tr>';

	//  ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\\

	// Insertamos la cabecera + el cuerpo + el Pié de página.
	gant_html_1 += gant_html_2 + gant_html_3;

	document.getElementById('gant').innerHTML += gant_html_1;


	CargandoGif(2);

}














/* 		M A X I M I Z A R   */
var mxmz_gnt = true;
function MaximizarGant(ide) {
	var elem = document.getElementById(ide);
	if (mxmz_gnt) {
		elem.classList.remove("fa-compress");
		elem.classList.add("fa-arrows-alt");
		mxmz_gnt = false;
	} else {
		elem.classList.remove("fa-arrows-alt");
		elem.classList.add("fa-compress");
		mxmz_gnt = true;
	}
}







/* 		L I M P I A R   G A N T   */
function LimpiarGant() {
	var tab_l_gnt = document.getElementById('gant');
	LimpiarVariables();
	tab_l_gnt.innerHTML = "";
}

/*  Vacía las variables */
function LimpiarVariables() {
	Gjson = {}		//		Registros del gant
	lstCOL = [];		//		Lista de colaboradores
	lstIDs = [];		//		Lista de IDs de los colaboradores
	id_Cli = 0;		// 		Id del cliente
	cant_dias = 0;		//		Cantidad de días del mes
	cant_rep = 0; 		// 		Cantidad de repeticiones del colaborador en la lista
	gant_html = ""; 		//		Gante en HTML.
	cant_col = 0;  		// 		Obtenemos cantidad de colaboradores
	col_span = 0;  		//		Cantidad filas que ocuparan
	cliente = "";		//		Cliente
	var_fts = "";		// 		Concepto del cliente
	mes = "";
	anio = "";
	pais = "";
	sem = 1;
}





/*     M O D A L  D E T    */
function DetGant(ide, val) {
	//Variable de borrado
	var gantz = true;

	/*if (window.event.ctrlKey && val.length > 8) {*/
	if (val.length > 3) {

		var modal_carg = '<tr><td style="text-align:center;">' +
			'<span><img src="/static/img/cargando.gif"></span> </td></tr>';

		var tab_modal = document.getElementById('tab_modal');

		// Activamos el modal con el gif
		tab_modal.innerHTML = modal_carg;
		window.location.assign('#openModal');
		CargandoGif(1);

		//  Hacemos la solicitud al servidor
		var xhr = new XMLHttpRequest();
		var cad = "/gnt_d2/?ide=" + ide;
		xhr.open('GET', cad, true);
		xhr.onreadystatechange = function () {
			if (xhr.readyState == 4 && xhr.status == 200) {
				rpta = xhr.response;
				if (rpta != 'Nex') {
					var myObj = JSON.parse(rpta);
					tab_modal.innerHTML = MdlTabHtml(myObj);
				} else {
					tab_modal.innerHTML = '<tr><td><h1 style="color:red;">No encontrado</h1></td></tr>';
				}
			}
		}
		xhr.send();
		CargandoGif(2);

	} else {

		// Obtenemos el 1° td que parece columna y le reducimos uno
		// idtd_34_21_07
		var lstID = ide.split('_');
		var rpta = false;

		//alert(Event.ctrlKey);
		var fn = function (event) {
			if (event.which == "17") {
				alert('ok');
			}
		}

		if (window.event.ctrlKey) { rpta = true; }
		else { rpta = confirm("¿Desea eliminar toda la fila del gant?"); }

		if (rpta) {
			var idx = 'idtd_' + lstID[1] + '_' + lstID[3] + '_' + lstID[4] + '';
			var tdx = document.getElementById(idx);
			tdx.rowSpan = tdx.rowSpan - 1;
			// Obtenemos la fila (<tr>) y la eliminamos.
			// idtr_34_1_21_07_0
			var trx = 'idtr_' + lstID[1] + '_' + lstID[2] + '_' + lstID[3] + '_' + lstID[4] + '_' + lstID[7];
			document.getElementById(trx).remove();
		}
	}
	gant = false;
}


// CUERPO DEL MODAL DETALLE DE GANT
function MdlTabHtml(myObj) {
	/* Cuerpo del Modal*/

	var modal_html = '<tr><td style="text-align:center; background:' + myObj['pet_col'] + ';" class="let-somb"><b>' + myObj['pet_nom'] + '</b></td></tr>' +
		'<tr><td style="text-align: center; background:#EAF6FF;color:#6A6C75;"><b>' + myObj['req_nom'] + '</b></td></tr>' +
		'<tr><td>Tarea de <b>' + myObj['usu'] + '</b> con un total de <b>' + myObj['usu_inc'] + 'h</b> planificadas para hoy, <small style="font-style:italic;">tarea modificada por <b>' + myObj['usu_mod'] + '</b></small>.</td></tr>' +
		'<tr><td> <i class="inv">___</i> <b>REQUERIMIENTO</b></tr>' +
		'<tr><td>Planificado en gant <b style="color:#bc68e9">' + myObj['gnt_pla'] + 'h</b>, en task <b>' + myObj['tsk_pla'] +
		'h</b> y se ha incurrido <b style="color:red">' + myObj['tsk_inc'] + 'h</b>, horas acuerdo <b style="color:blue">' + 
		myObj['req_hac'] + 'h</b> y <b>ETC</b> en <b style="color:#05bd05">' + myObj['etc'] + 'h</b>.   </td></tr>' +

		'<tr><td><b>' + myObj['tsk_cnt'] + '</b> tareas en task y <b>' + myObj['gnt_cnt'] + '</b> tareas planificadas en gant.</td></tr>';


	return modal_html;

}









/*  - - - - - - - - - -  AJUSTES A H.ACUERDO POR DÍA  - - - - - - - - - - - - */
// Consultar al server si si ya existe ajuste
function MdlConfig(idg) {
	//alert('fdsfd');
	var modal_carg = '<tr><td style="text-align:center;"><span><img src="/static/img/cargando.gif"></span> </td></tr>';
	var tab_modal = document.getElementById('tab_cog');

	// Activamos el modal con el gif
	tab_modal.innerHTML = modal_carg;

	// Consultamos si la cantidad de su ajuste
	var cad = '/gnt_haj_get/?llv=' + idg + '';
	AjxSrvr(cad, IngrMdlCog);
}


//  Respuesta del server si ¿ya tiene ajuste?
function IngrMdlCog(jsn) {
	// 
	if (jsn[0] == 'ok') {
		// Todo bien
		window.location.href = '#MdlConfig'

		var llv = jsn['llv'];

		var bdy = '<tr> <td> <input type="number" style="width:75px" step="0.25" id="id_td_ajh" value="' + jsn['val'] + '"/>';
		bdy += '<input type="text" value="' + llv + '" id="id_td_llv" hidden  /> <a class="btn btn-sm" style="background: #CFD4FF; color:#8200cd;" onclick="AjustarHA()">';
		bdy += '<i class="inv">_</i><b>Crear ajuste<i class="inv">_</i><i class="fa fa-save"></i></b></a>';
		bdy += '<i style="font-size:0.8em;color:#A2A8D4;font-style:italic;"> <i class="inv">______</i> Las horas ajuste se restaran a las horas acuerdo del día.</b></i> </tr>';

		var tab_modal = document.getElementById('tab_cog');
		tab_modal.innerHTML = bdy;

	} else {
		/*		ERRORES      */
		// document.getElementById(('td_sel_resp_'+idr)).style.background = '#FF99A0';
		switch (jsn[0]) {
			case 'Nll': alert('Error al enviar consulta al server'); break;
			default: alert('Error en el servidor:' + jsn[0]); break;
		}
	}
}



// Enviar el server actualización de H.Acuerdo diarias.
function AjustarHA() {

	var val = document.getElementById('id_td_ajh').value;
	var llv = document.getElementById('id_td_llv').value;
	// Creamos el ajust
	var cad = '/gnt_haj_mdf/?llv=' + llv + '&&val=' + val;
	AjxSrvr(cad, AjustarHA2);
}

//  Respuestadel srvr de la actualización de las H.Acuerdo diarias
function AjustarHA2(jsn) {
	if (jsn[0] == 'ok') {
		// Todo bien
		//window.location.href = '#close'
	} else {
		/*		ERRORES      */
		// document.getElementById(('td_sel_resp_'+idr)).style.background = '#FF99A0'; 
		switch (jsn[0]) {
			case 'NAsi': alert("Colaborador No está asignado a ese cliente (Solicite a un líder que lo asigne)."); break;
			case 'NUsr': alert("Usted no tiene asignación aquí, nopuede modificar.");break;
			case 'Nll': alert('Error al enviar consulta al server'); break;
			default: alert('Error en el servidor:' + jsn[0]); break;
		}
	}
}




// -  -  -  -  -  -  -  -  - DÍAS NO LABORABLES  -  -  -  -  -  -  -  -  -  -  \\
// Cosultar al srvr si tiene algo previo guardado
function MdlDiasNL1() {

	// Consultamos si la cantidad de su ajuste
	//  AAAA_MM_CLI
	if (id_Cli != '' && id_Cli != 0) {
		var cad = '/gnt_dnl_get/?consum=' + anio + '_' + mes + '_' + id_Cli + '';
		AjxSrvr(cad, MdlDiasNL2);
	} else {
		alert('Cargar gant primero.');
	}
}


// Rpta del srvr a la consulta si tiene algo guardado
// y abre modal
function MdlDiasNL2(jsn) {
	// 
	if (jsn[0] == 'ok') {
		// Abrir modal 
		document.getElementById('id_td_dnl').value = jsn['val01'];
		document.getElementById('id_tx_nota').value = jsn['val02'];
		window.location.href = '#MdlDiasNL';
	} else {
		/*		ERRORES      */
		switch (jsn[0]) {
			case 'Nen': window.location.href = '#MdlDiasNL'; break; // No encontrado
			default: alert('Error en el servidor:' + jsn[0]); break;
		}
	}
}


// Enviar al server la actualización del comentario
function MdlDiasNL3() {

	//  Actualizamos
	//  AAAA_MM_CLI
	if (id_Cli != '' && id_Cli != 0) {
		// Actualizamos
		var v1 = document.getElementById('id_td_dnl').value;
		var v2 = document.getElementById('id_tx_nota').value;

		// Reemplazmos caracteres no permitidos
		v2 = v2.replace(/;/g, '~');

		// Set request
		var cad = '/gnt_dnl_upd/?consum=' + anio + '_' + mes + '_' + id_Cli + '';
		cad += '&&val01=' + v1 + '&&val02=' + v2 + '';
		AjxSrvr(cad, MdlDiasNL4);
	} else {
		alert('Cargar gant primero.');
	}
}


// Respues del server al actualizar el comentario
function MdlDiasNL4(jsn) {
	// 
	if (jsn[0] == 'ok') {
		// todo OK
		window.location.href = '#close';
	} else {
		/*		ERRORES      */
		switch (jsn[0]) {
			case 'NUsr': alert("Usted no tiene asignación aquí, nopuede modificar.");break;
			case 'Nll': alert('Error al enviar consulta al server'); break; 
			default: alert('Error en el servidor:' + jsn[0]); break;
		}
	}
}



// Reiniciar los acumulados 
function MdlDiasNL5() {
	//
	if (id_Cli != '' && id_Cli != 0) {
		var rpta = confirm("¿Desea reiniciar los cáculos de acumulados?, deberá hacer almenos un click en cada día laboral");
		if (rpta) {
			var cad = '/gnt_dnl_ref/?anio=' + anio + '&&mes=' + mes + '&&idc=' + id_Cli + '';
			AjxSrvr(cad, MdlDiasNL6);
		}
	} else {
		alert('Cargar gant primero.');
	}
}

// Respuesta del server si eliminó todas los cáculos de acumulados
function MdlDiasNL6(jsn) {
	// 
	if (jsn[0] == 'ok') {
		// todo OK
		window.location.href = '#close';
	} else {
		/*		ERRORES      */
		switch (jsn[0]) {
			case 'Noe': alert('No se encontró data para eliminar'); break;
			case 'Nll': alert('No llegaron los datos al server'); break;
			case 'Nel': alert('Ud. no es líder'); break;
			default: alert('Error en el servidor:' + jsn[0]); break;
		}
	}
}