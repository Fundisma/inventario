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
            {"data": "nacionalidad"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/base/autor/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" title="Editar"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/base/autor/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat" title="Eliminar"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}); 

