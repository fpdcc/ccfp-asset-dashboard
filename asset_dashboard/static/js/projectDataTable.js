$(document).ready(function() {
    // soft refresh doesn't clear the filters, 
    // so always do it when the page loads 
    resetFilters()
    var table = $('#project-list-table').DataTable({
        serverSide: true,
        ajax: 'projects/json/',
        columns: [
            {
                name: 'id',
                orderable: true,
                searchable: true,
                visible: true,
                targets: [0]
            },
            {
                name: 'name',
                orderable: true,
                searchable: true,
                targets: [1]
            },
            {
                name: 'description',
                orderable: true,
                searchable: true,
                targets: [2],
            },
            {
                name: 'section_owner',
                orderable: true,
                searchable: false,
                targets: [3]
            },
            {
                name: 'category',
                orderable: true,
                searchable: false,
                targets: [4]
            },
            {
                name: 'project_manager',
                orderable: true,
                searchable: true,
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

                if (columnHeaderName === 'Section' || columnHeaderName === 'Category') {
                    const idSelectorName = columnHeaderName.toLowerCase()

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
            const projectId = data[0]

            // add the id as an attribute to the <tr> element
            $(row).data('project-id', projectId)

            // show the cursor pointer when a user hovers over the row
            // so they know they can click on it
            $(row).addClass('cursor-pointer')

            return row
        }
    });

    // listen to click event for redirecting to a project detail page
    $('#project-list-table tbody').on('click', 'tr', function () {
        const id = $(this).data('project-id')
        window.location = id ? '/projects/' + id : ''
    })

    // callback function for the search text input
    $('#search-filter').on('keyup', function() {
        table.search(this.value).draw();
    });
    
    $('#reset').on('click', function () {
      table.search( '' ).columns().search( '' ).draw()
      resetFilters()
    })

    // styling configuration for the table's pagination components
    $('div.dataTables_length').addClass('pt-3');
    $('div.dataTables_length label').addClass('d-flex flex-row');
    $('div.dataTables_paginate').addClass('pt-1');
  });
  
  function resetFilters() {
    $('#section-select').val('')
    $('#category-select').val('')
    $('#search-filter').val('')
  }
