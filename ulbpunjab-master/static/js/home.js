//Global variable for markers
var markers = [];

//For the center of the map, fits perfectly for 1242*640
var center = {lat: 31.192873, lng: 75.411712 };

// Changes height of map elemnt based on the broser size
// var height_of_map = window.innerHeight - $("#map").offset().top + 10;
// $("#map").height(height_of_map);

// window.addEventListener('resize', function (event) {
//       var height_of_map = window.innerHeight - $("#map").offset().top + 10;
//       $("#map").height(height_of_map);
// });
//End changing height

//Declaring new map
var customMapTypeId = 'pure_blank';
var customMapType = new google.maps.StyledMapType([
  {
  "featureType": "water",
  "elementType": "geometry",
  "stylers": [
    { "visibility": "off" }
  ]
  },{
  "featureType": "landscape",
  "stylers": [
    { "visibility": "off" }
  ]
  },{
  "featureType": "road",
  "stylers": [
    { "visibility": "off" }
  ]
  },{
  "featureType": "administrative",
  "stylers": [
    { "visibility": "off" }
  ]
  },{
  "featureType": "poi",
  "stylers": [
    { "visibility": "off" }
  ]
  },{
  "featureType": "administrative",
  "stylers": [
    { "visibility": "off" }
  ]
  },{
  "elementType": "labels",
  "stylers": [
    { "visibility": "off" }
  ]
  }
], {
  name: 'pure_blank'
});

var map = new google.maps.Map(document.getElementById('map'), {
  zoom: 7,
  center: center,
  mapTypeId: google.maps.MapTypeId.ROADMAP,
  disableDefaultUI: true,
  draggable: true,
  // backgroundColor: '#FFF',
  scaleControl: true,
  scrollwheel: true,
  zoomControl: true,
  zoomControlOptions: 'BOTTOM_RIGHT',
});
map.mapTypes.set(customMapTypeId, customMapType);
map.setMapTypeId(customMapTypeId);

// The data provided by pollution board to swagatam.  -1 is for places with no data
var json_no_landfills = {'Andaman & Nicobar Island': 0,
'Andhra Pradesh': 108,
'Arunanchal Pradesh': 2,
'Assam': 94,
'Bihar': -1,
'Chandigarh': 0,
'Chhattisgarh': 79,
'Dadara & Nagar Havelli': -1,
'Daman & Diu': -1,
'Goa': 4,
'Gujarat': 170,
'Haryana': 60,
'Himachal Pradesh': -1,
'Jammu & Kashmir': 27,
'Jharkhand': -1,
'Karnataka': 204,
'Kerala': -1,
'Lakshadweep': -1,
'Madhya Pradesh': 0,
'Maharashtra': 265,
'Manipur': -1,
'Meghalaya': 6,
'Mizoram': -1,
'Nagaland': -1,
'NCT of Delhi': 0,
'Puducherry': 3,
'Punjab': 161,
'Rajasthan': -1,
'Sikkim': -1,
'Tamil Nadu': 0,
'Telangana': 68,
'Tripura': 17,
'Uttar Pradesh': 2,
'Uttarakhand': 87,
'West Bengal': -1,
'Odisha': 60 };

// Loads The states data layer to maps
states_load_geojson = new google.maps.Data();
states_load_geojson.loadGeoJson(states_url);
states_load_geojson.setMap(map);
// states_load_geojson = map.data.loadGeoJson(states_url);

// Colour states based on whether or not data provided.
function setStyleStates(feature) {
  var color = 'gray';
  var state = feature.getProperty('ST_NM').toString();
  if (json_no_landfills[state] == -1) {
    color = '#FF0000';
  }
  else {
    color = '#0000FF';
  }
  return /** @type {google.maps.Data.StyleOptions} */({
    fillColor: color,
    // strokeColor: color,
    // strokeWeight: 2
  });
}
states_load_geojson.setStyle(function(feature) {
  return setStyleStates(feature);
});

//States mouseover display the data(no. of landfills) about states and changes colour to white
// var lol = [];

function listener1_func(event) {
  states_load_geojson.overrideStyle(event.feature, {fillColor: 'white'});
  // console.log(event.feature);
  var state = event.feature.getProperty('DISTRICT').toString();
  if (json_no_landfills[state] != -1) {
    document.getElementById('info-box').innerHTML = state;
  }
  else {
    document.getElementById('info-box').innerHTML = 'Data Not Provided in ' + state;
  }

}
var listener1 = states_load_geojson.addListener('mouseover', function (event) {
  listener1_func(event);
});


//Restores to the (landfill data provided or not) colour when mouse leaves the feature
function listener2_func(event) {
  var state = event.feature.getProperty('ST_NM').toString();
  if (json_no_landfills[state] != -1) {
    states_load_geojson.overrideStyle(event.feature, {fillColor: '#0000FF'});
  }
  else {
    states_load_geojson.overrideStyle(event.feature, {fillColor: '#FF0000'});
  }
}
var listener2 = states_load_geojson.addListener('mouseout', function (event) {
  listener2_func(event);
});

// Listening to clicking on the states feature and zooms into the districts view
// then loads the districts from separate districts files from the server
var district_load_geojson = new google.maps.Data(); // Creates a layer for loading districts geojson data
var listener3;
var flag0 = 0; //Makes sure clicking on districts more than once does not break code.
var flag1 = 0; // Makes sure clicking on states more than once does not break code.

function listener_click_states_func(event) {
  if (flag1 == 0) {
    flag1 = 1;
    var district = (event.feature.getProperty('DISTRICT')).toString();
    console.log(district);

    switch (district) {
      case "Hoshiarpur":
        window.location.href='/details/11/';
        break;
      case "Gurdaspur":
        window.location.href='/details/12/';
        break;
      case "Amritsar":
      window.location.href='/details/13/';
      break;
      case "Tarn Taran":
      window.location.href='/details/14/';
      break;
      case "Firozpur":
      window.location.href='/details/15/';
      break;
      case "Faridkot":
      window.location.href='/details/16/';
      break;
      case "Muktsar":
      window.location.href='/details/17/';
      break;
      case "Moga":
      window.location.href='/details/18/';
      break;
      case "Bathinda":
      window.location.href='/details/19/';
      break;
      case "Mansa":
      window.location.href='/details/20/';
      break;
      case "Sangrur":
      window.location.href='/details/21/';
      break;
      case "Barnala":
      window.location.href='/details/22/';
      break;
      case "Ludhiana":
      window.location.href='/details/23/';
      break;
      case "Fatehgarh Sahib":
      window.location.href='/details/24/';
      break;
      case "Patiala":
      window.location.href='/details/25/';
      break;
      case "Sahibzada Ajit Singh Nagar":
      window.location.href='/details/26/';
      break;
      case "Rupnagar":
      window.location.href='/details/27/';
      break;
      case "Shahid Bhagat Singh Nagar":
      window.location.href='/details/28/';
      break;
      case "Jalandhar":
      window.location.href='/details/29/';
      break;
      case "Kapurthala":
      window.location.href='/details/30/';
      break;

    }

  }
}
var listener_click_states = states_load_geojson.addListener('click', function(event) {
  listener_click_states_func(event);
});

// Adding the landfill markers.
function addMarker(location, map, data) {

}


// Searching features
var input = document.getElementById('pac-input');
var searchBox = new google.maps.places.SearchBox(input);
// var autocomplete = new google.maps.places.Autocomplete(input);

map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

// Bias the SearchBox results towards current map's viewport.
map.addListener('bounds_changed', function() {
  searchBox.setBounds(map.getBounds());
});


// var markers1 = [];
// Listen for the event fired when the user selects a prediction and retrieve
// more details for that place.
searchBox.addListener('places_changed', function(event) {
  var places = searchBox.getPlaces();

  if (places.length == 0) {
    return;
  }

  if (flag0 !=0 || flag1 !=0) {
      $('#back_to_states').trigger('click');
  }

  // For each place, get the icon, name and location.
  var bounds = new google.maps.LatLngBounds();
  places.forEach(function(place) {
    if (!place.geometry) {
      console.log("Returned place contains no geometry");
      return;
    }

    // new google.maps.event.trigger(listener_click_states , 'click' , event);
    // trigger(instance:Object, eventName:string, var_args:...)
    // console.log(place.geometry.location.latLng);
    // google.maps.event.trigger(place.geometry.location, 'click');
    // clickOnMap(place.geometry.location.lat(), place.geometry.location.lng(), map, )
    var event1 = {latLng: {}};
      // event1.latLng.lat = place.geometry.location.lat();
      event1.latLng.lat = function() { return place.geometry.location.lat() };
      // event1.latLng.lng = place.geometry.location.lng();
      event1.latLng.lng = function() { return place.geometry.location.lng() };
    console.log(event1);
    // var l = google.maps.event.trigger(states_load_geojson, 'click', {feature: {"ST_NM": "Assam"}});
    // var l = google.maps.event.trigger(states_load_geojson, 'click', event1);
    // var l = new google.maps.event.trigger( event1, 'click' );
    // var l = new google.maps.event.trigger(map.data, "click", event1);
    // console.log(l);
    clickOnMap(place.geometry.location.lat(), place.geometry.location.lng());
    // google.maps.event.trigger(map, 'click', event1);

    if (place.geometry.viewport) {
      // Only geocodes have viewport.
      bounds.union(place.geometry.viewport);
    } else {
      bounds.extend(place.geometry.location);
    }
  });
  map.fitBounds(bounds);
});
//
function clickOnMap(lat, lng) {
  var event = {latLng: {}};
  event.latLng.lat = function() { return lat };
  event.latLng.lng = function() { return lng };
  var y = google.maps.event.trigger(map.data, 'click', event);
  console.log(y);
}
