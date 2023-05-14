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
            {"data": "titulo"},
            {"data": "autor.nombres"},
            {"data": "categoriaLibro.nombre"},
            {"data": "cantidad"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(data > 0){
                        return '<span class="badge badge-success">'+data+'</span>'
                    }
                    return '<span class="badge badge-danger">'+data+'</span>'
                }
            },
            
            
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/base/libro/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" title="Editar"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/base/libro/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat" title="Eliminar"><i class="fas fa-trash-alt"></i></a>&nbsp' ;
                    buttons += '<a href="/base/detalle-libro/pdf/' + row.id + '/" class="btn btn-info btn-xs btn-flat" title="Ver Libro"> <i class="fas fa-eye"></i></a> ';
 
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
