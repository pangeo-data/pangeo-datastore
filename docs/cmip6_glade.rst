GLADE CMIP6 Catalog
===================

This is a dynamically generated ESMCol collection.
This collection can be viewed directly at::

  https://raw.githubusercontent.com/NCAR/intake-esm-datastore/master/catalogs/glade-cmip6.json

.. raw:: html

  <pre id="json-renderer"></pre>

  <div style="display: flex; flex-direction: row">
    <div style="overflow: auto; flex-grow: 1">
      <div id="myGrid" class="ag-theme-balham" style="height: 600px; width: 100%;"></div>
    </div>
  </div>

  <script type="text/javascript" charset="utf-8">
    // fetch json file
    jQuery.getJSON("https://raw.githubusercontent.com/NCAR/intake-esm-datastore/master/catalogs/glade-cmip6.json", function(results) {
      $('#json-renderer').jsonViewer(results, {collapsed: true, rootCollapsable: false});
    })

    // load in sample CSV catalog
    Papa.parse("https://storage.googleapis.com/pangeo-cmip6/glade-cmip6.csv.gz", {
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
