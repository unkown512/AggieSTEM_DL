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
  var table = $('#users_table').DataTable( {
    dom: "Bfrtip",
    responsive: true,
    idSrc: 'uid',
    data: dataSet['data'],
    'createdRow': function(row, data, dataIndex) {
      if(data['deleted'] == "True") {
        console.log("WTF");
        $(row).addClass('red');
      }
    },
    order: [[1, 'asc']],
    columns: [
      {
        title: "",
        data: null,
        defaultContent: '',
        className: 'control',
        orderable: false

      },
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
      {extend: "remove", editor: editor},
      {extend: "edit", editor: editor},
      {
        text: "Undelete",
        action: function(e, dt, node, config) {
          var row = table.rows({ selected: true  }).data()[0];
          if(row['deleted'] == "True") {
            console.log(row);
            var json_data = { "data" : {"uid": row['uid']}, "action": "unremove"};
            undelete_user(json_data);
          }
        }
      }
    ]
  }); // END of datatables
  function undelete_user(json_data) {
    $.ajax({
      url: "manage_users",
      type: "POST",
      data: { "data" : JSON.stringify(json_data)},
      success: function() {
        console.log("success")
      }, function(error) {
        console.log(error);
      }
    });

  }
}); // END of document onready
