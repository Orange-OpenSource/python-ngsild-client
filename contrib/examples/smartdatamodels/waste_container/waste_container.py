from datetime import datetime
from dateutil.tz import tzstr
from ngsildclient import Entity

obstime = datetime(2021, 3, 11, 15, 51, 2, tzinfo=tzstr("UTC+05:30"))  # Time of Observation

e = Entity("WasteContainer", "1021:AAWD")
e.ctx = [
    "iudx:WmgmtBin",
    "https://raw.githubusercontent.com/smart-data-models/dataModel.WasteManagement/master/context.jsonld",
]
e.prop("RFID", "67855734").prop("binCapacity", 43).prop("binCategory", "Household Bin")
e.tprop("binClearedTime", obstime).prop("binColor", "Green")
e.prop("binFillingLevel", 0.65).prop("binFullnessThreshold", 80)
e.prop("binId", 12).tprop("binLoggedTime", obstime)
e.prop("binMaxLoad", 75).prop("binRecommendedLoad", 30)
e.prop("licensePlate", "KA23F2345").loc(42.60214472222222, -8.768460000000001)
e.prop("wardId", 21)
