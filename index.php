<html>
<head><title>GeoJSON</title>
<script src='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.js'></script>
 <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link href='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.css' rel='stylesheet' />
<link href="ico.css" rel='stylesheet'/>

<style type="text/css">

body {
  font-family: Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
}

#toolbar {
  height: 3%;
  position: absolute;
  top: 0%;
  right: 0%;
  background: #2c3e50;
  -webkit-box-shadow: 4px 3px 0px 0px rgba(52, 73, 94,0.75);
  -moz-box-shadow:    4px 3px 0px 0px rgba(52, 73, 94,0.75);
  box-shadow:         4px 3px 0px 0px rgba(52, 73, 94,0.75);
}

#toolbar ul {
  color: #fff;
  padding: 0.6em;
  margin: 0;
  text-align: right;
}

#toolbar ul li {
  list-style: none;
  display: inline;
  margin: 0 1em 0 0;
}

#toolbar ul li a {
  font-style: normal;
  text-decoration: none;
  color: #fff;
}

#toolbar ul li a:hover {
  text-decoration: underline;
}

#toolbar span {
  margin: 0 0.3em 0 0;
}

#map {
	width: 100%;
	height: 100%;

}

.custom-popup .leaflet-popup-content-wrapper {
  background:#95a5a6;
  color:#fff;
  font-size:1em;
  line-height:24px;
  font-weight: normal;
  text-decoration: none;
  font-style: normal;
}

.custom-popup .leaflet-popup-content-wrapper a {
  color:rgba(255,255,255,0.5);
}

.custom-popup .leaflet-popup-tip-container {
  width:30px;
  height:15px;
}

.custom-popup .leaflet-popup-tip {
  border-left:15px solid transparent;
  border-right:15px solid transparent;
  border-top:15px solid #95a5a6;
}

.info {
  position: absolute;
  top: 10%;
  left: 1%;
}

.graph {
  width:100px;
  height: 100px;
  margin-top: 2em;
  overflow: hidden;
  background: transparent;
  box-shadow: none;
  float:left;
}

.info .graph img {
  width: 300px;
  position: absolute;
  display: block;
  clip: rect(0px,100px,100px,0px);
}

.info div {
  background:#95a5a6;
  padding: 1em;
  border-radius: 0.8m;
  color: #fff;
  box-shadow: 0.1em 0.1em 0 #95a5a6;
}




</style>
</head>

<body>

<?php

//Connect to MySQL

$connect = mysql_connect("localhost","root","your_password");

$mapa = "SELECT * FROM plantMatrix.coordsTest WHERE plantMatrix.coordsTest.LatitudeDec != 'NA' && LongitudeDec !='NA' && SpeciesAccepted !='NA' GROUP BY SpeciesAccepted";

$dbquery = mysql_query($mapa,$connect);

//Creating GeoJSON array, ready to store values in GeoJSON format 
//GeoJSON format reference - http://geojson.org/
$geojson = array( 'type' => 'FeatureCollection', 'features' => array());


  while($row = mysql_fetch_assoc($dbquery)){

    $marker = array(
      'type' => 'Feature',
      'properties' => array(
        'title' => '<em>'.$row['SpeciesAccepted'].'</em><br>'.$row['Population'],
          'database' => array(
          'title' => $row['SpeciesAccepted'],
          'speciesauthor' => $row['SpeciesAuthor'],
          'population' => $row['Population'],
          'journal' => $row['Journal'],
          'isbn' => $row['DOIISBN'],
          'growthtype' => $row['GrowthType'],
          'growthform' => $row['GrowthFormRaunkiaer'],
          'numberpopulations' => $row['NumberPopulations'],
          'kingdom' => $row['Kingdom'],
          'phylum' => $row['Phylum'],
          'angiogymno' => $row['AngioGymno'],
          'dicotmonoc' => $row['DicotMonoc'],
          'class' => $row['Class'],
          'order' => $row['_Order'],
          'family' => $row['Family'],
          'genus' => $row['Genus'],
          'studiedsex' => $row['StudiedSex'],
          'matrixcomposite' => $row['MatrixComposite'],
          'matrixtreatment' => $row['MatrixTreatment'],
          'latitudedec' => $row['LatitudeDec'],
          'longitudedec' => $row['LongitudeDec'],
          'altitude' => $row['Altitude'],
          'country' => $row['Country'],
          'continent' => $row['Continent'],
          'matrixsplit' => $row['MatrixSplit'],
          'matrixnumber' => $row['Matrixnumber'],
          'dimension' => $row['Dimension'],
          'planttype' => $row['plantType'],
          'matrix' => $row['matrix'],
          'classnames' => "–Nodes',–Small plants',–Large plants'",
          'statusstudy' => $row['StatusStudy'],
          'statuselsewhere' => $row['StatusElsewhere']
          
        ),
        'marker-color' => '#e74c3c',
        'marker-size' => 'small',
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


<div class="custom-popup" id="map"></div>

<div id="toolbar">
<ul>
  <li><span class="icon-leaf"></span><strong>PlantMatrix</strong></li>
  <li><span class="icon-users"></span><a href="http://144.173.72.162:8080/share">Sign In</li>
</ul>
</div>

<div class="info" id="info"></div>


<script>

var 
    click = document.getElementById('click'),
    mousemove = document.getElementById('mousemove');

//Get GeoJSON from PHP, store as js var
var geoJson = <?php echo json_encode($geojson,JSON_NUMERIC_CHECK); ?>;
console.log(geoJson);

L.mapbox.accessToken = 'pk.eyJ1IjoiZnJhbmNlc2Nhc2FyZ2VudCIsImEiOiJvZmFuUzM0In0.-gsScOsPRxKs9E8qNy3qwg';

var map = L.mapbox.map('map', 'francescasargent.ja3p4m1n', {
  tileLayer: {
    continuousWorld: false,
    noWrap: true
  }
})
    .setView([28.67, -4.66], 4).featureLayer.setGeoJSON(geoJson);


map.eachLayer(function(layer) {
  map.on('mouseover', function(e, layer) {
    e.layer.openPopup();

  });

  map.on('mouseout', function(e, layer) {
	if (!isClicked) {
	
	} else {
		e.layer.closePopup();
	}
    
  });
});

// Listen for individual marker clicks.
map.on('click',function(e) {
	isClicked = $(this).data('clicked');
    //e.layer.closePopup();

	e.layer.openPopup();

    var feature = e.layer.feature;
    var ob = feature.properties.database;

    

    //print array in console.log for reference
    for (var key in ob) {
      if (ob.hasOwnProperty(key)) {
        var object = key + " -> " + ob[key].toString();
        console.log(object);
      }
    }

    var content = '<div>' + '<strong>' + 'Species Name: </strong>' + ob.title + '<br>'
                          + '<strong>' + 'Population: </strong>' + ob.population + '<br>'  
                          + '<sub>' + ob.journal + ob.isbn + '</sub><br>'  
                          + '<strong>' + 'Growth Type: </strong>' + ob.growthtype + '<br>' 
                          + '<strong>' + 'Plant Type: </strong>' + ob.planttype + '<br>' 
                          + '<strong>' + 'Continent: </strong>' + ob.continent + '<br>'
                          + '<strong>' + 'Matrix Composite: </strong>' + ob.matrixcomposite + '<br>' 
                          + '<strong>' + 'Continent: </strong>' + ob.continent + '<br>' 
                          + '<div class="graph"><a href= "graph/'+ ob.matrixnumber +'_' + ob.speciesauthor + '_dot.png" target="_blank"><img src="graph/'+ ob.matrixnumber +'_' + ob.speciesauthor +'_dot.png"></a></div>'


    +'</div>';
    info.innerHTML = content;

});


// Clear the tooltip when map is clicked.
map.on('move', empty);

// Trigger empty contents when the script
// has loaded on the page.
empty();

function empty() {
  info.innerHTML = '';
	
  }



map.on('dblclick'), function(e) {
	map.setView(e.latlng, map.getZoom() + 2).panTo(e.latlng);
	map.panTo(e.latlng);
}




</script>


</body>
</html>
