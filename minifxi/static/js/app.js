
// GLOBALS VARIBALES
var gv_foto    = '';
var gv_codigo  = '';
var gv_cliente = '';
var gv_equipo = '';




// AL CARGAR LA PÁGINA
window.onload = function() {
	CargarPerfil();
	//CargarImgs();
	OcultarPanelLateral();

	// Colocar el mes en el Gant
	if(typeof ColocarHora === 'function') {
	    //Es seguro ejecutar la función
	    ColocarHora();
	}

				
	// Colocar fecha siempre que exista el input id='fecha_desde1'
	ColocarFechas();


}
 







// Colocar fecha siempre que exista el input id='fecha_desde1'1
function ColocarFechas(){

	var f = new Date();
	var dd = "00";
	var mm = "00";

	// Get Day
	if( f.getDate() < 10 ){
		dd = "0" + f.getDate();
	}else{
		dd = f.getDate();
	};
	// Get Month
	if( f.getMonth() < 9 ){  mm = "0" + (f.getMonth() +1);
	}else{ mm = (f.getMonth() + 1 );  };

	// - - -  Fecha AAAA-MM-DD  - - - //
	fec = "" + f.getFullYear() + "-" + mm + "-" + dd ;


	// De existir se le coloca a la fecha del primer día del mes
	var fec01 = document.getElementById('fecha_desde1');
	if (fec01) { fec01.value = ( fec ); };

	// De existir tambien se le coloca a la fecha fin
	var fec02 = document.getElementById('fecha_hasta1');
	if (fec02) { fec02.value = ( fec ); };

}






















/*       Cargando      */
var cargando =document.getElementById('cargando');
var tim1;

function CargandoGif(est){
	if (est == 1) {
		cargando.innerHTML = '<img src="/static/img/cargando.gif">';
	}else{
		clearTimeout(tim1);
		tim1 = setTimeout(CargandoRm, 500);
	}
}

function CargandoRm(){
	cargando.innerHTML = " ";
}





/*   validaciones  */
function Consultar() {
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
		var clie = document.getElementById('sel_cliente').value;

		url = url+"?fecha_desde='"+fecha_desde1+"'&&fecha_hasta='"+fecha_hasta1+"'&&clie="+clie;		
		window.location.href = url
	}
}



function ActualizarTSf(idt){

	var xhr = new XMLHttpRequest();
	var idsf = 'sf_'+idt;
	var sf_td = document.getElementById(idsf) ;
	CargandoGif(1);
	var cad = "/task_sf/?idtask="+idt;
	xhr.open('GET',cad,true); 	
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			if( xhr.response == '1'){
				sf_td.classList.remove("sf-n");
				sf_td.classList.add("sf-y");
			}else if( xhr.response == '0'){
				sf_td.classList.remove("sf-y");
				sf_td.classList.add("sf-n");
			}else{
				alert("A ocurrido un error.");
			}
		}
	}
	xhr.send();
	CargandoGif(2);
}



function TaskXCodigo(sf) {
	var codigo = document.getElementById('cod_col').value;
	if(codigo > 000010000 && codigo < 999999999 ){//001532815
		var url = "/task_x_codigo/?idr="+codigo+"&&sf="+sf;	
		window.location.href = url
	}
	else{
	    alert("Ingrese un código de empleado correcto.");
	}
}

 



/*  ----------------------------------------------- Act Task ---------------------*/

function ActTask(id_td,idtask,campo) {
	var tdee = document.getElementById(id_td);
	tdee.removeAttribute("onclick");
	num = tdee.innerHTML.replace(",",".");
	tdee.innerHTML = '<input id="inpt'+id_td+'"  type="number" step="0.25" min="0" value="'+num+
						'" onkeyup="ActTaskInput('+idtask+',this.value,'+campo+')" '+
						'  onclick="ActTaskInput('+idtask+',this.value,'+campo+')">';
}





function ActTaskInput(idt,valr,camp) {

	var campo = "";
	CargandoGif(1);
	if (camp == 1 ){ campo = "esfuerzo_total_estandar"; }
	else{ campo = "esfuerzo_ejecutado"; }

	var xhr = new XMLHttpRequest();
	var cad = "/act_task/?idtask="+idt+"&&campo="+campo+"&&valor="+valr;
	xhr.open('GET',cad,true); 
	
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			if( xhr.response == '1'){
			}else{
				alert("A ocurrido un error al guardar, favor verifique.");
			}
		}
	}
	xhr.send();
	CargandoGif(2);
	ActualizarTotalTask();
}


// Atualiza los cálculos del resumen diario.
function ActualizarTotalTask(){

	var resume_table = document.getElementById("tabla1");
	var ep = 0.0, ej = 0.0, et = 0.0, epp = 0.0, ejj = 0.0;
	var idinp = '';
	var idinp2 = '';

	for (var i = 1; i < (resume_table.rows.length - 1); i++) {

		idinp  = ''+ resume_table.rows[i].cells[8].id + '';
		idinp2 = ''+ resume_table.rows[i].cells[9].id + '';

		// Esfuerzo planificado
		var inpt0 = document.getElementById(('inpt'+idinp));
		if(inpt0){
			epp = parseFloat( inpt0.value.replace(',', '.') );
		}else{
			var td0 = document.getElementById(idinp);
			epp = parseFloat( td0.innerHTML.replace(',', '.') );
		}

		// Esfuerzo ejecutado
		var inpt0 = document.getElementById(('inpt'+idinp2));
		if(inpt0){
			ejj = parseFloat( inpt0.value.replace(',', '.') );
		}else{
			var td0 = document.getElementById(idinp2);
			ejj = parseFloat( td0.innerHTML.replace(',', '.') );
		}

		// ETC
		$(('#'+idinp+'_et')).html((epp - ejj));

		// Acumulados
		ep = ep + epp;
		ej = ej + ejj;
		et = et + ( epp - ejj );

	}
	// Actualizamos el domm
	$('#idges_tot_pla').html(ep);	
	$('#idges_tot_inc').html(ej);
	$('#idges_tot_etc').html(et); 
}



function GenerarACC(cod){
	var cod = document.getElementById('cod_col').value;
	//if(cod > 100000 && cod < 999999 ){
	if( cod > 000010000 && cod < 999999999 ){//001532815
		var url = "/task_acc/?cod="+cod;
		window.location.href = url
	}
	else{
	    alert("Ingrese un código de empleado correcto.");
	}
}
















/* =======================================  R E Q U E R I M I E N T O ================*/


// Volver editable  OBSOLETO
function AgrComentario(idr){
	var idtdc = 'tdc'+idr;
	var tdc1 = document.getElementById(idtdc);
	tdc1.removeAttribute("onclick");
	var txt = tdc1.innerHTML;
	tdc1.innerHTML =  '<textarea id="txa'+idr+'" rows="10" onkeyup="GuardarTxt('+idr+',this.value)">'+
											txt+'</textarea>';
}



// Agregar comentario  OBSOLETO
function GuardarTxt(idr,txt){
	if (event.keyCode === 13) {
		CargandoGif(1);

		var xhr = new XMLHttpRequest();
		var cad = "/req_agr_comn/?idreq="+idr+"&&campo=comentario&&valor="+txt;
		xhr.open('GET',cad,true); 
		xhr.onreadystatechange = function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				if( xhr.response == '1'){
					CargandoGif(2);
				}else{
					alert("A ocurrido un error.  [COD00"+xhr.response+"]");
				}
			}
		}
		xhr.send();	
	}
}




// Hacer editable el código del requerimiento.
function hcrEditable(pk){
	document.getElementById(pk).removeAttribute('readonly');
}


// Editar bitácora del requerimiento
function BitacoraReq(pk){
	 //grcl1
	url = "/req_bita/"+pk+"/";		
	window.open(url,'_blank');
}





/*   G R A F I C O S    */
// Reporte de clientes
function GrafRp001(){
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
		url = url+"?fecha_desde='"+fecha_desde1+"'&&fecha_hasta='"+fecha_hasta1+"'";		
		window.location.href = url
	}
}



/*   Resporte de colaboradores  */
function GrafRp002() {
	var url = document.getElementById('url_rep002').value;
	var fecha = document.getElementById('input_mes').value;
	var f1 = new Date(fecha);
	    
	if(f1 == 'Invalid Date' ){
	    alert("Ingrese una fecha correcta.");
	}
	else{
		url = url+"?fecha='"+fecha+"'";		
		window.location.href = url
	}
}


/*   Incurrido-Disponibilidad-horas acuerdo  */
function GrafRp003() {
	var url = document.getElementById('url_rep003').value;
	var fecha = document.getElementById('input_mes').value;
	var f1 = new Date(fecha);
	    
	if(f1 == 'Invalid Date' ){
	    alert("Ingrese una fecha correcta.");
	}
	else{
		var mes = 0;
		switch (f1.getMonth()){
			case 11:
				mes = 1;
				break;
			default:
				mes = 2 + f1.getMonth();
				break;
		}
		url = url+"?anio="+f1.getFullYear()+"&&mes="+mes;		
		window.location.href = url
	}
}



/*           Acotamiento     */
function ConsultaRep004(){
	var url = document.getElementById('input_url').value;
	var pet_cod 	 = document.getElementById('pet_cod').value;
	var fecha_desde1 = document.getElementById('fecha_desde1').value;
	var fecha_hasta1 = document.getElementById('fecha_hasta1').value;

	var f1 = new Date(fecha_desde1);
	var f2 = new Date(fecha_hasta1);
	    
	if(f1 == 'Invalid Date' || f2 == 'Invalid Date' || pet_cod < 1093514 ){
	    alert("Corrija los datos.");
	}
	else{
		if (f1 > f2) {
			var ft = fecha_desde1;
			fecha_desde1 = fecha_hasta1;
			fecha_hasta1 = ft;
		}
		url = url+"?pet_cod="+pet_cod+"&&fec_des='"+fecha_desde1+"'&&fec_has='"+fecha_hasta1+"'";		
		window.location.href = url
	}
}


 

/*             P  E R F I L    */
function  CargarPerfil(){
	var prf_1=document.getElementById('prf_1');
	var prf_2=document.getElementById('prf_2');
	var prf_3=document.getElementById('prf_3');
	CargandoGif(1);

	var xhr = new XMLHttpRequest();
	xhr.open('GET',"/col/fot/",true); 
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			var rpta = xhr.response;
			if (rpta!="") {
				//
				var myObj = JSON.parse(rpta);
				gv_foto    = myObj['Foto']; 
				gv_codigo  = myObj['Codigo']; 
				gv_cliente = myObj['Cliente']; 
				gv_equipo  = myObj['Equipo']; 


				// Si existe el Combobox id = 'sel_cliente'
				var sel00 = document.getElementById('sel_cliente');
				if (sel00) {
					sel00.value = gv_cliente;
					var sel02 = document.getElementById('sel_cliente1');
					if (sel02) {
						sel02.value = gv_cliente;
					}
				}


				// Si existe el codigo del colaborador
				var col00 = document.getElementById('cod_col');
				if (col00) {
					col00.value = gv_codigo;
				}


				// Si existe el Combobox id = 'sel_cliente'
				var sel01 = document.getElementById('sel_equipo');
				if (sel01) {
					sel01.value = gv_equipo;
				}


			}
			if (gv_foto != "Inv") {
				prf_1.setAttribute('src', '/media/'+gv_foto);
				prf_2.setAttribute('src', '/media/'+gv_foto);
				prf_3.setAttribute('src', '/media/'+gv_foto);
			}
		
		}
	}
	xhr.send();
	CargandoGif(2);
}



/*
// Cargar los baner del inicio
function CargarImgs() {
	var img1=document.getElementById('img1');
	var img2=document.getElementById('img2');
	var img3=document.getElementById('img3');
	if (img1 != null){
		var rdn1 = Math.floor(Math.random() * 8);
		var rdn2 = Math.floor(Math.random() * 8);
		var rdn3 = Math.floor(Math.random() * 8);
		if (rdn1 == rdn2) {if (rdn2 == 7) { rdn2 -= 1; }else{ rdn2 += 1; }	}
		img1.setAttribute('src', '/static/img/fnd/fondo_'+rdn1+'.jpg');
		img2.setAttribute('src', '/static/img/fnd/fondo_'+rdn2+'.jpg');
		img3.setAttribute('src', '/static/img/fnd/fondo_'+rdn3+'.jpg');
	}
}
*/

function OcultarPanelLateral(){	
	// Ocultar panel lateral en automático...
	var btn_panel = document.getElementById("hide_panel");
	if(btn_panel != null){
		document.getElementById("btn_0").click();
	}
}

	

// -------------------------xxxxx-----xxxxx---------------
var camb = true;
function  CambiarPass(){
	if (camb == true) {
		camb = false;
		var div1=document.getElementById('set_priemro');
		div1.removeAttribute('hidden');
	}else {
		var ps10=document.getElementById('ps10').value;
		var ps11=document.getElementById('ps11').value;
		var ps12=document.getElementById('ps12').value;
		var div1=document.getElementById('set_priemro');
		div1.setAttribute('hidden','hidden');
		camb = true;
		if (ps11 == ps12 && ps11.length > 4) {
			CargandoGif(1);
			var xhr = new XMLHttpRequest();
			cad = '/col_pas/?prmr='+ps12+'&&sgnd='+ps10;
			xhr.open('GET',cad,true); 
			xhr.onreadystatechange = function(){
				if(xhr.readyState == 4 && xhr.status == 200){
					var rpta = xhr.response;
					if (rpta=="Ok") {
						alert("Cambio de contraseña exitoso.")
						CargandoGif(2);
					}else{
						alert("Contraseña antigua no validada, contacte al administrador.")
					}				
				}
			}
			xhr.send();
		}else{
			alert("Problema en la contraseña nueva.")
		}
	}	
}


//
function CambiarPass2() {
	var pss = document.getElementById('col_pss1').value;
	var cod = document.getElementById('col_cod1').value;
	CargandoGif(1);
	var xhr = new XMLHttpRequest();
	cad = '/col_set_pas/?pss='+pss+'&&cod='+cod;
	xhr.open('GET',cad,true); 
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			var rpta = xhr.response;
			if (rpta=="Ok") {
				alert("Cambio de contraseña exitoso.");
				CargandoGif(2);
			}else{
				// 
				switch (rpta) {
			  		case "nco": alert("Código no encontrado"); break;
					default: alert("Error intente nuevamente"); break;
				}
			}				
		}
	}
	xhr.send();
}



/* ============= F I L T R A R ==================*/
/*
function Filtrar() {
	  // Declare variables 
	  var input, filter, table, tr, td, i, j, visible, invisible;
	  input = document.getElementById("txt_buscar");
	  filter = input.value.toUpperCase();
	  table = document.getElementById("tablaf");
	  tr = table.getElementsByTagName("tr");
	  CargandoGif(1);

	  // recorremos todas las rows
	  for (i = 0; i < tr.length; i++) {
		visible = false;
		// Obtenemos todas las celdas de la fila, no sólo la primera 
		td = tr[i].getElementsByTagName("td");
		for (j = 0; j < td.length; j++) {
		  if (td[j] && td[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
			visible = true;
		  }
		}
		if (visible === true) {
		  tr[i].style.display = "";
		} else {
		  tr[i].style.display = "none";
		}
	  }
	  CargandoGif(2);
} 
*/

/* =================== S F ======================== */
function ActualizarSf(tab,idt){

	var xhr = new XMLHttpRequest();
	var idsf = 'sf_'+idt;
	var sf_td = document.getElementById(idsf) ;
	CargandoGif(1);

	var cad = "/act_sf/?ide="+idt+"&&tip="+tab;

	xhr.open('GET',cad,true); 
	
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			if( xhr.response == '1'){
				sf_td.classList.remove("sf-n");
				sf_td.classList.add("sf-y");
				CargandoGif(2);
			}else if( xhr.response == '0'){
				sf_td.classList.remove("sf-y");
				sf_td.classList.add("sf-n");
				CargandoGif(2);
			}else{
				alert("A ocurrido un error.");
			}
		}
	}
	xhr.send();
}




/*   --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  */
/*   --  --  --  --  --  --  --    F I L T R O S     --  --  --  --  --  --  --  */
/*   --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  */

var tabla_fil;
var ArrA = new Array();
var ArrB = new Array();
var cant_col;
var typF = 'in';


function ActivarFiltros(td_id,typ){

	typF = typ;

	var tbody = "tab-body-fil"+td_id.substr(7,1)+"";
	ControladorFiltro(tbody,td_id);

	var  fil_avz=document.getElementById(td_id);//("fil-avz");
	var testClass = fil_avz.className;

	// Muestra y oculta la fila de filtros
	switch (testClass) {
  		case "fil-avz":
			fil_avz.classList.remove("fil-avz");
			fil_avz.classList.add("fil-avz-v");
			break;
		case "fil-avz-v":
			fil_avz.classList.remove("fil-avz-v");
			fil_avz.classList.add("fil-avz");
		    break;
	}	
}




// 	NEGOCIO :: 
function ControladorFiltro(tbody,td_id){

	tabla_fil = document.getElementById(tbody); 		// "tab-body-fil");
	tr_fil 	  = document.getElementById(td_id); 		// "fil-avz");
	cant_col  = tr_fil.getElementsByTagName("td").length;
	CrearArrayDeBusqueda();
}


// Crea array bidimiencional para guardar el texto buscado en la columna indicada
function CrearArrayDeBusqueda(){
	for (var i = 0; i < cant_col; i++) {
		ArrA[i] = '.'; // -  - -  - -  - -  - -  -> Cadenas a que SI deben coincidir
		ArrB[i] = '.'; // -  - -  - -  - -  - -  -> Cadenas a que NO deben coincidir
	}
}


// filtra
function Filtrar(id_tdi) {
	var tdp_value = document.getElementById(id_tdi).innerHTML.toUpperCase();	// Toma el valor buscado
	var col =parseInt(id_tdi.substr(4,2));										// Toma la columna desde al id
	if(tdp_value != ''){ 					// Guarda 'col' y 'val' buscado y llama al filtro avanzado

		// Array con los distintos valores a buscar
		ArrA[col] = tdp_value.split('%');
		ArrB[col] = tdp_value.split('%');

		// Emilinamos los de exclusión 
		for (var i = ArrA[col].length - 1; i >= 0; i--) {
			if (ArrA[col][i].charAt(0) == '~') {
				ArrA[col].splice(i, 1);
			}
		} if ( ArrA[col].length == 0) {  ArrA[col] = "."; }

		// Eliminamos los de filtrado 
		for (var i = ArrB[col].length - 1; i >= 0; i--) {
			if (ArrB[col][i].charAt(0) != '~') {
				ArrB[col].splice(i, 1);
			}else{
				ArrB[col][i] = ArrB[col][i].substring(1); // eliminamos la pestaña '~'
			}
		} if ( ArrB[col].length == 0) {  ArrB[col] = "."; }


	}else{
		ArrA[col] = '.';  // Se inicializan
		ArrB[col] = '.';
	}

	// Realizamos las comparaciones de textos
	if( typF == 'in'){   FilAvanzIn();  }
	else{   FilAvanzEx();  }
	
}



/// ------------------- FILTRO INCLUYENTE ------------------- \\\
function FilAvanzIn() {
	tr = tabla_fil.getElementsByTagName("tr");
	var nof = false;

	// Recorre las filas de la tabla.
	for (i = 0; i < tr.length; i++) { 		
		visible 	= false;
		invisible 	= false;

		td = tr[i].getElementsByTagName("td"); 	

		// Recorre las columnas de la tabla ( o mejor dicho las celdas de esa fila ) .
		nof = true;
		for (j = 0; j < td.length; j++) { 	

			// Verifica si hay filtro para esa columna.
			if (ArrA[j] != '.' || ArrB[j] != '.' ) {	

				// Hay filtros, no se muestra por defecto
				nof = false;			
				//  Recorre las distintas cadenas que se están buscando para esa columna
				for (k = 0; k < ArrB[j].length; k++) { 
					if (td[j].innerHTML.toUpperCase().indexOf(ArrB[j][k]) > -1 ) {  invisible = true; break;   } // Comparamos los textos
				}
				for (k = 0; k < ArrA[j].length; k++) { 
					if (td[j].innerHTML.toUpperCase().indexOf(ArrA[j][k]) > -1 ) { 	visible = true; break;  	}// Comparamos los textos
				}
				if(visible || invisible){break;};
			}
		}
		// Si no hay nada que filtrar, por defecto se muestra
		if (nof) { visible = true; }

		// Agregamo o ocultamos según la verificación
		if (invisible) {	tr[i].style.display = "none";   }
		else if (visible) { tr[i].style.display = "";  		} 
		else { 				tr[i].style.display = "none"; 	}
	}	
}

/// ------------------- FILTRO EXCLUYENTE ------------------- \\\
function FilAvanzEx() {
	tr = tabla_fil.getElementsByTagName("tr");
	var nof = false;

	// Recorre las filas de la tabla.
	for (i = 0; i < tr.length; i++) { 		
		visible = true; invisible = false;
		td = tr[i].getElementsByTagName("td"); 	
		// Recorre las columnas de la tabla ( o mejor dicho las celdas de esa fila ) .
		nof = true;
		for (j = 0; j < td.length; j++) { 	
			// Verifica si hay filtro para esa columna.
			if (ArrA[j] != '.' || ArrB[j] != '.' ) {
				//  Recorre las distintas cadenas que se están buscando para esa columna
				for (k = 0; k < ArrB[j].length; k++) { 
					if (ArrB[j][k] != '.') {
						if (td[j].innerHTML.toUpperCase().indexOf(ArrB[j][k]) > -1  && visible == true ) { invisible = true; }
					}
				}
				for (k = 0; k < ArrA[j].length; k++) { 
					if (ArrA[j][k] != '.') {
						if (td[j].innerHTML.toUpperCase().indexOf(ArrA[j][k]) > -1 && visible == true ) { visible = true; }	
						else{ visible = false; }
					}
				}
			}
		}
		// Agregamo o ocultamos según la verificación
		if (invisible == false & visible == true)  { tr[i].style.display = "";  } 
		else { tr[i].style.display = "none";  }
	}	
}




/// ------------------- FILTRO EXCLUYENTE ------------------- \\\
/*
function FilAvanzEx() {
	tr = tabla_fil.getElementsByTagName("tr");

	for (i = 0; i < tr.length; i++) { 		// Recorre las Filas.
		visible = true;		
		td = tr[i].getElementsByTagName("td"); 	
		
		for (j = 0; j < td.length; j++) { 		// Recorre las columnas.
			if (ArrB[j] != '.') {				// Verifica si hay filtro para esa columna.
				if (td[j].innerHTML.toUpperCase().indexOf(ArrB[j]) > -1 && visible == true) {  // Compara  td con 
					visible = true;
				}else{
					visible = false;
				}	  	
			}
		}
		if (visible) {
		  tr[i].style.display = "";
		} else {
		  tr[i].style.display = "none";
		}
	}	
}
*/

/*   --  --  --  --  --  --    E N D   F I L T R O S    --  --  --  --  --  --  --  */






/* ==================================   I N C I D E N C I A   ==================================  */

function Exportar(){

	var url = document.getElementById('input_url2').value;
	url = url + '?id_cli=' + document.getElementById('sel_cliente1').value + 
				'&cod_col=' + document.getElementById('cod_col').value+"";
	//alert(url);
	window.location.href = url
}





/*  =================   E S T A T U S ===============  */
/*   validaciones  */
function CrearStatus() {
	var url = document.getElementById('input_url').value;
	var cli_id = document.getElementById('sel_cliente').value;
	var fec_des = document.getElementById('fecha_desde1').value;
	url = url+"?cli_id="+cli_id+"&&fec_des="+fec_des+"";
	window.location.href = url
}







/* =======   P A N E L    I N D E X ========*/
function ConsultarPanel(){

	var url = document.getElementById('input_url').value;
	var fecha_hasta1 = document.getElementById('fecha_hasta1').value;
	var col_cod      = document.getElementById('cod_col').value;	 
	url = url+"?fech="+fecha_hasta1+"&&col_cod="+col_cod+"";		
	window.location.href = url
	
}






/* =======   P A N E L    I N D E X ========*/
function ConsulReq(){
	
	var url = document.getElementById('input_req').value;
	if(url.length > 2){
		url = "/req_filt/?filt="+url+"";		
		window.location.href = url
	}else{
		alert('Ingrese al menos 3 caracteres');
	}
}





/* ------------------------------------------*/
/* Actualización en la DDBBB ----------------*/
/*-----   MÉTO AJAX GENÉRICO PARA    --------*/
/*-----   CUALQUIER CONSULTA GET QUE --------*/
/*-----   DEVUELVA UN JSON.          --------*/
/*-------------------------------------------*/
function AjxSrvr(cad,fn){

	var xhr = new XMLHttpRequest();
	CargandoGif(1);
	xhr.open('GET',cad,true); 	
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			// return Function() rpta
			var rpta = xhr.response;
			var json = JSON.parse(rpta);
			fn(json);
		}
	}
	xhr.send();
	CargandoGif(2);
}
