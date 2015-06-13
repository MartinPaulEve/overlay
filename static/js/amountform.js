    $( document ).ready(function() {
        $('#{{wizard.form.reduced.auto_id}}').bind("change", update_value);
        $('#{{wizard.form.other_amount.auto_id}}').bind("keyup", argumentWrapper);
        $('#{{wizard.form.years.auto_id}}').bind("change", argumentWrapper);
    });

    function update_value() {
        var reduced = $('#{{wizard.form.reduced.auto_id}}');
        var other_amount = $('#{{wizard.form.other_amount.auto_id}}');

        var update_value = 0;

        var cascade = false;

        if(other_amount.val() != "")
        {
            if(isNaN(other_amount.val())){
                cascade = true;
            }

            if(cascade == false){
                if(parseInt(other_amount.val()) > 0){
                    update_value = other_amount.val();
                } else {
                    cascade = true;
                }
            }
        } else {
            cascade = true;
        }

        if(cascade) {
            if(reduced.is( ":checked" )) {
                update_value = "600";
            }
            else
            {
                update_value = "1000";   
            }
        }

        multiplier = parseInt($('#{{wizard.form.years.auto_id}}').val());

        update_value = update_value * multiplier;

        $('#level').text("$" + update_value);
    }

    function argumentWrapper(event)
    {
        update_value();
    }