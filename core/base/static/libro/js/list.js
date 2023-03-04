var tblLibro;
var modal_title;

function getData() {
            tblLibro= $('#data').DataTable(  {
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
                    { "data": "titulo"},
                    { "data": "autor.nombres"},
                    { "data": "f_publicacion"},
                    { "data": "opciones"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            var buttons = '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                            buttons += '<a href="#" rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                            return buttons;
                        }
                    },
                ],
                initComplete: function(settings, json) {
                }
            });
        }  

$(function () {

modal_title = $('.modal-title');

    getData();

    $('.btnAdd').on('click', function() {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un Libro');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-user-plus');
        $('form')[0].reset();
        $('#myModalLib').modal('show'); 
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de un Libro');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblLibro.cell($(this).closest('td, li')).index();
            var data = tblLibro.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="titulo"]').val(data.titulo);
            $('input[name="autor.nombres"]').val(data.autor.nombres);
            $('input[name="f_publicacion"]').val(data.f_publicacion);
            $('input[name="opciones"]').val(data.opciones);
            $('#myModalLib').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblLibro.cell($(this).closest('td, li')).index();
            var data = tblLibro.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el siguiente registro?', parameters, function () {
                tblLibro.ajax.reload();
            });
        
        });

    $('#myModalLib').on('shown.bs.modal', function () {

    });


    $('form').on('submit', function (e) { 
        e.preventDefault();
        //var parameters = $(this).serializeArray();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalLib').modal('hide'); 
            tblLibro.ajax.reload();
            //getData();
        });
    });
});




