# -*- coding: utf-8 -*-
from osrm_request import travel_time
import math

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

  return min_lat, min_lon

lats = []
lons = []

step_number = 30
for step in range(step_number):
  angle = 2 * step * math.pi / step_number
  try:
    current_lat, current_lon = limit_in_single_direction(48.85, 2.35, 60, angle)
  except Exception as e:
    # Ignoring cases where the dichotomic search encounters an unfound
    # route
    continue
  lats.append(current_lat)
  lons.append(current_lon)

print lats, lons

