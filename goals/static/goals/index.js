document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM ready")


    // TEST FETCH REST API
    fetch('/api/v1/goals/?format=json')
    .then(response => response.json())
    .then(data => {
        console.log(data.results)
    })
    .catch(err => {
        console.log(err)
    })
    // WORKS !!




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


        //User Profile
        // Show Overview and hide others by default

        $(".profile-overview").show();
        $(".profile-overview").siblings().hide();

        // Show and hide Profile sections
        $(document).on("click", ".profile-nav", function() {

            const myTarget = this.dataset.name;
            $(".profile-" + myTarget).show()
            $(".profile-" + myTarget).siblings().hide()
        })

    // User Profile Password change
    // Enable submit if new password and confirm password match
    const confirmHelp = document.getElementById('confirmHelp');
    const submitPassword = document.getElementById('submitPassword');

    $("#confirmPassword").on('keyup', function() {

        if($("#newPassword").val() === $("#confirmPassword").val()) {
            confirmHelp.innerHTML = "Passwords match!";
            confirmHelp.style.color = "green";
            submitPassword.disabled = false;
        } else {
            confirmHelp.innerHTML = "Passwords do not match...";
            confirmHelp.style.color = "red";
            submitPassword.disabled = true;
        }
    })
    });

})