$(document).ready(function() {
    var table = $('#project-list-table').dataTable({
        "serverSide": true,
        ajax: "json",
        columnDefs: [
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
                targets: [1]
            },
            {
                name: 'section_owner',
                orderable: true,
                searchable: true,
                targets: [2]
            },
            {
                name: 'category',
                orderable: true,
                searchable: true,
                targets: [3]
            },
            {
                name: 'id',
                orderable: false,
                searchable: false,
                visible: false,
                targets: [4]
            },
        ],

        // custom styles on some parts of the table
        // see https://datatables.net/reference/option/dom
        dom: "<f>" +
          "<'row'<'col-sm-12'tr>>" +
          "<'row'<'col'l><'col'i><'col'p>>",

        // hide the search input label and add the text as placeholder
        language: {
          search: "",
          searchPlaceholder: "Search projects"
        },

        // render the select widgets for filtering
        initComplete: function () {
            this.api().columns().every( function () {
                let column = this;

                let columnHeaderName = column.header().textContent

                if (columnHeaderName === 'Section' || columnHeaderName === 'Category') {
                  // create the select widget and add it to the DOM
                  var selectWidget = $(`<select class="form-control-sm col-4 m-1">
                                          <option value="" disabled selected>
                                            Filter by ${columnHeaderName}
                                          </option>
                                        </select>`)

                    .appendTo($('#project-list-table_filter'))
                    .on('change', function() {
                      var val = $.fn.dataTable.util.escapeRegex(
                        $(this).val()
                      );

                      column
                        .search(val ? val : '', true, false)
                        .draw();
                    });
                    
                    // add the available options
                    column.data().unique().sort().each(function (fieldText) {
                      selectWidget.append(`<option value="${fieldText}">${fieldText}</option>`)
                    });
                }
            });
        },
        
        // make each row clickable in order to redirect to the detail page
        fnRowCallback: function (row, data) {
            const projectId = data[4]

            // add the id as an attribute to the <tr> element
            $(row).data('project-id', projectId)

            // show the cursor pointer when a user hovers over the row
            // so they know they can click on it
            $(row).addClass('cursor-pointer')

            return row
        }
        
    });

    // add the click event in order to redirect to a project detail page
    $('#project-list-table tbody').on('click', 'tr', function () {
        const id = $(this).data('project-id')
        window.location = '/projects/' + id
    })

    // configure styling for some of the table components
    $('div.dataTables_filter').addClass('row');
    $('div.dataTables_filter label').addClass('col-3 m-1');
    $('div.dataTables_length').addClass('pt-3');
    $('div.dataTables_length label').addClass('d-flex flex-row');
    $('div.dataTables_paginate').addClass('pt-1');
  });
