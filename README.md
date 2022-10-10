# GRIB info tools

This project is designed to quickly obtain information about GRIB data.

For example, you can read the description of the grid and the order of coordinates. 
Or extract the data of some parameter

In addition to examining a single file, you can pass the path to a set 
of files to the input to find out what parameters, dates, levels, etc. are in the set.

## Grid command

Get grid information

```shell
python main.py grid <in> <out>
```
* **grid** - command for get grid information.
* **in** - file in GRIB format. Your can set only one file, no folder path.
* **out** - this parameter is optional. If you do not specify it, the output will be made only to the console.

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

## Message command

Information about one GRIB file 

```shell
python main.py message <in> <out>
```
* **grid** - command for get information about GRIB file.
* **int** - file in GRIB format. Your can set only one file, no folder path.
* **out** - this parameter is optional. If you do not specify it, the output will be made only to the console.

Example:

```shell
python main.py message example.grib grid.txt
```

Output:

Output shortened.

```text
MESSAGES output for example.grib
Reftime: 2022-03-21 00:00:00+00:00 | Predict: 180

Center:          kwbc
Code:            260074
Pname:           Pressure reduced to MSL
Sname:           prmsl
....
```

## Messages command

Information about many GRIB files. Base time, offset times, parameters, levels.

```shell
python main.py messages <in> <out>
```
* **messages** - command for many GRIB files.
* **in** - path of directory with GRIB files.
* **out** - this parameter is optional. If you do not specify it, the output will be made only to the console.

Example:

```shell
python main.py messages mydir/gribs grid.txt
```

Output:

Output shortened.

```text
GRIB FILES output for mydir/gribs

Reftime:  2022-03-21 00:00:00+00:00
Predicts: [180, 1320]
Params:
Pressure reduced to MSL                                      prmsl          260074 meanSea                                 0
Cloud mixing ratio                                           clwmr          260019 hybrid                                  1
Ice water mixing ratio                                       icmr           260020 hybrid                                  1
Rain mixing ratio                                            rwmr           260021 hybrid                                  1
```

## Restriction

The current version of the utility only works with a regular grid.
In the future, support for non-regular grids such as gaussian grids will be added.