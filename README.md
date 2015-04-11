# A quick, fast and dirty python script to generate rough isochrone lines using [OSRM](http://www.project-osrm.org)

## Map example

![alt text](./img/example.gif "Map picture example.")

The map used to produce this image can be found [here on
umap](umap.openstreetmap.fr/m/35416/).

## Description

For a given place _p_ and duration _d_, we want to generate a line
linking points that are at a travel time _d_ from _p_ using the road
network.

- Put it simple: kind of like drawing "circles" on a map
with travel time on roads replacing usual euclidean distance.

- Put it formally: we seek the convex envelope of the set _S_ of
  points _q_ such that d(_p_, _q_) <= _d_.

### Quick?

The script was written in a few hours' time to produce a rough result
on a bunch of cities so don't expect too much refinements here.

### Fast?

Starting from _p_, we just look around in different directions. For
each of them, we find a spot at distance _d_ from _p_. This search is
performed dichotomically with several OSRM requests so it's quite
fast. Examples show in addition that it's not necessary to explore
loads of directions to get a rough picture.

### Dirty?

We just use a bunch of points around _p_ on the map, whose relevance
is determined by OSRM requests. The real thing would be to get into
the graph structure of the road network and perform some kind of deep
search.

## Usage

The script handles list of durations and locations to generate a
geojson file for each isochrone line. You need an up and running OSRM
server at hand to handle the requests.

For example, to compute isochrone line at 20 and 40 minutes for Paris
and Lyon, use:

```bash
python isochrone_line.py --duration 20 40 --loc 48.8565056,2.3521334 45.7575926,4.8323239
```

## Limitations

* Using a few points around just gives an outline of the convex
  enveloppe of the above mentioned set _S_. But using more points
  doesn't necessarily provide more precision as it tends to emphasize
  local discontinuities. So in all cases, the obtained lines remains
  rough approximations.

* Moreover the set _S_ of points _q_ such that d(_p_, _q_) <= _d_ is
  arc-connected but has no reason to be convex so looking for a single
  point in each direction is quite an approximation: for a given
  direction, there is actually no guarantee concerning the uniqueness
  of a point _q_ such that d(_p_, _q_) = d.