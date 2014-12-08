from flask import render_template, abort, jsonify
from . import main
from ..models import User, Plant, Species


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/map')
def map():
	species = Species.query.all()
	plants = Plant.query.all()
	return render_template('map.html', plants=plants, species=species)

@main.route('/map/<param>/<filters>')
def mapfilter(param, filters):
	species = Species.query.all()
	plants = Plant.query.all()
	return render_template('mapfilter.html', plants=plants, species=species, param=param, filters=filters)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/geojson/all')
def geojson():

	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}



	plants = Plant.query.all()

	for plant in plants:
		longi = plant.longitudedec
		lati = plant.latitudedec

		if longi == 'NA':
			pass

		elif lati == 'NA':
			pass

		else:

			fe = {
					'type' : 'Feature',
					'geometry' : {
						'type' : 'Point',
						'coordinates' : [plant.longitudedec, plant.latitudedec]
					},
					'properties' : {
						'title' : '<em>'+plant.name+'</em>',
						'name' : plant.name,
						'matrixnumber' : plant.matrixnumber,
						'matrix' : plant.matrix,
						'dimension' : plant.dimension,
						'matrixclassnumber' : plant.matrixclassnumber,
						'matrixclassorganised' : plant.matrixclassorganised,
						'matrixsplit' : plant.matrixsplit,
						'classnames' : plant.classnames,
						'observation' : plant.observation,
						'matrixcomposite' : plant.matrixcomposite,
						'matrixtreatment' : plant.matrixtreatment,
						'matrixcaptivity' : plant.matrixcaptivity,
						'matrixstartyear' : plant.matrixstartyear,
						'matrixstartseason' : plant.matrixstartseason,
						'matrixstartmonth' : plant.matrixstartmonth,
						'matrixendyear' : plant.matrixendyear,
						'matrixendseason' : plant.matrixendseason,
						'matrixendmonth' : plant.matrixendmonth,
						'studiedsex' : plant.studiedsex,
						'population' : plant.population,
						'latdeg' : plant.latdeg,
						'latmin' : plant.latmin,
						'latsec' : plant.latsec,
						'londeg' : plant.londeg,
						'lonmin' : plant.lonmin,
						'lonsec' : plant.lonsec,
						'altitude' : plant.altitude,
						'country' : plant.country,
						'continent' : plant.continent,
						'criteriasize' : plant.criteriasize,
						'criteriaontogeny' : plant.criteriaontogeny,
						'authors' : plant.authors,
						'journal': plant.journal,
						'yearpublication' : plant.yearpublication,
						'doiisbn' : plant.doiisbn,
						'enteredby' : plant.enteredby,
						'entereddate' : plant.entereddate,
						'source' : plant.source,
						'statusstudy' : plant.statusstudy,
						'statusstudyref' : plant.statusstudyref,
						'statuselsewhere' : plant.statuselsewhere,
						'statuselsewhereref' : plant.statuselsewhereref,
						'marker-color' : '#e74c3c',
						'marker-size' : 'small',
						}
					
				}


			geojson["features"].append(fe)

	


	return jsonify(geojson)

@main.route('/geojson/<param>/<filters>')
def geojsonfilter(param, filters):

	kwargs = {
		param : filters
	}

	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}


	plants = Plant.query.filter_by(**kwargs)

	for plant in plants:
		longi = plant.longitudedec
		lati = plant.latitudedec

		if longi == 'NA':
			pass

		elif lati == 'NA':
			pass

		else:
			fe = {
					'type' : 'Feature',
					'geometry' : {
						'type' : 'Point',
						'coordinates' : [plant.longitudedec, plant.latitudedec]
					},
					'properties' : {
						'title' : '<em>'+plant.name+'</em>',
						'name' : plant.name,
						'matrixnumber' : plant.matrixnumber,
						'matrix' : plant.matrix,
						'dimension' : plant.dimension,
						'matrixclassnumber' : plant.matrixclassnumber,
						'matrixclassorganised' : plant.matrixclassorganised,
						'matrixsplit' : plant.matrixsplit,
						'classnames' : plant.classnames,
						'observation' : plant.observation,
						'matrixcomposite' : plant.matrixcomposite,
						'matrixtreatment' : plant.matrixtreatment,
						'matrixcaptivity' : plant.matrixcaptivity,
						'matrixstartyear' : plant.matrixstartyear,
						'matrixstartseason' : plant.matrixstartseason,
						'matrixstartmonth' : plant.matrixstartmonth,
						'matrixendyear' : plant.matrixendyear,
						'matrixendseason' : plant.matrixendseason,
						'matrixendmonth' : plant.matrixendmonth,
						'studiedsex' : plant.studiedsex,
						'population' : plant.population,
						'latdeg' : plant.latdeg,
						'latmin' : plant.latmin,
						'latsec' : plant.latsec,
						'londeg' : plant.londeg,
						'lonmin' : plant.lonmin,
						'lonsec' : plant.lonsec,
						'altitude' : plant.altitude,
						'country' : plant.country,
						'continent' : plant.continent,
						'criteriasize' : plant.criteriasize,
						'criteriaontogeny' : plant.criteriaontogeny,
						'authors' : plant.authors,
						'journal': plant.journal,
						'yearpublication' : plant.yearpublication,
						'doiisbn' : plant.doiisbn,
						'enteredby' : plant.enteredby,
						'entereddate' : plant.entereddate,
						'source' : plant.source,
						'statusstudy' : plant.statusstudy,
						'statusstudyref' : plant.statusstudyref,
						'statuselsewhere' : plant.statuselsewhere,
						'statuselsewhereref' : plant.statuselsewhereref,
						'marker-color' : '#e74c3c',
						'marker-size' : 'small',
						}
					
				}


			geojson["features"].append(fe)

	return jsonify(geojson)

@main.route('/speciesjson/<name>')
def speciesjson(name):


	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}

	kwargs = {
	'name' : name
	}

	species = Species.query.filter_by(**kwargs)

	for sp in species:

		if sp.name == 'NA':
			fe = {
			'name' : 'Not Enough Data'
			}
			

		else:
			fe = {
					'name' : sp.name,
					'speciesauthor' : sp.speciesauthor,
					'kingdom' : sp.kingdom,
					'phylum' : sp.phylum,
					'angiogymno' : sp.angiogymno,
					'dicotmonoc' : sp.dicotmonoc,
					'class' : sp._class,
					'order' : sp._order,
					'family': sp.family,
					'genus' : sp.genus,
					'ecoregion' : sp.ecoregion,
					'growthtype' : sp.growthtype,
					'growthformraunkiaer' : sp.growthformraunkiaer,
					'annualperiodicity' : sp.annualperiodicity,
					'planttype' : sp.planttype,
					'commonname' : sp.commonname,
					'originalimageurl' : sp.originalimageurl
						}
					
				


			geojson['features'].append(fe)

	return jsonify(geojson)
