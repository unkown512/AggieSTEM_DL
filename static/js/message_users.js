/* 
  Add databtales to display user data or w.e
*/

console.log(dataSet);
console.log("wtf mate")
// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/
$(document).ready(function() {
  $('#users_table').DataTable( {
    data: dataSet,
    columns: [
      { title: "User" },
      { title: "Phone Number" },
      { title: "Groups" }
      
    ]
  } );
});