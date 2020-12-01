document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM ready")

    $(document).ready(function() {
        $( function() {
            $('#datepicker').datepicker({ dateFormat: 'yy-mm-dd' });
            console.log("JQuery ok")
        })

    });
})