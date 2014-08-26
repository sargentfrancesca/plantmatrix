<html>
<head><title>GeoJSON</title>
<script src='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.js'></script>
<link href='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.css' rel='stylesheet' />

<style type="text/css">

#map {
	width: 100%;
	height: 100%;
}


</style>
</head>

<body>

<?php

//Connect to MySQL

$connect = mysql_connect("localhost","root","");

$mapa = "SELECT * FROM plantMatrix.coordsTest WHERE plantMatrix.coordsTest.LatitudeDec != 'NA'";

$dbquery = mysql_query($mapa,$connect);

//Creating GeoJSON array, ready to store values in GeoJSON format 
//GeoJSON format reference - http://geojson.org/
$geojson = array( 'type' => 'FeatureCollection', 'features' => array());

while($row = mysql_fetch_assoc($dbquery)){

  $marker = array(
    'type' => 'Feature',
    'properties' => array(
      'title' => $row['SpeciesAccepted'],
      'marker-color' => '#9b59b6',
      'marker-size' => 'small'
    ),
    'geometry' => array(
      'type' => 'Point',
      'coordinates' => array( 
        $row['LongitudeDec'],
        $row['LatitudeDec']
      )
    )
  );
  array_push($geojson['features'], $marker);
  //echo json_encode($marker);
}

?>

<div id="map"></div>

<script>
//Get GeoJSON from PHP, store as js var
var geoJson = <?php echo json_encode($geojson,JSON_NUMERIC_CHECK); ?>;
console.log(geoJson);

L.mapbox.accessToken = 'pk.eyJ1IjoiZnJhbmNlc2Nhc2FyZ2VudCIsImEiOiJvZmFuUzM0In0.-gsScOsPRxKs9E8qNy3qwg';

// Create a map in the div #map
L.mapbox.map('map', 'francescasargent.ja3p4m1n').setView([-34.67, -46.295508], 3).featureLayer.setGeoJSON(geoJson);





</script>


</body>
</html>
