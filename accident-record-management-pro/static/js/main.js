
$(document).ready(function(){
  if($.fn.dataTable) {
    $('table').not('#latestTable').DataTable();
  }
});
