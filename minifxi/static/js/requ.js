
/*   TODOS LOS RECURSOS JS PARA LOS REQUERIMIENTOS  */


/* 2022.03.26 */
function ReqUpdBit(idr){
    //console.log("OT: "+idr);
    var id_frm = '#REQ_FORM_BITA_'+idr+'';
    var url = '/req_upd_bit/' + idr + '/';
    CargandoGif(1);
    $.ajax({
      type: "POST",
      url: url,
      data: $(id_frm).serialize() ,
    })
    .done( function(rpta) { switch (rpta) { case "Ok": break;
                                            case "NEq": alert("Ud. no tiene asignación activa al cliente."); break;
                                            default: alert("Error, intente nuevamente"); break; } 
                            CargandoGif(2);  }) //grcl4
    .fail( function() {alert("Error en el server."); })
}
   