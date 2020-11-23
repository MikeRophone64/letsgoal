document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM ready")

    $(document).ready(function() {
        $( function() {
            $('#datepicker').datepicker();
            console.log("JQuery ok")
        })

    });
})