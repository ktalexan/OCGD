# Import necessary libraries
import os
import sys
import datetime
import json
from pathlib import Path
import shutil
import importlib
import re
import requests
import wmi
import pandas as pd
import arcpy
from arcpy import metadata as md
from arcgis.features import FeatureLayer # for REST API interaction
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from dotenv import load_dotenv
from ocgd import OCTGL

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCTL instance
tgl = OCTGL(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCTL class object
prj_meta = tgl.prj_meta
prj_dirs = tgl.prj_dirs

out_sr = tgl.sr

# scratch_path = tgl.scratch_gdb()

# url = "https://api.census.gov/data.json"
# response = requests.get(url, timeout = 20)
# datasets = response.json()['dataset']
# dataset_names = [dataset['c_dataset'] for dataset in datasets]

# Get TIGERweb dictionary from the OCTGL class object (do not export if it is current and recently updated)
tigerweb_dict = tgl.get_tigerweb_dictionary(export = True)

tigerweb_dict["acs"]["2025"]["layers"]

print(json.dumps(tigerweb_dict["acs"]["2025"]["layers"], indent=4))

[key for key in tigerweb_dict["acs"]["2025"]["layers"]]


service_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2025/MapServer/8"
feature_layer = FeatureLayer(service_url)



QUERY = "STATE = '06' AND COUNTY = '059'"



# --- USER PARAMETERS ---
rest_url = r"https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2025/MapServer/8"
out_gdb = tgl.scratch_gdb()
out_fc_name = "Census_Tracts"

# Ensure output GDB exists
if not arcpy.Exists(out_gdb):
    folder = os.path.dirname(out_gdb)
    gdb_name = os.path.basename(out_gdb)
    arcpy.CreateFileGDB_management(folder, gdb_name)

# Temporary layer name
temp_layer = "temp_layer"




try:
    # Create a feature layer from the REST service, applying the QUERY where-clause
    arcpy.MakeFeatureLayer_management(rest_url, temp_layer, QUERY)

    # Ensure spatial reference matches out_sr; accept existing SpatialReference or construct one
    if isinstance(out_sr, arcpy.SpatialReference):
        target_sr = out_sr
    else:
        try:
            target_sr = arcpy.SpatialReference(out_sr)
        except Exception:
            # Try common fallbacks (numeric WKID inside dict or string)
            if isinstance(out_sr, dict):
                wkid = out_sr.get("wkid") or out_sr.get("factoryCode")
                target_sr = arcpy.SpatialReference(int(wkid)) if wkid is not None else arcpy.SpatialReference(4269)
            else:
                try:
                    target_sr = arcpy.SpatialReference(int(out_sr))
                except Exception:
                    target_sr = arcpy.SpatialReference(4269)
    desc = arcpy.Describe(temp_layer)
    src_sr = getattr(desc, 'spatialReference', None)

    layer_to_export = temp_layer
    projected_temp = None

    try:
        src_wkid = getattr(src_sr, 'factoryCode', None) if src_sr is not None else None
        tgt_wkid = getattr(target_sr, 'factoryCode', None)
        needs_project = (src_wkid is None) or (tgt_wkid != src_wkid)
    except Exception:
        needs_project = True

    if needs_project:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        projected_name = f"{out_fc_name}_proj_{ts}"
        projected_temp = os.path.join(out_gdb, projected_name)
        arcpy.Project_management(temp_layer, projected_temp, target_sr)
        layer_to_export = projected_temp

    # Export the (possibly projected) layer to a feature class
    out_fc_path = os.path.join(out_gdb, out_fc_name)
    arcpy.FeatureClassToFeatureClass_conversion(layer_to_export, out_gdb, out_fc_name)

    print(f"✅ Feature class created: {out_fc_path}")

except arcpy.ExecuteError:
    print("ArcPy Error:", arcpy.GetMessages(2))
except Exception as e:
    print("Python Error:", e)
finally:
    # Clean up temporary layer
    if arcpy.Exists(temp_layer):
        arcpy.Delete_management(temp_layer)
