# -*- coding: utf-8 -*-
import json
import requests

osrm_ip = "0.0.0.0"
osrm_port = "5000"

def travel_time(first_lat, first_lon, second_lat, second_lon):

  # OSRM viaroute request
  r = requests.get("http://" + osrm_ip + ":" + osrm_port
                   + "/viaroute?loc=" + str(first_lat) + ',' + str(first_lon)
                   + "&loc=" + str(second_lat) + ',' + str(second_lon))

  route = r.json()

  total_time = "inf"
  if route["status"] == 0:
    total_time = route["route_summary"]["total_time"]

  # Travel time in minutes, rounded to lowest integer
  return total_time / 60

