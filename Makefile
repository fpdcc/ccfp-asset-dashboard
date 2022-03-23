districts: asset_dashboard/fixtures/boundaries/state_senate.geojson asset_dashboard/fixtures/boundaries/state_house.geojson asset_dashboard/fixtures/boundaries/state_commissioner.geojson asset_dashboard/fixtures/boundaries/zones.geojson
	for file in $^; do\
		python manage.py import_boundaries $${file};\
	done

asset_dashboard/fixtures/zones.geojson:
	python manage.py create_zone_geojson > $@

asset_dashboard/fixtures/state_commissioner.geojson:
	curl -o $@ 'https://opendata.arcgis.com/api/v3/datasets/b3acc7df1a484c10b46072e2dc009894_1/downloads/data?format=geojson&spatialRefId=4326'

asset_dashboard/fixtures/state_house.geojson:
	curl -o $@ 'https://opendata.arcgis.com/api/v3/datasets/dc242b0364e640a795c21cd8eaaca63f_11/downloads/data?format=geojson&spatialRefId=4326'

asset_dashboard/fixtures/state_senate.geojson:
	curl -o $@ 'https://opendata.arcgis.com/api/v3/datasets/830b42882b2c4d95b7255ecd4c425ffa_12/downloads/data?format=geojson&spatialRefId=4326'
