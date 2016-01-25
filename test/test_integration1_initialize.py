# coding=utf-8
"""
########## Functionality integration tests #############
This module contains tests that doesn't provide clean up.
After run this file, the test tables are populated, and to run
other tests must be manually truncated.
Consistency of data stored can be tested by entering queries from
psql or using the method below. It is useful to understand how the
popping-over algorithm works.

#todo: add also some automatic checks for the inserted data
"""
from datetime import datetime
__author__ = 'Lorenzo'

from test.utils_for_tests import rand_coordinates, rand_data
from src.xco2 import Xco2
from src.dbproxy import dbProxy


TESTLENGTH = 1000  # set a number of iteration

# test functionality
TEST1 = (100, True)    # short test - random points from small portion of surface (1 square)
# test solidity (even increasing the number of points the number of area remains still)
TEST2 = (1000, True)  # long test - random points from small portion of surface (1 square)
# test scope (many points are created and many areas. Total plane should be around 33600 squares)
TEST3 = (10000, False) # long test - random points from all the cartesian plane


def test_should_store_new_points_and_areas(rng, square):
    """Test insertion of a area alongside with a xco2 data"""
    print('TEST1: INSERTION PROCEDURE\n')
    for _ in range(rng):
        # use squared params to limit to a limited portion
        longitude, latitude = rand_coordinates(squared=square)
        xco2 = Xco2(
            xco2=rand_data(),
            longitude=longitude,
            latitude=latitude,
            timestamp=datetime(1970, 1, 1)
        )
        xco2.store_xco2()
    print('Done\n')
    print(
        '###########'
        '# RESULTS\n\n'
        '# Try the following queries on the database:\n'
        '#####\n'
        'SELECT t_co2.id, ST_X(geometry) as long, ST_Y(geometry) as lat, t_areas.data as geojson FROM t_co2, t_areas WHERE ST_Contains(t_areas.aoi, t_co2.geometry) LIMIT 1;\n'
        'SELECT ST_AsText(t_co2.geometry), t_areas.data FROM t_co2, t_areas WHERE ST_Contains(t_areas.aoi, t_co2.geometry);\n'
        '# each area contains the GeoJSON in the \'data\' field\n'
        'SELECT id, center from t_areas;\n'
        '# compare the number of insertions with the number of areas (should be around 10%)\n'
        'SELECT count(*) from t_co2;\n'
        'SELECT count(*) from t_areas;)\n'
        '# print xco2 data with relative area\'s center\n'
        'SELECT t_co2.id, ST_X(t_co2.geometry) as long, ST_Y(t_co2.geometry) as lat, ST_AsText(t_areas.center) as area_center FROM t_co2, t_areas WHERE ST_Contains(t_areas.aoi, t_co2.geometry);'
        '###########'
    )


def test_should_load_data_and_return_result_proxy():
    query = Xco2.__table__.select().limit(5)
    proxy = dbProxy.alchemy.execute(query)
    one = proxy.fetchall()
    if one:
        for o in one:
            print(o.id)
    else:
        print('Database is void')


def test_should_update_an_exisiting_area():
    from src.areasops import areasOps
    from src.spatial import spatial
    geometry = spatial.shape_geometry(rand_coordinates()[0], rand_coordinates()[1])
    square = spatial.shape_aoi(geometry)
    areasOps.store_area(geometry)


def test_should_find_all_xco2_points_in_aoi():
    pass


def test_should_get_aoi_that_contains_():
    pass


if __name__ == '__main__':

    """Choose a test from above"""
    rng, square = TEST1
    try:
        test_should_store_new_points_and_areas(rng, square)
        test_should_load_data_and_return_result_proxy()
    except KeyboardInterrupt as e:
        raise e
