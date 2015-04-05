# -*- coding: utf-8 -*-
import math, json
from osrm_request import travel_time, nearest_point

def midpoint(x1, y1, x2, y2):
  return (x1 + x2)/2, (y1 + y2)/2

def limit_in_single_direction(lat, lon, minutes, angle):
  cs = math.cos(angle)
  sn = math.sin(angle)

  # Setting initial "rough" frame
  i = 0.01
  current_lat = lat + cs * i
  current_lon = lon + sn * i

  while travel_time(lat, lon, current_lat, current_lon) < minutes:
    min_lat = current_lat
    min_lon = current_lon
    i += 1
    current_lat = min_lat + cs * i
    current_lon = min_lon + sn * i

  max_lat, max_lon = current_lat, current_lon

  # Starting dichotomic search
  lower_time = travel_time(lat, lon, min_lat, min_lon)
  upper_time = travel_time(lat, lon, max_lat, max_lon)

  while lower_time < upper_time:

    middle_lat, middle_lon = midpoint(min_lat, min_lon, max_lat, max_lon)
    middle_time = travel_time(lat, lon, middle_lat, middle_lon)

    # Avoid infinite loop when lower_time never reaches upper_time
    if lower_time == middle_time or middle_time == upper_time:
      break

    # Update frame
    if middle_time < minutes:
      min_lat = middle_lat
      min_lon = middle_lon
      lower_time = middle_time
    else:
      max_lat = middle_lat
      max_lon = middle_lon
      upper_time = middle_time

  return nearest_point(min_lat, min_lon)

def get_lines(durations, init_lats, init_lons, step_number):
  for i in range(len(init_lats)):
    init_lat = init_lats[i]
    init_lon = init_lons[i]
    # print init_lat, init_lon

    for duration in durations:
      # print duration
      lats = []
      lons = []

      for step in range(step_number):
        angle = 2 * step * math.pi / step_number
        try:
          current_lat, current_lon = limit_in_single_direction(init_lat,
                                                               init_lon,
                                                               duration,
                                                               angle)
        except Exception as e:
          # Ignoring cases where the dichotomic search encounters an unfound
          # route
          continue
        lats.append(current_lat)
        lons.append(current_lon)


        geojson_output = {"type": "FeatureCollection",
                          "features": [
                            {
                              "type": "Feature",
                              "geometry": {
                                "type": "Point",
                                "coordinates": [
                                  init_lon,
                                  init_lat
                                ]
                              },
                              "properties": {}
                            },
                            {
                              "type": "Feature",
                              "geometry": {
                                "type": "Polygon",
                                "coordinates": [
                                  [
                                  ]
                                ]
                              },
                              "properties": {
                                "name": "Isochrone map",
                                "desc": str(duration) + " minutes from "
                                + str(init_lat) + "," + str(init_lon)
                              }
                            }
                          ]
                        }

        point_number = len(lats)

        for i in range(point_number + 1):
          geojson_output["features"][1]["geometry"]["coordinates"][0].append(
            [lons[i % point_number], lats[i % point_number]])

      with open('output_' + str(init_lat) + '_' + str(init_lon)
                + '_' + str(duration) + '.geojson', 'w') as f:
        json.dump(geojson_output, f, indent = 2)

if __name__ == "__main__":
  get_lines([30, 60], [48.85, 45.7529], [2.35, 4.9830], 25)
