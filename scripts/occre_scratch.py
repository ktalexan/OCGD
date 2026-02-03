# Import necessary libraries
#from __future__ import annotations
import os
import sys
import datetime
import json
from pathlib import Path
import logging
import unicodedata
from typing import Optional, Dict, Any
import re
import shutil
import importlib
import wmi
import pandas as pd
import requests
import arcpy
from arcpy import metadata as md
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from dotenv import load_dotenv
from ocgd import DualOutput, OCcre

# Load environment variables from .env file
load_dotenv()

# Set pandas options
pd.options.mode.copy_on_write = True

# Set environment workspace to the current working directory
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True

# Initialize OCcre instance
cre = OCcre(part= 1, version= 2026.1)

# Get the project metadata and directories from the OCcre class object
prj_meta = cre.prj_meta
prj_dirs = cre.prj_dirs

# Load the CRE codebook
cb_cre = cre.cb

# Run and log the CRE CB Variables fetch
cre_years = cre.cre_years

# Run and log the ACS CB Variables fetch
# logger = cre.logger

# # Create CRE feature classes for each year (with logging)
# logger.enable(meta = prj_meta, filename = f"cre_feature_classes_{cre.version}.log", replace = True)
# print("CRE Feature Classes Log\n")
# for year in cre_years:
#     print(f"\nCRE feature class for year {year}\n")
#     cre.create_cre_feature_class(year)
# print("\nCRE feature classes creation completed.")
# logger.disable()




### ArcGIS Pro Paths ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n- ArcGIS Pro Paths")

# Get the paths for the ArcGIS Pro project and geodatabase
aprx_path = prj_dirs.get("gis_cre_aprx", "")
gdb_path = prj_dirs.get("gis_cre_gdb", "")
# ArcGIS Pro Project object
aprx, workspace = cre.load_aprx(aprx_path = aprx_path, gdb_path = gdb_path, add_to_map = False)
# Close all map views
aprx.closeViews()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 1.4. Map and Layout Lists ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.4. Map and Layout Lists")

### Project Maps ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n- Project Maps")

# List of maps to be created for the project
map_list = ["Map"]

for year in cre_years:
    map_list.append(f"Map{year}")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 1.5. Feature Class Definitions ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n1.5. Feature Class Definitions")


### Raw Data Feature Classes ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Raw Data Feature Classes")

arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

# List of raw data feature classes
fc_list = []
for fc in arcpy.ListFeatureClasses():
    fc_list.append(fc)
    print(f"Found raw data feature class: {fc}")


### Supporting Data Feature Classes ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Supporting Data Feature Classes")

sup_gdb = prj_dirs.get("gis_cre_sup_gdb", "")
# Define paths for the feature classes in the supporting data feature dateset of the geodatabase
# boundaries: str = os.path.join(prj_dirs.get("gis_cre_sup_gdb", ""), "boundaries")
# cities = os.path.join(prj_dirs.get("gis_cre_sup_gdb", ""), "cities")
# blocks = os.path.join(prj_dirs.get("gis_cre_sup_gdb", ""), "blocks")
# roads = os.path.join(prj_dirs.get("gis_cre_sup_gdb", ""), "roads")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Project Maps ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n2. Project Maps")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 2.1. Setup Maps ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n2.1. Setup Maps")


### Remove Old Maps ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Remove Old Maps")

# First delete all raw data maps from ArcGIS pro current project
if aprx.listMaps():
    for m in aprx.listMaps():
        if m.name in map_list:
            print(f"Removing {m.name} map from the project...")
            aprx.deleteItem(m)
        else:
            print(f"Map {m.name} is not in the list of maps to be created.")
else:
    print("No maps are currently in the project.")


### Create New Maps ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Create New Maps")

# Create new raw data maps in current ArcGIS Pro project
# for each of the maps in the list, if it exists, delete it
c = 1
for m in map_list:
    for i in aprx.listMaps():
        if i.name == m:
            print(f"Deleting map: {m}")
            aprx.deleteItem(i)
    # Create new maps
    print(f"Creating map {c}: {m}")
    aprx.createMap(m)
    c += 1

# Store the map objects in variables
cre_maps = dict()
for m in aprx.listMaps():
    cre_maps[m.name] = m

### Change Map Basemaps ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Change Map Basemaps")

# For each map, replace the existing basemap ("Topographic") with the "Dark Gray Canvas" basemap

# for m in aprx.listMaps():
#     print(f"Map: {m.name}")
#     for l in m.listLayers():
#         if l.isBasemapLayer:
#             print(f"  - Removing Basemap: {l.name}")
#             m.removeLayer(l)
#     print("  - Adding Basemap: Light Gray Canvas")
#     m.addBasemap("Light Gray Canvas")
# # Turn off the basemap reference layer for all maps
# for m in aprx.listMaps():
#     print(f"Map: {m.name}")
#     for l in m.listLayers():
#         if l.name == "Light Gray Reference":
#             l.visible = False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 2.2. Map Metadata ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n2.2. Map Metadata")

# Define OCPW logos thumbnail URLs
ocpw_logos = {
    "gradient": "https://ocpw.maps.arcgis.com/sharing/rest/content/items/67ce28a349d14451a55d0415947c7af3/data",
    "white": "https://ocpw.maps.arcgis.com/sharing/rest/content/items/49c8edf21288446785a721cfa6b10b7e/data",
    "blue": "https://ocpw.maps.arcgis.com/sharing/rest/content/items/1abb3e5d9bdb4efdbeb46e4b2dbc577c/data",
    "green": "https://ocpw.maps.arcgis.com/sharing/rest/content/items/4a40df7cb7264cc89c1af21ce70c718e/data",
    "transparent": "https://ocpw.maps.arcgis.com/sharing/rest/content/items/07a732e641374cfd99cfa8cfe47c697c/data'"
}

### Main Map Metadata ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Main Map Metadata")

map_main = cre_maps.get("Map")
if map_main:
    print("Setting metadata for Map...")
    md_map_main = md.Metadata(map_main)
    md_map_main.title = "County of Orange Collision Records Extract (CRE)"
    md_map_main.tags = "Orange County, California, Community Resilience Estimates, CRE, OCCRE, Census Tracts"
    md_map_main.summary = "Orange County Community Resilience Estimates for all available years at Census Tracts geography level."
    md_map_main.description = f"Orange County Community Resilience Estimates (OCCRE) for year {year} at Census Tracts geography level. The data contains composite social vulnerability indicators derived from U.S. Census data. Version: {self.version}, last updated on {self.data_date}."
    md_map_main.credits = "Dr. Kostas Alexandridis, GISP, Data Scientist, OC Public Works Geospatial Services"
    md_map_main.accessConstraints = """The feed data and associated resources (maps, apps, endpoints) can be used under a <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">Creative Commons CC-SA-BY</a> License, providing attribution to OC Public Works Geospatial Services. <div><br /></div><div>We make every effort to provide the most accurate and up-to-date data and information. Nevertheless the data feed is provided, 'as is' and OC Public Work's standard <a href="https://www.ocgov.com/contact-county/disclaimer" target="_blank">Disclaimer</a> applies.</div><div><br /></div><div>For any inquiries, suggestions or questions, please contact:</div><div><br /></div><div style="text-align:center;"><a href="https://www.linkedin.com/in/ktalexan/" target="_blank"><b>Dr. Kostas Alexandridis, GISP</b></a><br /></div><div style="text-align:center;">GIS Analyst | Spatial Complex Systems Scientist</div><div style="text-align:center;">OC Public Works Geospatial Services</div><div style="text-align:center;"><div>601 N. Ross Street, P.O. Box 4048, Santa Ana, CA 92701</div><div>Email: <a href="mailto:kostas.alexandridis@ocpw.ocgov.com" target="_blank">kostas.alexandridis@ocpw.ocgov.com</a> | Phone: (714) 967-0826</div></div>"""
    md_map_main.thumbnailUri = ocpw_logos["gradient"]
    md_map_main.save()

### Annual Maps Metadata ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Annual Maps Metadata")

for year in cre_years:
    map_year = cre_maps.get(f"Map{year}")
    if map_year:
        print(f"Setting metadata for Map{year}...")
        md_map_year = md.Metadata(map_year)
        md_map_year.title = f"County of Orange Collision Records Extract (CRE) - {year}"
        md_map_year.tags = "Orange County, California, Community Resilience Estimates, CRE, OCCRE, Census Tracts"
        md_map_year.summary = f"Orange County Community Resilience Estimates for year {year} at Census Tracts geography level."
        md_map_year.description = f"Orange County Community Resilience Estimates (OCCRE) for year {year} at Census Tracts geography level. The data contains composite social vulnerability indicators derived from U.S. Census data. Version: {self.version}, last updated on {self.data_date}."
        md_map_year.credits = "Dr. Kostas Alexandridis, GISP, Data Scientist, OC Public Works Geospatial Services"
        md_map_year.accessConstraints = """The feed data and associated resources (maps, apps, endpoints) can be used under a <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">Creative Commons CC-SA-BY</a> License, providing attribution to OC Public Works Geospatial Services. <div><br /></div><div>We make every effort to provide the most accurate and up-to-date data and information. Nevertheless the data feed is provided, 'as is' and OC Public Work's standard <a href="https://www.ocgov.com/contact-county/disclaimer" target="_blank">Disclaimer</a> applies.</div><div><br /></div><div>For any inquiries, suggestions or questions, please contact:</div><div><br /></div><div style="text-align:center;"><a href="https://www.linkedin.com/in/ktalexan/" target="_blank"><b>Dr. Kostas Alexandridis, GISP</b></a><br /></div><div style="text-align:center;">GIS Analyst | Spatial Complex Systems Scientist</div><div style="text-align:center;">OC Public Works Geospatial Services</div><div style="text-align:center;"><div>601 N. Ross Street, P.O. Box 4048, Santa Ana, CA 92701</div><div>Email: <a href="mailto:kostas.alexandridis@ocpw.ocgov.com" target="_blank">kostas.alexandridis@ocpw.ocgov.com</a> | Phone: (714) 967-0826</div></div>"""
        md_map_year.thumbnailUri = ocpw_logos["gradient"]
        md_map_year.save()
    else:
        print(f"Map{year} not found in the project.")


### Save Project ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Save Project")

# Save the project
aprx.save()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3. Map Layers Processing ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\nMap Layers Processing")

# In this section we will be creating map layers for the feature classes in the geodatabase. The layers will be added to the maps and layouts.


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 3.1 Time Settings Configuration ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n3.1 Time Settings Configuration")

dt_start = datetime.datetime.combine(prj_meta["date_start"], datetime.time(0, 0, 0))
dt_end = datetime.datetime.combine(prj_meta["date_end"], datetime.time(23, 59, 59))
dt_diff = dt_end - dt_start

# Define time settings configuration for the map layers
# Define the key time parameters for the layers using a dictionary
time_settings = {
    "st": dt_start,
    "et": dt_end,
    "td": dt_diff,
    "stf": "date_datetime",
    "tsi": 1.0,
    "tsiu": "months",
    "tz": arcpy.mp.ListTimeZones("*Pacific*")[0],
}
# where, st: start time, et: end time, td: time extent, stf: time field,
# tsi: time interval, tsiu: time units, tz: time zone


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 3.2 Collisions Map Layers ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n3.2 Collisions Map Layers")


### Open Map View ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Open Map View")

# Close all previous map views
aprx.closeViews()
# Open the roads map view
map_collisions.openView()
# set the main map as active map
map_active = aprx.activeMap
# Remove all layers from the active map
for lyr in map_collisions.listLayers():
    if not lyr.isBasemapLayer:
        print(f"Removing layer: {lyr.name}")
        map_collisions.removeLayer(lyr)


### Add Layers to Map ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Add Layers to Map")

# Add the feature classes as layers to the map (in order, as the first layer goes to the bottom of the contents)
# Add the data layers to the map
map_collisions_lyr_boundaries = map_collisions.addDataFromPath(boundaries)
map_collisions_lyr_cities = map_collisions.addDataFromPath(cities)
map_collisions_lyr_blocks = map_collisions.addDataFromPath(blocks)
map_collisions_lyr_roads = map_collisions.addDataFromPath(roads)
map_collisions_lyr_collisions = map_collisions.addDataFromPath(collisions)
# Set layer visibility on the map
map_collisions_lyr_boundaries.visible = False
map_collisions_lyr_cities.visible = False
map_collisions_lyr_blocks.visible = False
map_collisions_lyr_roads.visible = False
map_collisions_lyr_collisions.visible = False


### Enable Time Settings ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Enable Time Settings")

# Setup and enable time settings for the collisions map layers
octr.set_layer_time(time_settings = time_settings, layer = map_collisions_lyr_collisions)


### Layer Symbology ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Layer Symbology")

# Define symbology for each of the map layers. The symbology is predefined in the project's template layer folders.

# - Collisions layer
# Apply the symbology for the Collisions data layer
arcpy.management.ApplySymbologyFromLayer(
    in_layer = map_collisions_lyr_collisions,
    in_symbology_layer = os.path.join(prj_dirs.get("gis_layers_templates", ""), "OCTraffic Collisions.lyrx"),
    symbology_fields = [["VALUE_FIELD", "coll_severity", "coll_severity"]],
    update_symbology = "MAINTAIN",
)
print(arcpy.GetMessages())

# - Roads layer
# Apply the symbology for the Roads data layer
arcpy.management.ApplySymbologyFromLayer(
    in_layer = map_collisions_lyr_roads,
    in_symbology_layer = os.path.join(prj_dirs.get("gis_layers_templates", ""), "OCTraffic Roads.lyrx"),
    symbology_fields = [["VALUE_FIELD", "road_cat", "road_cat"]],
    update_symbology = "MAINTAIN",
)
print(arcpy.GetMessages())

# - Census Blocks layer
# Apply the symbology for the US Census 2020 Blocks data layer
arcpy.management.ApplySymbologyFromLayer(
    in_layer = map_collisions_lyr_blocks,
    in_symbology_layer = os.path.join(prj_dirs.get("gis_layers_templates", ""), "OCTraffic Census Blocks.lyrx"),
    symbology_fields = [["VALUE_FIELD", "population_density", "population_density"]],
    update_symbology = "MAINTAIN",
)
print(arcpy.GetMessages())

# - Cities layer
# Apply the symbology for the Cities data layer
arcpy.management.ApplySymbologyFromLayer(
    in_layer = map_collisions_lyr_cities,
    in_symbology_layer = os.path.join(prj_dirs.get("gis_layers_templates", ""), "OCTraffic Cities.lyrx"),
    symbology_fields = [["VALUE_FIELD", "city_pop_dens", "city_pop_dens"]],
    update_symbology = "MAINTAIN",
)
print(arcpy.GetMessages())

# - Boundaries layer
# Apply the symbology for the Boundaries data layer
arcpy.management.ApplySymbologyFromLayer(
    in_layer = map_collisions_lyr_boundaries,
    in_symbology_layer = os.path.join(prj_dirs.get("gis_layers_templates", ""), "OCTraffic Boundaries.lyrx"),
    symbology_fields = None,
    update_symbology = "MAINTAIN",
)
print(arcpy.GetMessages())


### Layer CIM Operations ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Layer CIM Operations")

# Generate CIM JSON configuration for layers
# Get CIM definitions for the collisions map layers
map_collisions_cim_boundaries = map_collisions_lyr_boundaries.getDefinition("V3")
map_collisions_cim_cities = map_collisions_lyr_cities.getDefinition("V3")
map_collisions_cim_blocks = map_collisions_lyr_blocks.getDefinition("V3")
map_collisions_cim_roads = map_collisions_lyr_roads.getDefinition("V3")
map_collisions_cim_collisions = map_collisions_lyr_collisions.getDefinition("V3")

# Set symbology headings and update CIM definitions for layers
# Set the layer headings
map_collisions_cim_boundaries.renderer.heading = "Boundaries"
map_collisions_cim_cities.renderer.heading = "City Population Density"
map_collisions_cim_blocks.renderer.heading = "Population Density"
map_collisions_cim_roads.renderer.heading = "Road Categories"
map_collisions_cim_collisions.renderer.heading = "Severity Level"
# Update the map layer definitions
map_collisions_lyr_boundaries.setDefinition(map_collisions_cim_boundaries)
map_collisions_lyr_cities.setDefinition(map_collisions_cim_cities)
map_collisions_lyr_blocks.setDefinition(map_collisions_cim_blocks)
map_collisions_lyr_roads.setDefinition(map_collisions_cim_roads)
map_collisions_lyr_collisions.setDefinition(map_collisions_cim_collisions)
# Update the CIM definition for the collisions map
cim_collisions = map_collisions.getDefinition("V3")  # Collisions map CIM


### Export Map and Map Layers ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Export Map and Map Layers")

# Update the collisions map mapx file
octr.export_cim(aprx = aprx, cim_type = "map", cim_object = map_collisions, cim_name = "collisions")
# Export map layers as CIM JSON `.lyrx` files to the layers folder directory of the project.
for l in map_collisions.listLayers():
    if not l.isBasemapLayer:
        octr.export_cim(aprx = aprx, cim_type = "layer", cim_object = l, cim_name = l.name)


### Save Project ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Save Project")

# Save the project
aprx.save()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 4 Map CIM and Exporting ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n4 Map CIM and Exporting")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 4.1 Map CIM Processing ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n4.1 Map CIM Processing")


### Get Map CIM ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Get Map CIM")

# Get the CIM definitions for the OCSWIRS maps
cim_collisions = map_collisions.getDefinition("V3")
cim_crashes = map_collisions.getDefinition("V3")
cim_parties = map_collisions.getDefinition("V3")
cim_victims = map_victims.getDefinition("V3")
cim_injuries = map_injuries.getDefinition("V3")
cim_fatalities = map_fatalities.getDefinition("V3")
cim_fhs_100m1km = map_fhs_100m1km.getDefinition("V3")
cim_fhs_150m2km = map_fhs_150m2km.getDefinition("V3")
cim_fhs_100m5km = map_fhs_100m5km.getDefinition("V3")
cim_fhs_roads_500ft = map_fhs_roads_500ft.getDefinition("V3")
cim_ohs_roads_500ft = map_ohs_roads_500ft.getDefinition("V3")
cim_road_crashes = map_road_crashes.getDefinition("V3")
cim_road_hotspots = map_road_hotspots.getDefinition("V3")
cim_road_buffers = map_road_buffers.getDefinition("V3")
cim_road_segments = map_road_segments.getDefinition("V3")
cim_roads = map_roads.getDefinition("V3")
cim_point_fhs = map_point_fhs.getDefinition("V3")
cim_point_ohs = map_point_ohs.getDefinition("V3")
cim_pop_dens = map_pop_dens.getDefinition("V3")
cim_hou_dens = map_hou_dens.getDefinition("V3")
cim_area_cities = map_area_cities.getDefinition("V3")
cim_area_blocks = map_area_blocks.getDefinition("V3")
cim_summaries = map_summaries.getDefinition("V3")
cim_analysis = map_analysis.getDefinition("V3")
cim_regression = map_regression.getDefinition("V3")


### Use Service Layer IDs ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Use Service Layer IDs")

# Change the map properties to allow assignment of unique numeric IDs for sharing web layers

# Collisions Map
cim_collisions.useServiceLayerIDs = True
map_collisions.setDefinition(cim_collisions)
# Crashes Map
cim_crashes.useServiceLayerIDs = True
map_crashes.setDefinition(cim_crashes)
# Parties Map
cim_parties.useServiceLayerIDs = True
map_parties.setDefinition(cim_parties)
# Victims Map
cim_victims.useServiceLayerIDs = True
map_victims.setDefinition(cim_victims)
# Injuries Map
cim_injuries.useServiceLayerIDs = True
map_injuries.setDefinition(cim_injuries)
# Fatalities Map
cim_fatalities.useServiceLayerIDs = True
map_fatalities.setDefinition(cim_fatalities)
# FHS 100m 1km Map
cim_fhs_100m1km.useServiceLayerIDs = True
map_fhs_100m1km.setDefinition(cim_fhs_100m1km)
# FHS 150m 2km Map
cim_fhs_150m2km.useServiceLayerIDs = True
map_fhs_150m2km.setDefinition(cim_fhs_150m2km)
# FHS 100m 5km Map
cim_fhs_100m5km.useServiceLayerIDs = True
map_fhs_100m5km.setDefinition(cim_fhs_100m5km)
# FHS Roads 500ft Map
cim_fhs_roads_500ft.useServiceLayerIDs = True
map_fhs_roads_500ft.setDefinition(cim_fhs_roads_500ft)
# OHS Roads 500ft Map
cim_ohs_roads_500ft.useServiceLayerIDs = True
map_ohs_roads_500ft.setDefinition(cim_ohs_roads_500ft)
# Road Crashes Map
cim_road_crashes.useServiceLayerIDs = True
map_road_crashes.setDefinition(cim_road_crashes)
# Road Hotspots Map
cim_road_hotspots.useServiceLayerIDs = True
map_road_hotspots.setDefinition(cim_road_hotspots)
# Road Buffers Map
cim_road_buffers.useServiceLayerIDs = True
map_road_buffers.setDefinition(cim_road_buffers)
# Road Segments Map
cim_road_segments.useServiceLayerIDs = True
map_road_segments.setDefinition(cim_road_segments)
# Roads Map
cim_roads.useServiceLayerIDs = True
map_roads.setDefinition(cim_roads)
# Point FHS Map
cim_point_fhs.useServiceLayerIDs = True
map_point_fhs.setDefinition(cim_point_fhs)
# Point OHS Map
cim_point_ohs.useServiceLayerIDs = True
map_point_ohs.setDefinition(cim_point_ohs)
# Population Density Map
cim_pop_dens.useServiceLayerIDs = True
map_pop_dens.setDefinition(cim_pop_dens)
# Housing Density Map
cim_hou_dens.useServiceLayerIDs = True
map_hou_dens.setDefinition(cim_hou_dens)
# Area Cities Map
cim_area_cities.useServiceLayerIDs = True
map_area_cities.setDefinition(cim_area_cities)
# Area Blocks Map
cim_area_blocks.useServiceLayerIDs = True
map_area_blocks.setDefinition(cim_area_blocks)
# Summaries Map
cim_summaries.useServiceLayerIDs = True
map_summaries.setDefinition(cim_summaries)
# Analysis Map
cim_analysis.useServiceLayerIDs = True
map_analysis.setDefinition(cim_analysis)
# Regression Map
cim_regression.useServiceLayerIDs = True
map_regression.setDefinition(cim_regression)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## 4.2 Export Maps to JSON ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n4.2 Export Maps to JSON")

# Export maps to mapx CIM JSON files
for m in aprx.listMaps():
    print(f"Exporting {m.name} map...")
    octr.export_cim(aprx = aprx, cim_type = "map", cim_object = m, cim_name = m.name)


### Save Project ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("- Save Project")

# Save the project
aprx.save()

