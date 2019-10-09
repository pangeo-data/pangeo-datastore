CMIP6 CSV Catalog
=================

.. raw:: html

  <head>
    <script src="https://unpkg.com/papaparse@5.1.0/papaparse.min.js"></script>
    <script src="https://unpkg.com/ag-grid-community/dist/ag-grid-community.min.noStyle.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/dist/styles/ag-grid.css">
    <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/dist/styles/ag-theme-balham.css">
  </head>

  <body>
    <div style="display: flex; flex-direction: row">
      <div style="overflow: auto; flex-grow: 1">
        <div id="myGrid" class="ag-theme-balham" style="height: 600px; width: 100%;"></div>
      </div>
    </div>

    <script type="text/javascript" charset="utf-8">
      // load in sample CSV catalog
      Papa.parse("https://storage.googleapis.com/pangeo-cmip6/pangeo-cmip6-zarr-consolidated-stores.csv", {
        download: true,
        header: true,
        complete: function(results) {
          makeGrid(results);
        }
      });

      // Main function to produce ag-Grid based on CSV table
      function makeGrid(results) {

        // specify the columms
        var columnDefs = getColumnDefs(results.meta.fields);

        // let the grid know which columns and what data to use
        var gridOptions = {
          defaultColDef: {
            editable: true,
            sortable: true,
            filter: true
          },
          columnDefs: columnDefs,
          rowData: results.data,
          rowSelection: 'multiple',
          enableCellTextSelection: true,
          onGridReady: function(params) {
            params.api.sizeColumnsToFit();

            window.addEventListener('resize', function() {
              setTimeout(function() {
                params.api.sizeColumnsToFit();
              })
            })
          }
        };

        // lookup the container we want the Grid to use
        var eGridDiv = document.querySelector('#myGrid');

        // create the grid passing in the div to use together with the columns & data we want to use
        new agGrid.Grid(eGridDiv, gridOptions);
      }

      // Get column definitions based on parsed fields
      function getColumnDefs(fields) {

        var columnDefs = [];

        for (var i = 0; i < fields.length; i++) {
          columnDefs.push({
            headerName: fields[i],
            field: fields[i]
          });
        }

        return columnDefs;
      }
    </script>
  </body>
