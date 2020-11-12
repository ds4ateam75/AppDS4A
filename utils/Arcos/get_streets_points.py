import pandas as pd
import json

"""
This code takes a geojson with streets and transforms the streets
in points that can be ploted by dash more easily
"""


def get_streets():

    """
    This function returns a dataframe with the streets coordinates.
    """

    """import geojson with the streets"""
    with open('arcos.json') as f:
        geojson = json.load(f)

    """Initialize arrays to store values"""
    points = []
    ids = []

    """Loop over each features"""
    for feature in geojson['features']:

        """Save the coordinates depends on the geometry type"""
        if feature['geometry']['type'] == 'Polygon':
            ids.extend([str(feature["properties"]["ID"]) for x in feature['geometry']['coordinates'][0]])
            points.extend(feature['geometry']['coordinates'][0])
            ids.append(str(feature["properties"]["ID"]))
            points.append([None, None])  # mark the end of a polygon

        elif feature['geometry']['type'] == 'MultiPolygon':
            for polyg in feature['geometry']['coordinates']:
                ids.extend([str(feature["properties"]["ID"]) for x in polyg[0]])
                points.extend(polyg[0])
                ids.append(str(feature["properties"]["ID"]))
                points.append([None, None])  # end of polygon

        elif feature['geometry']['type'] == 'LineString':
            ids.extend([str(feature["properties"]["ID"]) for x in feature['geometry']['coordinates']])
            points.extend(feature['geometry']['coordinates'])
            ids.append(str(feature["properties"]["ID"]))
            points.append([None, None])  # end of Linestring

        elif feature['geometry']['type'] == 'MultiLineString':
            for line in feature['geometry']['coordinates']:
                line_points = get_point(line)
                ids.extend([str(feature["properties"]["ID"]) for x in line_points])
                ids.append(str(feature["properties"]["ID"]))
                points.extend(line_points)
                points.append([None, None])  # end of MultilineString
        else:
            pass
    lons, lats = zip(*points)

    data = {
        "Arco": ids,
        "Latitud": lats,
        "Longitud": lons
    }
    df = pd.DataFrame(data)
    return df


def intermediates(p1, p2):
    """"
    Return a list of nb_points equally spaced points
    between p1 and p2

    Parameters
    ----------
    p1 : array
        latitude and logituded of the first point.
    p2 : array
        latitude and logituded of the second point.
    """

    nb_points = 1
    x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
    y_spacing = (p2[1] - p1[1]) / (nb_points + 1)

    points = [[p1[0]+i*x_spacing, p1[1]+i*y_spacing] for i in range(1, nb_points+1)]
    points.insert(0, p1)
    points.insert(0, p2)

    return points


def get_point(coordinates):
    """"
    Iterate through all the point in the geometry coordinates section of each
    feature ang get more points

    Parameters
    ----------
    coordinates : array
        has the coordinates of a point
    """
    streets = []
    for point in range(1, len(coordinates)):
        streets.extend(intermediates(coordinates[point-1], coordinates[point]))
    return streets


df_streets = get_streets()
df_streets.to_csv("arcos.csv")
