# GRIB info tools

This project is designed to quickly obtain information about GRIB data.

For example, you can read the description of the grid and the order of coordinates. 
Or extract the data of some parameter

In addition to examining a single file, you can pass the path to a set 
of files to the input to find out what parameters, dates, levels, etc. are in the set.

## Get grid information

```shell
python main.py <grib file> <out file>
```
* **grid** - command for get grid information.
* **grib file** - file in GRIB format. Your can set only one file, no folder path.
* **out file** - this parameter is optional. If you do not specify it, the output will be made only to the console.

Example:

```shell
python main.py grid example.grib grid.txt
```

Output:

Output shortened.

```text
GRID output for example.grib
First point (lat/lon): 90.0 0.0
Last point (lat/lon): -90.0 359.75
Lat step: 0.25
Lon step: 0.25
Lat count: 721
Lon count: 1440

Coords:
90.0 0.0
90.0 0.25
90.0 0.5
90.0 0.75
....
```

## Restriction

The current version of the utility only works with a regular grid.
In the future, support for non-regular grids such as gaussian grids will be added.