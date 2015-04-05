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

  if route["status"] != 0:
    raise Exception("Unfound route")

  # Travel time in minutes, rounded to lowest integer
  return route["route_summary"]["total_time"] / 60

def nearest_point(lat, lon):

  # OSRM nearest request
  r = requests.get("http://" + osrm_ip + ":" + osrm_port
                   + "/nearest?loc=" + str(lat) + ',' + str(lon))

  point = r.json()

  ret_lat = lat
  ret_lon = lon
  if point["status"] == 0:
    ret_lat = point["mapped_coordinate"][0]
    ret_lon = point["mapped_coordinate"][1]

  return ret_lat, ret_lon
                   
                   

