/*
  Add databtales to display user data or w.e
*/

console.log(groupSet);
// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/
$(document).ready(function() {
   var option = '';
   for(var i=0; i<groupSet.length; i++) {
     console.log(groupSet[i]);
     option += '<option value="' + groupSet[i] + '">' + groupSet[i] + '</option>';
   }
   $('#boot-multiselect-demo').append(option);
   $('#boot-multiselect-demo').multiselect({
       includeSelectAllOption: true,
       buttonWidth: 250,
       enableFiltering: true
   });
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
  }); // End of datatables
}); // End of document on ready
