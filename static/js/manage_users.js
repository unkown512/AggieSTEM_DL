/*
  Add databtales to display user data or w.e
*/
$(document).ready(function() {
  $('#users_table').DataTable( {
    responsive: true,
    data: dataSet,
    columns: [
      {
        title: "User",
        "render": function(data, type, row, meta) {
          data = '<a href="userProfile?username=' + row[0]
            + '&email=' + row[3]
            + '&phonenumber=' + row[4]
            + '&type=1">' + data + '</a>';
          return data;
        }
      },
      { title: "Position" },
      { title: "Access" },
      { title: "Email" },
      { title: "Phone Number" },
      { title: "Groups" },
      { title: "Last Login" },

    ]
  } );
});
