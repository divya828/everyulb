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
