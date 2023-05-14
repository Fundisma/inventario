var tblProducto;
var suministro = {
    items : {
        beneficiario: '',
        fecha_registro: '',
        total: 0.000,
        producto:[]
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.producto, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function(){
        var subtotal = 0.000;
        $.each(this.items.producto, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.total = this.items.subtotal;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(3));
        $('input[name="total"]').val(this.items.total.toFixed(3));

    },
    add: function(item){
        this.items.producto.push(item);
        this.listado();
    },
    listado: function (){
        this.calculate_invoice();

        tblProducto = $('#tblProducto').DataTable(  { 
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.producto, 
            columns: [
                { "data": "id"},
                { "data": "full_name"},
                { "data": "stock"},
                { "data": "pvp"},
                { "data": "cantidad"},
                { "data": "subtotal"},

            ],
            columnDefs: [
                
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" title="Eliminar" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-4],
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
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(3);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="'+ row.cantidad +'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(3);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                    step: 1 
                });
            },
            initComplete: function(settings, json) {
            }
        });
        console.clear();
        console.log(this.items);
        console.log(this.get_ids());
    }
};
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.full_name + '<br>' +
        '<b>Cantidad o Stock:</b> ' + repo.stock + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function(){
    $('.select2').select2({
        theme: "bootstrap4", 
        language: 'es'
    });

    $('#fecha_registro').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD")
    });

    //busqueda de beneficiario
    $('select[name="beneficiario"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_beneficiario'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    });

    //busquesda de productos
    /*$('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_producto',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cantidad = 1;
            ui.item.subtotal = 0.00;
            console.log(suministro.items);
            suministro.add(ui.item);            
            $(this).val('');
        }


    });*/

    //eliminar todo registro
    $('.btnRemoveAll').on('click', function () {
        if (suministro.items.producto.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            suministro.items.producto = [];
            suministro.listado();
        });

    });

    //cantidad
    $('#tblProducto tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?', function () {
                suministro.items.producto.splice(tr.row, 1);
                suministro.listado();
            });
        })

        .on('change', 'input[name="cantidad"]', function(){
        console.clear();
        var cantidad = parseInt($(this).val());
        var tr = tblProducto.cell($(this).closest('td, li')).index();
        suministro.items.producto[tr.row].cantidad = cantidad;
        suministro.calculate_invoice();
        $('td:eq(5)', tblProducto.row(tr.row).node()).html('$' +suministro.items.producto[tr.row].subtotal.toFixed(3));
        
    });
    //suministro guardar
    $('form').on('submit', function (e) {
        e.preventDefault();

        if(suministro.items.producto.length === 0){
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        suministro.items.fecha_registro = $('input[name="fecha_registro"]').val();
        suministro.items.beneficiario = $('select[name="beneficiario"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('suministro', JSON.stringify(suministro.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            Swal.fire({
                title: 'Alerta',
                text: 'Registro creado correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/base/suministro/listado/';
                }
            })    
        });
    });
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_producto',
                    ids: JSON.stringify(suministro.get_ids()),
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cantidad = 1;
        data.subtotal = 0.000;
        suministro.add(data);
        $(this).val('').trigger('change.select2');
    });

    suministro.listado();
    
});
