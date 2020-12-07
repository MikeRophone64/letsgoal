document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM ready")

    $(document).ready(function() {
        $( function() {
            $('#datepicker').datepicker({ dateFormat: 'yy-mm-dd' });
            console.log("JQuery ok")
        })

        $(document).on("click",".delete-goal", function() {
            const id = $(this).attr("data-id");
            const container = $('#card_' + id);
            console.log(container)

            const r = confirm("Delete this Goal?")
            if(r == true) {
                container.hide()
                fetch("/delete_goal/" + id)
            }
        })
    });

})