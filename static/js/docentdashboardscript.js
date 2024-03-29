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
    $("#groepenbewerken").hide();
    $("#groepenbekijken").hide();

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
                    $("#studentenlijst").append('<li> <div class="collapsible-header studentlijststyle"> ' + rij[i].STU_achternaam + ' ' + rij[i].STU_voornaam + '</i></div> <div class="collapsible-body"><p>mail: ' + rij[i].STU_mail + '</p> <p> rol: ' + rij[i].STU_rol + '</p></div></li>');
                }
            }
        })


    })

    $("#btnStudentToevoegen").on('click', function() {

        var voornaam, achternaam, mail, paswoord, school = "";

        voornaam = $("#voornaam").val();
        achternaam = $("#achternaam").val();
        mail = $("#mail").val();
        paswoord = $("#paswoord").val();
        school = $("#school").val();


        $.ajax({
            type: "POST",
            url: "/studenttoevoegen",
            data: {
                voornaam: voornaam,
                achternaam: achternaam,
                paswoord: paswoord,
                mail: mail,
                school: school
            },

            success: function(html) {
                $("#voornaam").val('');
                $("#achternaam").val('');
                $("#mail").val('');
                $("#paswoord").val('');
                $("#school").val('');
                Materialize.toast('Student is toegevoegd aan de databank', 3000, 'rounded');
            }
        });

    });

    $("#TileGroepenBewerken").on('click', function() {

        $("#dashboarddocent").hide();
        $("#groepenbewerken").show();

        var AlGebruikteStudenten = [];

        $.ajax({
            type: "GET",
            url: "/studentengroepenopvragen",
            success: function(html) {
                var rij = jQuery.parseJSON(html);

                var studententeller = 0;

                for (var i = 0; i < rij.length; i++) {
                    if ($("#" + rij[i].GRO_naam).length != 0) {
                        console.log("Groep staat al op het scherm");
                    } else {
                        $("#groepenlijst").prepend('<ul id="' + rij[i].GRO_naam + '" class="collection with-header groepslijst "><li class="collection-header groepslijst"><h4>' + rij[i].GRO_naam + '</h4></lu>');
                        for (var j = studententeller; j < rij.length; j++) {
                            if (rij[i].GRO_naam == rij[j].GRO_naam)
                                if (rij[j].STU_rol != null) {
                                    $("#" + rij[i].GRO_naam).append(rij[j].STU_achternaam + ' ' + rij[j].STU_voornaam + ' -- ' + rij[j].STU_rol + '<br>');

                                } else {
                                    $("#" + rij[i].GRO_naam).append(rij[j].STU_achternaam + ' ' + rij[j].STU_voornaam + '<br>');
                                }
                            AlGebruikteStudenten.push(rij[j].STU_id);
                        }
                    }

                    console.log(rij[1]);

                }

                $(".collection").droppable({
                    drop: function(event, ui) {
                        $(this).append((ui.draggable).text() + "<br>");

                        var studentid = $(ui.draggable).attr('id');

                        var groep = $(this).find("h4").text() //Aangezien de titel in een groep in h4 staat

                        $.ajax({
                            type: "POST",
                            url: "/studentaangroeptoevoegen",
                            data: {
                                groep: groep,
                                studentid: studentid
                            },
                            success: function(html) {
                                Materialize.toast('Student is toegevoegd aan zijn groep', 3000, 'rounded');
                            }
                        })
                        $(ui.draggable).remove();
                    }
                })
            }

        })

        $.ajax({
            type: "POST",
            url: "/studentenbekijken",
            data: {},
            success: function(html) {
                var rij = jQuery.parseJSON(html);
                for (var i = 0; i < rij.length; i++) {
                    console.log(AlGebruikteStudenten);
                    if (AlGebruikteStudenten.indexOf(rij[i].STU_id) < 0) {
                        if (rij[i].STU_rol == null) {
                            $("#lijstmetstudenten").append('<div class="chip" id = "' + rij[i].STU_id.toString() + '">  ' + rij[i].STU_achternaam + ' ' + rij[i].STU_voornaam + '</div><br>');
                        } else {
                            $("#lijstmetstudenten").append('<div class="chip" id = "' + rij[i].STU_id.toString() + '">  ' + rij[i].STU_achternaam + ' ' + rij[i].STU_voornaam + ' -- ' + rij[i].STU_rol + '</div><br>');
                        }
                    }
                }
                $(".chip").draggable();
            }
        })


    })

    $("#GroepToevoegenAanLijst").on('click', function() {
        var groepsnaam = prompt("Voer de naam in voor de groep", "Groepsnaam");
        console.log(groepsnaam);

        $("#groepenlijst").prepend('<ul class="collection with-header groepslijst "><li class="collection-header groepslijst"><h4>' + groepsnaam + '</h4></lu>'); //</li><li class="collection-item">test</li>
        $(".collection").droppable({
            drop: function(event, ui) {
                $(this).append((ui.draggable).text() + "<br>");

                var studentid = $(ui.draggable).attr('id');

                var groep = $(this).find("h4").text() //Aangezien de titel in een groep in h4 staat

                $.ajax({
                    type: "POST",
                    url: "/studentaangroeptoevoegen",
                    data: {
                        groep: groep,
                        studentid: studentid
                    },
                    success: function(html) {
                        Materialize.toast('Student is toegevoegd aan zijn groep', 3000, 'rounded');
                    }
                })
                $(ui.draggable).remove();
            }
        })
    })

    $("#TileGroepenBekijken").on('click', function() {
        $("#groepenbekijken").show();
        $("#dashboarddocent").hide();

        $.ajax({
            type: 'GET',
            url: "/beoordelingenophalen",
            success: function(html) {
                var rij = jQuery.parseJSON(html);

                for (var i = 0; i < rij.length; i++) {

                    console.log(rij[i]);
                    if ($("#" + rij[i].BEO_groep).length == 0)
                        $("#groepenophalenlijst").append('<li id="' + rij[i].BEO_groep + '"> <div class="collapsible-header studentlijststyle"> ' + rij[i].BEO_groep + '</div></i>');

                    if ($("#" + rij[i].BEO_groep + " #" + rij[i].STU_id).length == 0)
                        $("#" + rij[i].BEO_groep).append('<div id="' + rij[i].STU_id + '" class="collapsible-body">Student: ' + rij[i].STU_voornaam + ' ' + rij[i].STU_achternaam + '<br> Gemiddelde punten: <div class="' + rij[i].BEO_groep + ' ' + rij[i].STU_id + 'punten"></div> <br> Commentaar: <div class="' + rij[i].BEO_groep + ' ' + rij[i].STU_id + 'commentaar"> </div></div></li>');

                    if (rij[i].BEO_commentaar != "")
                        $("." + rij[i].BEO_groep + '.' + rij[i].STU_id + "commentaar").append(rij[i].BEO_commentaar + "<br>");

                    $("#" + rij[i].BEO_groep + " #" + rij[i].STU_id).append("<br>");

                    var totaalpunten = 0;
                    var totaalbeoordelingen = 0;

                    for (var j = 0; j < rij.length; j++){
                      if (rij[i].STU_id == rij[j].STU_id){
                        totaalpunten += parseInt(rij[j].BEO_punt);
                        totaalbeoordelingen += 1;
                      }
                      if (j == rij.length - 1){
                        var gemiddeldescore = totaalpunten / totaalbeoordelingen;
                        console.log(gemiddeldescore);
                        console.log("." + rij[i].BEO_groep + " " + rij[i].STU_id + "punten");
                        $("." + rij[i].BEO_groep + "." + rij[i].STU_id + "punten").html(gemiddeldescore);
                      }
                    }

                }

            }
        })
    })

});
