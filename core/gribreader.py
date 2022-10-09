import logging
from datetime import datetime, timezone

import eccodes as e

import common.grib


class GribReader:
    """GRIB files reader"""

    def __init__(self):
        self.log = logging.getLogger("gribinfo")

    def find_grib_messages(self, fpath: str, iks: list[str], params: list[list[str]]) -> list[common.grib.GribMessage]:
        """Reading and find data by index from GRIB file"""

        if len(iks) != len(params):
            raise Exception("FIND GRIB MESSAGES:: length iks != params length")

        messages = []
        try:
            fin = open(fpath, 'rb')
            try:
                iid = e.codes_index_new_from_file(fpath, iks)

                try:
                    for param_items in params:
                        for iidx in range(0, len(param_items)):
                            e.codes_index_select(iid, iks[iidx], param_items[iidx])

                        while 1:
                            msid = e.codes_new_from_index(iid)
                            try:
                                if msid is None:
                                    break

                                self.log.debug(f"FIND GRIB MESSAGES:: init msid {msid}")

                                sn = e.codes_get(msid, "shortName")

                                date = e.codes_get(msid, 'date')
                                time = e.codes_get(msid, 'time')
                                predict = e.codes_get(msid, 'step') * 60

                                reftime = datetime(date // 10000, date % 10000 // 100, date % 100, time // 100, 0, 0, 0,
                                                   tzinfo=timezone.utc)

                                center = e.codes_get(msid, "centre")
                                lt = e.codes_get(msid, "typeOfLevel")
                                lvl = e.codes_get(msid, "level")
                                pn = e.codes_get(msid, "name")
                                code = e.codes_get(msid, "paramId")
                                unit = e.codes_get(msid, "units")
                                values = e.codes_get_double_array(msid, "values")

                                if center == 'kwbc':
                                    step_type_internal = e.codes_get_string(msid, 'stepTypeInternal')

                                    if step_type_internal == 'accum':

                                        start = e.codes_get(msid, "startStep")
                                        if start != 0:
                                            continue

                                if center == 'kwbc':
                                    ext = e.codes_is_defined(msid, 'scaledValueOfFirstFixedSurface')

                                    if ext == 1:
                                        lvl = e.codes_get(msid, 'scaledValueOfFirstFixedSurface')

                                    code = code + lvl

                                if center == 'kwbc':
                                    exists = False

                                    for msg in messages:
                                        if msg.sname == sn and msg.level_type == lt and msg.level == lvl:
                                            exists = True
                                            break

                                    if exists is True:
                                        continue

                                messages.append(
                                    common.grib.GribMessage(lt, lvl, pn, sn, code, unit, center, reftime, predict, 0,
                                                            values))

                            finally:
                                if msid is not None:
                                    e.codes_release(msid)
                                    self.log.debug(f"FIND GRIB MESSAGES:: release msid {msid}")

                except e.CodesInternalError:
                    self.log.exception("FIND GRIB MESSAGES:: error when reading GRIB file")
                    raise

                finally:
                    e.codes_index_release(iid)
            finally:
                fin.close()
        except IOError:
            self.log.exception("FIND GRIB MESSAGES:: file error")
            raise

        if len(messages) > 0:
            self.log.info(
                f"FIND GRIB MESSAGESS:: decode date {messages[0].reftime} messages count"
                f" {len(messages)} success")

        return messages

    def get_grib_messages(self, fpath: str) -> list[common.grib.GribMessage]:
        """Reading all data from GRIB file"""

        messages = []
        try:
            fin = open(fpath, 'rb')
            try:
                try:
                    while 1:
                        msid = e.codes_grib_new_from_file(fin)
                        try:
                            if msid is None:
                                break

                            self.log.debug(f"FIND GRIB MESSAGES:: init msid {msid}")

                            sn = e.codes_get(msid, "shortName")

                            date = e.codes_get(msid, 'date')
                            time = e.codes_get(msid, 'time')
                            predict = e.codes_get(msid, 'step') * 60

                            reftime = datetime(date // 10000, date % 10000 // 100, date % 100, time // 100, 0, 0, 0,
                                               tzinfo=timezone.utc)

                            center = e.codes_get(msid, "centre")
                            lt = e.codes_get(msid, "typeOfLevel")
                            lvl = e.codes_get(msid, "level")
                            pn = e.codes_get(msid, "name")
                            code = e.codes_get(msid, "paramId")
                            unit = e.codes_get(msid, "units")
                            values = e.codes_get_double_array(msid, "values")

                            if center == 'kwbc':
                                step_type_internal = e.codes_get_string(msid, 'stepTypeInternal')

                                if step_type_internal == 'accum':

                                    start = e.codes_get(msid, "startStep")
                                    if start != 0:
                                        continue

                            if center == 'kwbc':
                                ext = e.codes_is_defined(msid, 'scaledValueOfFirstFixedSurface')

                                if ext == 1:
                                    lvl = e.codes_get(msid, 'scaledValueOfFirstFixedSurface')

                                code = code + lvl

                            if center == 'kwbc':
                                exists = False

                                for msg in messages:
                                    if msg.sname == sn and msg.level_type == lt and msg.level == lvl:
                                        exists = True
                                        break

                                if exists is True:
                                    continue

                            messages.append(
                                common.grib.GribMessage(lt, lvl, pn, sn, code, unit, center, reftime, predict, 0,
                                                        values))

                        finally:
                            if msid is not None:
                                e.codes_release(msid)
                                self.log.debug(f"FIND GRIB MESSAGES:: release msid {msid}")

                except e.CodesInternalError:
                    self.log.exception("FIND GRIB MESSAGES:: error when reading GRIB file")
                    raise
            finally:
                fin.close()
        except IOError:
            self.log.exception("FIND GRIB MESSAGES:: file error")
            raise

        if len(messages) > 0:
            self.log.info(
                f"FIND GRIB MESSAGESS:: decode date {messages[0].reftime} messages count"
                f" {len(messages)} success")

        return messages

    def get_grib_grid(self, fpath: str) -> common.grib.GribGrid:
        """Reading all data from GRIB file"""

        grid = common.grib.GribGrid()

        try:
            fin = open(fpath, 'rb')
            try:
                try:
                    while 1:
                        msid = e.codes_grib_new_from_file(fin)
                        try:
                            if msid is None:
                                break

                            self.log.debug(f"GET GRIB GRID:: init msid {msid}")

                            lat_of_first_grid_point = e.codes_get(msid, "latitudeOfFirstGridPointInDegrees")
                            lon_of_first_grid_point = e.codes_get(msid, 'longitudeOfFirstGridPointInDegrees')

                            lat_of_last_grid_point = e.codes_get(msid, 'latitudeOfLastGridPointInDegrees')
                            lon_of_last_grid_point = e.codes_get(msid, 'longitudeOfLastGridPointInDegrees')

                            lat_step = e.codes_get(msid, "iDirectionIncrementInDegrees")
                            lon_step = e.codes_get(msid, "jDirectionIncrementInDegrees")
                            lon_count = e.codes_get(msid, "Ni")
                            lat_count = e.codes_get(msid, "Nj")

                            grid.first_grid_point = common.grib.GribCoordinate(lat_of_first_grid_point,
                                                                               lon_of_first_grid_point)
                            grid.last_grid_point = common.grib.GribCoordinate(lat_of_last_grid_point,
                                                                              lon_of_last_grid_point)
                            grid.lat_step = lat_step
                            grid.lon_step = lon_step
                            grid.lat_count = lat_count
                            grid.lon_count = lon_count

                            grid.coords = []

                            if lat_of_first_grid_point > lat_of_last_grid_point:
                                lat_step *= -1

                            for i in range(0, lat_count):
                                lat = lat_of_first_grid_point + (lat_step * i)
                                for j in range(0, lon_count):
                                    lon = lon_of_first_grid_point + (lon_step * j)
                                    grid.coords.append(common.grib.GribCoordinate(lat, lon))

                            break

                        finally:
                            if msid is not None:
                                e.codes_release(msid)
                                self.log.debug(f"GET GRIB GRID:: release msid {msid}")

                except e.CodesInternalError:
                    self.log.exception("GET GRIB GRID:: error when reading GRIB file")
                    raise
            finally:
                fin.close()
        except IOError:
            self.log.exception("GET GRIB GRID:: file error")
            raise

        return grid
