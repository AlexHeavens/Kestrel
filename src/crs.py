from pyproj import CRS, Transformer

british_national_grid = CRS.from_epsg(27700)
world_geodetic_system = CRS.from_epsg(4326)

bng_to_wgs = Transformer.from_crs(crs_from=british_national_grid, crs_to=world_geodetic_system)
