var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');

function generate_reporte() {
    var parameters = {
        'action': 'search_reporte',
        'start_date': date_now,
        'end_date': date_now,
    };

    if(date_range !== null){
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: { 
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
            }
        ],
        //columns: [
        //    {"data": "position"},
        //    {"data": "nombre"},
        //    {"data": "descripcion"},
        //    {"data": "id"},
        //],
        columnDefs: [
        
            {
                targets: [-1,],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+parseFloat(data).toFixed(3);
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });  
}
$(function () {
   $('input[name="date_range"]').daterangepicker({
        locale : {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
   }).on('apply.daterangepicker', function (ev, picker) {
        date_range = picker;
        generate_reporte();
    }).on('cancel.daterangepicker', function (ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_reporte();
    });
   generate_reporte();
});