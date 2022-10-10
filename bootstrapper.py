import os

from core.gribreader import GribReader


class Bootstrapper(object):
    """Command line operator"""

    def grid(self, path: str, out: str = ""):
        grib_reader = GribReader()

        grid = grib_reader.get_grib_grid(path)

        result = f"GRID output for         {path}\n"
        result += f"First point (lat/lon): {grid.first_grid_point.lat} {grid.first_grid_point.lon}\n"
        result += f"Last point (lat/lon):  {grid.last_grid_point.lat} {grid.last_grid_point.lon}\n"
        result += f"Lat step:              {grid.lat_step}\n"
        result += f"Lon step:              {grid.lon_step}\n"
        result += f"Lat count:             {grid.lat_count}\n"
        result += f"Lon count:             {grid.lon_count}\n\n"
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

    def message(self, path: str, out: str = ""):
        grib_reader = GribReader()

        messages = grib_reader.get_grib_messages(path)

        if len(messages) == 0:
            return

        result = f"MESSAGES output for {path}\n"
        result += f"Reftime: {messages[0].reftime} | Predict: {messages[0].predict}\n\n"

        for msg in messages:
            result += f"Center:          {msg.center}\n"
            result += f"Code:            {msg.code}\n"
            result += f"Pname:           {msg.pname}\n"
            result += f"Sname:           {msg.sname}\n"
            result += f"Unit:            {msg.unit}\n"
            result += f"Level type:      {msg.level_type}\n"
            result += f"Level:           {msg.level}\n"
            result += f"Ensemble member: {msg.ensemble_member}\n\n"

        print(result)

        if len(out) == 0:
            return

        print(f"File result {out} saved")
        with open(out, 'w') as f:
            f.write(result)

    def messages(self, path: str, out: str = ""):
        grib_reader = GribReader()

        result_dicts = []

        for file in os.listdir(path):
            messages = grib_reader.get_grib_messages(f"{path}/{file}")

            result_dict = None

            for rd in result_dicts:
                if rd["reftime"] == messages[0].reftime:
                    result_dict = rd
                    break

            if result_dict is None:
                result_dict = {"reftime": messages[0].reftime, "predicts": [], "params": [], "levels": []}
                result_dicts.append(result_dict)

            for msg in messages:

                if len(messages) == 0:
                    continue

                param = None
                for param_dict in result_dict["params"]:
                    if param_dict["sname"] == msg.sname \
                            and param_dict["level_type"] == msg.level_type \
                            and param_dict["level"] == msg.level:
                        param = param_dict
                        break

                if param is None:
                    param = {"sname": msg.sname, "pname": msg.pname, "level_type": msg.level_type, "level": msg.level,
                             "code": msg.code}

                    result_dict["params"].append(param)

                if msg.predict not in result_dict["predicts"]:
                    result_dict["predicts"].append(msg.predict)

        if len(result_dicts) == 0:
            return

        result = f"GRIB FILES output for {path}\n\n"

        for rd in result_dicts:
            reftime = rd["reftime"]
            params = rd["params"]
            predicts = rd["predicts"]

            result += f"Reftime:  {reftime}\n"
            result += f"Predicts: {predicts}\n"
            result += f"Params:\n"

            for param in params:
                result += f"{param['pname']:60} {param['sname']:10} {param['code']:7} {param['level_type']:30} {param['level']:7}\n"

            result += "\n"

        print(result)

        if len(out) == 0:
            return

        print(f"File result {out} saved")
        with open(out, 'w') as f:
            f.write(result)
