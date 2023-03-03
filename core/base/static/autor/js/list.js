var tblAutor;
var modal_title;

function getData() {
            tblAutor= $('#data').DataTable(  {
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
                    { "data": "nombres"},
                    { "data": "apellidos"},
                    { "data": "nacionalidad"},
                    { "data": "descripciones"},
                    { "data": "descripcion"},
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
        modal_title.find('span').html('Creación de un Autor');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-user-plus');
        $('form')[0].reset();
        $('#myModalAut').modal('show'); 
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de un Autor');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblAutor.cell($(this).closest('td, li')).index();
            var data = tblAutor.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombres"]').val(data.nombres);
            $('input[name="apellidos"]').val(data.apellidos);
            $('input[name="nacionalidad"]').val(data.nacionalidad);
            $('input[name="descripciones"]').val(data.descripcion);
            $('#myModalAut').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblAutor.cell($(this).closest('td, li')).index();
            var data = tblAutor.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el siguiente registro?', parameters, function () {
                tblAutor.ajax.reload();
            });
        
        });

    $('#myModalAut').on('shown.bs.modal', function () {

    });


    $('form').on('submit', function (e) { 
        e.preventDefault();
        //var parameters = $(this).serializeArray();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalAut').modal('hide'); 
            tblAutor.ajax.reload();
            //getData();
        });
    });
});




