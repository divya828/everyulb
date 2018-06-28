$(document).ready(function(){

  // progress-bar mods
  makeProgressBaseline();
  makeProgressSiteConceptual();
  makeProgressSiteCharacteristics();
  makeProgressWasteCharacteristics();

  // datepicker-css and js files initialized
  $('#datePicker').datepicker({format: 'mm-dd-yyyy'});

  //accordian collapse and expand chevron-up and down
  $('.collapse').on('shown.bs.collapse', function(){
    $(this).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down ");
  }).on('hidden.bs.collapse', function(){
    $(this).parent().find(".fa-chevron-down ").removeClass("fa-chevron-down ").addClass("fa-chevron-up");
  });

  $('#state').change(function() {
    $.ajax({
        url: api_sendDistricts,
        method: 'POST',
        data: {
            "state": document.getElementById('state').value.toString(),
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
            "button": "state"
        },
        success: function (data) {
          var district_html = '';
          for(var i = 0; i < data["districts"].length; i++) {
              var obj = data["districts"][i];
              district_html = district_html + '<option value="' + obj["district"] + '">' + obj["district"] + '</option>';
          }
          document.getElementById('district').innerHTML = district_html;
        }
    });

  });

});

var iBaseline = 0;
function makeProgressBaseline(){

  var count = 0;
  if($('#village_name').val() != "")
    count++;
  if($('#area').val() != "")
    count++;
  if($('#age').val() != "")
    count++;
  if($('#avg_depth').val() != "")
    count++;
  if($('#avg_height').val() != "")
    count++;
  if($('#status_summary_legal').val() != "")
    count++;
  if($('#fire_burning').val() != "")
    count++;
  if($('#fire_date').val() != "")
    count++;
  if($('#status_summary_fire').val() != "")
    count++;

  count = parseInt((count/9)*100) ;
  if(iBaseline <= count){
      iBaseline = count;
      if(iBaseline >=100)
      {
        $("#baseline_progress").removeClass('bg-warning');
        $("#baseline_progress").removeClass('bg-danger');
        $("#baseline_progress").addClass('bg-success');
        $("#baseline_progress").css("width", 100 + "%").text(100 + " %");
        $("#headingOneProgress").text("Scheme Baseline Data (" + 100 + " %" + " Completed)");
      }
      else if(iBaseline == 0)
      {
        $("#baseline_progress").removeClass('bg-warning');
        $("#baseline_progress").removeClass('bg-success');
        $("#baseline_progress").addClass('bg-danger');
        $("#baseline_progress").css("width", 100 + "%").text("Not Yet started");
        $("#headingOneProgress").text("Scheme Baseline Data (" + 0 + " %" + " Completed)");
      }
      else {
        $("#baseline_progress").removeClass('bg-success');
        $("#baseline_progress").removeClass('bg-danger');
        $("#baseline_progress").addClass('bg-warning');
        if (iBaseline < 5) {
          $("#baseline_progress").css("width", iBaseline + "%").text("");
        }
        else {
          $("#baseline_progress").css("width", iBaseline + "%").text(iBaseline + " %");
        }
        $("#headingOneProgress").text("Scheme Baseline Data (" + iBaseline + " %" + " Completed)");
      }
  }
  iBaseline = count;
  setTimeout("makeProgressBaseline()", 500);
}

var iSiteConceptual = 0;
function makeProgressSiteConceptual(){

  var count = 0;
  for (var i = 0; i < 10; i++) {
    if($('#s' + i).val() != "")
      count++;
  }

  count = parseInt((count/10)*100) ;
  if(iSiteConceptual <= count){
      iSiteConceptual = count;
      if(iSiteConceptual >=100)
      {
        $("#site_conceptual_progress").removeClass('bg-warning');
        $("#site_conceptual_progress").removeClass('bg-danger');
        $("#site_conceptual_progress").addClass('bg-success');
        $("#site_conceptual_progress").css("width", 100 + "%").text(100 + " %");
        $("#headingFourProgress").text("O & M Cost (" + 100 + " %" + " Completed)");
      }
      else if(iSiteConceptual == 0)
      {
        $("#site_conceptual_progress").removeClass('bg-warning');
        $("#site_conceptual_progress").removeClass('bg-success');
        $("#site_conceptual_progress").addClass('bg-danger');
        $("#site_conceptual_progress").css("width", 100 + "%").text("Not Yet started");
        $("#headingFourProgress").text("O & M Cost (" + 0 + " %" + " Completed)");
      }
      else {
        $("#site_conceptual_progress").removeClass('bg-success');
        $("#site_conceptual_progress").removeClass('bg-danger');
        $("#site_conceptual_progress").addClass('bg-warning');
        if (iSiteConceptual < 5) {
          $("#site_conceptual_progress").css("width", iSiteConceptual + "%").text("");
        }
        else {
            $("#site_conceptual_progress").css("width", iSiteConceptual + "%").text(iSiteConceptual + " %");
        }
        $("#headingFourProgress").text("O & M Cost (" + iSiteConceptual + " %" + " Completed)");
      }
  }
  iSiteConceptual = count;
  setTimeout("makeProgressSiteConceptual()", 500);
}

var iSiteCharacteristics = 0;
function makeProgressSiteCharacteristics(){

  var count = 0;
  for (var i = 0; i < 27; i++) {
    if(parseFloat(($('#site_characteristics_' + i).val())) != 0.0 && ($('#site_characteristics_' + i).val()) != "")
      count++;
  }

  count = parseInt((count/27)*100) ;
  if(iSiteCharacteristics <= count){
      iSiteCharacteristics = count;
      if(iSiteCharacteristics >=100)
      {
        $("#site_characteristics_progress").removeClass('bg-warning');
        $("#site_characteristics_progress").removeClass('bg-danger');
        $("#site_characteristics_progress").addClass('bg-success');
        $("#site_characteristics_progress").css("width", 100 + "%").text(100 + " %");
        $("#headingThreeProgress").text("Financial Details (" + 100 + " %" + " Completed)");
      }
      else if(iSiteCharacteristics == 0)
      {
        $("#site_characteristics_progress").removeClass('bg-warning');
        $("#site_characteristics_progress").removeClass('bg-success');
        $("#site_characteristics_progress").addClass('bg-danger');
        $("#site_characteristics_progress").css("width", 100 + "%").text("Not Yet started");
        $("#headingThreeProgress").text("Financial Details (" + 0 + " %" + " Completed)");
      }
      else {
        $("#site_characteristics_progress").removeClass('bg-success');
        $("#site_characteristics_progress").removeClass('bg-danger');
        $("#site_characteristics_progress").addClass('bg-warning');
        if (iSiteCharacteristics < 5) {
          $("#site_characteristics_progress").css("width", iSiteCharacteristics + "%").text("");
        }
        else {
          $("#site_characteristics_progress").css("width", iSiteCharacteristics + "%").text(iSiteCharacteristics + " %");
        }
        $("#headingThreeProgress").text("Financial Details (" + iSiteCharacteristics + " %" + " Completed)");
      }
  }
  iSiteCharacteristics = count;
  setTimeout("makeProgressSiteCharacteristics()", 500);
}

var iWasteCharacteristics = 0;
function makeProgressWasteCharacteristics(){

  var count = 0;
  var sum = 0;
  for (var i = 0; i < 2; i++) {
    sum = sum + parseFloat(($('#waste_characteristics_' + i).text()).slice(0,-1));
  }

  count = parseInt(sum/2) ;
  if(iWasteCharacteristics <= count){
      iWasteCharacteristics = count;
      if(iWasteCharacteristics >=100)
      {
        $("#waste_characteristics_progress").removeClass('bg-warning');
        $("#waste_characteristics_progress").removeClass('bg-danger');
        $("#waste_characteristics_progress").addClass('bg-success');
        $("#waste_characteristics_progress").css("width", 100 + "%").text(100 + " %");
        $("#headingTwoProgress").text("Water Quality Analysis (" + 100 + " %" + " Completed)");
      }
      else if(iWasteCharacteristics == 0)
      {
        $("#waste_characteristics_progress").removeClass('bg-warning');
        $("#waste_characteristics_progress").removeClass('bg-success');
        $("#waste_characteristics_progress").addClass('bg-danger');
        $("#waste_characteristics_progress").css("width", 100 + "%").text("Not Yet started");
        $("#headingTwoProgress").text("Water Quality Analysis (" + 0 + " %" + " Completed)");
      }
      else {
        $("#waste_characteristics_progress").removeClass('bg-success');
        $("#waste_characteristics_progress").removeClass('bg-danger');
        $("#waste_characteristics_progress").addClass('bg-warning');
        if (iWasteCharacteristics < 5) {
          $("#waste_characteristics_progress").css("width", iWasteCharacteristics + "%").text("");
        }
        else {
          $("#waste_characteristics_progress").css("width", iWasteCharacteristics + "%").text(iWasteCharacteristics + " %");
        }
        $("#headingTwoProgress").text("Water Quality Analysis (" + iWasteCharacteristics + " %" + " Completed)");
      }
  }
  iWasteCharacteristics = count;
  setTimeout("makeProgressWasteCharacteristics()", 500);
}
