//Global variable for markers
var markers = [];

//For the center of the map, fits perfectly for 1242*640
var center = {lat:   24.767666172, lng:  80.58949661 };

// Changes height of map elemnt based on the broser size
var height_of_map = window.innerHeight - $("#map").offset().top + 10;
$("#map").height(height_of_map);

window.addEventListener('resize', function (event) {
      var height_of_map = window.innerHeight - $("#map").offset().top + 10;
      $("#map").height(height_of_map);
});
//End changing height


//Declaring new map
var map = new google.maps.Map(document.getElementById('map'), {
  zoom: 4,
  center: center,
  mapTypeId: google.maps.MapTypeId.ROADMAP,
  disableDefaultUI: true,
  draggable: true,
  // backgroundColor: '#FFF',
  scaleControl: true,
  scrollwheel: true,
  zoomControl: true,
  zoomControlOptions: 'BOTTOM_RIGHT',
  styles: [
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
  ]
});

// The data provided by pollution board to swagatam
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

var flag0 = 0;
var flag1 = 0;

// Loads The states data layer to maps
// states_load_geojson = new google.maps.Data();
// states_load_geojson.loadGeoJson(states_url);
// states_load_geojson.setMap(map);
states_load_geojson = map.data.loadGeoJson(states_url);

map.data.setStyle(function(feature) {
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
});


//States mouseover display the data about states
var listener1 = map.data.addListener('mouseover', function(event) {
      map.data.overrideStyle(event.feature, {fillColor: 'white'});
      // console.log(event.feature);
      var state = event.feature.getProperty('ST_NM').toString();
      if (json_no_landfills[state] != -1) {
        document.getElementById('info-box').innerHTML = json_no_landfills[state] + ' Landfills in ' + state;
      }
      else {
        document.getElementById('info-box').innerHTML = 'Data Not Provided in ' + state;
      }

});

var listener3 = map.data.addListener('mouseout', function(event) {
      var state = event.feature.getProperty('ST_NM').toString();
      if (json_no_landfills[state] != -1) {
        map.data.overrideStyle(event.feature, {fillColor: '#0000FF'});
      }
      else {
        map.data.overrideStyle(event.feature, {fillColor: '#FF0000'});
      }

});

var listener2;

var listener_click_states = map.data.addListener('click', function(event) {
  if (flag1 == 0) {
    flag1 = 1;
    var state = (event.feature.getProperty('ST_NM')).toString();
    var iter1 = 0;
    map.data.forEach(function(feature) {
      // if (iter1 % 2 == 0) {
      //
      // }
      // else {
      //   map.data.overrideStyle(event.feature, {fillColor: 'blue'});
      // }
      // if ((feature.getProperty('ST_NM')).toString() != state) {
              map.data.remove(feature);
          // }
    });

    map.data.loadGeoJson(district_url + encodeURI(state) + '.geojson', null, function(enjoy) {
      flag0 = 1;
      google.maps.event.removeListener(listener1);
      listener2 = map.data.addListener('mouseover', function(event1) {
        if (event1.feature.getProperty('DISTRICT')) {
            document.getElementById('info-box').innerHTML = 'Landfills in ' + event1.feature.getProperty('DISTRICT') + ", " + event1.feature.getProperty('ST_NM');
        }
      });
    });

    if (map.getZoom() < 6) {
      map.setZoom(6);
    }
    map.panTo(event.latLng);
  }

});

// Adds a marker to the map.
function addMarker(location, map, data) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    animation: google.maps.Animation.DROP
  });
  marker.setMap(map);
  var contentString = '<div class="container">' +
  '<h2 align="center">' + data["name"] + '</h2>' +
  '<span id="more_details"><a href="' + data["url"] +  '">More Details</a></span>' +
  '<div class="row-fluid">' +
  '<div class="card">' +
  '<ul class="list-group list-group-flush">' +
  '<li class="list-group-item"><strong>Coordinates(Lat, Lng) : ' + data["latitude"] + ',' + data["longitude"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The area is : ' + data["area"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The nearest Airport is : ' + data["airport_name"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The distance from the Airport is : ' + data["distance_airport"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The nearest Road is : ' + data["road_name"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The distance from Road is : ' + data["distance_road"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The distance from nearest WaterBody(Lakes, Ponds) is : ' + data["distance_water"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The distance from nearest Well is : ' + data["distance_well"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The nearest River is : ' + data["river_name"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The distance from River is : ' + data["distance_river"] + 'meters</strong></li>' +
  '</ul>' +
  '</div>' +
  '</div>' +
  '</div>';

  var infowindow = new google.maps.InfoWindow({
    content: contentString
  });
  marker.addListener('click', function() {
    if (map.getZoom() < 15) {
      map.setZoom(15);
    }
    map.panTo(marker.getPosition());
    infowindow.open(map, marker);
  });
  return marker;
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


var markers1 = [];
// Listen for the event fired when the user selects a prediction and retrieve
// more details for that place.
searchBox.addListener('places_changed', function(event) {
  var places = searchBox.getPlaces();

  if (places.length == 0) {
    return;
  }

  // Clear out the old markers.
  markers1.forEach(function(marker) {
    marker.setMap(null);
  });
  markers1 = [];

  // For each place, get the icon, name and location.
  var bounds = new google.maps.LatLngBounds();
  places.forEach(function(place) {
    if (!place.geometry) {
      console.log("Returned place contains no geometry");
      return;
    }
    // var icon = {
    //   url: place.icon,
    //   size: new google.maps.Size(71, 71),
    //   origin: new google.maps.Point(0, 0),
    //   anchor: new google.maps.Point(17, 34),
    //   scaledSize: new google.maps.Size(25, 25)
    // };
    //
    // Create a marker for each place.
    // markers1.push(new google.maps.Marker({
    //   map: map,
    //   icon: icon,
    //   title: place.name,
    //   position: place.geometry.location
    // }));

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
    var l = new google.maps.event.trigger(map.data, "click", event1);
    console.log(l);
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
// function clickOnMap(lat, lng, map, name) {
//   var event = {latLng: {}};
//   event.latLng.lat = function() { return lat };
//   event.latLng.lng = function() { return lng };
//   event.feature.getProperty = function(property) { return name; };
//   console.log("YESs");
//   google.maps.event.trigger(map.data , 'click' , event);
//   // google.maps.event.trigger(map, 'click', event);
//
// }
