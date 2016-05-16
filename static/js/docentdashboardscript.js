$(".button-collapse").sideNav();
// Initialize collapsible (uncomment the line below if you use the dropdown variation)
//$('.collapsible').collapsible();

$(document).ready(function() {

    $('.collapsible').collapsible({
        accordion: false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });

    $("#dashboarddocent").show();
    $("#StudentToevoegen").hide();
    $("#studentbekijken").hide();

    $("#TileStudentToevoegen").on('click', function() {
        $("#dashboarddocent").hide();
        $("#StudentToevoegen").show();
    })

    $("#TileStudenBekijken").on('click', function() {
        $("#dashboarddocent").hide();
        $("#studentbekijken").show();

        $.ajax({
            type: "POST",
            url: "/studentenbekijken",
            data: {},
            success: function(html) {
                var rij = jQuery.parseJSON(html);
                for (var i = 0; i < rij.length; i++) {
                   $("#studentenlijst").append('<li> <div class="collapsible-header studentlijststyle"> ' + rij[i].STU_achternaam + ' ' + rij[i].STU_voornaam + '</i></div> <div class="collapsible-body"><p>klas: ' + rij[i].STU_klas + '</p> <p>mail: ' + rij[i].STU_mail + '</p> <p> rol: ' + rij[i].STU_rol + '</p></div></li>');
                }
            }
        })


    })

    $("#btnStudentToevoegen").on('click', function() {

        var voornaam, achternaam, mail, paswoord, klas, les = "";

        voornaam = $("#voornaam").val();
        achternaam = $("#achternaam").val();
        mail = $("#mail").val();
        paswoord = $("#paswoord").val();
        klas = $("#klas").val();
        les = $("#les").val();

        $.ajax({
            type: "POST",
            url: "/studenttoevoegen",
            data: {
                voornaam: voornaam,
                achternaam: achternaam,
                paswoord: paswoord,
                mail: mail,
                klas: klas,
                les: les
            },

            success: function(html) {
                $("#voornaam").val('');
                $("#achternaam").val('');
                $("#mail").val('');
                $("#paswoord").val('');
                $("#klas").val('');
                $("#les").val('');
                Materialize.toast('Student is toegevoegd aan de databank', 3000, 'rounded');
            }
        });

    });
});
