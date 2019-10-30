/* 
  Add databtales to display user data or w.e
*/
var dataSet = [
    [ "Tiger_Nixon", "Professor", "3", "tiger_nixon@tamu.edu", "610-432-2121", "Star, Spec","01/13/2019(21:45 GMT)"],
    [ "Garrett_Winters", "Research Assistant", "1", "garrett_winters@tamu.edu", "230-845-5846", "Web, Hrbb","10/24/2019(5:30 GMT)"],
    [ "James_Brown", "Research Assistant", "1", "j_brown@tamu.edu", "430-765-3446", "Spy, Nxt","08/01/2019(8:32 GMT)"]
];

$(document).ready(function() {
    $('#users_table').DataTable( {
        data: dataSet,
        columns: [
            { title: "User" },
            { title: "Position" },
            { title: "Access" },
            { title: "Email" },
            { title: "Phone Number" },
            { title: "Groups" },
            { title: "Last Login" },
            
        ]
    } );
});