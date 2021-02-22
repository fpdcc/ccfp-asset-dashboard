$(document).ready(function() {
    var table = $('#project-by-district-list').DataTable({
        serverSide: true,
        ajax: 'json/',
        columns: [
            {
                name: 'name',
                orderable: true,
                searchable: true,
                targets: [0]
            },
            {
                name: 'description',
                orderable: true,
                searchable: true,
                targets: [1],
            },
            {
                name: 'senate_districts',
                orderable: true,
                searchable: false,
                targets: [2]
            },
            {
                name: 'house_districts',
                orderable: true,
                searchable: false,
                targets: [3]
            },
            {
                name: 'commissioner_districts',
                orderable: false,
                searchable: false,
                visible: true,
                targets: [4]
            },
            {
                name: 'id',
                orderable: false,
                searchable: false,
                visible: false,
                targets: [5]
            },
        ],

        // custom styles on some parts of the table
        // see https://datatables.net/reference/option/dom
        dom: "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col'l><'col'i><'col'p>>",

        // add callback functions to the select widgets for filtering
        initComplete: function () {
            this.api().columns().every( function () {
                let column = this;
                let columnHeaderName = column.header().textContent

                const idSelectorName = columnHeaderName.toLowerCase().split(' ')[0]

                const idSelectorsForFiltering = [
                    'senate',
                    'house',
                    'commissioner'
                ]

                if (idSelectorsForFiltering.includes(idSelectorName)) {
                    // add a callback to the html page's existing <select> 
                    $(`#${idSelectorName}-select`).on('change', function() {
                        let val = $.fn.dataTable.util.escapeRegex(
                          $(this).val()
                        );
  
                        return column.search(val ? val : '', true, false).draw();
                      });
                }

                    
            });
        },
        
        // make each row clickable for redirecting to the detail page
        fnRowCallback: function (row, data) {
            const projectId = data[5]

            // add the id as an attribute to the <tr> element
            $(row).data('project-id', projectId)

            // show the cursor pointer when a user hovers over the row
            // so they know they can click on it
            $(row).addClass('cursor-pointer')

            return row
        }
    });

    // listen to click event for redirecting to a project detail page
    $('#project-by-district-list tbody').on('click', 'tr', function () {
        const id = $(this).data('project-id')
        window.location = id ? '/projects/' + id : ''
    })

    // styling configuration for the table's pagination components
    $('div.dataTables_length').addClass('pt-3');
    $('div.dataTables_length label').addClass('d-flex flex-row');
    $('div.dataTables_paginate').addClass('pt-1');
    $('div.dataTables_info').addClass('text-center');
  });
