/*
  Add databtales to display user data or w.e
*/
$(document).ready(function() {
  var editor = new $.fn.dataTable.Editor({
    ajax: {
      url: "/manage_users",
      type: "POST",
      data: function(args) {
        return { "data": JSON.stringify(args) };
      }
    },
    idSrc: 'uid',
    data: dataSet,
    table: "#users_table",
    fields: [{
      label: "User:",
      name: "username"
    }, {
      label: "Position:",
      name: "position"
    }, {
      label: "Access:",
      name: "access_level"
    }, {
      label: "Email:",
      name: "email"
    }, {
      label: "Phone Number:",
      name: "phone"
    }, {
      label: "Groups:",
      name: "groups"
    }, {
      label: "Last Login:",
      name: "last_login"
    }]
  });
  // Activate inline edit of a table cell
  $('#users_table').on('click', 'tbody td:not(:first-child)', function(e) {
    editor.inline(this, {
      submit: 'allIfChanged'
    });
  });

  // Create Data Table
  $('#users_table').DataTable( {
    dom: "Bfrtip",
    responsive: true,
    idSrc: 'uid',
    data: dataSet['data'],
    order: [[1, 'asc']],
    columns: [
      {
        title: "",
        data: null,
        defaultContent: '',
        className: 'select-checkbox',
        orderable: false
      },
      {
        title: "Username",
        data: "username",
        "render": function(data, type, row, meta) {
          data = '<a href="userProfile?username=' + row[0]
            + '&email=' + row['email']
            + '&phonenumber=' + row['phone']
            + '&type=1">' + data + '</a>';
          return data;
        }
      },
      {
        title: "Position",
        data: "position"
      },
      {
        title: "Access Level",
        data: "access_level"
      },
      {
        title: "Email",
        data: "email"
      },
      {
        title: "Phone Number",
        data: "phone",
        "render": function(data, type, row, meta) {
          return format_phonenumber(row['phone']);
        }
      },
      {
        title: "Groups",
        data: "groups"
      },
      {
        title: "Last-login",
        data: "last_login"
      },
    ],
    select: {
      style: 'os',
      selector: 'td:first-child'
    },
    buttons: [
      {extend: "remove", editor: editor}
    ]
  } ); // END of datatables
}); // END of document onready
