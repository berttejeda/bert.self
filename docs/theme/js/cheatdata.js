$(document).ready(function() {
  $('#cheatData').DataTable( 
    {
      "searching": true,
      "paging": true, 
      "info": true,         
      "lengthChange": true,
      scrollX:        true,
      fixedColumns:   true,
      language: {
        searchPlaceholder: "Filter notes",
        search: "",
      }   
    }

  );


});


