# Import necessary libraries
from arcgis._impl.common._spatial import arcpy
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
from ocgd import OCTL

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCTL instance
octl = OCTL(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCTL class object
prj_meta = octl.prj_meta
prj_dirs = octl.prj_dirs

# Get the spatial reference from the OCTL class object (Web Mercator, WKID 3857)
out_sr = octl.sr

# scratch_path = octl.scratch_gdb()

# url = "https://api.census.gov/data.json"
# response = requests.get(url, timeout = 20)
# datasets = response.json()['dataset']
# dataset_names = [dataset['c_dataset'] for dataset in datasets]

# Get TIGERweb dictionary from the OCTL class object (do not export if it is current and recently updated)
# twr_cb = octl.get_tigerweb_dictionary(export = True)
twr_cb = octl.get_tigerweb_dictionary(export = False)





def create_gdb_from_twr(year: int, level: str = "acs", out_gdb: str = octl.scratch_gdb()):
    """
    Create a file geodatabase from the TIGERweb REST API layers for a specified level and year.

    Parameters:
    level (str): The level of data to retrieve (e.g., "acs").
    year (int): The year of the data to retrieve (e.g., 2025).
    """
    # Set the arcpy environment to the output geodatabase
    arcpy.env.workspace = out_gdb
    arcpy.env.overwriteOutput = True

    # Get the TIGERweb dictionary
    print("Updating TIGERweb dictionary...")
    cb = octl.get_tigerweb_dictionary(export = False)

    # Validate level and year
    if level in cb:
        level_years = [y for y in cb[level]]
        if str(year) not in level_years:
            raise ValueError(f"Year {year} not found in level '{level}'. Available years: {level_years}")
            return
    else:
        raise ValueError(f"Level '{level}' not found in TIGERweb dictionary. Available levels: {list(cb.keys())}")
    
    # Get the specific year dictionary for the level
    cb_layers = cb.get(level, {}).get(str(year), {}).get("layers", {})

    # Part 1: Create Counties feature class as reference
    
    # Find the Counties layer information and populate variables
    if "Counties" in cb_layers:
        print("\n--- Processing layer: Counties ---")
        # The REST endpoint for the Counties layer
        layer_rest = cb_layers["Counties"]["rest"]
        # The Counties alias
        layer_alias = cb_layers["Counties"]["alias"]
        # The Counties layer code
        layer_code = cb_layers["Counties"]["code"]
        # The output feature class name (same as layer code)
        out_fc_name = layer_code
        # The where-clause to filter for Orange County, CA
        QUERY = "STATE = '06' AND COUNTY = '059'"  # Orange County, CA

        # Ensure output GDB exists
        if not arcpy.Exists(out_gdb):
            folder = os.path.dirname(out_gdb)
            gdb_name = os.path.basename(out_gdb)
            arcpy.CreateFileGDB_management(folder, gdb_name)

        # Temporary layer name
        temp_layer = "temp_layer"

        try:
            print("- Using direct_query method")
            # Create a feature layer from the REST service, applying the QUERY where-clause
            arcpy.MakeFeatureLayer_management(layer_rest, temp_layer, QUERY)

            # Get the spatial reference of the temporary layer
            print("- Checking spatial reference")
            temp_sr = arcpy.Describe(temp_layer).spatialReference

            # Check if the spatial reference is the desired output spatial reference
            if temp_sr.factoryCode != out_sr.factoryCode:
                print("- Projecting to desired spatial reference (Web Mercator, WKID 3857)")
                # Project the layer to the desired spatial reference
                projected_temp = "projected_temp_layer"
                arcpy.Project_management(temp_layer, projected_temp, out_sr)
                # Delete the temporary layer
                arcpy.Delete_management(temp_layer)
                # Recreate the temporary layer variable to point to the projected layer
                arcpy.MakeFeatureLayer_management(projected_temp, temp_layer)
            else:
                print("- No projection needed. Spatial reference matches.")

            # Export the (possibly projected) layer to a feature class
            print("- Exporting temporary layer to a feature class")
            out_fc_path = os.path.join(out_gdb, out_fc_name)
            arcpy.FeatureClassToFeatureClass_conversion(temp_layer, out_gdb, out_fc_name)
            
            # Set the alias name for the output feature class
            print(f"- Setting alias: {layer_alias} for the output feature class: {out_fc_name}")
            if arcpy.Exists(out_fc_path):
                arcpy.AlterAliasName(out_fc_path, layer_alias)

            print(f"✅ Feature class created: {out_fc_path}")

        except arcpy.ExecuteError:
            print("- ArcPy Error:", arcpy.GetMessages(2))
        except Exception as e:
            print("- Python Error:", e)
        finally:
            # Clean up temporary layer
            print("- Cleaning up temporary layers")
            if arcpy.Exists(temp_layer):
                arcpy.Delete_management(temp_layer)

    # Part 2: Process other layers

    # Loop through each layer in the TIGERweb dictionary for the specified level and year
    for layer, layer_info in cb_layers.items():

        # Skip the Counties layer as it has already been processed
        if layer == "Counties":
            continue
        
        # Process each layer
        print(f"\n--- Processing layer: {layer} ---")
        # Get the layer code, alias, and REST endpoint
        layer_code = layer_info["code"]
        layer_alias = layer_info["alias"]
        layer_rest = layer_info["rest"]

        # Define output feature class name and path
        out_fc_name = layer_code
        out_fc_path = os.path.join(out_gdb, out_fc_name)

        # Define the path to the Counties feature class for spatial selection (the one created earlier)
        county_path = os.path.join(out_gdb, "CO")

        # Ensure output GDB exists
        if not arcpy.Exists(out_gdb):
            folder = os.path.dirname(out_gdb)
            gdb_name = os.path.basename(out_gdb)
            arcpy.CreateFileGDB_management(folder, gdb_name)

        # Temporary layer name
        temp_layer = "temp_layer"

        # Initialize method variable
        method = ""

        # Determine method based on layer code
        if layer_code in ["TR", "CO", "CS", "BG", "BL", "TZ"]:
            method = "direct_query"
            QUERY = "STATE = '06' AND COUNTY = '059'"
            print(f"- Using {method} method")
            try:
                # Create a feature layer from the REST service, applying the QUERY where-clause
                print("- Creating feature layer with query")
                arcpy.MakeFeatureLayer_management(layer_rest, temp_layer, QUERY)

                # Get the spatial reference of the temporary layer
                print("- Checking spatial reference")
                temp_sr = arcpy.Describe(temp_layer).spatialReference

                # Check if the spatial reference is the desired output spatial reference
                if temp_sr.factoryCode != out_sr.factoryCode:
                    print("- Projecting to desired spatial reference (Web Mercator, WKID 3857)")
                    # Project the layer to the desired spatial reference
                    projected_temp = "projected_temp_layer"
                    arcpy.Project_management(temp_layer, projected_temp, out_sr)
                    # Delete the temporary layer
                    arcpy.Delete_management(temp_layer)
                    # Recreate the temporary layer variable to point to the projected layer
                    arcpy.MakeFeatureLayer_management(projected_temp, temp_layer)
                else:
                    print("- No projection needed. Spatial reference matches.")

                # Export the (possibly projected) layer to a feature class
                print("- Exporting temporary layer to a feature class")
                out_fc_path = os.path.join(out_gdb, out_fc_name)
                arcpy.FeatureClassToFeatureClass_conversion(temp_layer, out_gdb, out_fc_name)

            except arcpy.ExecuteError:
                print("ArcPy Error:", arcpy.GetMessages(2))
            except Exception as e:
                print("Python Error:", e)
            finally:
                # Clean up temporary layer
                if arcpy.Exists(temp_layer):
                    arcpy.Delete_management(temp_layer)

                # Check if the output feature class is empty
                if int(arcpy.GetCount_management(out_fc_path).getOutput(0)) == 0:
                    arcpy.Delete_management(out_fc_path)
                else:
                    # Set the alias name for the output feature class
                    print(f"- Setting alias: {layer_alias} for the output feature class: {out_fc_name}")
                    if arcpy.Exists(out_fc_path):
                        arcpy.AlterAliasName(out_fc_path, layer_alias)
                    
                    print(f"✅ Feature class created: {out_fc_path}")

        else:
            method = "spatial_selection"
            print(f"- Using {method} method")

            if "STATE" in [f.name for f in arcpy.ListFields(layer_rest)]:
                QUERY = "STATE = '06'"

                # Create a feature layer from the REST service, applying the QUERY where-clause
                print("- Creating feature layer with query")
                arcpy.MakeFeatureLayer_management(layer_rest, temp_layer, QUERY)
            else:
                # Create a feature layer from the REST service without a where-clause
                print("- Creating feature layer without query")
                arcpy.MakeFeatureLayer_management(layer_rest, temp_layer)

            # Check if the temp_lyr is empty
            print("- Checking if temp_lyr is empty")
            if int(arcpy.management.GetCount("temp_lyr").getOutput(0)) == 0:
                arcpy.Delete_management(temp_layer)
                continue

            # Get the spatial reference of the temporary layer
            print("- Checking spatial reference")
            temp_sr = arcpy.Describe(temp_layer).spatialReference

            # Check if the spatial reference is the desired output spatial reference
            if temp_sr.factoryCode != out_sr.factoryCode:
                print("- Projecting to desired spatial reference (Web Mercator, WKID 3857)")
                # Project the layer to the desired spatial reference
                projected_temp = "projected_temp_layer"
                arcpy.Project_management(temp_layer, projected_temp, out_sr)
                # Delete the temporary layer
                arcpy.Delete_management(temp_layer)
                # Recreate the temporary layer variable to point to the projected layer
                arcpy.MakeFeatureLayer_management(projected_temp, temp_layer)
            else:
                print("- No projection needed. Spatial reference matches.")

            # Apply your spatial selection with the negative distance
            print("- Applying spatial selection within -1000 Feet of County boundary")
            arcpy.management.SelectLayerByLocation(
                in_layer = temp_layer,
                overlap_type = "WITHIN_A_DISTANCE",
                select_features = county_path,
                search_distance = "-1000 Feet",
                selection_type = "NEW_SELECTION",
                invert_spatial_relationship = "NOT_INVERT"
            )

            # Export the selection to a new fc
            print("- Exporting selected features to a feature class")
            out_fc_path = os.path.join(out_gdb, out_fc_name)
            arcpy.conversion.FeatureClassToFeatureClass(temp_layer, out_gdb, out_fc_name)

            # Clean up temporary layer
            if arcpy.Exists(temp_layer):
                arcpy.Delete_management(temp_layer)

            # Check if the output feature class is empty
            if int(arcpy.GetCount_management(out_fc_path).getOutput(0)) == 0:
                arcpy.Delete_management(out_fc_path)
            else:
                # Set the alias name for the output feature class
                print(f"- Setting alias: {layer_alias} for the output feature class: {out_fc_name}")
                if arcpy.Exists(out_fc_path):
                    arcpy.AlterAliasName(out_fc_path, layer_alias)

                print(f"✅ Feature class created: {out_fc_path}")
    print("\nAll layers processed.")
    return out_gdb



out_gdb = create_gdb_from_twr(year=2025, level="acs")






layer_dict = {}
for level, content in twr_cb.items():
    if level != "main":
        for year, year_content in content.items():
            layers = year_content["layers"]
            for layer_name, layer_info in layers.items():
                layer_code = layer_info["code"]
                if layer_name not in layer_dict:
                    layer_dict[layer_name] = layer_code

print(json.dumps(layer_dict, indent=4))


rest = twr_cb["acs"]["2025"]["layers"]["2020 Census Public Use Microdata Areas"]["rest"]

arcpy.ListFields(rest)
fields = [f.name for f in arcpy.ListFields(rest)]
fields

if "STATE" in [f.name for f in arcpy.ListFields(rest)]:
    print("STATE field exists")

if 'STATE' in fields:
    arcpy.MakeFeatureLayer_management(rest, 'temp_lyr')
else:
    raise RuntimeError("REST layer has no 'STATE' field: {}".format(rest))

