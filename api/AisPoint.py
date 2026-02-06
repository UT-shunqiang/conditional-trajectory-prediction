class AisPoint(object):
    def __init__(self, mmsi: int, timestamp: int, lon: float, lat: float, \
                 sog: float, cog: float, \
                    heading:None, rot:None, statu:None, shiptype:None
                 ):
        self.mmsi = mmsi
        self.timestamp = timestamp
        self.lon = lon
        self.lat = lat
        self.sog = sog
        self.cog = cog
        self.heading = heading
        self.rot = rot
        self.statu = statu
        self.shiptype = shiptype

    def to_string(self) -> str:
        return "%d,%d,%f,%f,%f,%f,%f,%d,%f,%d" % (self.mmsi, self.timestamp, self.lon, \
                                               self.lat, self.sog, self.cog, \
                                                self.heading, self.statu, self.rot, self.shiptype)

    def append_ais_str(self, ais_old_str: str) -> str:
        if ais_old_str == "":
            return self.to_string()
        return ais_old_str + ";" + self.to_string()

    @staticmethod
    def list_to_string(ais_points: list) -> str:
        if len(ais_points) == 0:
            return ""

        ais_str = ais_points[0].to_string()
        for i in range(1, len(ais_points)):
            ais_str += ";" + ais_points[i].to_string()

        return ais_str

    @staticmethod
    def from_string(ais_str: str) -> object:
        vals = ais_str.split(",")
        try:
            mmsi = int(vals[0])
            timestamp = int(vals[1])
            lon = float(vals[2])
            lat = float(vals[3])
            sog = float(vals[4])
            cog = float(vals[5])
            heading = float(vals[6])
            statu = int(vals[7])
            rot = float(vals[8])
            return AisPoint(mmsi, timestamp, lon, lat, sog, cog, heading, statu, rot)
        except Exception as e:
            return None

    @staticmethod
    def list_from_string(ais_str: str) -> list:
        ais_points = []
        ais_vals = ais_str.split(";")
        for ais_val in ais_vals:
            ais_points.append(AisPoint.from_string(ais_val))
        return ais_points

    def to_dict(self) -> dict:
        return {'userid': self.mmsi, 'time': self.timestamp, 'Lon': self.lon, 'Lat': self.lat, 'Sog': self.sog,
                'Cog': self.cog}

    def set_timestamp(self, time: int):
        self.timestamp = time

    def get_timestamp(self):
        return self.timestamp

    def get_mmsi(self):
        return self.mmsi

    def get_lon(self):
        return self.lon

    def get_lat(self):
        return self.lat

    def get_sog(self):
        return self.sog

    def get_cog(self):
        return self.cog

    def get_heading(self):
        return self.heading
    
    def get_statu(self):
        return self.statu
    
    def get_rot(self):
        return self.rot
    def get_shiptype(self):
        return self.shiptype


if __name__ == '__main__':
    aisPoint = AisPoint(1, 2, 3, 4, 5, 6,7,8,9, 10)
    aisPoint.get_statu()
#     print(aisPoint.to_string())
#     print(aisPoint.to_dict())
#     aisPoint2 = AisPoint(2, 22, 23, 24, 25, 26)
#     str1 = aisPoint2.append_ais_str(aisPoint.to_string())
#     print(str1)

#     aisPoint2_val = AisPoint.from_string(aisPoint2.to_string())
#     print(aisPoint2_val)
#     aisPoints = AisPoint.list_from_string(str1)
#     print(aisPoints)
