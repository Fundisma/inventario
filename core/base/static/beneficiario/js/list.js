$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "nombres"},
            {"data": "apellidos"},
            {"data": "tipoDocumento"},
            {"data": "documento"},
            {"data": "tipo"},
            {"data": "cumpleaños"},
            {"data": "telefono"},
            {"data": "zona"},
            {"data": "direccion"},
            {"data": "barrio"},
            {"data": "gender"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/base/beneficiario/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/base/beneficiario/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    
});
$(function(){
    $('#cumpleaños').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });
});
