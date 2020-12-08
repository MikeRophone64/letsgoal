document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM ready")

    $(document).ready(function() {

        // Datepicker function
        $( function() {
            $('#datepicker').datepicker({ dateFormat: 'yy-mm-dd' });
            console.log("JQuery ok")
        })

        // Click X to delete Goal
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

        // hover over like buttons to color them
        $(document).on("mouseenter", ".like", function() {
            const target_like = $(this);
            target_like.find(".like-fill").css({
                "fill-opacity": "50%",
            });
        })
        .on("mouseleave", ".like", function() {
            const target_like = $(this);
            target_like.find(".like-fill").css({
                "fill-opacity": "0%",
            });
        })

        // Click  like buttons to toggle Active class
        // and fetch data through API
        $(document).on("click", ".like", function() {

            // change color
            const target_like = $(this);
            

            // fetch like API
            const id = this.dataset.id;
            const url = "like/" + id;


            fetch(url)
            .then(response => response.json())
            .then(goal_response => {

                // change color
                if(goal_response.active_class === 'liked') {
                    target_like.find(".like-fill").addClass("like-active");
                } else {
                    target_like.find(".like-fill").removeClass("like-active");
                }

                // update Like count
                target_like.find(".numlikes").html(goal_response.num_likes)
            })
        })
    });

})