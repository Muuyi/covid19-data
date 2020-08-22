$(document).ready(function(){
    $("#covid-data").dataTable({
        "ajax":{
            "processing":true,
            "serverSide" : true,
            "url":"{% url 'datatables-data' %}"
        } 
    })
})