/* 
  Add databtales to display user data or w.e
*/

console.log(groupSet);
console.log("wtf mate")
// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/
$(document).ready(function() {
   function cbDropdown(column) {
     //console.log(button)
    return $('<ul>', {
      'class': 'cb-dropdown'
    }).appendTo($('<div>', {
      'class': 'cb-dropdown-wrap'
    }).appendTo(column));
  }
  
  var table = $('#message_users_table').DataTable( {
    responsive: true,
    data: dataSet,
    groups: groupSet,
    dom: 'Blfrtip',
    buttons: [
        'selectAll',
        'selectNone'/*,
        {
          extend: 'collection',
          text: 'Select Groups',
          select: {
          selector: 'td.select-checkbox'
            
          }
        }*/
        
    ],
    language: {
        buttons: {
            selectAll: "Select all Users",
            selectNone: "Select none",
            //selectGroups: "Select Groups"
        }
    },
    columns: [
      {
        data: null,
        defaultContent: '',
        className: 'control',
        orderable: false
      },
      {
        data: null,
        defaultContent: '',
        className: 'select-checkbox',
        orderable: false
      },
      { 
        title: "User",
        data: 0 
      },
      { 
        title: "Phone Number",
        data: 1 
      },
      { 
        title: "Groups",
        data: 2
      },

    ],
      
    select: {
      style:    'multi',
      selector: 'td.select-checkbox'
        },
        
        initComplete: function() {
      this.api().columns([4]).every(function() {
        var column = this;
        console.log(column);
       
        var ddmenu = cbDropdown($(column.header())).click(function(event){event.stopPropagation();})
          .on('change', ':checkbox', 'click', function(e){
            e.stopPropagation();
            var vals = $(':checked', ddmenu).map(function(index, element) {
              return $.fn.dataTable.util.escapeRegex($(element).val());
            }).toArray();
            
            /*var x;
            console.log(vals);
            for (x of vals){
              console.log(column.search(x).row())
              //table.row(column.search(x).row.deselect();
              if (column.search(x)) {
                column.search(x).draw();
                //table.row(column.search(x).draw()).select();
              }
              
            //  column.draw();
            }*/
            column
                        .search( vals ? vals : '', true, false ) 
                        .draw();
            e.stopPropagation();
          });
          

        groupSet.forEach(function(d, j) {
          var // wrapped
            $label = $('<label>'),
            $text = $('<span>', {
              text: d,
              orderable: false
            }),
            $cb = $('<input>', {
              type: 'checkbox',
              value: d,
              orderable: false
            });

          $text.appendTo($label);
          $cb.appendTo($label);

          ddmenu.append($('<li>').append($label));
        });
      });
    }
        
  } );
});
