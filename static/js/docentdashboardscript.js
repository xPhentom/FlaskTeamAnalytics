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

    $("#TileGroepenBewerken").on('click', function(){

      $("#dashboarddocent").hide();
      $("#groepenbewerken").show();

      $.ajax({
        type: "GET",
        url: "/studentengroepenopvragen",
        success: function(html){
          var rij = jQuery.parseJSON(html);

          for (var i = 0; i < rij.length; i++) {
            if($("#" + rij[i].GRO_naam).length != 0){
                console.log("Groep bestaat al");
            } else {
                $("#groepenlijst").prepend('<ul id="' + rij[i].GRO_naam + '" class="collection with-header groepslijst "><li class="collection-header groepslijst"><h4>' + rij[i].GRO_naam + '</h4></lu>');
            }
          }

          console.log(rij[1]);
        }
      })

      $.ajax({
          type: "POST",
          url: "/studentenbekijken",
          data: {},
          success: function(html) {
              var rij = jQuery.parseJSON(html);
              for (var i = 0; i < rij.length; i++) {
                if (rij[i].STU_rol == null) {
                  $("#lijstmetstudenten").append('<div class="chip" id = "' + rij[i].STU_id.toString() +'">  ' + rij[i].STU_achternaam + ' ' + rij[i].STU_voornaam + '</div><br>');
                } else {
                  $("#lijstmetstudenten").append('<div class="chip" id = "' + rij[i].STU_id.toString() + '">  ' + rij[i].STU_achternaam + ' ' + rij[i].STU_voornaam + ' -- ' + rij[i].STU_rol + '</div><br>');
                }
              }
              $(".chip").draggable();
          }
      })

    })

    $("#GroepToevoegenAanLijst").on('click', function(){
      var groepsnaam = prompt("Voer de naam in voor de groep", "Groepsnaam");
      console.log(groepsnaam);

      $("#groepenlijst").prepend('<ul class="collection with-header groepslijst "><li class="collection-header groepslijst"><h4>' + groepsnaam + '</h4></lu>'); //</li><li class="collection-item">test</li>
      $(".collection").droppable({
        drop: function (event, ui){
          $( this ).append((ui.draggable).text() + "<br>");

          var studentid = $(ui.draggable).attr('id');

          var groep =  $( this ).find("h4").text() //Aangezien de titel in een groep in h4 staat

          $.ajax({
            type:"POST",
            url:"/studentaangroeptoevoegen",
            data:{
              groep: groep,
              studentid: studentid
            },
            success: function(html) {
                Materialize.toast('Student is toegevoegd aan zijn groep', 3000, 'rounded');
          }
        })
          $( ui.draggable ).remove();
        }
      })
    })

});
