from core.gribreader import GribReader


class Bootstrapper(object):
    """Command line operator"""

    def grid(self, path: str, out: str = ""):
        grib_reader = GribReader()

        grid = grib_reader.get_grib_grid(path)

        result = f"GRID output for {path}\n"
        result += f"First point (lat/lon): {grid.first_grid_point.lat} {grid.first_grid_point.lon}\n"
        result += f"Last point (lat/lon): {grid.last_grid_point.lat} {grid.last_grid_point.lon}\n"
        result += f"Lat step: {grid.lat_step}\n"
        result += f"Lon step: {grid.lon_step}\n"
        result += f"Lat count: {grid.lat_count}\n"
        result += f"Lon count: {grid.lon_count}\n\n"
        result += "Coords:\n"

        points = ""
        for coord in grid.coords[:10]:
            points += f"{coord.lat} {coord.lon} "
        points += "... more only file"

        print(result + points)

        if len(out) == 0:
            return

        points = ""
        for coord in grid.coords:
            points += f"{coord.lat} {coord.lon}\n"

        print(f"File result {out} saved")
        with open(out, 'w') as f:
            f.write(result + points)

    def message(self, path: str):
        pass

    def messages(self, path: str):
        pass
