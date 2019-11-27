/*
  Add databtales to display user data or w.e
*/

// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/
$(document).ready(function() {

   var option = '';
   for(var i=0; i<groupSet.length; i++) {
     option += '<option value="' + groupSet[i] + '">' + groupSet[i] + '</option>';
   }
   $('#boot-multiselect-demo').append(option);

   $('#boot-multiselect-demo').multiselect({
       includeSelectAllOption: true,
       buttonWidth: 250,
       enableFiltering: true
   });
   function cbDropdown(column) {
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
    buttons: [],
    language: {},
    columns: [
      {
        data: null,
        defaultContent: '',
        className: 'control',
        orderable: false
      },
      {
        title: "Send",
        defaultContent: '',
        className: 'select-checkbox',
        data: null,
        orderable: false,
        "createdCell": function(td, cellData, rowData, row, col) {
          $(td).attr('id', rowData[0]);
        }
      },
      {
        title: "User",
        data: 1
      },
      {
        title: "Phone Number",
        "render": function(data, type, row, meta) {
          return format_phonenumber(row[2]);
        },
        data: 2
      },
      {
        title: "Groups",
        data: 3
      },

    ],
    select: {
      style:    'multi',
      selector: 'td.select-checkbox'
        },
  }); // End of datatables

  $('#boot-multiselect-demo').on('change', function() {
    var selected_groups = $('#boot-multiselect-demo').val();
    table.rows().data().each(function (value, index) {
      var has_group = 0;
      var row = table.row(index).node();
      if(value.includes("Select all")) {
        has_group = 1;
      } else {
        for(var i=0; i<selected_groups.length; i++) {
          if(value.includes(selected_groups[i])) {
            has_group = 1;
            break;
          }
        }
      }
      if(has_group == 1) {
        $(row).addClass('selected');
      } else {
        $(row).removeClass('selected');
      }
    });
  });
}); // End of document on ready
