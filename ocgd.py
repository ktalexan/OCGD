# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Orange County US Census Geodemographics (OCGD)
# Title: OCGD Project Template Main Class ----
# Author: Dr. Kostas Alexandridis, GISP
# Date: January 2026
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import necessary libraries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import datetime
from pathlib import Path
import json
import re
import logging
import unicodedata
from typing import Union, Optional, Dict, Any
import wmi
import pytz
import pandas as pd
import requests
import arcpy
from arcpy import metadata as md
from arcgis.features import GeoAccessor, GeoSeriesAccessor


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the DualOutput class for logging ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DualOutput:
    """
    A class to duplicate console output to a log file.
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Class initialization ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, filename: Optional[str] = None, meta: Optional[dict] = None):
        self._orig = None
        self._log = None
        self._filename = filename
        self._start_time = None
        self._end_time = None
        self._duration = None
        self._filetype = "log"  # Default filetype
        # Store optional project metadata so other methods can access it
        self.meta: Optional[dict] = meta
        self.project_name: Optional[str] = meta.get("name") if meta else None
        self.project_title: Optional[str] = meta.get("title") if meta else None
        self.project_version: Optional[float] = meta.get("version") if meta else None
        self.project_author: Optional[str] = meta.get("author") if meta else None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Open log file ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _open_log(self, meta: dict, filename: str):
        # From the filename, determine if it's a .log, .txt, or .md file
        if filename.endswith(".md"):
            self._filetype = "markdown"
        elif filename.endswith(".log") or filename.endswith(".txt"):
            self._filetype = "log"
        if meta is not None:
            self.project_name = meta.get("name")
            self.project_title = meta.get("title")
            self.project_version = meta.get("version")
            self.project_author = meta.get("author")
        # Open the log file in append mode in the tests directory
        path = os.path.join(os.getcwd(), "logs", os.path.basename(filename))
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok = True)
        # If the file does not exist, open it and writh an initial line
        if not os.path.isfile(path):
            with open(path, "w", encoding="utf-8") as f:
                # If it is a markdown file, write the header as the meta.get("project_name")
                if self._filetype == "markdown":
                    f.write(f"# {self.project_name}\n- Title: {self.project_title}\n- Version: {self.project_version}\n- Author: {self.project_author}\n- Filename: **{os.path.basename(filename)}**\n")
                elif self._filetype == "log":
                    # Wtite the project name and title in uppercase
                    f.write(f"Project Name: {self.project_name.upper()}\nProject Title: {self.project_title.upper()}\nVersion: {self.project_version}\nAuthor: {self.project_author}\nFilename: {os.path.basename(filename)}\n\n")
        # Return the opened file object
        return open(path, "a", encoding="utf-8")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Enable logging ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def enable(self, meta: Optional[dict] = None, filename: Optional[str] = None, replace: bool = False):
        logid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if self._orig is not None:
            return
        # Prefer provided meta, otherwise use stored meta
        if meta is not None:
            self.meta = meta
        # Determine the filetype based on the filename extension
        fn = filename or self._filename or "output.log"
        if fn.endswith(".md"):
            self._filetype = "markdown"
        elif fn.endswith(".log"):
            self._filetype = "log"
        elif fn.endswith(".txt"):
            self._filetype = "text"
        else:
            print("Warning: Unrecognized file extension. Defaulting to .log")
            self._filetype = "log"  # Default to log if no extension provided
            # Change filename to have .log extension
            fn = os.path.splitext(fn)[0] + ".log"
        self._orig = sys.stdout

        # If replace is requested, remove any existing file before opening
        if replace:
            try:
                path_to_remove = os.path.join(os.getcwd(), "logs", os.path.basename(fn))
                if os.path.isfile(path_to_remove):
                    os.remove(path_to_remove)
            except OSError:
                # If we cannot remove the file, continue and let _open_log handle errors
                pass

        self._log = self._open_log(meta, fn)
        sys.stdout = self
        self._start_time = datetime.datetime.now()

        if self._filetype == "markdown":
            print("----\n")
            print(f"\n> [!NOTE]\n> - Log ID: {logid}\n> - Date: {datetime.datetime.now().strftime('%B %d, %Y')}\n> - Logging started at {self._start_time.strftime('%m/%d/%Y %H:%M:%S')}\n")
        else:
            print(f"---- Start of log ID: {logid} ----")
            print(f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}")
            print(f"Logging started at {self._start_time.strftime('%m/%d/%Y %H:%M:%S')}\n\n")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Disable logging ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def disable(self):
        self._end_time = datetime.datetime.now()
        if self._filetype == "markdown":
            print(f"\n> [!NOTE]\n> - Logging ended at {self._end_time.strftime('%m/%d/%Y %H:%M:%S')}")
        else:
            print(f"\n\nLogging ended at {self._end_time.strftime('%m/%d/%Y %H:%M:%S')}")
        self._duration = self._end_time - self._start_time
        if self._duration.total_seconds() < 60:
            if self._filetype == "markdown":
                print(f"> - Elapsed Time: {self._duration.total_seconds():.0f} seconds\n")
                print("----\n")
            else:
                print(f"Elapsed Time: {self._duration.total_seconds():.0f} seconds")
                print("---- End of log ----\n")
        else:
            # Display time in days, hours, minutes and seconds
            days, remainder = divmod(self._duration.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            # Only show non-zero values
            if days > 0:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds")
                    print("---- End of log ----\n")
            elif hours > 0:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds")
                    print("---- End of log ----\n")
            elif minutes > 0:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(minutes)} minutes and {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(minutes)} minutes and {int(seconds)} seconds")
                    print("---- End of log ----\n")
            else:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(seconds)} seconds")
                    print("---- End of log ----\n")
        
        if self._orig is None:
            return
        sys.stdout = self._orig
        try:
            if self._log:
                self._log.close()
        finally:
            self._orig = None
            self._log = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Context manager enter ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __enter__(self):
        # Use stored metadata when entering context if available
        self.enable(meta=self.meta, filename=self._filename)
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Context manager exit ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __exit__(self, exc_type, exc, tb):
        self.disable()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Write output ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def write(self, message):
        if self._orig:
            self._orig.write(message)
        if self._log:
            try:
                self._log.write(message)
            except (OSError, UnicodeEncodeError):
                # Ignore known I/O/encoding errors when writing to the log; allow other exceptions to propagate
                pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Flush output ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def flush(self):
        if self._orig:
            self._orig.flush()
        if self._log:
            try:
                self._log.flush()
            except OSError:
                # Ignore known I/O errors when flushing the log; allow other exceptions to propagate
                pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the OCGD Class ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OCGD:
    """
    A class to initialize the Orange County Geodemographics (OCGD) main project structure.
    The ProjectDirs class provides methods to set up the project directories and metadata. It is called by other classes such as OCGD, OCACS, OCTL, OCDC, and OCCR to inherit common functionality.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Initialize project structure ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, part: int = 0, version: float = float(datetime.datetime.now().year)):
        """
        Initialize the OCGD project structure.
        Args:
            Nothing
        Returns:
            Nothing
        Raises:
            Nothing
        Example:
            >>> gd_init = GDInit()
        Notes:
            This function initializes the OCGD project structure.
        """
        # Create a DualOutput instance for logging
        self.logger = DualOutput()

        # Set the part and version
        self.part = part
        self.version = version

        # Set the base path and data date
        self.base_path = os.getcwd()
        self.data_date = datetime.datetime.now().strftime("%B %Y")

        # Create a prj_dirs variable calling the project_directories function
        self.prj_dirs = self.project_directories(silent = False)

        # Attach project directories to logger so it's available to all logger methods
        try:
            self.logger.meta = self.prj_dirs
        except AttributeError:
            # Logger does not support 'meta' attribute; ignore safely
            pass

        # Get the available ACS5 years
        self.acs5_years = self.get_census_years(dataset = "acs5")
        # self.acs5_years = self.get_available_acs5_years()

        # Get the available CR years
        self.cr_years = self.get_census_years(dataset = "cr")

        # Set the Spatial Reference to Web Mercator
        self.sr = arcpy.SpatialReference(3857)  # Web Mercator

        # Load the codebook
        #self.cb_path = os.path.join(self.prj_dirs["codebook"], "cb.json")
        #self.cb, self.df_cb = self.load_cb(silent = False)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Project directories ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def project_directories(self, silent: bool = False) -> dict:
        """
        Function to generate project directories for the OCGD data processing project.
        Args:
            silent (bool, optional): Whether to print the project directories. Defaults to False.
        Returns:
            directories (dict): A dictionary containing the project directories.
        Raises:
            None
        Example:
            >>> prj_dirs = project_directories("/path/to/project")
        Notes:
            The project_directories function is used to generate project directories for the OCGD data processing project.
        """
        # Define the project directories
        directories = {
            "root": self.base_path,
            "admin": os.path.join(self.base_path, "admin"),
            "analysis": os.path.join(self.base_path, "analysis"),
            "codebook": os.path.join(self.base_path, "codebook"),
            "data": os.path.join(self.base_path, "data"),
            "data_archived": os.path.join(self.base_path, "data", "archived"),
            "data_processed": os.path.join(self.base_path, "data", "processed"),
            "data_raw": os.path.join(self.base_path, "data", "raw"),
            "documentation": os.path.join(self.base_path, "documentation"),
            "gis": os.path.join(self.base_path, "gis"),
            "gis_archived": os.path.join(self.base_path, "gis", "archived"),
            "gis_layers": os.path.join(self.base_path, "gis", "layers"),
            "gis_layers_templates": os.path.join(self.base_path, "gis", "layers", "templates"),
            "gis_layouts": os.path.join(self.base_path, "gis", "layouts"),
            "gis_maps": os.path.join(self.base_path, "gis", "maps"),
            "gis_ocdc": os.path.join(self.base_path, "gis", "ocdc"),
            "gis_ocdc_aprx": os.path.join(self.base_path, "gis", "ocdc", "ocdc.aprx"),
            "gis_ocdc_gdb": os.path.join(self.base_path, "gis", "ocdc", "ocdc.gdb"),
            "gis_ocdc_sup_gdb": os.path.join(self.base_path, "gis", "ocdc_sup.gdb"),
            "gis_ocacs": os.path.join(self.base_path, "gis", "ocacs"),
            "gis_ocacs_aprx": os.path.join(self.base_path, "gis", "ocacs", "ocacs.aprx"),
            "gis_ocacs_gdb": os.path.join(self.base_path, "gis", "ocacs", "ocacs.gdb"),
            "gis_ocacs_sup_gdb": os.path.join(self.base_path, "gis", "ocacs_sup.gdb"),
            "gis_octl": os.path.join(self.base_path, "gis", "octl"),
            "gis_octl_aprx": os.path.join(self.base_path, "gis", "octl", "octl.aprx"),
            "gis_octl_gdb": os.path.join(self.base_path, "gis", "octl", "octl.gdb"),
            "gis_octl_sup_gdb": os.path.join(self.base_path, "gis", "octl_sup.gdb"),
            "gis_occr": os.path.join(self.base_path, "gis", "occr"),
            "gis_occr_aprx": os.path.join(self.base_path, "gis", "occr", "occr.aprx"),
            "gis_occr_gdb": os.path.join(self.base_path, "gis", "occr", "occr.gdb"),
            "gis_occr_sup_gdb": os.path.join(self.base_path, "gis", "occr_sup.gdb"),
            "graphics": os.path.join(self.base_path, "graphics"),
            "logs": os.path.join(self.base_path, "logs"),
            "metadata": os.path.join(self.base_path, "metadata"),
            "metadata_archived": os.path.join(self.base_path, "metadata", "archived"),
            "notebooks": os.path.join(self.base_path, "notebooks"),
            "notebooks_archived": os.path.join(self.base_path, "notebooks", "archived"),
            "scripts": os.path.join(self.base_path, "scripts"),
            "scripts_archived": os.path.join(self.base_path, "scripts", "archived"),
            "tests": os.path.join(self.base_path, "tests")
        }

        # Print the project directories
        if not silent:
            print("Project Directories:")
            for key, value in directories.items():
                print(f"- {key}: {value}")

        # Return the project directories
        return directories


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Get available census years ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    def get_census_years(self, dataset: str = "acs5") -> list[int]:
        """
        Get the available years for ACS5 data from the Census API.
        Args:
            None
        Returns:
            years (list): A list of available years for ACS5 data.
        Raises:
            None
        Example:
            >>> years = get_available_acs5_years()
        Notes:
            This function gets the available years for ACS5 data from the Census API.
        """
        # The discovery API lists all available endpoints
        url = "https://api.census.gov/data.json"
        response = requests.get(url, timeout = 20)
        datasets = response.json()['dataset']
        
        # Filter for acs5 endpoints
        years = []
        for ds in datasets:
            # We look for the specific acs5 path in the distribution links
            if dataset in ds.get("c_dataset", ""):
                # Extract the year from the identifier or title
                # Example identifier: "https://api.census.gov/data/2022/acs/acs5"
                year = ds.get("c_vintage")
                if year and year >= 2010:
                    years.append(year)
        
        # Return sorted unique years
        return sorted(list(set(years)))



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Load ArcGIS Pro Project ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_aprx(self, aprx_path: str, gdb_path: str, add_to_map: bool = False) -> tuple:
        """
        Loads an ArcGIS Pro project and sets the workspace to the geodatabase.
        Args:
            aprx_path (str): Path to the ArcGIS Pro project.
            gdb_path (str): Path to the geodatabase.
            add_to_map (bool): Whether to add outputs to the map.
        Raises:
            FileNotFoundError: If the ArcGIS Pro project or geodatabase does not exist.
            ValueError: If the ArcGIS Pro project or geodatabase path is invalid.
        Examples:
            >>> aprx, workspace = load_aprx(aprx_path, gdb_path, add_to_map=True)
        Returns:
            tuple: A tuple containing the ArcGIS Pro project object and the workspace.
        Notes:
            - The ArcGIS Pro project will be closed before loading.
            - The workspace will be set to the geodatabase path.
            - The ArcGIS Pro project will be closed after loading.
        """
        # ArcGIS Pro Project object
        aprx = arcpy.mp.ArcGISProject(aprx_path)
        # Current ArcGIS workspace (arcpy)
        arcpy.env.workspace = gdb_path
        workspace = arcpy.env.workspace
        # Enable overwriting existing outputs
        arcpy.env.overwriteOutput = True
        # Disable adding outputs to map
        arcpy.env.addOutputsToMap = add_to_map
        return aprx, workspace


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Crawl TIGERweb REST API ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def crawl_tigerweb(self, export: bool = False) -> dict:
        """
        Function to crawl the TIGERweb REST API and create a full inventory of services and layers.
        Args:
            export (bool, optional): Whether to export the inventory to a JSON file. Defaults to False.
        Returns
            inventory (dict): A dictionary containing the full inventory of TIGERweb services and layers.
        Raises:
            None
        Example:
            >>> inventory = crawl_tigerweb(export=True)
        Notes:
            The crawl_tigerweb function retrieves the full inventory of TIGERweb services and layers from the Census REST API.
        """

        # Set the base REST API URL for TIGERweb services
        base_rest = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb"
        base_params = {"f": "json"}

        # Initialize the inventory dictionary
        inventory = {"series": {}, "standalone": {}}

        exclusion_list = ["Labels", "Tribal", "Estates", "Subbarrios", "Alaska", "American Indian", "Off-Reservation", "Hawaiian", "Census Divisions", "Census Regions", "New England", "States", "Oklahoma", "Voting Districts"]

        # Get the base REST services
        base_response = requests.get(base_rest, params = base_params, timeout = 30)
        base_response.raise_for_status()
        base_data = base_response.json()
        # only keep services that contain "TIGERweb/tigerWMS_" in the name
        base_data = [service for service in base_data.get("services", []) if "TIGERweb/tigerWMS_" in service["name"]]

        for service in base_data:
            service_name = service["name"].replace("TIGERweb/tigerWMS_", "")
            service_type = service["type"]

            # if the last four characters of service_name are digits:
            if re.search(r'\d{4}$', service_name):                
                # Get the unique names without the year
                # category = "series"
                category_name = re.sub(r'\d{4}$', '', service_name)
                category_year = re.search(r'\d{4}$', service_name).group()

                print(f"\nSeries Service: {category_name}, Year: {category_year} ({service_type})")

                # Get the service REST URL and parameters
                service_rest = f"{base_rest}/tigerWMS_{service_name}/{service_type}"
                service_param = {"f": "pjson"}

                # Add to the inventory dictionary
                if category_name not in inventory["series"]:
                    inventory["series"][category_name] = {}
                if category_year not in inventory["series"][category_name]:
                    inventory["series"][category_name][category_year] = {
                        "rest": service_rest,
                        "name": service_name,
                        "type": service_type
                    }

                # Get the service details
                service_response = requests.get(service_rest, params = service_param, timeout = 30)
                service_response.raise_for_status()
                service_data = service_response.json()

                # Update the inventory with service details
                inventory["series"][category_name][category_year].update({
                    "currentVersion": service_data.get("currentVersion"),
                    "cimVersion": service_data.get("cimVersion"),
                    "mapName": service_data.get("mapName"),
                    "description": service_data.get("description"),
                    "spatialReference": service_data.get("spatialReference", {}).get("latestWkid", None),
                })

                # Get the layers for the service
                if "layers" in service_data:
                    inventory["series"][category_name][category_year]["layers"] = {}

                    # Iterate through each layer in the service
                    for layer in service_data.get("layers", []):
                        if layer.get("type") != "Feature Layer":
                            continue
                        # If the layer["name"] contains any of the exclusion terms, skip it
                        if any(exclusion in layer["name"] for exclusion in exclusion_list):
                            continue

                        layer_type = layer["type"]
                        layer_id = layer["id"]
                        layer_name = layer["name"]
                        layer_label = f"{layer_name} ({layer_id})"
                        print(f"- {layer_type}: {layer_name} (ID: {layer_id})")

                        # Get the layer REST URL and parameters
                        layer_rest = f"{base_rest}//tigerWMS_{service_name}/{service_type}/{layer_id}"
                        layer_param = {"f": "pjson"}

                        # Get the layer details
                        layer_response = requests.get(layer_rest, params = layer_param, timeout = 30)
                        layer_response.raise_for_status()
                        layer_data = layer_response.json()
                        layer_id = layer_data["id"]
                        layer_type = layer_data["type"]
                        layer_name = layer_data["name"]
                        layer_description = layer_data["description"]
                        layer_version = layer_data["currentVersion"]
                        layer_cim_version = layer_data["cimVersion"]
                        layer_geometry = layer_data["geometryType"]
                        layer_fields = [f["name"] for f in layer_data["fields"]]
                        # If both "STATE" and "COUNTY" are not in layer_fields set gp_method to "query", else if only "STATE" is in layer_fields set gp_method to "spatial with query", else set gp_method to "spatial only"
                        if "STATE" in layer_fields and "COUNTY" in layer_fields:
                            gp_method = "query"
                        elif "STATE" in layer_fields:
                            gp_method = "spatial with query"
                        else:
                            gp_method = "spatial only"

                        # Update the inventory with layer details
                        inventory["series"][category_name][category_year]["layers"][layer_label] = {
                            "rest": layer_rest,
                            "id": layer_id,
                            "name": layer_name,
                            "type": layer_type,
                            "description": layer_description,
                            "currentVersion": layer_version,
                            "cimVersion": layer_cim_version,
                            "geometryType": layer_geometry,
                            "gp_method": gp_method,
                            "fields": layer_fields
                        }

            else:
                category_name = service_name

                print(f"\nStandalone Service: {category_name} ({service_type})")

                # Get the service REST URL and parameters
                service_rest = f"{base_rest}/tigerWMS_{service_name}/{service_type}"
                service_param = {"f": "pjson"}

                if category_name not in inventory["standalone"]:
                    inventory["standalone"][category_name] = {
                        "rest": service_rest,
                        "name": service_name,
                        "type": service_type
                    }

                # Get the service details
                service_response = requests.get(service_rest, params = service_param, timeout = 30)
                service_response.raise_for_status()
                service_data = service_response.json()

                # Update the inventory with service details
                inventory["standalone"][category_name].update({
                    "currentVersion": service_data.get("currentVersion"),
                    "cimVersion": service_data.get("cimVersion"),
                    "mapName": service_data.get("mapName"),
                    "description": service_data.get("description"),
                    "spatialReference": service_data.get("spatialReference", {}).get("latestWkid", None),
                })

                # Get the layers for the service
                if "layers" in service_data:
                    inventory["standalone"][category_name]["layers"] = {}

                    # Iterate through each layer in the service
                    for layer in service_data.get("layers", []):
                        if layer.get("type") != "Feature Layer":
                            continue

                        # If the layer["name"] contains any of the exclusion terms, skip it
                        if any(exclusion in layer["name"] for exclusion in exclusion_list):
                            continue

                        layer_type = layer["type"]
                        layer_id = layer["id"]
                        layer_name = layer["name"]
                        layer_label = f"{layer_name} ({layer_id})"
                        print(f"- {layer_type}: {layer_name} (ID: {layer_id})")

                        # Get the layer REST URL and parameters
                        layer_rest = f"{base_rest}//tigerWMS_{service_name}/{service_type}/{layer_id}"
                        layer_param = {"f": "pjson"}

                        # Get the layer details
                        layer_response = requests.get(layer_rest, params = layer_param, timeout = 30)
                        layer_response.raise_for_status()
                        layer_data = layer_response.json()
                        layer_id = layer_data["id"]
                        layer_type = layer_data["type"]
                        layer_name = layer_data["name"]
                        layer_description = layer_data["description"]
                        layer_version = layer_data["currentVersion"]
                        layer_cim_version = layer_data["cimVersion"]
                        layer_geometry = layer_data["geometryType"]
                        layer_fields = [f["name"] for f in layer_data["fields"]]
                        # If both "STATE" and "COUNTY" are not in layer_fields set gp_method to "query", else if only "STATE" is in layer_fields set gp_method to "spatial with query", else set gp_method to "spatial only"
                        if "STATE" in layer_fields and "COUNTY" in layer_fields:
                            gp_method = "query"
                        elif "STATE" in layer_fields:
                            gp_method = "spatial with query"
                        else:
                            gp_method = "spatial only"

                        # Update the inventory with layer details
                        inventory["standalone"][category_name]["layers"][layer_label] = {
                            "rest": layer_rest,
                            "id": layer_id,
                            "name": layer_name,
                            "type": layer_type,
                            "description": layer_description,
                            "currentVersion": layer_version,
                            "cimVersion": layer_cim_version,
                            "geometryType": layer_geometry,
                            "gp_method": gp_method,
                            "fields": layer_fields
                        }

        if export:
            # Export inventory to JSON file
            output_path = os.path.join(self.prj_dirs["codebook"], "octl_cb_twr.json")
            with open(output_path, "w", encoding = "utf-8") as f:
                json.dump(inventory, f, indent=4)
            print(f"Inventory exported to {output_path}")

        # Return the final inventory
        return inventory


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Get TIGERweb dictionary ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_tigerweb_dictionary(self, export: bool = False) -> dict:
        """
        Function to get the available TIGERweb services and their years from the Census REST API.
        Returns a dictionary with service names as keys and list of years as values.
        Args:
            export (bool, optional): Whether to export the dictionary to a JSON file. Defaults to False.
        Returns:
            twr_cb (dict): A dictionary containing the TIGERweb services and their years.
        Raises:
            None
        Example:
            >>> tigerweb_dict = get_tigerweb_dictionary(export=True)
        Notes:
            The get_tigerweb_dictionary function retrieves the available TIGERweb services and their years from the Census REST API.
        """
        # Initialize the dictionary
        twr_dict = dict()

        # The base REST API URL for TIGERweb services
        twr_base = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb"

        codes = {
            "Public Use Microdata Areas": "PU",
            "ZIP Code Tabulation Areas": "ZC",
            "Zip Code Tabulation Areas": "ZC",
            "Tracts": "TR",
            "Block Groups": "BG",
            "Blocks": "BL",
            "Unified School Districts": "SU",
            "Secondary School Districts": "SS",
            "Elementary School Districts": "SE",
            "County Subdivisions": "CS",
            "Consolidated Cities": "CC",
            "Incorporated Places": "CP",
            "Designated Places": "DP",
            "Congressional Districts": "CD",
            "State Legislative Districts - Upper": "LU",
            "State Legislative Districts - Lower": "LL",
            "Urban Areas": "UA",
            "Urban Clusters": "UC",
            "Urban Growth Areas": "UG",
            "Urbanized Areas": "UR",
            "Combined Statistical Areas": "CA",
            "Metropolitan Divisions": "MD",
            "Metropolitan Statistical Areas": "MS",
            "Counties": "CO",
            "Economic Places": "EP",
            "Traffic Analysis Zones": "TZ",
            "Traffic Analysis Districts": "TD"
        }        
        
        # Get the response from the base URL
        response = requests.get(twr_base, timeout = 20)
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            return {}

        # Get the content of the URL
        content = response.text

        # Clean the content
        # Remove all html tags including script and style tags, and '&nbsp', '&qt'
        content = re.sub(r'<[^>]*>', '', content)
        content = re.sub(r'&nbsp;', ' ', content)
        content = re.sub(r'&qt;', ' ', content)
        # If lines contain "TIGERweb", keep them, otherwise remove them
        search_content = "TIGERweb/tigerWMS_"
        # Split the content into lines
        lines = content.splitlines()
        # Filter lines that contain the search content
        lines = [line for line in lines if search_content in line]
        # Get the content of each line after the last occurrence of the search content
        lines = [line.split(search_content)[-1].strip() for line in lines]
        # Remove " (MapServer)" till the end of the line
        lines = [re.sub(r' \(MapServer\).*', '', line) for line in lines]
        # the text in lines have a year at the end in their string, get only these lines
        lines = [line for line in lines if re.search(r'\d{4}$', line)]
        # Split the lines into two parts: before the year and the year
        lines = [re.match(r'^(.*?)(\d{4})$', line).groups() for line in lines]

        # for each unique first part, get the list of years
        unique_lines = {}
        for line in lines:
            if line[0] not in unique_lines:
                unique_lines[line[0]] = []
            unique_lines[line[0]].append(int(line[1]))

        # Process the ACS Services from the unique lines
        if "ACS" in unique_lines:
            twr_dict["acs"] = {}
            acs_years = unique_lines["ACS"]

            # For each year, get the layers from the REST API
            for year in acs_years:
                base_url = f"{twr_base}/tigerWMS_ACS{year}/MapServer"
                response = requests.get(base_url, timeout = 20)
                if response.status_code != 200:
                    print(f"Error fetching data for ACS {year}: {response.status_code}")
                    continue
                # Get the content of the URL
                content = response.text
                # Remove all html tags including script and style tags, and '&nbsp', '&qt'
                content = re.sub(r'<[^>]*>', '', content)
                content = re.sub(r'&nbsp;', ' ', content)
                content = re.sub(r'&qt;', ' ', content)
                # Only keep the section of the content that lists the layers (between "Layers:" and "Description:")
                layer_section = re.search(r'Layers:(.*?)Description:', content, re.DOTALL)
                if layer_section:
                    layer_section = layer_section.group(1)
                    # Remove empty lines
                    layer_section = os.linesep.join([s for s in layer_section.splitlines() if s.strip()])
                    # Split the content into lines
                    lines = layer_section.splitlines()
                    # Each line has the layer name followed by space and then the layer ID in parenthesis (a number). Split them.
                    lines = [re.match(r'^(.*?)[\s]+\((\d+)\)$', line.strip()).groups() for line in lines]

                    # Create a dictionary of layer names and their IDs and codes
                    layer_dict = {}
                    for lyr_name, lyr_id in lines:
                        line_code = None
                        for code_key, code_val in codes.items():
                            if code_key in lyr_name:
                                line_code = code_val
                                line_alias = code_key
                                break
                        layer_dict[lyr_name] = {
                            "code": line_code,
                            "alias": line_alias,
                            "rest": base_url + f"/{lyr_id}"
                        }

                # Add to the tigerweb dictionary
                twr_dict["acs"][str(year)] = {
                    "rest": base_url,
                    "layers": layer_dict
                }
                
        # Process the Census Services from the unique lines
        if "Census" in unique_lines:
            twr_dict["census"] = {}
            census_years = unique_lines["Census"]

            # For each year, get the layers from the REST API
            for year in census_years:
                base_url = f"{twr_base}/tigerWMS_Census{year}/MapServer"
                response = requests.get(base_url, timeout = 20)
                if response.status_code != 200:
                    print(f"Error fetching data for ACS {year}: {response.status_code}")
                    continue
                # Get the content of the URL
                content = response.text
                # Remove all html tags including script and style tags, and '&nbsp', '&qt'
                content = re.sub(r'<[^>]*>', '', content)
                content = re.sub(r'&nbsp;', ' ', content)
                content = re.sub(r'&qt;', ' ', content)
                # Only keep the section of the content that lists the layers (between "Layers:" and "Description:")
                layer_section = re.search(r'Layers:(.*?)Description:', content, re.DOTALL)
                if layer_section:
                    layer_section = layer_section.group(1)
                    # Remove empty lines
                    layer_section = os.linesep.join([s for s in layer_section.splitlines() if s.strip()])
                    # Split the content into lines
                    lines = layer_section.splitlines()
                    # Each line has the layer name followed by space and then the layer ID in parenthesis (a number). Split them.
                    lines = [re.match(r'^(.*?)[\s]+\((\d+)\)$', line.strip()).groups() for line in lines]

                    # Create a dictionary of layer names and their IDs and codes
                    layer_dict = {}
                    for lyr_name, lyr_id in lines:
                        line_code = None
                        for code_key, code_val in codes.items():
                            if code_key in lyr_name:
                                line_code = code_val
                                line_alias = code_key
                                break
                        layer_dict[lyr_name] = {
                            "code": line_code,
                            "alias": line_alias,
                            "rest": base_url + f"/{lyr_id}"
                        }
                
                # Add to the tigerweb dictionary
                twr_dict["census"][str(year)] = {
                    "rest": base_url,
                    "layers": layer_dict
                }

        # Process the ECON Services from the unique lines
        if "ECON" in unique_lines:
            twr_dict["econ"] = {}
            econ_years = unique_lines["ECON"]

            # For each year, get the layers from the REST API
            for year in econ_years:
                base_url = f"{twr_base}/tigerWMS_ECON{year}/MapServer"
                response = requests.get(base_url, timeout = 20)
                if response.status_code != 200:
                    print(f"Error fetching data for ACS {year}: {response.status_code}")
                    continue
                # Get the content of the URL
                content = response.text
                # Remove all html tags including script and style tags, and '&nbsp', '&qt'
                content = re.sub(r'<[^>]*>', '', content)
                content = re.sub(r'&nbsp;', ' ', content)
                content = re.sub(r'&qt;', ' ', content)
                # Only keep the section of the content that lists the layers (between "Layers:" and "Description:")
                layer_section = re.search(r'Layers:(.*?)Description:', content, re.DOTALL)
                if layer_section:
                    layer_section = layer_section.group(1)
                    # Remove empty lines
                    layer_section = os.linesep.join([s for s in layer_section.splitlines() if s.strip()])
                    # Split the content into lines
                    lines = layer_section.splitlines()
                    # Each line has the layer name followed by space and then the layer ID in parenthesis (a number). Split them.
                    lines = [re.match(r'^(.*?)[\s]+\((\d+)\)$', line.strip()).groups() for line in lines]

                    # Create a dictionary of layer names and their IDs and codes
                    layer_dict = {}
                    for lyr_name, lyr_id in lines:
                        line_code = None
                        for code_key, code_val in codes.items():
                            if code_key in lyr_name:
                                line_code = code_val
                                line_alias = code_key
                                break
                        layer_dict[lyr_name] = {
                            "code": line_code,
                            "alias": line_alias,
                            "rest": base_url + f"/{lyr_id}"
                        }

                # Add to the tigerweb dictionary
                twr_dict["econ"][str(year)] = {
                    "rest": base_url,
                    "layers": layer_dict
                }

        # Define a list of included labels
        included_labels = ['Census Block Groups', 'Census Blocks', 'Census Designated Places', 'Census Public Use Microdata Areas', 'Census Tracts', 'Census Urbanized Areas', 'Census ZIP Code Tabulation Areas', 'Combined Statistical Areas', 'Congressional Districts', 'Consolidated Cities', 'Counties', 'County Subdivisions', 'Economic Places', 'Elementary School Districts', 'Incorporated Places', 'Metropolitan Divisions', 'Metropolitan Statistical Areas', 'Public Use Microdata Areas', 'Secondary School Districts', 'State Legislative Districts - Lower', 'State Legislative Districts - Upper', 'Traffic Analysis Districts', 'Traffic Analysis Zones', 'Unified School Districts', 'Urban Areas', 'Urban Clusters', 'Urban Growth Areas', 'Urbanized Areas', 'ZIP Code Tabulation Areas', 'Zip Code Tabulation Areas']

        # Create a new dictionary to hold the filtered layers
        twr_cb = twr_dict.copy()
        for level, content in twr_dict.items():
            print(f"Level: {level}")
            for year, value in content.items():
                layers_to_remove = []
                print(f"- Year: {year}, Original Count: {len(value['layers'])}")
                for layer_name in value["layers"]:
                    if layer_name.endswith("Labels"):
                        layers_to_remove.append(layer_name)
                        continue
                    if layer_name.startswith("Tribal"):
                        layers_to_remove.append(layer_name)
                        continue
                    # if any of the included labels is a part of the layer name, keep it
                    if not any(included_label in layer_name for included_label in included_labels):
                        layers_to_remove.append(layer_name)
                for lyr in layers_to_remove:
                    print(f" - Removing layer: {lyr}")
                    del twr_cb[level][year]["layers"][lyr]

        # Write the main REST API URL (twr_base) to the dictionary
        twr_cb["main"] = twr_base

        # Export the dictionary to a JSON file if export is True
        if export:
            # Export the dictionary to a JSON file in the scratch directory
            out_path = os.path.join(self.prj_dirs["codebook"], "ocgd_twr_cb.json")
            with open(out_path, "w", encoding = "utf-8") as f:
                json.dump(twr_cb, f, indent = 4)
            print(f"Tigerweb dictionary exported to {out_path}")

        # Return the dictionary
        return twr_cb

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Create GDB from TIGERweb REST API ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_gdb_from_twr(self, year: int, level: str = "acs", out_gdb: str = None):
        """
        Create a file geodatabase from the TIGERweb REST API layers for a specified level and year.
        Args:
            year (int): The year of the TIGERweb data to use.
            level (str, optional): The level of TIGERweb data to use. Defaults to "acs".
            out_gdb (str, optional): The output geodatabase path. If None, a scratch geodatabase will be created. Defaults to None.
        Returns:
            None
        Raises:
            None
        Example:
            >>> create_gdb_from_twr(year=2022, level="acs", out_gdb="path/to/output.gdb")
        Notes:
            The create_gdb_from_twr function creates a file geodatabase from the TIGERweb REST API layers for a specified level and year.
        """

        # If out_gdb is None, create a scratch geodatabase
        if out_gdb is None:
            out_gdb = self.scratch_gdb()

        # Set the arcpy environment to the output geodatabase
        arcpy.env.workspace = out_gdb
        arcpy.env.overwriteOutput = True

        # Get the TIGERweb dictionary
        print("Updating TIGERweb dictionary...")
        cb = self.get_tigerweb_dictionary(export = False)

        # Validate level and year
        # If the level is not "main"
        if level != "main":
            print(f"Validating level: {level} and year: {year}")
            # Check if the level exists in the TIGERweb dictionary
            if level in cb:
                level_years = [int(y) for y in cb[level]]
                # If the year is between the min and max of level_years, find the closest year. If the year is greater than min and less than max, if it is not in level_years, use the nearest year available.
                if year < min(level_years):
                    print(f"Year {year} is less than the minimum available year for level '{level}'. Using minimum year {min(level_years)}.")
                    year = min(level_years)
                elif year > max(level_years):
                    print(f"Year {year} is greater than the maximum available year for level '{level}'. Using maximum year {max(level_years)}.")
                    year = max(level_years)
                elif year not in level_years:
                    closest_year = min(level_years, key=lambda x: abs(x - year))
                    print(f"Year {year} is not available for level '{level}'. Using closest available year {closest_year}.")
                    year = closest_year
                else:
                    print(f"Year {year} is available for level '{level}'.")
            else:
                print(f"Level '{level}' is not available in the TIGERweb dictionary.")
                return None
        else:
            print(f"Level 'main' selected.\nMain TIGERweb REST API URL: {cb['main']}.\nExiting function.")
            return None
            
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
            query = "STATE = '06' AND COUNTY = '059'"  # Orange County, CA

            # Ensure output GDB exists
            if not arcpy.Exists(out_gdb):
                folder = os.path.dirname(out_gdb)
                gdb_name = os.path.basename(out_gdb)
                arcpy.CreateFileGDB_management(folder, gdb_name)

            # Temporary layer name
            temp_layer = "temp_layer"

            try:
                print("- Using direct_query method")
                # Create a feature layer from the REST service, applying the query where-clause
                arcpy.MakeFeatureLayer_management(layer_rest, temp_layer, query)

                # Get the spatial reference of the temporary layer
                print("- Checking spatial reference")
                temp_sr = arcpy.Describe(temp_layer).spatialReference

                # Check if the spatial reference is the desired output spatial reference
                if temp_sr.factoryCode != self.sr.factoryCode:
                    print("- Projecting to desired spatial reference (Web Mercator, WKID 3857)")
                    # Project the layer to the desired spatial reference
                    projected_temp = "projected_temp_layer"
                    arcpy.Project_management(temp_layer, projected_temp, self.sr)
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
            except (OSError, requests.RequestException, RuntimeError) as e:
                print(f"- Python Error: {e}")
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
                query = "STATE = '06' AND COUNTY = '059'"
                print(f"- Using {method} method")
                try:
                    # Create a feature layer from the REST service, applying the query where-clause
                    print("- Creating feature layer with query")
                    arcpy.MakeFeatureLayer_management(layer_rest, temp_layer, query)

                    # Get the spatial reference of the temporary layer
                    print("- Checking spatial reference")
                    temp_sr = arcpy.Describe(temp_layer).spatialReference

                    # Check if the spatial reference is the desired output spatial reference
                    if temp_sr.factoryCode != self.sr.factoryCode:
                        print("- Projecting to desired spatial reference (Web Mercator, WKID 3857)")
                        # Project the layer to the desired spatial reference
                        projected_temp = "projected_temp_layer"
                        arcpy.Project_management(temp_layer, projected_temp, self.sr)
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
                except (OSError, requests.RequestException, RuntimeError) as e:
                    print(f"Python Error: {e}")
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
                    query = "STATE = '06'"

                    # Create a feature layer from the REST service, applying the query where-clause
                    print("- Creating feature layer with query")
                    arcpy.MakeFeatureLayer_management(layer_rest, temp_layer, query)
                else:
                    # Create a feature layer from the REST service without a where-clause
                    print("- Creating feature layer without query")
                    arcpy.MakeFeatureLayer_management(layer_rest, temp_layer)

                # Get the spatial reference of the temporary layer
                print("- Checking spatial reference")
                temp_sr = arcpy.Describe(temp_layer).spatialReference

                # Check if the spatial reference is the desired output spatial reference
                if temp_sr.factoryCode != self.sr.factoryCode:
                    print("- Projecting to desired spatial reference (Web Mercator, WKID 3857)")
                    # Project the layer to the desired spatial reference
                    projected_temp = "projected_temp_layer"
                    arcpy.Project_management(temp_layer, projected_temp, self.sr)
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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the OCTL main class ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OCTL(OCGD):
    """Class Containing the Orange County Tiger/Line (OCTL) Processing Workflow Functions.

    This class encapsulates the workflow for processing Orange County Tiger Lines (OCTL)
    data. It includes methods for initialization, main execution, and retrieving
    metadata for various feature classes.
    """
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Class initialization ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, part: int = 0, version: float = float(datetime.datetime.now().year)):
        """
        Initialize the OCTL class.
        """
        # Initialize the OCgdm class with provided part/version
        super().__init__(part, version)

        # Create a prj_meta variable calling the project_metadata function
        self.prj_meta = self.project_metadata(silent = False)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Get remote path ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_remote_path(self, label_name: str) -> str | None:
        """
        Get the remote path based on the drive label name.
        Args:
            label_name (str): The label name of the drive to search for.
        Returns:
            str | None: The remote path if found, otherwise None.
        Raises:
            ValueError: If label_name is not a string.
        Example:
            >>> remote_path = get_remote_path("DRKWD02")
        Notes:
            This function uses the WMI library to query the system's logical disks
            and find the drive with the specified label name. If found, it constructs
            and returns the remote path; otherwise, it returns None.
        """
        # Validate input
        if not isinstance(label_name, str):
            raise ValueError("label_name must be a string")
        # Query WMI for logical disks
        c = wmi.WMI()
        # Iterate through logical disks to find the one with the specified label
        for drive in c.Win32_LogicalDisk():
            # VolumeName is the disk label (e.g., "Backup", "USB_DRIVE")
            if drive.VolumeName == label_name:
                # Returns network path or drive letter
                drive_letter = drive.ProviderName if drive.ProviderName else drive.DeviceID
                # Construct the remote path
                remote_path = f"{drive_letter}\\Professional\\OCPW Projects\\ocgd\\octl\\tl_raw"
                # Return the remote path
                return remote_path
        # If no drive is found, return None
        return None


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Print arcpy messages ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def arcpy_messages(self, text = None) -> None:
        """Print arcpy messages."""
        for message in arcpy.GetMessages().splitlines():
            if text:
                print(f"{text} {message}")
            else:
                print(message)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Project metadata ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def project_metadata(self, silent: bool = False) -> dict:
        """
        Function to generate project metadata for the OCTL data processing object.
        Args:
            silent (bool): If True, suppresses the print output. Default is False.
        Returns:
            metadata (dict): A dictionary containing the project metadata. The dictionary includes: name, title, description, version, author, years, date_start, date_end, date_updated, and TIMS metadata.
        Raises:
            ValueError: If part is not an integer, or if version is not numeric.
        Example:
            >>> metadata = self.project_metadata()
        Notes:
            This function generates a dictionary with project metadata based on the provided part and version.
            The function also checks if the TIMS metadata file exists and raises an error if it does not.
        """
        
        # Match the part to a specific step and description (with default case)
        match self.part:
            case 0:
                step = "Part 0: General Data Updating"
                desc = "General Data Updating and Mentenance"
            case 1:
                step = "Part 1: Raw Data Processing"
                desc = "Processing Raw Tiger/Line Shapefiles Folder"
            case 2:
                step = "Part 2: Part 2: ArcGis Pro Project Map Processing"
                desc = "Initialize the ArcGIS Pro Project with Maps and Layers, and process map layers from the TL Geodatabases"
            case 3:
                step = "Part 3: Sharing and Publishing Feature Classes"
                desc = "Sharing and Publishing Feature Classes to ArcGIS Online"
            case _:
                step = "Part 0: General Data Updating"
                desc = "General Data Updating and Maintenance (default)"
        
        # Create a dictionary to hold the metadata
        metadata = {
            "name": "OCTL Tiger/Line Data Processing",
            "title": step,
            "description": desc,
            "version": self.version,
            "date": self.data_date,
            "author": "Dr. Kostas Alexandridis, GISP",
            "years": "",
        }

        # If not silent, print the metadata
        if not silent:
            print(
                f"\nProject Metadata:\n- Name: {metadata['name']}\n- Title: {metadata['title']}\n- Description: {metadata['description']}\n- Version: {metadata['version']}\n- Author: {metadata['author']}"
            )
        
        # Return the metadata
        return metadata


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Codebook metadata ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def codebook_metadata(self, year: int, layers_metadata: dict) -> dict:
        """
        Create a codebook dictionary for geographic layers based on provided metadata.
        Parameters:
            layers_metadata (dict): A dictionary containing metadata for each geographic layer.
        Returns:
            dict: A codebook dictionary with detailed information for each layer.
        Raises:
            None
        Example:
            >>> codebook = self.codebook_metadata(layers_metadata)
            >>> print(codebook)
        Note:
            This function assumes that the input dictionary contains all necessary keys for each layer.
        """
        # Create standard entry values
        entry_gdb = f"tl{year}.gdb"
        entry_tags = "Orange County, California, OCTL, TigerLines"
        entry_credits = "Dr. Kostas Alexandridis, GISP, Data Scientist, OC Public Works, OC Survey Geospatial Services"
        entry_access = """The feed data and associated resources (maps, apps, endpoints) can be used under a <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">Creative Commons CC-SA-BY</a> License, providing attribution to OC Public Works, OC Survey Geospatial Services. <div><br /></div><div>We make every effort to provide the most accurate and up-to-date data and information. Nevertheless the data feed is provided, 'as is' and OC Public Work's standard <a href="https://www.ocgov.com/contact-county/disclaimer" target="_blank">Disclaimer</a> applies.</div><div><br /></div><div>For any inquiries, suggestions or questions, please contact:</div><div><br /></div><div style="text-align:center;"><a href="https://www.linkedin.com/in/ktalexan/" target="_blank"><b>Dr. Kostas Alexandridis, GISP</b></a><br /></div><div style="text-align:center;">GIS Analyst | Spatial Complex Systems Scientist</div><div style="text-align:center;">OC Public Works/OC Survey Geospatial Applications</div><div style="text-align:center;"><div>601 N. Ross Street, P.O. Box 4048, Santa Ana, CA 92701</div><div>Email: <a href="mailto:kostas.alexandridis@ocpw.ocgov.com" target="_blank">kostas.alexandridis@ocpw.ocgov.com</a> | Phone: (714) 967-0826</div></div>"""
        entry_uri = "https://ocpw.maps.arcgis.com/sharing/rest/content/items/67ce28a349d14451a55d0415947c7af3/data"
        
        # Create the codebook dictionary
        codebook = {
            "addr": {
                "type": layers_metadata["addr"]["type"],
                "file": layers_metadata["addr"]["file"],
                "scale": layers_metadata["addr"]["scale"],
                "spatial": layers_metadata["addr"]["spatial"],
                "abbrev": layers_metadata["addr"]["abbrev"],
                "postfix": layers_metadata["addr"]["postfix"],
                "postfix_desc": layers_metadata["addr"]["postfix_desc"],
                "alias": f"OCTL {year} Address Ranges",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Address Ranges Relationship File",
                "code": "AD",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Adress Ranges Relationship",
                "tags": f"{entry_tags}, Address, Relationships, Table",
                "summary": f"Orange County Tiger Lines {year} Address Ranges Relationship Table",
                "description": f"Orange County Tiger Lines {year} Address Ranges Relationship Table. This table contains address range information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
                },
            "addrfeat": {
                "type": layers_metadata["addrfeat"]["type"],
                "file": layers_metadata["addrfeat"]["file"],
                "scale": layers_metadata["addrfeat"]["scale"],
                "spatial": layers_metadata["addrfeat"]["spatial"],
                "abbrev": layers_metadata["addrfeat"]["abbrev"],
                "postfix": layers_metadata["addrfeat"]["postfix"],
                "postfix_desc": layers_metadata["addrfeat"]["postfix_desc"],
                "alias": f"OCTL {year} Address Range Features",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Address Range Feature Shapefile",
                "code": "AF",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Address Range Features",
                "tags": f"{entry_tags}, Address, Relationships, Table",
                "summary": f"Orange County Tiger Lines {year} Address Range Features",
                "description": f"Orange County Tiger Lines {year} Address Range Features. This shapefile contains address range feature information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "addrfn": {
                "type": layers_metadata["addrfn"]["type"],
                "file": layers_metadata["addrfn"]["file"],
                "scale": layers_metadata["addrfn"]["scale"],
                "spatial": layers_metadata["addrfn"]["spatial"],
                "abbrev": layers_metadata["addrfn"]["abbrev"],
                "postfix": layers_metadata["addrfn"]["postfix"],
                "postfix_desc": layers_metadata["addrfn"]["postfix_desc"],
                "alias": f"OCTL {year} Address Range Feature Names",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Address Range-Feature Name Relationship File",
                "code": "AN",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Address Range-Feature Name Relationship",
                "tags": f"{entry_tags}, Address, Relationships, Table",
                "summary": f"Orange County Tiger Lines {year} Address Range-Feature Name Relationship Table",
                "description": f"Orange County Tiger Lines {year} Address Range-Feature Name Relationship Table. This table contains address range-feature name information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "arealm": {
                "type": layers_metadata["arealm"]["type"],
                "file": layers_metadata["arealm"]["file"],
                "scale": layers_metadata["arealm"]["scale"],
                "spatial": layers_metadata["arealm"]["spatial"],
                "abbrev": layers_metadata["arealm"]["abbrev"],
                "postfix": layers_metadata["arealm"]["postfix"],
                "postfix_desc": layers_metadata["arealm"]["postfix_desc"],
                "alias": f"OCTL {year} Area Landmarks",
                "group": "Features",
                "category": "Landmarks",
                "label": "Area Landmarks",
                "code": "LA",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Area Landmarks",
                "tags": f"{entry_tags}, Area, Landmarks, Features",
                "summary": f"Orange County Tiger Lines {year} Area Landmarks",
                "description": f"Orange County Tiger Lines {year} Area Landmarks. This shapefile contains area landmark feature information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "areawater": {
                "type": layers_metadata["areawater"]["type"],
                "file": layers_metadata["areawater"]["file"],
                "scale": layers_metadata["areawater"]["scale"],
                "spatial": layers_metadata["areawater"]["spatial"],
                "abbrev": layers_metadata["areawater"]["abbrev"],
                "postfix": layers_metadata["areawater"]["postfix"],
                "postfix_desc": layers_metadata["areawater"]["postfix_desc"],
                "alias": f"OCTL {year} Area Hydrography",
                "group": "Features",
                "category": "Water",
                "label": "Area Hydrography",
                "code": "WA",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Area Hydrography",
                "tags": f"{entry_tags}, Water, Hydrography, Features",
                "summary": f"Orange County Tiger Lines {year} Area Hydrography",
                "description": f"Orange County Tiger Lines {year} Area Hydrography. This shapefile contains area hydrography feature information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "bg": {
                "type": layers_metadata["bg"]["type"],
                "file": layers_metadata["bg"]["file"],
                "scale": layers_metadata["bg"]["scale"],
                "spatial": layers_metadata["bg"]["spatial"],
                "abbrev": layers_metadata["bg"]["abbrev"],
                "postfix": layers_metadata["bg"]["postfix"],
                "postfix_desc": layers_metadata["bg"]["postfix_desc"],
                "alias": f"OCTL {year} Block Groups",
                "group": "Geographic Areas",
                "category": "Block Groups",
                "label": "Block Group",
                "code": "BG",
                "method": "query",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Block Groups",
                "tags": f"{entry_tags}, US Census, Block Groups",
                "summary": f"Orange County Tiger Lines {year} Block Groups",
                "description": f"Orange County Tiger Lines {year} Block Groups. This shapefile contains block group geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "cbsa": {
                "type": layers_metadata["cbsa"]["type"],
                "file": layers_metadata["cbsa"]["file"],
                "scale": layers_metadata["cbsa"]["scale"],
                "spatial": layers_metadata["cbsa"]["spatial"],
                "abbrev": layers_metadata["cbsa"]["abbrev"],
                "postfix": layers_metadata["cbsa"]["postfix"],
                "postfix_desc": layers_metadata["cbsa"]["postfix_desc"],
                "alias": f"OCTL {year} Metropolitan Statistical Areas",
                "group": "Geographic Areas",
                "category": "Core Based Statistical Areas",
                "label": "Metropolitan/Micropolitan Statistical Area",
                "code": "SM",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Metropolitan Statistical Areas",
                "tags": f"{entry_tags}, US Census, Metropolitan Statistical Areas",
                "summary": f"Orange County Tiger Lines {year} Metropolitan Statistical Areas",
                "description": f"Orange County Tiger Lines {year} Metropolitan Statistical Areas. This shapefile contains metropolitan statistical area geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "coastline": {
                "type": layers_metadata["coastline"]["type"],
                "file": layers_metadata["coastline"]["file"],
                "scale": layers_metadata["coastline"]["scale"],
                "spatial": layers_metadata["coastline"]["spatial"],
                "abbrev": layers_metadata["coastline"]["abbrev"],
                "postfix": layers_metadata["coastline"]["postfix"],
                "postfix_desc": layers_metadata["coastline"]["postfix_desc"],
                "alias": f"OCTL {year} Coastlines",
                "group": "Features",
                "category": "Coastlines",
                "label": "Coastline",
                "code": "CL",
                "method": "clip",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Coastlines",
                "tags": f"{entry_tags}, Coastlines",
                "summary": f"Orange County Tiger Lines {year} Coastlines",
                "description": f"Orange County Tiger Lines {year} Coastlines. This shapefile contains coastline geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "county": {
                "type": layers_metadata["county"]["type"],
                "file": layers_metadata["county"]["file"],
                "scale": layers_metadata["county"]["scale"],
                "spatial": layers_metadata["county"]["spatial"],
                "abbrev": layers_metadata["county"]["abbrev"],
                "postfix": layers_metadata["county"]["postfix"],
                "postfix_desc": layers_metadata["county"]["postfix_desc"],
                "alias": f"OCTL {year} Orange County",
                "group": "Geographic Areas",
                "category": "Counties",
                "label": "County and Equivalent",
                "code": "CO",
                "method": "query",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Orange County",
                "tags": f"{entry_tags}, Counties",
                "summary": f"Orange County Tiger Lines {year} Orange County",
                "description": f"Orange County Tiger Lines {year} Orange County. This shapefile contains county geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "csa": {
                "type": layers_metadata["csa"]["type"],
                "file": layers_metadata["csa"]["file"],
                "scale": layers_metadata["csa"]["scale"],
                "spatial": layers_metadata["csa"]["spatial"],
                "abbrev": layers_metadata["csa"]["abbrev"],
                "postfix": layers_metadata["csa"]["postfix"],
                "postfix_desc": layers_metadata["csa"]["postfix_desc"],
                "alias": f"OCTL {year} Combined Statistical Areas",
                "group": "Geographic Areas",
                "category": "Core Based Statistical Areas",
                "label": "Combined Statistical Area",
                "code": "SC",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Combined Statistical Areas",
                "tags": f"{entry_tags}, US Census, Statistical Areas",
                "summary": f"Orange County Tiger Lines {year} Combined Statistical Areas",
                "description": f"Orange County Tiger Lines {year} Combined Statistical Areas. This shapefile contains combined statistical area geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "cd": {
                "type": layers_metadata["cd"]["type"],
                "file": layers_metadata["cd"]["file"],
                "scale": layers_metadata["cd"]["scale"],
                "spatial": layers_metadata["cd"]["spatial"],
                "abbrev": layers_metadata["cd"]["abbrev"],
                "postfix": layers_metadata["cd"]["postfix"],
                "postfix_desc": layers_metadata["cd"]["postfix_desc"],
                "alias": f"OCTL {year} Congressional Districts",
                "group": "Geographic Areas",
                "category": "Congressional Districts",
                "label": f"Congressional Districts of the {layers_metadata["cd"]["postfix_desc"]}",
                "code": "CD",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Congressional Districts",
                "tags": f"{entry_tags}, Congressional Districts",
                "summary": f"Orange County Tiger Lines {year} Congressional Districts of the {layers_metadata["cd"]["postfix_desc"]}",
                "description": f"Orange County Tiger Lines {year} Congressional Districts of the {layers_metadata["cd"]["postfix_desc"]}. This shapefile contains congressional district geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "cousub": {
                "type": layers_metadata["cousub"]["type"],
                "file": layers_metadata["cousub"]["file"],
                "scale": layers_metadata["cousub"]["scale"],
                "spatial": layers_metadata["cousub"]["spatial"],
                "abbrev": layers_metadata["cousub"]["abbrev"],
                "postfix": layers_metadata["cousub"]["postfix"],
                "postfix_desc": layers_metadata["cousub"]["postfix_desc"],
                "alias": f"OCTL {year} County Subdivisions",
                "group": "Geographic Areas",
                "category": "County Subdivisions",
                "label": "County Subdivisions",
                "code": "CS",
                "method": "query",
                "gdb": entry_gdb,
                "title": f"OCTL {year} County Subdivisions",
                "tags": f"{entry_tags}, counties, subdivisions",
                "summary": f"Orange County Tiger Lines {year} County Subdivisions",
                "description": f"Orange County Tiger Lines {year} County Subdivisions. This shapefile contains county subdivision geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "edges": {
                "type": layers_metadata["edges"]["type"],
                "file": layers_metadata["edges"]["file"],
                "scale": layers_metadata["edges"]["scale"],
                "spatial": layers_metadata["edges"]["spatial"],
                "abbrev": layers_metadata["edges"]["abbrev"],
                "postfix": layers_metadata["edges"]["postfix"],
                "postfix_desc": layers_metadata["edges"]["postfix_desc"],
                "alias": f"OCTL {year} All Lines",
                "group": "Features",
                "category": "All Lines",
                "label": "All Lines",
                "code": "ED",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} All Lines",
                "tags": f"{entry_tags}, all lines",
                "summary": f"Orange County Tiger Lines {year} All Lines",
                "description": f"Orange County Tiger Lines {year} All Lines. This shapefile contains all line features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "elsd": {
                "type": layers_metadata["elsd"]["type"],
                "file": layers_metadata["elsd"]["file"],
                "scale": layers_metadata["elsd"]["scale"],
                "spatial": layers_metadata["elsd"]["spatial"],
                "abbrev": layers_metadata["elsd"]["abbrev"],
                "postfix": layers_metadata["elsd"]["postfix"],
                "postfix_desc": layers_metadata["elsd"]["postfix_desc"],
                "alias": f"OCTL {year} Elementary School Districts",
                "group": "Geographic Areas",
                "category": "School Districts",
                "label": "Elementary School Districts",
                "code": "SE",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Elementary School Districts",
                "tags": f"{entry_tags}, schools, school districts, elementary schools",
                "summary": f"Orange County Tiger Lines {year} Elementary School Districts",
                "description": f"Orange County Tiger Lines {year} Elementary School Districts. This shapefile contains elementary school district geographic area information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "facesmil": {
                "type": layers_metadata["facesmil"]["type"],
                "file": layers_metadata["facesmil"]["file"],
                "scale": layers_metadata["facesmil"]["scale"],
                "spatial": layers_metadata["facesmil"]["spatial"],
                "abbrev": layers_metadata["facesmil"]["abbrev"],
                "postfix": layers_metadata["facesmil"]["postfix"],
                "postfix_desc": layers_metadata["facesmil"]["postfix_desc"],
                "alias": f"OCTL {year} Topological Faces-Military Installations",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Topological Faces-Military Installations Relationship File",
                "code": "FM",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Topological Faces-Military Installations",
                "tags": f"{entry_tags}, military installations",
                "summary": f"Orange County Tiger Lines {year} Topological Faces-Military Installations Table",
                "description": f"Orange County Tiger Lines {year} Topological Faces-Military Installations. This shapefile contains topological faces and military installations relationship information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "faces": {
                "type": layers_metadata["faces"]["type"],
                "file": layers_metadata["faces"]["file"],
                "scale": layers_metadata["faces"]["scale"],
                "spatial": layers_metadata["faces"]["spatial"],
                "abbrev": layers_metadata["faces"]["abbrev"],
                "postfix": layers_metadata["faces"]["postfix"],
                "postfix_desc": layers_metadata["faces"]["postfix_desc"],
                "alias": f"OCTL {year} Topological Faces",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Topological Faces (Polygons with all Geocodes) Shapefile",
                "code": "FC",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Topological Faces",
                "tags": f"{entry_tags}, faces, relationships",
                "summary": f"Orange County Tiger Lines {year} Topological Faces",
                "description": f"Orange County Tiger Lines {year} Topological Faces. This shapefile contains topological faces (polygons with all geocodes) information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "facesah": {
                "type": layers_metadata["facesah"]["type"],
                "file": layers_metadata["facesah"]["file"],
                "scale": layers_metadata["facesah"]["scale"],
                "spatial": layers_metadata["facesah"]["spatial"],
                "abbrev": layers_metadata["facesah"]["abbrev"],
                "postfix": layers_metadata["facesah"]["postfix"],
                "postfix_desc": layers_metadata["facesah"]["postfix_desc"],
                "alias": f"OCTL {year} Topological Faces-Area Hydrography",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Topological Faces-Area Hydrography Relationship File",
                "code": "FH",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Topological Faces-Area Hydrography",
                "tags": f"{entry_tags}, feces, water, hydrography",
                "summary": f"Orange County Tiger Lines {year} Topological Faces-Area Hydrography",
                "description": f"Orange County Tiger Lines {year} Topological Faces-Area Hydrography. This shapefile contains topological faces and area hydrography relationship information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "facesal": {
                "type": layers_metadata["facesal"]["type"],
                "file": layers_metadata["facesal"]["file"],
                "scale": layers_metadata["facesal"]["scale"],
                "spatial": layers_metadata["facesal"]["spatial"],
                "abbrev": layers_metadata["facesal"]["abbrev"],
                "postfix": layers_metadata["facesal"]["postfix"],
                "postfix_desc": layers_metadata["facesal"]["postfix_desc"],
                "alias": f"OCTL {year} Topological Faces-Area Landmark",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Topological Faces-Area Landmark Relationship File",
                "code": "FL",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Topological Faces-Area Landmark",
                "tags": f"{entry_tags}, faces, landmarks",
                "summary": f"Orange County Tiger Lines {year} Topological Faces-Area Landmark",
                "description": f"Orange County Tiger Lines {year} Topological Faces-Area Landmark. This shapefile contains topological faces and area landmark relationship information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "featnames": {
                "type": layers_metadata["featnames"]["type"],
                "file": layers_metadata["featnames"]["file"],
                "scale": layers_metadata["featnames"]["scale"],
                "spatial": layers_metadata["featnames"]["spatial"],
                "abbrev": layers_metadata["featnames"]["abbrev"],
                "postfix": layers_metadata["featnames"]["postfix"],
                "postfix_desc": layers_metadata["featnames"]["postfix_desc"],
                "alias": f"OCTL {year} Feature Names",
                "group": "Feature Relationships",
                "category": "Relationship Files",
                "label": "Feature Names Relationship File",
                "code": "FN",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Feature Names",
                "tags": f"{entry_tags}, names, relationships",
                "summary": f"Orange County Tiger Lines {year} Feature Names Table",
                "description": f"Orange County Tiger Lines {year} Feature Names. This shapefile contains feature names relationship information for features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "linearwater": {
                "type": layers_metadata["linearwater"]["type"],
                "file": layers_metadata["linearwater"]["file"],
                "scale": layers_metadata["linearwater"]["scale"],
                "spatial": layers_metadata["linearwater"]["spatial"],
                "abbrev": layers_metadata["linearwater"]["abbrev"],
                "postfix": layers_metadata["linearwater"]["postfix"],
                "postfix_desc": layers_metadata["linearwater"]["postfix_desc"],
                "alias": f"OCTL {year} Linear Hydrography",
                "group": "Features",
                "category": "Water",
                "label": "Linear Hydrography",
                "code": "WL",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Linear Hydrography",
                "tags": f"{entry_tags}, water, hydrography",
                "summary": f"Orange County Tiger Lines {year} Linear Hydrography",
                "description": f"Orange County Tiger Lines {year} Linear Hydrography. This shapefile contains linear hydrography features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "metdiv": {
                "type": layers_metadata["metdiv"]["type"],
                "file": layers_metadata["metdiv"]["file"],
                "scale": layers_metadata["metdiv"]["scale"],
                "spatial": layers_metadata["metdiv"]["spatial"],
                "abbrev": layers_metadata["metdiv"]["abbrev"],
                "postfix": layers_metadata["metdiv"]["postfix"],
                "postfix_desc": layers_metadata["metdiv"]["postfix_desc"],
                "alias": f"OCTL {year} Metropolitan Divisions",
                "group": "Geographic Areas",
                "category": "Core Based Statistical Areas",
                "label": "Metropolitan Division",
                "code": "MD",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Metropolitan Divisions",
                "tags": f"{entry_tags}, metropolitan divisions",
                "summary": f"Orange County Tiger Lines {year} Metropolitan Divisions",
                "description": f"Orange County Tiger Lines {year} Metropolitan Divisions. This shapefile contains metropolitan division features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "mil": {
                "type": layers_metadata["mil"]["type"],
                "file": layers_metadata["mil"]["file"],
                "scale": layers_metadata["mil"]["scale"],
                "spatial": layers_metadata["mil"]["spatial"],
                "abbrev": layers_metadata["mil"]["abbrev"],
                "postfix": layers_metadata["mil"]["postfix"],
                "postfix_desc": layers_metadata["mil"]["postfix_desc"],
                "alias": f"OCTL {year} Military Installations",
                "group": "Features",
                "category": "Military Installations",
                "label": "Military Installations",
                "code": "ML",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Military Installations",
                "tags": f"{entry_tags}, military installations",
                "summary": f"Orange County Tiger Lines {year} Military Installations",
                "description": f"Orange County Tiger Lines {year} Military Installations. This shapefile contains military installation features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "place": {
                "type": layers_metadata["place"]["type"],
                "file": layers_metadata["place"]["file"],
                "scale": layers_metadata["place"]["scale"],
                "spatial": layers_metadata["place"]["spatial"],
                "abbrev": layers_metadata["place"]["abbrev"],
                "postfix": layers_metadata["place"]["postfix"],
                "postfix_desc": layers_metadata["place"]["postfix_desc"],
                "alias": f"OCTL {year} Cities or Places",
                "group": "Geographic Areas",
                "category": "Places",
                "label": "Place (Cities or Unincorporated)",
                "code": "PL",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Cities or Places",
                "tags": f"{entry_tags}, places, cities",
                "summary": f"Orange County Tiger Lines {year} Cities or Places",
                "description": f"Orange County Tiger Lines {year} Cities or Places. This shapefile contains city and place features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "pointlm": {
                "type": layers_metadata["pointlm"]["type"],
                "file": layers_metadata["pointlm"]["file"],
                "scale": layers_metadata["pointlm"]["scale"],
                "spatial": layers_metadata["pointlm"]["spatial"],
                "abbrev": layers_metadata["pointlm"]["abbrev"],
                "postfix": layers_metadata["pointlm"]["postfix"],
                "postfix_desc": layers_metadata["pointlm"]["postfix_desc"],
                "alias": f"OCTL {year} Point Landmarks",
                "group": "Features",
                "category": "Landmarks",
                "label": "Point Landmarks",
                "code": "LP",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Point Landmarks",
                "tags": f"{entry_tags}, points, landmarks",
                "summary": f"Orange County Tiger Lines {year} Point Landmarks",
                "description": f"Orange County Tiger Lines {year} Point Landmarks. This shapefile contains point landmark features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "primaryroads": {
                "type": layers_metadata["primaryroads"]["type"],
                "file": layers_metadata["primaryroads"]["file"],
                "scale": layers_metadata["primaryroads"]["scale"],
                "spatial": layers_metadata["primaryroads"]["spatial"],
                "abbrev": layers_metadata["primaryroads"]["abbrev"],
                "postfix": layers_metadata["primaryroads"]["postfix"],
                "postfix_desc": layers_metadata["primaryroads"]["postfix_desc"],
                "alias": f"OCTL {year} Primary Roads",
                "group": "Features",
                "category": "Roads",
                "label": "Primary Roads",
                "code": "RP",
                "method": "clip",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Primary Roads",
                "tags": f"{entry_tags}, roads, primary",
                "summary": f"Orange County Tiger Lines {year} Primary Roads",
                "description": f"Orange County Tiger Lines {year} Primary Roads. This shapefile contains primary road features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "prisecroads": {
                "type": layers_metadata["prisecroads"]["type"],
                "file": layers_metadata["prisecroads"]["file"],
                "scale": layers_metadata["prisecroads"]["scale"],
                "spatial": layers_metadata["prisecroads"]["spatial"],
                "abbrev": layers_metadata["prisecroads"]["abbrev"],
                "postfix": layers_metadata["prisecroads"]["postfix"],
                "postfix_desc": layers_metadata["prisecroads"]["postfix_desc"],
                "alias": f"OCTL {year} Primary and Secondary Roads",
                "group": "Features",
                "category": "Roads",
                "label": "Primary and Secondary Roads",
                "code": "RS",
                "method": "clip",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Primary and Secondary Roads",
                "tags": f"{entry_tags}, roads, primary, secondary",
                "summary": f"Orange County Tiger Lines {year} Primary and Secondary Roads",
                "description": f"Orange County Tiger Lines {year} Primary and Secondary Roads. This shapefile contains primary and secondary road features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "puma": {
                "type": layers_metadata["puma"]["type"],
                "file": layers_metadata["puma"]["file"],
                "scale": layers_metadata["puma"]["scale"],
                "spatial": layers_metadata["puma"]["spatial"],
                "abbrev": layers_metadata["puma"]["abbrev"],
                "postfix": layers_metadata["puma"]["postfix"],
                "postfix_desc": layers_metadata["puma"]["postfix_desc"],
                "alias": f"OCTL {year} Public Use Microdata Areas",
                "group": "Geographic Areas",
                "category": "Public Use Microdata Areas",
                "label": "Public Use Microdata Areas",
                "code": "PU",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Public Use Microdata Areas",
                "tags": f"{entry_tags}, public use microdata areas",
                "summary": f"Orange County Tiger Lines {year} Public Use Microdata Areas",
                "description": f"Orange County Tiger Lines {year} Public Use Microdata Areas. This shapefile contains public use microdata area features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "rails": {
                "type": layers_metadata["rails"]["type"],
                "file": layers_metadata["rails"]["file"],
                "scale": layers_metadata["rails"]["scale"],
                "spatial": layers_metadata["rails"]["spatial"],
                "abbrev": layers_metadata["rails"]["abbrev"],
                "postfix": layers_metadata["rails"]["postfix"],
                "postfix_desc": layers_metadata["rails"]["postfix_desc"],
                "alias": f"OCTL {year} Rails",
                "group": "Features",
                "category": "Rails",
                "label": "Rails",
                "code": "RL",
                "method": "clip",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Rails",
                "tags": f"{entry_tags}, rails, railroads",
                "summary": f"Orange County Tiger Lines {year} Rails",
                "description": f"Orange County Tiger Lines {year} Rails. This shapefile contains rail features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "roads": {
                "type": layers_metadata["roads"]["type"],
                "file": layers_metadata["roads"]["file"],
                "scale": layers_metadata["roads"]["scale"],
                "spatial": layers_metadata["roads"]["spatial"],
                "abbrev": layers_metadata["roads"]["abbrev"],
                "postfix": layers_metadata["roads"]["postfix"],
                "postfix_desc": layers_metadata["roads"]["postfix_desc"],
                "alias": f"OCTL {year} All Roads",
                "group": "Features",
                "category": "Roads",
                "label": "All Roads",
                "code": "RD",
                "method": "copy",
                "gdb": entry_gdb,
                "title": f"OCTL {year} All Roads",
                "tags": f"{entry_tags}, roads",
                "summary": f"Orange County Tiger Lines {year} All Roads",
                "description": f"Orange County Tiger Lines {year} All Roads. This shapefile contains road features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "scsd": {
                "type": layers_metadata["scsd"]["type"],
                "file": layers_metadata["scsd"]["file"],
                "scale": layers_metadata["scsd"]["scale"],
                "spatial": layers_metadata["scsd"]["spatial"],
                "abbrev": layers_metadata["scsd"]["abbrev"],
                "postfix": layers_metadata["scsd"]["postfix"],
                "postfix_desc": layers_metadata["scsd"]["postfix_desc"],
                "alias": f"OCTL {year} Secondary School Districts",
                "group": "Geographic Areas",
                "category": "School Districts",
                "label": "Secondary School Districts",
                "code": "SS",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Secondary School Districts",
                "tags": f"{entry_tags}, schools, school districts, secondary schools",
                "summary": f"Orange County Tiger Lines {year} Secondary School Districts",
                "description": f"Orange County Tiger Lines {year} Secondary School Districts. This shapefile contains secondary school district features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "sldl": {
                "type": layers_metadata["sldl"]["type"],
                "file": layers_metadata["sldl"]["file"],
                "scale": layers_metadata["sldl"]["scale"],
                "spatial": layers_metadata["sldl"]["spatial"],
                "abbrev": layers_metadata["sldl"]["abbrev"],
                "postfix": layers_metadata["sldl"]["postfix"],
                "postfix_desc": layers_metadata["sldl"]["postfix_desc"],
                "alias": f"OCTL {year} State Assembly Legislative Districts",
                "group": "Geographic Areas",
                "category": "State Legislative Districts",
                "label": "State Legislative District - Lower Chamber (Assembly)",
                "code": "LL",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} State Assembly Legislative Districts",
                "tags": f"{entry_tags}, legislative districts, state assembly",
                "summary": f"Orange County Tiger Lines {year} State Assembly Legislative Districts",
                "description": f"Orange County Tiger Lines {year} State Assembly Legislative Districts. This shapefile contains state assembly legislative district (lower chamber) features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "sldu": {
                "type": layers_metadata["sldu"]["type"],
                "file": layers_metadata["sldu"]["file"],
                "scale": layers_metadata["sldu"]["scale"],
                "spatial": layers_metadata["sldu"]["spatial"],
                "abbrev": layers_metadata["sldu"]["abbrev"],
                "postfix": layers_metadata["sldu"]["postfix"],
                "postfix_desc": layers_metadata["sldu"]["postfix_desc"],
                "alias": f"OCTL {year} State Senate Legislative Districts",
                "group": "Geographic Areas",
                "category": "State Legislative Districts",
                "label": "State Legislative District - Upper Chamber (Senate)",
                "code": "LU",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} State Senate Legislative Districts",
                "tags": f"{entry_tags}, legislative districts, state senate",
                "summary": f"Orange County Tiger Lines {year} State Senate Legislative Districts",
                "description": f"Orange County Tiger Lines {year} State Senate Legislative Districts. This shapefile contains state senate legislative district (upper chamber) features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "tabblock": {
                "type": layers_metadata["tabblock"]["type"],
                "file": layers_metadata["tabblock"]["file"],
                "scale": layers_metadata["tabblock"]["scale"],
                "spatial": layers_metadata["tabblock"]["spatial"],
                "abbrev": layers_metadata["tabblock"]["abbrev"],
                "postfix": layers_metadata["tabblock"]["postfix"],
                "postfix_desc": layers_metadata["tabblock"]["postfix_desc"],
                "alias": f"OCTL {year} Blocks",
                "group": "Geographic Areas",
                "category": "Blocks",
                "label": "Block",
                "code": "BL",
                "method": "query",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Blocks",
                "tags": f"{entry_tags}, US Census, blocks",
                "summary": f"Orange County Tiger Lines {year} Blocks",
                "description": f"Orange County Tiger Lines {year} Blocks. This shapefile contains block features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "tract": {
                "type": layers_metadata["tract"]["type"],
                "file": layers_metadata["tract"]["file"],
                "scale": layers_metadata["tract"]["scale"],
                "spatial": layers_metadata["tract"]["spatial"],
                "abbrev": layers_metadata["tract"]["abbrev"],
                "postfix": layers_metadata["tract"]["postfix"],
                "postfix_desc": layers_metadata["tract"]["postfix_desc"],
                "alias": f"OCTL {year} Census Tracts",
                "group": "Geographic Areas",
                "category": "Census Tracts",
                "label": "Census Tract",
                "code": "TR",
                "method": "query",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Census Tracts",
                "tags": f"{entry_tags}, US Census, census tracts",
                "summary": f"Orange County Tiger Lines {year} Census Tracts",
                "description": f"Orange County Tiger Lines {year} Census Tracts. This shapefile contains census tract features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "unsd": {
                "type": layers_metadata["unsd"]["type"],
                "file": layers_metadata["unsd"]["file"],
                "scale": layers_metadata["unsd"]["scale"],
                "spatial": layers_metadata["unsd"]["spatial"],
                "abbrev": layers_metadata["unsd"]["abbrev"],
                "postfix": layers_metadata["unsd"]["postfix"],
                "postfix_desc": layers_metadata["unsd"]["postfix_desc"],
                "alias": f"OCTL {year} Unified School Districts",
                "group": "Geographic Areas",
                "category": "School Districts",
                "label": "Unified School Districts",
                "code": "SU",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Unified School Districts",
                "tags": f"{entry_tags}, schools, school districts, unified schools",
                "summary": f"Orange County Tiger Lines {year} Unified School Districts",
                "description": f"Orange County Tiger Lines {year} Unified School Districts. This shapefile contains unified school district features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "uac": {
                "type": layers_metadata["uac"]["type"],
                "file": layers_metadata["uac"]["file"],
                "scale": layers_metadata["uac"]["scale"],
                "spatial": layers_metadata["uac"]["spatial"],
                "abbrev": layers_metadata["uac"]["abbrev"],
                "postfix": layers_metadata["uac"]["postfix"],
                "postfix_desc": layers_metadata["uac"]["postfix_desc"],
                "alias": f"OCTL {year} Urban Areas",
                "group": "Geographic Areas",
                "category": "Urban Areas",
                "label": "Urban Areas",
                "code": "UA",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} Urban Areas",
                "tags": f"{entry_tags}, urban areas",
                "summary": f"Orange County Tiger Lines {year} Urban Areas",
                "description": f"Orange County Tiger Lines {year} Urban Areas. This shapefile contains urban area features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            },
            "zcta5": {
                "type": layers_metadata["zcta5"]["type"],
                "file": layers_metadata["zcta5"]["file"],
                "scale": layers_metadata["zcta5"]["scale"],
                "spatial": layers_metadata["zcta5"]["spatial"],
                "abbrev": layers_metadata["zcta5"]["abbrev"],
                "postfix": layers_metadata["zcta5"]["postfix"],
                "postfix_desc": layers_metadata["zcta5"]["postfix_desc"],
                "alias": f"OCTL {year} ZIP Code Tabulation Areas",
                "group": "Geographic Areas",
                "category": "ZIP Code Tabulation Areas",
                "label": "ZIP Code Tabulation Areas",
                "code": "ZC",
                "method": "within",
                "gdb": entry_gdb,
                "title": f"OCTL {year} ZIP Code Tabulation Areas",
                "tags": f"{entry_tags}, ZIP Codes, ZCTA",
                "summary": f"Orange County Tiger Lines {year} ZIP Code Tabulation Areas",
                "description": f"Orange County Tiger Lines {year} ZIP Code Tabulation Areas. This shapefile contains ZIP Code Tabulation Area features in the Tiger/Line shapefiles. Version {self.version}, Last Updated: {self.data_date}.",
                "credits": entry_credits,
                "access": entry_access,
                "uri": entry_uri
            }
        }

        # Define the codebook path
        cb_path = os.path.join(self.prj_dirs["codebook"], f"octl_cb_{year}.json")
        
        # Export the codebook to a JSON file
        with open(cb_path, "w", encoding = "utf-8") as json_file:
            json.dump(codebook, json_file, indent = 4)
            print(f"Codebook exported to (codebook) {os.path.basename(cb_path)}")

        # Return the constructed codebook
        return codebook


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Folder metadata ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def folder_metadata(self, year: int, remote: bool = True, export: bool = False) -> dict:
        """
        Generate metadata for the Tiger/Line folder of a specified year.
        Parameters:
            year (int): The year of the Tiger/Line data.
            remote (bool): Whether to use the remote data path. Default is True.
            export (bool): Whether to export the metadata to a JSON file. Default is False.
        Returns:
            dict: A dictionary containing the folder metadata.
        Raises:
            ValueError: If the remote path is not found.
        Example:
            metadata = OCTL.folder_metadata(year=2022, remote=True, export=True)
            print(metadata)
        Note:
            This method reads the Tiger/Line data folder for the specified year,
        """
        
        # Initialize metadata dictionary
        metadata_path = os.path.join(self.prj_dirs["metadata"], "octl_folder_metadata.json")
        # Load existing metadata if available
        if os.path.exists(metadata_path):
            # Load existing metadata
            with open(metadata_path, "r", encoding = "utf-8") as json_file:
                metadata = json.load(json_file)
        else:
            # Create an empty metadata dictionary
            metadata = {}

        # Set the raw data directory
        raw_directory = self.prj_dirs["data_raw"]
        # Set the root directory
        root_directory = self.prj_dirs["root"] 

        # Redefine raw_directory if running remotely
        if remote:
            # Get the remote path by drive label name
            raw_directory = self.get_remote_path("DRKWD02")
            if not raw_directory:
                raise ValueError("Remote path not found. Please ensure the drive is connected.")
            # Set the root directory based on the raw directory
            root_directory = Path(raw_directory).parent.as_posix()

        # Define the folder name based on the year
        folder = f"tl{year}"

        # Define the layers to be checked
        layers = ["addr", "addrfeat", "addrfn", "arealm", "areawater", "bg", "cbsa", "cd", "coastline", "county", "cousub", "csa", "edges", "elsd", "faces", "facesah", "facesal", "facesmil", "featnames", "linearwater", "metdiv", "mil", "place", "pointlm", "primaryroads", "prisecroads", "puma", "rails", "roads", "scsd", "sldl", "sldu", "tabblock", "tract", "uac", "unsd", "zcta5"]

        # Define the full folder path
        folder_path = os.path.join(raw_directory, folder)
        # Define the relative folder path
        relative_folder_path = os.path.relpath(folder_path, root_directory)

        # Initialize the year metadata
        metadata[year] = {
            "version": self.version,
            "date": self.data_date,
            "year": int(year),
            "folder": folder,
            "path": folder_path,
            "relative_path": relative_folder_path,
            "layers": {}
            }

        # Initialize lists for shapefiles and tables
        try:
            # Set environment workspace to the folder path
            arcpy.env.workspace = folder_path

            # Get the shapefiles in the folder
            shp_files = sorted([os.path.splitext(s)[0] for s in arcpy.ListFeatureClasses()])

            # Get the list of tables in the folder
            dbf_files = sorted([os.path.splitext(s)[0] for s in arcpy.ListTables()])
        finally:
            # Set environment workspace to the current working directory
            arcpy.env.workspace = os.getcwd()

        # Combine shapefiles and tables
        files = sorted(list(set(shp_files + dbf_files)))

        # Print the count of files by type
        print(f"Year: {year}\n- Total Files: {len(files)}\n- Shapefiles: {len(shp_files)}\n- Tables: {len(dbf_files)}")

        # Create an intermediary layers dictionary
        layers_metadata = {}

        # Loop through each file
        for f in files:
            # Split the file name into components
            file_components = f.split("_")
            # Extract the year, spatial level, and abbreviation
            # file_year = file_components[0][3:]
            file_spatial = file_components[1]
            file_abbrev = file_components[2]

            # Check if the file is a shapefile or table
            if f in shp_files:
                file_type = "Shapefile"
            elif f in dbf_files:
                file_type = "Table"
            else:
                file_type = "Unknown"

            # Check if the file layer is in the defined layers
            if file_abbrev in layers:
                file_layer = file_abbrev
                file_postfix = ""
            else:
                # Find all the matches in file_abbrev that start with the layer
                matches = [layer for layer in layers if file_abbrev.startswith(layer)]
                # Check if any matches were found
                if matches:
                    # Get the match with the longest length
                    file_layer = max(matches, key = len)
                    # Extract the postfix from the file_abbrev
                    file_postfix = file_abbrev.removeprefix(file_layer)
                else:
                    file_layer = "Unknown"
                    file_postfix = ""

            # Determine spatial level description
            match file_spatial:
                case "us":
                    spatial_level = "US"
                case "06":
                    spatial_level = "CA"
                case "06059":
                    spatial_level = "OC"
                case _:
                    spatial_level = "Unknown"

            # Calculate the length of the postfix
            len_postfix = len(file_postfix)

            # Determine postfix description
            if len_postfix == 2:
                file_postfix_desc = f"20{file_postfix} US Census"
            elif len_postfix == 3:
                file_postfix_desc = f"{file_postfix}th US Congress"
            else:
                file_postfix_desc = ""

            # Populate the metadata dictionary
            layers_metadata[file_layer] = {
                "type": file_type,
                "file": f,
                "scale": spatial_level,
                "spatial": file_spatial,
                "abbrev": file_abbrev,
                "postfix": file_postfix,
                "postfix_desc": file_postfix_desc
            }

        # Sort the metadata dictionary by file_layer
        layers_metadata = dict(sorted(layers_metadata.items()))

        # Add layers metadata to the main metadata dictionary
        metadata[year]["layers"] = self.codebook_metadata(int(year), layers_metadata)

        if export:
            # Export metadata to JSON file
            json_path = os.path.join(self.prj_dirs["metadata"], f"octl_raw_metadata_tl_{year}.json")
            with open(json_path, "w", encoding = "utf-8") as json_file:
                json.dump(metadata[year], json_file, indent=4)
                print(f"Metadata for year {year} exported to (metadata) {os.path.basename(json_path)}")

            # Export updated metadata to JSON file
            json_path = os.path.join(self.prj_dirs["metadata"], "octl_folder_metadata.json")
            with open(json_path, "w", encoding = "utf-8") as json_file:
                json.dump(metadata, json_file, indent=4)
                print(f"Metadata for year {year} exported to (metadata) {os.path.basename(json_path)}")

        # Return the populated metadata dictionary
        return metadata


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Load codebook ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_cb(self, year: int, cbdf: bool = False) -> tuple:
        """
        Load the codebook.
        Args:
            cbdf (bool): If True, returns the codebook as a DataFrame. Default is False.
        Returns:
            cb (dict): The codebook.
            df_cb (pd.DataFrame): The codebook data frame.
        Raises:
            Nothing
        Example:
            >>>cb, df_cb = load_cb(year, cbdf = True)
        Notes:
            This function loads the codebook from the codebook path.
        """

        # Set the codebook from the JSON file
        cb_path = os.path.join(self.prj_dirs["codebook"], f"octl_cb_{year}.json")
        with open(cb_path, "r", encoding = "utf-8") as json_file:
            cb = json.load(json_file)
        
        if cbdf:
            # Create a codebook data frame
            cbdf = pd.DataFrame(cb).transpose()
            # Add attributes to the codebook data frame
            cbdf.attrs["name"] = "Codebook"        
            print("\nCodebook:\n", cbdf)
            return cb, cbdf
        else:
            return cb


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Scratch geodatabase ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def scratch_gdb(self, method: str = "create"):
        """
        Create a scratch geodatabase.
        Args:
            method (str): The method to use. Default is "create".
        Returns:
            gdb_path (str): The path to the scratch geodatabase.
        Raises:
            Nothing
        Example:
            >>>scratch_gdb(method = "create")
        Notes:
            This function creates a scratch geodatabase.
        """
        # Get the path to the scratch geodatabase
        gdb_path = os.path.join(self.prj_dirs["gis"], "scratch.gdb")

        if method == "create":
            # Check if the geodatabase exists
            if arcpy.Exists(gdb_path):
                # Delete the geodatabase
                arcpy.management.Delete(gdb_path)
                print("Scratch geodatabase deleted successfully.")
            # Create a scratch geodatabase
            arcpy.management.CreateFileGDB(self.prj_dirs["gis"], "scratch.gdb")
            print("Scratch geodatabase created successfully.")
        elif method == "delete":
            if not arcpy.Exists(gdb_path):
                print("Scratch geodatabase does not exist.")
                return
            # Delete the scratch geodatabase
            arcpy.management.Delete(gdb_path)
            print("Scratch geodatabase deleted successfully.")
        else:
            print("Invalid method. Please choose 'create' or 'delete'.")
        
        # Return the path to the scratch geodatabase
        return gdb_path


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Create geodatabase ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_gdb(self, year: int) -> str:
        """
        Create a geodatabase.
        Args:
            year (int): The year of the geodatabase.
        Returns:
            gdb_path (str): The path to the geodatabase.
        Raises:
            Nothing
        Example:
            >>>create_gdb()
        Notes:
            This function creates a geodatabase.
        """
        gdb_name = f"octl{year}.gdb"
        gdb_path = os.path.join(self.prj_dirs["gis"], gdb_name)

        if not arcpy.Exists(gdb_path):
            # Create a new file geodatabase
            arcpy.management.CreateFileGDB(self.prj_dirs["gis"], gdb_name)
            print(f"Geodatabase {gdb_name} created successfully.")
            return gdb_path
        else:
            # Delete the existing geodatabase
            arcpy.management.Delete(gdb_path)
            # Create a new file geodatabase
            arcpy.management.CreateFileGDB(self.prj_dirs["gis"], gdb_name)
            print("Geodatabase already exists. Deleted and recreated.")
            return gdb_path


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Process raw data ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def process_raw_data(self, year: int, remote: bool = True, export: bool = False, logging = False) -> dict:
        """
        Process raw data from the raw data directory and create a geodatabase.
        Args:
            year (int): The year of the data to process.
            remote (bool): Whether to use the remote data path. Default is True.
            export (bool): Whether to export the processed data. Default is False.
            logging (bool): Whether to enable logging. Default is False.
        Returns:
            final_list (dict): A dictionary of feature classes and their codes.
        Raises:
            Nothing
        Example:
            >>>process_raw_data(year=2020, logging=True)
        Notes:
            This function processes raw data from the raw data directory and creates a geodatabase.
        """
        if logging:
            str_ver = str(self.version).replace(".", "0")
            self.logger.enable(meta = self.prj_meta, filename = f"octl_process_shapefiles_{str_ver}_{year}.log", replace = True)
            print("OCTL Process Shapefiles Log\n")

        # Get the folder metadata
        folder_metadata = self.folder_metadata(year = year, remote = remote, export = export)
        
        # Get the metadata for the specified year
        tl_metadata = folder_metadata[year]
        print(f"\nProcessing Tiger Lines for year {year}...\n")

        # Load the codebook for the specified year
        cb = self.load_cb(tl_metadata["year"], cbdf = False)

        # Create a scratch geodatabase
        scratch_gdb = self.scratch_gdb(method = "create")

        # Set environment workspace to the folder containing shapefiles
        arcpy.env.workspace = tl_metadata["path"]

        # Get a list of all shapefiles in the folder
        shapefiles = arcpy.ListFeatureClasses("*.shp")
        tables = arcpy.ListTables("*.dbf")

        if shapefiles:
            # FeatureClassToGeodatabase accepts a list of inputs
            arcpy.conversion.FeatureClassToGeodatabase(shapefiles, scratch_gdb)
            self.arcpy_messages("-")
            print(f"\nSuccessfully imported {len(shapefiles)} shapefiles to scratch.gdb\n")
        else:
            print("No shapefiles found in the specified directory.")

        if tables:
            # FeatureClassToGeodatabase accepts a list of inputs
            arcpy.conversion.TableToGeodatabase(tables, scratch_gdb)
            self.arcpy_messages("-")
            print(f"\nSuccessfully imported {len(tables)} tables to scratch.gdb\n")
        else:
            print("No tables found in the specified directory.")

        # Create a geodatabase for the year
        tl_gdb = self.create_gdb(tl_metadata["year"])

        print(f"Processing {cb['county']['file']}...")

        # Define the input and output feature classes for the county feature class
        in_oc = os.path.join(scratch_gdb, tl_metadata["layers"]["county"]["file"]
)
        out_oc = os.path.join(tl_gdb, cb["county"]["code"])

        # Get the field name from the arcpy.ListFields(in_oc) if field.name contains "STATEFP" and "COUNTYFP"
        state_field = ""
        county_field = ""
        for field in arcpy.ListFields(in_oc):
            if "STATEFP" in field.name:
                state_field = field.name
            elif "COUNTYFP" in field.name:
                county_field = field.name

        # Select rows with State and County FIPS codes
        if state_field and county_field:
            # Select rows with State and County FIPS codes
            arcpy.analysis.Select(
                in_features = in_oc,
                out_feature_class = out_oc,
                where_clause = f"{state_field} = '06' And {county_field} = '059'"
            )
            self.arcpy_messages("-")

        # Check if the output feature class is empty
        if int(arcpy.GetCount_management(out_oc).getOutput(0)) == 0:
            arcpy.management.Delete(out_oc)
            self.arcpy_messages("-")
            print(f"- Deleted empty feature class: {os.path.basename(out_oc)}")


        # Create a list to store the final feature classes
        final_list = dict()

        # Create a list of feature classes to process and remove the us_county feature class
        fc_list = list(cb.keys())
        fc_list.remove("county")
        final_list["CO"] = "county"
        
        # Alter the alias name of the county feature class
        arcpy.AlterAliasName(out_oc, cb["county"]["alias"])
        self.arcpy_messages("-")

        # Loop through the feature classes in the fc_list
        for f in fc_list:
            # Define the feature class name and code from the codebook
            fc = cb[f]["file"]
            code = cb[f]["code"]
            # Define the input and output feature classes
            in_fc = os.path.join(scratch_gdb, fc)
            out_fc = os.path.join(tl_gdb, code)
            method = cb[f]["method"]
            print(f"Processing {fc}...")

            # Match the method for executing geoprocessing operations
            match method:
                case "clip":
                    # Clip the feature class to the extent of the county
                    arcpy.analysis.Clip(
                        in_features = in_fc,
                        clip_features = out_oc,
                        out_feature_class = out_fc,
                        cluster_tolerance = None
                    )
                    self.arcpy_messages("-")
                    # Check if the output feature class is empty
                    if int(arcpy.GetCount_management(out_fc).getOutput(0)) == 0:
                        arcpy.management.Delete(out_fc)
                        self.arcpy_messages("-")
                        print(f"- Deleted empty feature class: {os.path.basename(out_fc)}")
                    else:
                        final_list[code] = f
                        # Alter the alias name of the feature class
                        arcpy.AlterAliasName(out_fc, cb[f]["alias"])
                        self.arcpy_messages("-")
                case "copy":
                    # Copy the feature class as is
                    arcpy.management.Copy(
                        in_data = in_fc,
                        out_data = out_fc,
                        data_type = "FeatureClass",
                        associated_data = None
                    )
                    self.arcpy_messages("-")
                    # Check if the output feature class is empty
                    if int(arcpy.GetCount_management(out_fc).getOutput(0)) == 0:
                        arcpy.management.Delete(out_fc)
                        self.arcpy_messages("-")
                        print(f"- Deleted empty feature class: {os.path.basename(out_fc)}")
                    else:
                        final_list[code] = f
                        # Alter the alias name of the feature class
                        arcpy.AlterAliasName(out_fc, cb[f]["alias"])
                        self.arcpy_messages("-")
                case "within":
                    # Create a temporary layer (this stays in memory, not in your Pro Map)
                    arcpy.management.MakeFeatureLayer(in_fc, "temp_lyr")
                    self.arcpy_messages("-")
                    # Check if the temp_lyr is empty
                    if arcpy.management.GetCount("temp_lyr") == 0:
                        arcpy.management.Delete("temp_lyr")
                        self.arcpy_messages("-")
                        print(f"- Deleted empty feature class: {os.path.basename(out_fc)}")
                        continue
                    # Apply your spatial selection with the negative distance
                    arcpy.management.SelectLayerByLocation(
                        in_layer = "temp_lyr",
                        overlap_type = "WITHIN_A_DISTANCE",
                        select_features = out_oc,
                        search_distance = "-1000 Feet",
                        selection_type = "NEW_SELECTION",
                        invert_spatial_relationship = "NOT_INVERT"
                    )
                    self.arcpy_messages("-")
                    # Export the selection to a new fc
                    arcpy.conversion.FeatureClassToFeatureClass("temp_lyr", tl_gdb, code)
                    self.arcpy_messages("-")
                    # Delete the temporary layer
                    arcpy.management.Delete("temp_lyr")
                    self.arcpy_messages("-")
                    # Check if the output feature class is empty
                    if int(arcpy.GetCount_management(out_fc).getOutput(0)) == 0:
                        arcpy.management.Delete(out_fc)
                        self.arcpy_messages("-")
                        print(f"- Deleted empty feature class: {out_fc}")
                    else:
                        final_list[code] = f
                        # Alter the alias name of the feature class
                        arcpy.AlterAliasName(out_fc, cb[f]["alias"])
                        self.arcpy_messages("-")
                case "query":
                    # Get the field name from the arcpy.ListFields(in_fc) if field.name contains "STATEFP" and "COUNTYFP"
                    state_field = ""
                    county_field = ""
                    for field in arcpy.ListFields(in_fc):
                        if "STATEFP" in field.name:
                            state_field = field.name
                        elif "COUNTYFP" in field.name:
                            county_field = field.name
                    # Select rows with State and County FIPS codes
                    arcpy.analysis.Select(
                        in_features = in_fc,
                        out_feature_class = out_fc,
                        where_clause = f"{state_field} = '06' And {county_field} = '059'"
                    )
                    self.arcpy_messages("-")
                    # Check if the output feature class is empty
                    if int(arcpy.GetCount_management(out_fc).getOutput(0)) == 0:
                        arcpy.management.Delete(out_fc)
                        self.arcpy_messages("-")
                        print(f"- Deleted empty feature class: {os.path.basename(out_fc)}")
                    else:
                        final_list[code] = f
                        # Alter the alias name of the feature class
                        arcpy.AlterAliasName(out_fc, cb[f]["alias"])
                        self.arcpy_messages("-")
                case _:
                    print(f"- No valid method specified for {fc}. Skipping...")
                    continue
        
        # Get a list of all feature classes in the TL geodatabase
        try:
            arcpy.env.workspace = tl_gdb
            tl_fcs = arcpy.ListFeatureClasses()
            tl_tables = arcpy.ListTables()
            tl_features = sorted(tl_fcs) + sorted(tl_tables)
        finally:
            arcpy.env.workspace = os.getcwd()
        
        # Apply metadata to the TL geodatabase
        print(f"\nApplying metadata to the TL geodatabase: {os.path.basename(tl_gdb)}")
        for fc in tl_features:
            # Select the key from the cb dictionary where the value of cb[key]["code"] matches fc
            key = next((k for k, v in cb.items() if v["code"] == fc), None)

            # Define a metadata object for the feature class
            mdo = md.Metadata()
            mdo.title = cb[key]["title"]
            mdo.tags = cb[key]["tags"]
            mdo.summary = cb[key]["summary"]
            mdo.description = cb[key]["description"]
            mdo.credits = cb[key]["credits"]
            mdo.accessConstraints = cb[key]["access"]
            mdo.thumbnailUri = cb[key]["uri"]

            # Apply the metadata to the feature class
            md_fc = md.Metadata(os.path.join(tl_gdb, fc))
            if not md_fc.isReadOnly:
                md_fc.copy(mdo)
                md_fc.save()
                print(f"- Metadata applied to {final_list[fc]} ({fc})")
            else:
                print(f"- Metadata is read-only for {final_list[fc]} ({fc})")
            
            # Create a metadata object for the TL geodatabase
            print(f"\nApplying metadata to the TL geodatabase: {os.path.basename(tl_gdb)}")
            md_gdb = md.Metadata(tl_gdb)
            md_gdb.title = f"TL{tl_metadata["year"]} TigerLine Geodatabase"
            md_gdb.tags = "Orange County, California, OCTL, TigerLine, Geodatabase"
            md_gdb.summary = f"Orange County TigerLine Geodatabase for the {tl_metadata["year"]} year data"
            md_gdb.description = f"Orange County TigerLine Geodatabase for the {tl_metadata["year"]} year data. The data contains feature classes for all TigerLine data available for Orange County, California. Version: {self.version}, last updated on {self.data_date}."
            md_gdb.credits = "Dr. Kostas Alexandridis, GISP, Data Scientist, OC Public Works, OC Survey Geospatial Services"
            md_gdb.accessConstraints = """The feed data and associated resources (maps, apps, endpoints) can be used under a <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">Creative Commons CC-SA-BY</a> License, providing attribution to OC Public Works, OC Survey Geospatial Services. <div><br /></div><div>We make every effort to provide the most accurate and up-to-date data and information. Nevertheless the data feed is provided, 'as is' and OC Public Work's standard <a href="https://www.ocgov.com/contact-county/disclaimer" target="_blank">Disclaimer</a> applies.</div><div><br /></div><div>For any inquiries, suggestions or questions, please contact:</div><div><br /></div><div style="text-align:center;"><a href="https://www.linkedin.com/in/ktalexan/" target="_blank"><b>Dr. Kostas Alexandridis, GISP</b></a><br /></div><div style="text-align:center;">GIS Analyst | Spatial Complex Systems Scientist</div><div style="text-align:center;">OC Public Works/OC Survey Geospatial Applications</div><div style="text-align:center;"><div>601 N. Ross Street, P.O. Box 4048, Santa Ana, CA 92701</div><div>Email: <a href="mailto:kostas.alexandridis@ocpw.ocgov.com" target="_blank">kostas.alexandridis@ocpw.ocgov.com</a> | Phone: (714) 967-0826</div></div>"""
            md_gdb.thumbnailUri = "https://ocpw.maps.arcgis.com/sharing/rest/content/items/67ce28a349d14451a55d0415947c7af3/data"
            md_gdb.save()

        # Delete the scratch geodatabase
        self.scratch_gdb(method = "delete")

        # Print the list of feature classes in the TL geodatabase
        print(f"\nSuccessfully processed shapefiles:\n{tl_fcs}")

        if logging:
            print("\nOCTL Process Shapefiles Completed.")
            self.logger.disable()

        # Return the final list of processed feature classes
        return final_list


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Get gdb dictionary ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_gdb_dict(self) -> dict:
        """
        Function to get the gdb dictionary from the project directories.
        Args:
            Nothing
        Returns:
            gdb_dict (dict): The gdb dictionary.
        Raises:
            Nothing
        Example:
            >>> gdb_dict = get_gdb_dict()
        Notes:
            This function gets the gdb dictionary from the project directories.
        """
        # US Congress dictionary mapping years to Congress Numbers
        congress_dict = {"2010": "111", "2011": "112", "2012": "112", "2013": "113", "2014": "114", "2015": "114", "2016": "115", "2017": "115", "2018": "116", "2019": "116", "2020": "116", "2021": "116", "2022": "118", "2023": "118", "2024": "119", "2025": "119"}

        # Get the list of gdb files in the gis directory
        gdb_list = [f for f in os.listdir(self.prj_dirs["gis"]) if f.endswith(".gdb")]
        
        # Initialize the gdb dictionary
        gdb_dict = {}
        
        # Loop through the gdb files
        for gdb in gdb_list:
            year = int(gdb.split(".")[0].replace("TL", ""))
            path = os.path.join(self.prj_dirs["gis"], gdb)
            arcpy.env.workspace = path
            fc_list =arcpy.ListFeatureClasses()
            fc_dict = self.process_metadata(year)
            
            # Initialize the gdb dictionary for the year
            gdb_dict[str(year)] = {}
            
            # Loop through the feature classes
            for fc in fc_list:
                if fc == ["CD"]:
                    # get the congress number from the congress_dict
                    congress_number = congress_dict[str(year)]
                    for value in fc_dict.values():
                        value["alias"] = f"OCTL {year} Congressional Districts {congress_number}th Congress"
                        value["label"] = f"Congressional Districts of the {congress_number}th US Congress"
                        value["title"] = f"OCTL {year} Congressional Districts of the {congress_number}th US Congress"
                        value["description"] = f"Orange County Tiger Lines {year} Congressional Districts of the {congress_number}th US Congress"
                        gdb_dict[str(year)][fc] = value
                    continue
                else:
                    # get the fc_dict key that matches the fc name and update the value
                    for value in fc_dict.values():
                        if value["fcname"] == fc:
                            gdb_dict[str(year)][fc] = value
            
            # Reset the workspace
            arcpy.env.workspace = os.getcwd()
        
        # Return the gdb dictionary
        return gdb_dict

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Map metadata ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def map_metadata(self, year: int) -> dict:
        """Function to get the map metadata for a given year.
        Args:
            year (int): The year for which to get the map metadata.
        Returns:
            dict: A dictionary containing the map metadata for the given year.
        Raises:
            Nothing
        Example:
            >>> map_metadata(2020)
        Notes:
            This function gets the map metadata for a given year.
        """
        # Convert year to string
        year = str(year)

        # Create the map metadata dictionary
        md_map = {
            "title": f"OCTL {year} Map",
            "tags": f"Orange County, California, Tiger/Line, OCTL, tl{year}",
            "summary": f"Orange County Tiger Lines Map for {year}",
            "description": f"Orange County Tiger Lines {year} Map containing the most up-to-date spatial data for Orange County, California. This map is part of the Orange County Tiger Lines (OCTL) project, which provides comprehensive geospatial data for the county. The data includes roads, boundaries, hydrography, and other essential features derived from the U.S. Census Bureau's Tiger/Line shapefiles for {year}. Version: {self.version}, last updated on {self.data_date}.",
            "credits": "Dr. Kostas Alexandridis, GISP, Data Scientist, OC Public Works, OC Survey Geospatial Services",
            "access": """The feed data and associated resources (maps, apps, endpoints) can be used under a <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">Creative Commons CC-SA-BY</a> License, providing attribution to OC Public Works, OC Survey Geospatial Services. <div><br /></div><div>We make every effort to provide the most accurate and up-to-date data and information. Nevertheless the data feed is provided, 'as is' and OC Public Work's standard <a href="https://www.ocgov.com/contact-county/disclaimer" target="_blank">Disclaimer</a> applies.</div><div><br /></div><div>For any inquiries, suggestions or questions, please contact:</div><div><br /></div><div style="text-align:center;"><a href="https://www.linkedin.com/in/ktalexan/" target="_blank"><b>Dr. Kostas Alexandridis, GISP</b></a><br /></div><div style="text-align:center;">GIS Analyst | Spatial Complex Systems Scientist</div><div style="text-align:center;">OC Public Works/OC Survey Geospatial Applications</div><div style="text-align:center;"><div>601 N. Ross Street, P.O. Box 4048, Santa Ana, CA 92701</div><div>Email: <a href="mailto:kostas.alexandridis@ocpw.ocgov.com" target="_blank">kostas.alexandridis@ocpw.ocgov.com</a> | Phone: (714) 967-0826</div></div>""",
            "uri": "https://ocpw.maps.arcgis.com/sharing/rest/content/items/67ce28a349d14451a55d0415947c7af3/data"
        }

        # Return the map metadata dictionary
        return md_map


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Write dictionary to JSON ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def write_dict_to_json(self, data: dict, dict_type: str) -> str:
        """
        Write a dictionary to a JSON file.
        Args:
            data (dict): The dictionary to write to a JSON file.
            dict_type (str): The type of dictionary to determine the filename.
        Returns:
            str: The filename of the written JSON file.
        Raises:
            Nothing
        Example:
            >>> write_dict_to_json(data, "gdbs")
        Notes:
            This function writes a dictionary to a JSON file.
        """
        # Determine the filename based on the dict_type
        match dict_type:
            case "gdbs":
                dict_name = "gdb_dict.json"
            case "layers":
                dict_name = "layers_dict.json"
        
        # Create the full file path
        filename = os.path.join(self.prj_dirs["metadata"], dict_name)

        # Write the dictionary to a JSON file
        with open(filename, "w", encoding = "utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Dictionary written to {filename}")

        # Return the filename
        return filename


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Master codebook ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def master_codebook(self, create: bool = False) -> dict:
        """
        Create a master codebook JSON file from the raw metadata files
        Args:
            create (bool): If True, creates the master codebook. If False, loads the existing master codebook. Default is False.
        Returns:
            master_cb (dict): The master codebook.
        Raises:
            Nothing
        Example:
            >>> master_cb = master_codebook()
        Notes:
            This function creates a master codebook JSON file from the raw metadata files.
        """
        # Get the project directories
        master_cb = {}
        master_cb_path = os.path.join(self.prj_dirs["codebook"], "octl_cb_master.json")

        # Check if the create flag is set to True
        if create:
            # Get a list of json files from the raw metadata directory that start with "ram_metadata_tl_"
            json_files = list(Path(self.prj_dirs["metadata"]).glob("octl_raw_metadata_tl_*.json"))

            # Loop through the json files and read them into a list
            for jf in json_files:
                # Load the json file
                with open(jf, "r", encoding = "utf-8") as f:
                    jf_dict = json.load(f)
                print(f"Processing file for year {jf_dict['year']}")

                # Get the year from the json file
                year = jf_dict["year"]

                # Get the layers from the json file
                layers = jf_dict["layers"]

                # Add the layers to the master codebook dictionary
                master_cb[year] = layers

            # Save the master codebook to the master codebook path
            with open(master_cb_path, "w", encoding = "utf-8") as f:
                json.dump(master_cb, f, indent = 4)
            print(f"Master codebook created at {master_cb_path}")

            # Return the master codebook dictionary
            return master_cb
        else:
            # Check if the master codebook file exists
            if not os.path.exists(master_cb_path):
                raise FileNotFoundError(f"Master codebook file not found at {master_cb_path}. Please create it first by setting create=True.")
            print(f"Loading master codebook from {master_cb_path}")

            # Load the master codebook from the master codebook path
            with open(master_cb_path, "r", encoding = "utf-8") as f:
                master_cb = json.load(f)
            print("Master codebook loaded successfully.")

            # Return the master codebook dictionary
            return master_cb


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Get feature list ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_feature_list(self) -> dict:
        """
        Generate a list of all feature classes and their fields in the geodatabases.
        Args:
            Nothing
        Returns:
            feature_list (dict): A dictionary of feature classes and their fields.
        Raises:
            Nothing
        Example:
            >>>feature_list = get_feature_list()
        Notes:
            This function generates a list of all feature classes and their fields in the geodatabases.
        """
        # Get the master codebook (load from JSON file)
        cb = self.master_codebook(create = False)

        # Set the workspace to the GIS directory
        arcpy.env.workspace = self.prj_dirs["gis"]

        # Create a dictionary to store the feature list
        feature_list = dict()

        # Get a list of all geodatabases in the GIS directory
        gdbs = arcpy.ListWorkspaces("*", "FileGDB")

        # Loop through each geodatabase
        for gdb in gdbs:
            # Get the name of the geodatabase
            gdb_name = os.path.basename(gdb)
            gdb_year = gdb_name.replace(".gdb","").replace("TL","")
            print(f"Year {gdb_year}: processing {gdb_name}...")

            # Add the geodatabase to the feature list
            feature_list[gdb_year] = {
                    "name": gdb_name,
                    "path": gdb,
                    "features": {}
                    }
            
            # Set the workspace to the geodatabase
            arcpy.env.workspace = gdb
            # Get a list of all feature classes in the geodatabase
            fcs = arcpy.ListFeatureClasses()

            # Loop through each feature class
            for fc in fcs:
                print(f"-  Feature class: {fc}")
                # Get the full path of the feature class
                full_path = os.path.join(gdb, fc)

                # Find the key in the codebook for the specified year that has "code" == field.name as its value
                cb_key = next((k for k, v in cb[gdb_year].items() if v["code"] == fc), None)

                new_type = "Feature Class" if cb[gdb_year][cb_key]["type"] == "Shapefile" else cb[gdb_year][cb_key]["type"]

                # Add the feature class to the feature list
                feature_list[gdb_year]["features"][fc] = {
                    "name": fc,
                    "alias": cb[gdb_year][cb_key]["alias"],
                    "type": new_type,
                    "group": cb[gdb_year][cb_key]["group"],
                    "category": cb[gdb_year][cb_key]["category"],
                    "label": cb[gdb_year][cb_key]["label"],
                    "gdb": cb[gdb_year][cb_key]["gdb"],
                    "path": full_path,
                    "fields": {}}

                # Get a list of all fields in the feature class
                fields = arcpy.ListFields(fc)
                
                # Loop through each field
                for field in fields:
                    print(f"  - Field: {field.name}")

                    # Add the field to the feature list
                    feature_list[gdb_year]["features"][fc]["fields"][field.name] = {
                            "name": field.name,
                            "alias": field.aliasName,
                            "type": field.type,
                            "precision": field.precision,
                            "scale": field.scale,
                            "length": field.length,
                            "editable": field.editable,
                            "nullable": field.isNullable,
                            "required": field.required
                            }

        # Save the feature list to a JSON file
        output_path = os.path.join(self.prj_dirs["metadata"], "feature_list.json")
        print(f"Saving feature list to {output_path}...")
        with open(output_path, "w", encoding = "utf-8") as f:
            json.dump(feature_list, f, indent=4)
        
        # Return the feature list
        return feature_list


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the OCDC main class ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OCDC(OCGD):
    """
    A class containing functions and methods for the US Decennial Census (OCDC) Project.
    Attributes:
        None
    Methods:
        project_metadata(part: int, version: float = float(datetime.datetime.now().year), silent: bool = False) -> dict:
            Generates project metadata for the OCDC data processing project.
        project_directories(silent: bool = False) -> dict:
            Generates project directories for the OCDC data processing project.
    Returns:
        None
    Raises:
        None
    Examples:
        >>> metadata = project_metadata(1, 1)
        >>> prj_dirs = project_directories()
    Notes:
        This class is used to generate project metadata and directories for the project.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Class initialization ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, part: int = 0, version: float = float(datetime.datetime.now().year)):
        """
        Initializes the OCGD class.
        """
        # Initialize the OCgdm class with provided part/version
        super().__init__(part, version)

        # Create a prj_meta variable calling the project_metadata function
        self.prj_meta = self.project_metadata(silent = False)

        # Load the codebook
        #self.cb_path = os.path.join(self.prj_dirs["codebook"], "cb.json")
        #self.cb, self.df_cb = self.load_cb(silent = False)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Project metadata ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def project_metadata(self, silent: bool = False) -> dict:
        """
        Function to generate project metadata for the OCUP data processing project.
        Args:
            silent (bool, optional): Whether to print the metadata information. Defaults to False.
        Returns:
            prj_meta (dict): A dictionary containing the project metadata.
        Raises:
            ValueError: If part is not an integer, or if version is not numeric.
        Example:
            >>> metadata = project_metadata(1, 1)
        Notes:
            The project_metadata function is used to generate project metadata for the OCUP data processing project.
        """

        # Match the part to a specific step and description (with default case)
        match self.part:
            case 1:
                step = "Part 1: Raw Data Processing"
                desc = "Importing the raw data files and perform initial geocoding"
            case 2:
                step = "Part 2: Imported Data Geocoding"
                desc = "Geocoding the imported data and preparing it for GIS processing."
            case 3:
                step = "Part 3: GIS Data Processing"
                desc = "GIS Geoprocessing and formatting of the OCUP data."
            case 4:
                step = "Part 4: GIS Map Processing"
                desc = "Creating maps and visualizations of the OCUP data."
            case 5:
                step = "Part 5: GIS Data Sharing"
                desc = "Exporting and sharing the GIS data to ArcGIS Online."
            case _:
                step = "Part 0: General Data Processing"
                desc = "General data processing and analysis (default)."

        # Create a dictionary to hold the metadata
        metadata = {
            "name": "OCTL Tiger/Line Data Processing",
            "title": step,
            "description": desc,
            "version": self.version,
            "date": self.data_date,
            "author": "Dr. Kostas Alexandridis, GISP",
            "years": "",
        }

        # If not silent, print the metadata
        if not silent:
            print(
                f"\nProject Metadata:\n- Name: {metadata['name']}\n- Title: {metadata['title']}\n- Description: {metadata['description']}\n- Version: {metadata['version']}\n- Author: {metadata['author']}"
            )

        # Return the metadata
        return metadata


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the OCACS main class ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OCACS(OCGD):
    """
    A class containing functions and methods for the Orange County American Community Survey (OCACS) Project.
    Attributes:
        None
    Methods:
        project_metadata(part: int, version: float, silent: bool = False) -> dict:
            Generates project metadata for the OCUP data processing project.
        project_directories(silent: bool = False) -> dict:
            Generates project directories for the OCSWITRS data processing project.
    Returns:
        None
    Raises:
        None
    Examples:
        >>> metadata = project_metadata(1, 1)
        >>> prj_dirs = project_directories()
    Notes:
        This class is used to generate project metadata and directories for the project.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Class initialization ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, part: int = 0, version: float = float(datetime.datetime.now().year)):
        """
        Initializes the OCacs class.
        """
        # Initialize the OCgdm class with provided part/version
        super().__init__(part, version)

        # Create a prj_meta variable calling the project_metadata function
        self.prj_meta = self.project_metadata(silent = False)

        # Define the data_levels list
        self.datasets = ["Demographic", "Social", "Economic", "Housing"]

        # Define the geographies list
        self.geographies = [
            "CO",  # County
            "CS",  # County Subdivision
            "PL",  # Cities or Places
            "ZC",  # Zip Code Tabulation Area
            "CD",  # Congressional District
            "LL",  # State Assembly Legislative Districts (Lower)
            "LU",  # State Senate Legislative Districts (Upper)
            "SE",  # Elementary School District
            "SS",  # Secondary School District
            "SU",  # Unified School District
            "UA",  # Urban Area
            "PU",  # Public Use Microdata Area
            "BG",  # Block Group
            "TR"   # Census Tract
        ]
        

        # Load the codebook
        #self.cb_path = os.path.join(self.prj_dirs["codebook"], "cb.json")
        #self.cb, self.df_cb = self.load_cb(silent = False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Project metadata ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def project_metadata(self, silent: bool = False) -> dict:
        """
        Function to generate project metadata for the OCUP data processing project.
        Args:
            silent (bool, optional): Whether to print the metadata information. Defaults to False.
        Returns:
            prj_meta (dict): A dictionary containing the project metadata.
        Raises:
            ValueError: If part is not an integer, or if version is not numeric.
        Example:
            >>> metadata = project_metadata(1, 1)
        Notes:
            The project_metadata function is used to generate project metadata for the OCUP data processing project.
        """
        
        # Match the part to a specific step and description (with default case)
        match self.part:
            case 1:
                step = "Part 1: Raw Data Processing"
                desc = "Importing the raw data files and perform initial geocoding"
            case 2:
                step = "Part 2: Imported Data Geocoding"
                desc = "Geocoding the imported data and preparing it for GIS processing."
            case 3:
                step = "Part 3: GIS Data Processing"
                desc = "GIS Geoprocessing and formatting of the OCUP data."
            case 4:
                step = "Part 4: GIS Map Processing"
                desc = "Creating maps and visualizations of the OCUP data."
            case 5:
                step = "Part 5: GIS Data Sharing"
                desc = "Exporting and sharing the GIS data to ArcGIS Online."
            case _:
                step = "Part 0: General Data Processing"
                desc = "General data processing and analysis (default)."
        
        # Create a dictionary to hold the metadata
        metadata = {
            "name": "OCTL Tiger/Line Data Processing",
            "title": step,
            "description": desc,
            "version": self.version,
            "date": self.data_date,
            "author": "Dr. Kostas Alexandridis, GISP",
            "years": self.acs5_years
        }

        # If not silent, print the metadata
        if not silent:
            print(
                f"\nProject Metadata:\n- Name: {metadata['name']}\n- Title: {metadata['title']}\n- Description: {metadata['description']}\n- Version: {metadata['version']}\n- Author: {metadata['author']}\n- Date: {metadata['date']}\n- Available ACS5 Years: {metadata['years']}\n"
            )

        # Return the metadata
        return metadata


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: ACS variables codebook ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def acs_cb_variables(self, year: Optional[int] = None, session: Optional[requests.Session] = None) -> pd.DataFrame:
        """
        Fetch ACS variables from the U.S. Census Bureau API for specified years
        Args:
            year (Optional[int], optional): Specific year to fetch variables for. If None, fetches for all available years. Defaults to None.
            session (Optional[requests.Session], optional): An optional requests session for making API calls. Defaults to None.
        Returns:
            pd.DataFrame: A DataFrame containing the ACS variables for the specified years.
        Raises:
            ValueError: If the provided year is not an integer or not in the list of available years.
        Example:
            >>> df_vars = acs_cb_variables(year=2020)
        Notes:
            This function fetches ACS variables from the U.S. Census Bureau API for specified years.
        """
        # Get the list of available ACS years
        years = self.acs5_years
        # If the year is provided and is integer
        if year is not None:
            if isinstance(year, int) and year in years:
                years = [year]
            if not isinstance(year, int):
                raise ValueError("Year must be an integer.")
            if year not in years:
                raise ValueError(f"Year must be one of the following: {years}")

        # Define the master schema dictionary for the DataFrame
        master_schema = {
            "year": "object",
            "count_years": "int32",
            "all_years": "bool",
            "table": "object",
            "group": "object",
            "variable": "object",
            "alias": "object",
            "oid": "int32",
            "used": "bool",
            "level": "object",
            "level_group": "object",
            "category": "object",
            "label": "object",
            "concept": "object",
            "type": "object",
            "limit": "int32",
            "attributes": "object",
            "note": "object",
            "markdown": "object"
        }

        # For each year, add a column to the schema with bool type
        for acs_year in years:
            master_schema[str(acs_year)] = "bool"
        
        # Create an empty DataFrame with the defined schema called master_df
        master_df = pd.DataFrame(columns=master_schema.keys()).astype(master_schema)

        for acs_year in years:
            print(f"Fetching ACS variables for year {acs_year}...")
            # Construct the API URL for the specified year
            api_url = f"https://api.census.gov/data/{acs_year}/acs/acs5/variables.json"
            s = session or requests.Session()

            # Make the API request and parse the JSON response
            resp = s.get(api_url)
            resp.raise_for_status()
            data = resp.json()

            # Extract variables from the response
            variables = data.get("variables", {})

            # Keep only variables that start with a letter, followed by a digit,
            # and end with a capital 'E' (e.g. 'B01001_001E').
            pattern = re.compile(r'^[A-Za-z]\d.*E$')

            # Filter variables based on the pattern
            filtered_vars = {k: v for k, v in variables.items() if pattern.match(k)}

            # Convert the filtered variables dictionary to a pandas DataFrame and add the API year as a column
            df = pd.DataFrame.from_dict(filtered_vars, orient="index")
            # store year as string to avoid dtype conflicts when merging multiple years
            df["year"] = str(acs_year)

            # Move the index (variable names) into a regular column named 'variable' so the variable names appear as the first column in the returned DataFrame.
            df = df.reset_index().rename(columns={"index": "variable"})

            # Add comparison-cleaned columns for `variable` and `label` to ease later comparisons
            # variable: strip leading/trailing spaces
            df["_cmp_variable"] = df["variable"].astype(str).str.strip()

            # Clean the 'label' column per user rules
            if "label" in df.columns:
                # Vectorized cleaning using pandas string methods
                # Two-pass cleaning: first pass normalizes and removes unwanted chars,
                # second pass enforces dash-between-words and removes any leftover duplicates.
                s = df["label"].astype(str)
                # First pass
                s = s.str.replace("!!", ": ", regex=False)
                s = s.str.normalize("NFKD").str.encode("ascii", "ignore").str.decode("ascii")
                s = s.str.replace(r"[^A-Za-z0-9\s:\-]", "", regex=True)
                s = s.str.replace(r"\s*-\s*", "-", regex=True)
                s = s.str.replace(r"-{2,}", "-", regex=True)
                s = s.str.replace(r"(?<![A-Za-z0-9])-|-(?![A-Za-z0-9])", "", regex=True)
                s = s.str.replace(r":{2,}", ":", regex=True)
                s = s.str.replace(r"\s*:\s*", ": ", regex=True)
                s = s.str.replace(r"\s+", " ", regex=True)
                s = s.str.strip(" \t\n\r:-")

                # Second pass to ensure idempotency (remove any artifacts left by first pass)
                s = s.str.replace(r"-{2,}", "-", regex=True)
                s = s.str.replace(r"(?<![A-Za-z0-9])-|-(?![A-Za-z0-9])", "", regex=True)
                s = s.str.replace(r":{2,}", ":", regex=True)
                s = s.str.replace(r"\s*:\s*", ": ", regex=True)
                s = s.str.replace(r"\s+", " ", regex=True)
                s = s.str.strip(" \t\n\r:-")

                df["label"] = s

                # label: remove all spaces and colons, convert to lower
                df["_cmp_label"] = df["label"].astype(str).str.replace(r"[ :]", "", regex=True).str.lower().str.strip()
                # Remove all diacretics, spaces and dashes from the label comparison column
                df["_cmp_label"] = df["_cmp_label"].str.replace(r"[^\w\s]", "", regex = True)

                # Rename the 'predicateType' column to 'type' for clarity
                if "predicateType" in df.columns:
                    df = df.rename(columns={"predicateType": "type"})

                # Add additional metadata columns
                #df["oid"] = pd.Series("", index=df.index, dtype="int")
                # table is the first 3 characters of the variable name and it is dtype object
                df["table"] = df["variable"].str.slice(0, 3)
                df["used"] = pd.Series(False, index=df.index, dtype="bool")
                df["alias"] = df["label"].str.replace(r"^Estimate\s*", "", regex = True).str.strip(" :")
                df["level"] = pd.Series(None, index=df.index, dtype="object")
                df["level_group"] = pd.Series(None, index=df.index, dtype="object")
                df["category"] = pd.Series(None, index=df.index, dtype="object")
                df["note"] = pd.Series(None, index=df.index, dtype="object")

                # Reorder columns and ensure the 'year' column is preserved.
                cols_order = list(master_schema.keys())

                # Keep only columns that actually exist in the dataframe (prevents KeyError)
                cols_order = [c for c in cols_order if c in df.columns]
                df = df[cols_order]

            # If a 'group' column exists, sort by group then variable, then reset index
            if "group" in df.columns:
                df = df.sort_values(by=["group", "variable"]).reset_index(drop = True)

            print("- Data fetched. Processing Master DataFrame...")
            # Check if master_df is empty
            if master_df.empty:
                # Append the current year's dataframe to the master dataframe
                master_df = pd.concat([master_df, df], ignore_index=True)
                # Ensure master_df has comparison columns
                master_df["_cmp_variable"] = master_df["variable"].astype(str).str.strip()
                if "label" in master_df.columns:
                    master_df["_cmp_label"] = master_df["label"].astype(str).str.replace(r"[ :]", "", regex = True).str.lower().str.strip()
                    # Remove all diacretics, spaces and dashes from the label comparison column
                    master_df["_cmp_label"] = master_df["_cmp_label"].str.replace(r"[^\w\s]", "", regex = True)
            else:
                # For each of the records in the current year's dataframe (df), check if the variable already exists in the master dataframe (master_df) in the "variable" column, and if yes, check if the label is the same. If both are the same, do not add the record, but add the year to the existing record's "year" column as a comma-separated list. If the variable exists but the label is different, add the new record as a new row, and add a note to the "note" column of the master_df "same variable, different label". If the variable does not exist, add the new record as a new row.
                for _, row in df.iterrows():
                    var = row["variable"]
                    label = row.get("label", None)

                    # Cleaned comparison values
                    var_cmp = str(var).strip()
                    label_cmp = str(label).replace(" ", "").replace(":", "").lower().strip() if label is not None else ""

                    # Check if the variable exists in the master_df using cleaned comparison
                    existing_rows = master_df[master_df["_cmp_variable"] == var_cmp]

                    if not existing_rows.empty:
                        # Variable exists, check for label using cleaned comparison
                        match_idx = existing_rows[existing_rows["_cmp_label"] == label_cmp].index
                        if len(match_idx) > 0:
                            # Same label, update year (handle None/NaN and avoid duplicates)
                            idx = match_idx[0]
                            existing_years = master_df.loc[idx, "year"]
                            new_year = str(row["year"]) if not pd.isna(row["year"]) else ""
                            if pd.isna(existing_years) or str(existing_years).strip() == "":
                                master_df.loc[idx, "year"] = new_year
                            else:
                                existing_list = [y.strip() for y in str(existing_years).split(",") if y.strip()]
                                if new_year and new_year not in existing_list:
                                    master_df.loc[idx, "year"] = f"{existing_years}, {new_year}"
                        else:
                            # Different label, add new row with note and comparison cols
                            new_row = row.copy()
                            new_row["note"] = f"same variable ({var}), different label (existing: '{existing_rows.iloc[0]['label']}', new: '{label}')"
                            # ensure comparison columns are present for the new row
                            new_row["_cmp_variable"] = var_cmp
                            new_row["_cmp_label"] = label_cmp
                            master_df = pd.concat([master_df, pd.DataFrame([new_row])], ignore_index=True)
                    else:
                        # Variable does not exist, add new row (include comparison cols)
                        new_row = row.copy()
                        new_row["_cmp_variable"] = var_cmp
                        new_row["_cmp_label"] = label_cmp
                        master_df = pd.concat([master_df, pd.DataFrame([new_row])], ignore_index=True)

        # Remove the comparison columns before returning/saving
        master_df = master_df.drop(columns=["_cmp_variable", "_cmp_label"])

        # For each row, create a markdown string in the format "🆔 {variable}: {alias}" from the variable and alias values in the row
        master_df["markdown"] = master_df.apply(lambda x: f"🆔 {x['variable']}: {x['alias']}" if pd.notna(x['alias']) else f"🆔 {x['variable']}", axis=1)

        # Compute the count_years column as the number of years each variable appears in
        master_df["count_years"] = master_df["year"].apply(lambda x: len(str(x).split(",")) if pd.notna(x) else 0)

        # Compute the all_years column as True if count_years equals the total number of years fetched
        total_years = len(years)
        master_df["all_years"] = master_df["count_years"] == total_years

        # For each year column, set to True if the year is in the variable's year list, else False
        for acs_year in years:
            year_str = str(acs_year)
            # bind year_str into the lambda default argument to avoid late-binding of the loop variable
            master_df[year_str] = master_df["year"].apply(lambda x, ys=year_str: ys in [y.strip() for y in str(x).split(",")] if pd.notna(x) else False)

        # Reorder columns by master_schema keys
        cols_order = list(master_schema.keys())
        master_df = master_df[cols_order]

        # After processing all years, sort the master_df by: years first, then variable and reset index
        master_df = master_df.sort_values(by=["variable", "year"]).reset_index(drop = True)

        # Save the master dataframe to an Excel file in the codebook directory
        output_path = os.path.join(self.prj_dirs["codebook"], "acs_cb_variables_master.xlsx")
        master_df.to_excel(output_path, sheet_name = "Master", index_label = "index")
        print(f"Master ACS variables DataFrame saved to {output_path}")

        return master_df


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Get ACS variable list ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_acs_list(self, year: int, category: str):
        """
        Get ACS variable list for a given year and category.
        Args:
            year (int): The ACS year (e.g., 2010, 2023).
            category (str): The variable category (e.g., "Demographic", "Social", "Economic", "Housing").
        Returns:
            list: List of ACS variable strings including GEO_ID.
        Raises:
            ValueError: If the year is not in the available ACS5 years.
        Example:
            >>> get_acs_list(2010, "Demographic")
            ['B01001_001E', 'B01001_002E', 'B01001_003E', ...]
        Note:
            The actual variable codes will depend on the contents of the codebook for that year.
        """
        
        # Make sure the year is in the acs5_years list
        if year not in self.acs5_years:
            raise ValueError(f"Year {year} is not in the available ACS5 years: {self.acs5_years}")
        
        # Define the codebook path for that year
        cb_acs_path = os.path.join(self.prj_dirs["codebook"], f"acs_variables_{year}.json")
        
        # Load the ACS variables codebook for that year
        cb_acs = {}
        if os.path.exists(cb_acs_path):
            with open(cb_acs_path, "r", encoding = "utf-8") as f:
                cb_acs = json.load(f)
        
        # Get the variable list for the given category
        var_list = list(cb_acs[category].keys())
        
        # Return the variable string
        return var_list


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Get geoids ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_geoids(self, year: str, fc: str):
        """
        Get the GEOID field name and unique values for a given year and feature class.
        Args:
            year (str): The year of the geodatabase.
            fc (str): The feature class name.
        Returns:
            dict: A dictionary containing the GEOID field name and unique values.
        Raises:
            ValueError: If the geodatabase or feature class does not exist, or if no GEOID field is found.
        Examples:
            >>> geoids = get_geoids("2020", "TRACT")
        Notes:
            This function retrieves the GEOID field name and unique values from the specified feature class in the geodatabase for the given year.
        """
        # Set the workspace to the geodatabase for the specified year
        path = os.path.join(self.prj_dirs["gis"], f"tl{year}.gdb")
        if not os.path.exists(path):
            raise ValueError(f"Geodatabase for year {year} does not exist at path {path}.")
        
        # Set the arcpy workspace to the geodatabase
        arcpy.env.workspace = path
        if fc not in arcpy.ListFeatureClasses():
            raise ValueError(f"Feature class {fc} does not exist in geodatabase {path}.")
        
        # Loop through the fields in the feature class to find the GEOID field
        for f in arcpy.ListFields(fc):
            # Check if the field name contains "GEOID"
            if f.name.startswith("GEOID"):
                geoid_field = f.name
                geoids = set()
                # Get the unique values for the GEOID field
                with arcpy.da.SearchCursor(fc, geoid_field) as cursor:
                    # Loop through the rows in the cursor
                    for row in cursor:
                        geoids.add(row[0])
                # Convert the geoids to a sorted list
                geoids = sorted(list(geoids))

                # Return the GEOID field name and unique values
                return {"field": geoid_field, "values": geoids}
        raise ValueError(f"No GEOID field found in feature class {fc}.")


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Fetch ACS tables ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def fetch_acs_tables(self, year: int, variables: list[str], geography: str = "CO") -> pd.DataFrame:
        """
        Fetch ACS data for a given year and list of variables.
        This function will chunk requests when `variables` is large and merge
        results by `GEOID` so the caller receives a single record per geography
        with all requested variables.
        Args:
            year (int): The ACS year (e.g., 2010, 2023).
            variables (List[str]): List of ACS variable codes to fetch.
            geography (str): The geography type (e.g., "CO" for county, "TR" for tract). Defaults to "CO".
        Returns:
            DataFrame containing the requested ACS data for each geography.
        Raises:
            RuntimeError: If the CENSUS_API_KEY1 environment variable is not set.
        Example:
            >>> df_acs = fetch_acs_tables(2020, ["B01001_001E", "B01001_002E"], geography = "TR")
        Notes:
            This function fetches ACS data from the Census API, handling large variable
            requests by chunking them and merging results based on GEOID.
        """
        # Get Census API key from environment variable
        api_key = os.getenv("CENSUS_API_KEY1")
        if not api_key:
            raise RuntimeError("Environment variable CENSUS_API_KEY1 is not set")

        # Validate variables parameter
        if not isinstance(variables, (list, tuple)):
            raise TypeError("variables must be a list or tuple of ACS variable codes")

        # Base URL for ACS5 API
        base_url = f"https://api.census.gov/data/{year}/acs/acs5"

        # Census API accepts a maximum of 50 fields per request including GEOID.
        # Ensure we chunk variables so that each request has at most 49 variables
        # plus the GEOID field.
        chunk_size = 40

        # Prepare chunks (exclude GEOID from chunking)
        def _chunk_list_local(items: list[str], size: int) -> list[list[str]]:
            return [items[i : i + size] for i in range(0, len(items), size)]

        # Get the chunks
        chunks = _chunk_list_local(list(variables), chunk_size)
        if len(chunks) > 1:
            print(f"Total variables: {len(variables)} split into {len(chunks)} chunk(s)")

        # Dictionary to hold merged results by GEO_ID
        merged: dict[str, dict[str, str]] = {}

        # Determine for_clause and in_clause based on geography
        for_clause: str = ""
        in_clause: Union[str, list[str]] = ""
        print(f"Fetching data for geography: {geography}")
        match geography:
            case "CO":
                print("Fetching county data")
                geoids = self.get_geoids(str(year), "CO")
                for_clause = "county:059"
                in_clause = "state:06"
            case "CS":
                print("Fetching county subdivision data")
                geoids = self.get_geoids(str(year), "CS")
                for_clause = "county subdivision:*"
                in_clause = ["state:06", "county:059"]
            case "TR":
                print("Fetching census tract data")
                geoids = self.get_geoids(str(year), "TR")
                for_clause = "tract:*"
                in_clause = ["state:06", "county:059"]
            case "PL":
                print("Fetching cities or places data")
                geoids = self.get_geoids(str(year), "PL")
                for_clause = "place:*"
                in_clause = "state:06"
            case "CD":
                print("Fetching congressional district data")
                geoids = self.get_geoids(str(year), "CD")
                for_clause = "congressional district:*"
                in_clause = "state:06"
            case "ZC":
                print("Fetching zip code tabulation areas data")
                geoids = self.get_geoids(str(year), "ZC")
                for_clause = "zip code tabulation area:*"
                in_clause = ""
            case "LL":
                print("Fetching state assembly legislative districts (lower) data")
                geoids = self.get_geoids(str(year), "LL")
                for_clause = "state legislative district (lower chamber):*"
                in_clause = "state:06"
            case "LU":
                print("Fetching state senate legislative districts (upper) data")
                geoids = self.get_geoids(str(year), "LU")
                for_clause = "state legislative district (upper chamber):*"
                in_clause = "state:06"
            case "SE":
                print("Fetching elementary school district data")
                geoids = self.get_geoids(str(year), "SE")
                for_clause = "school district (elementary):*"
                in_clause = "state:06"
            case "SS":
                print("Fetching secondary school district data")
                geoids = self.get_geoids(str(year), "SS")
                for_clause = "school district (secondary):*"
                in_clause = "state:06"
            case "SU":
                print("Fetching unified school district data")
                geoids = self.get_geoids(str(year), "SU")
                for_clause = "school district (unified):*"
                in_clause = "state:06"
            case "UA":
                print("Fetching urban area data")
                geoids = self.get_geoids(str(year), "UA")
                for_clause = "urban area:*"
                in_clause = ""
            case "PU":
                print("Fetching public use microdata area data")
                geoids = self.get_geoids(str(year), "PU")
                for_clause = "public use microdata area:*"
                in_clause = "state:06"
            case "BG":
                print("Fetching block group data")
                geoids = self.get_geoids(str(year), "BG")
                for_clause = "block group:*"
                in_clause = ["state:06", "county:059", "tract:*"]
            case _:
                raise ValueError(f"Unsupported geography: {geography}")

        # Process each chunk and merge results
        print(f"Processing {len(chunks)}x{chunk_size} chunk(s) of variables...")
        for chunk in chunks:
            get_vars = ",".join(["GEO_ID"] + chunk)
            # Build params as a list of tuples so repeated keys (e.g. multiple
            # 'in=' parameters) are preserved in the query string.
            params_list = [("get", get_vars), ("key", api_key)]

            # 'for' is a single value (string)
            if for_clause:
                params_list.append(("for", for_clause))

            # Support multiple 'in' values by repeating the 'in' parameter.
            if in_clause:
                if isinstance(in_clause, (list, tuple)):
                    for val in in_clause:
                        params_list.append(("in", val))
                else:
                    params_list.append(("in", in_clause))

            resp = requests.get(base_url, params = params_list, timeout = 60)
            if resp.status_code != 200:
                print(f"Error fetching data: {resp.status_code} {resp.text}")
                #resp.raise_for_status()
                if resp.status_code == 400:
                    print("Bad Request - likely due to invalid parameters. Check if the geography exists for the specified year.")
                    print("Returning None.")
                    return None

            try:
                data = resp.json()
            except Exception as exc:
                raise RuntimeError(f"Invalid JSON response from Census API (status={resp.status_code}): {resp.text[:500]}") from exc

            if not data or len(data) < 2:
                continue

            headers = data[0]
            for row in data[1:]:
                rec = dict(zip(headers, row))
                geo_id = rec.get("GEO_ID")
                if geo_id is None:
                    # skip malformed row
                    continue
                if geo_id not in merged:
                    merged[geo_id] = {}
                # Only keep GEO_ID and variables requested by the caller
                allowed = set(variables)
                filtered = {k: v for k, v in rec.items() if k == "GEO_ID" or k in allowed}
                merged[geo_id].update(filtered)
        
        # Get the merged response list
        print("Merging chunk(s) and filtering results...")
        merged_list = list(merged.values())
        len_merged = len(merged_list)
        len_geoids = len(geoids["values"])

        if len_merged > len_geoids:
            print(f"- The results have more records ({len_merged}) than the TigerLine geodatabase ({len_geoids}). Filtering results.")
        elif len_merged < len_geoids:
            print(f"- The results have fewer records ({len_merged}) than the TigerLine geodatabase ({len_geoids}). Only the available records will be returned.")

        # If any of the merged_ids are not in the geoids["values"], remove it from the merged_list
        final_list = [rec for rec in merged_list if rec["GEO_ID"].split("US")[-1] in geoids["values"]]

        # Count of final_list and geoids
        len_final = len(final_list)
        len_geoids = len(geoids["values"])

        # Get counts of variables in each record (excluding GEO_ID)
        raw_counts =[len(d) - 1 for d in final_list]
        # Make sure all counts are the same
        if len(set(raw_counts)) == 1:
            print(f"Response has {len_final} records (of {len_geoids} in the TigerLine geodatabase) with {raw_counts[0]} variables each.")
        elif len(set(raw_counts)) > 1:
            print("Warning: Inconsistent variable counts in final_list")

        # Convert the results to a DataFrame
        df = pd.DataFrame(final_list)
        
        # Replace the value of the GEO_ID column with only the part after 'US' and rename the column to just the GEOID
        # Check if GEO_ID is part of the DataFrame columns
        if "GEO_ID" in df.columns:
            # get the column name index
            geo_id_index = df.columns.get_loc("GEO_ID")
            # Use the index to update the column values
            df.iloc[:, geo_id_index] = df.iloc[:, geo_id_index].str.split("US").str[-1]
            # Rename the column by index
            df.rename(columns={df.columns[geo_id_index]: "GEOID"}, inplace = True)
            
        if df.shape[0] == 0:
            print("No records found after filtering. Returning None.")
            return None

        # Get the acs variable codebook path for that year
        cb_acs_path = os.path.join(self.prj_dirs["codebook"], f"acs_variables_{year}.json")
        # Load the ACS variables codebook for that year
        cb_acs = {}
        if os.path.exists(cb_acs_path):
            with open(cb_acs_path, "r", encoding = "utf-8") as f:
                cb_acs = json.load(f)
        
        # For each column in the dataframe (except GEOID), get the column type from the codebook and convert the column to that type
        for col in df.columns:
            if col == "GEOID":
                continue
            # Find the category and variable in the codebook
            found = False
            for vars_dict in cb_acs.values():
                if col in vars_dict:
                    var_type = vars_dict[col]["type"]
                    found = True
                    break
            if found:
                if var_type == "int":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                elif var_type == "float":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("float")
                elif var_type == "str":
                    df[col] = df[col].astype("string")
            else:
                print(f"Warning: Variable {col} not found in codebook for year {year}")

        # Log the final DataFrame shape
        print(f"Returning DataFrame with {df.shape[0]} rows and {df.shape[1]} columns.")

        # Return list of filtered records
        return df

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: TL to SDF ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def tl_to_sdf(self, year: int, geography: str):
        """
        Convert TL tables to spatial data frames for a given year and geography.
        Args:
            year (int): The ACS year (e.g., 2010, 2015, 2020).
            geography (str): The geography type (e.g., "CO", "CS", "PL", etc.).
        Returns:
            pd.DataFrame: A spatial data frame containing the TL data for the specified year and geography.
        Raises:
            None
        Example:
            >>> tl_sdf = tl_to_sdf(2010, "CO")
        Note:
            Ensure that the TL geodatabase for the specified year exists in the GIS directory.
        """
        print(f"Converting TigerLine feature class to spatial data frame for year: {year} and geography: {geography}...")

        # Set the TL geodatabase path
        tl_gdb_path = os.path.join(self.prj_dirs["gis"], f"tl{year}.gdb")

        try:
            arcpy.env.workspace = tl_gdb_path
            arcpy.env.overwriteOutput = True

            # Load the TL feature class into a spatial data frame
            tl_sdf = pd.DataFrame.spatial.from_featureclass(os.path.join(tl_gdb_path, geography))
        finally:
            arcpy.env.workspace = os.getcwd()

        # Return the spatial data frame
        return tl_sdf


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Process ACS data ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def process_acs_data(self, process_year: list[int] = None, all_years: bool = False):
        """
        Process ACS data for all years, datasets, and geographies.
        Args:
            None
        Returns:
            None
        Raises:
            None
        Example:
            >>> process_acs_data()
        Notes:
            This function processes ACS data by creating geodatabases for each year, datasets, and geographies.
        """

        # Determine the years to process
        years = []
        if process_year is None and all_years:
            print("Processing ACS data for all years...")
            # Get the years to process
            years = self.acs5_years
        elif process_year is not None and not all_years:
            # Check if year is an integer or a list of integers
            if isinstance(process_year, int):
                years = [process_year]
                print(f"Processing ACS data for single year: {process_year}...")
            elif isinstance(process_year, list):
                print(f"Processing ACS data for years: {process_year}...")
                years = process_year
        else:
            raise ValueError("Either year must be specified or all_years must be True.")

        # Loop through each year
        for year in years:
            print(f"\nProcessing ACS year: {year}")
            # Create a new geodatabase for each year
            gdb_path = os.path.join(self.prj_dirs["gis"], f"acs{year}.gdb")

            # Get the acs variable codebook path for that year
            cb_acs_path = os.path.join(self.prj_dirs["codebook"], f"acs_variables_{year}.json")
            # Load the ACS variables codebook for that year
            cb_acs = {}
            if os.path.exists(cb_acs_path):
                with open(cb_acs_path, "r", encoding = "utf-8") as f:
                    cb_acs = json.load(f)
            
            # Check if the geodatabase already exists; if so, delete it before creating a new one
            if not arcpy.Exists(gdb_path):
                print(f"- Creating geodatabase: acs{year}.gdb")
                arcpy.CreateFileGDB_management(self.prj_dirs["gis"], f"acs{year}.gdb")
            else:
                print(f"- Deleting existing geodatabase: acs{year}.gdb")
                arcpy.Delete_management(gdb_path)
                print(f"- Creating geodatabase: acs{year}.gdb")
                arcpy.CreateFileGDB_management(self.prj_dirs["gis"], f"acs{year}.gdb")

            # Within each geodatabase, create feature datasets for each dataset
            for fd in self.datasets:
                # Set the feature dataset path
                fd_path = os.path.join(gdb_path, fd)

                # Check if the feature dataset already exists; if not, create it
                if not arcpy.Exists(fd_path):
                    print(f"\nCreating feature dataset: {fd}")
                    arcpy.CreateFeatureDataset_management(gdb_path, fd, spatial_reference = self.sr)

                for geo in self.geographies:
                    print(f"\nProcessing {year} geography: {geo}")

                    # Convert TL to SDF for the given year and geography
                    tl_sdf = self.tl_to_sdf(year, geo)
                    print(f"- Converted TL to SDF for geography: {geo}")

                    # Get the list of variables to process for the given dataset
                    process_vars = self.get_acs_list(year, fd)
                    print(f"- Retrieved {len(process_vars)} variables for dataset: {fd}")

                    # Fetch the ACS tables for the given year, variables, and geography
                    acs_df = self.fetch_acs_tables(year = year, variables = process_vars, geography = geo)

                    # Check if acs_df is None (no data returned)
                    if acs_df is None:
                        print(f"- No ACS data returned for geography: {geo}. Skipping...")
                        continue

                    print(f"- Fetched ACS tables for geography: {geo} with {len(acs_df)} records")

                    # Get the name of the tl_sdf column that contains the GEOID values
                    tl_geoid_col = [col for col in tl_sdf.columns if "GEOID" in col][0]
                    acs_geoid_col = [col for col in acs_df.columns if "GEOID" in col][0]

                    # Merge the demographic variables from acs_df (GEOID) to the tl_sdf (GEOID10)
                    tl_sdf = tl_sdf.merge(acs_df, left_on = tl_geoid_col, right_on = acs_geoid_col, how="left")
                    print(f"- Merged ACS data with TL SDF for geography: {geo}")

                    # Define the output feature class path
                    fc_path = os.path.join(fd_path, geo+fd[0])

                    # Set the arcpy environment to the feature dataset
                    arcpy.env.workspace = fd_path
                    arcpy.env.overwriteOutput = True

                    # Convert the merged DataFrame to a feature class in the geodatabase
                    tl_sdf.spatial.to_featureclass(location = fc_path, overwrite = True, has_z = None, has_m = None, sanitize_columns = False)
                    print(f"- Converted merged DataFrame to feature class: {geo+fd[0]}")

                    # Set field aliases based on the codebook
                    print(f"- Setting field aliases for feature class: {geo+fd[0]}")
                    for field in arcpy.ListFields(fc_path):
                        # Find the variable in the codebook to get the alias
                        found = False
                        for vars_dict in cb_acs.values():
                            if field.name in vars_dict:
                                field_alias = vars_dict[field.name]["alias"]
                                found = True
                                break
                        if found:
                            # Set the field alias
                            arcpy.AlterField_management(fc_path, field.name, new_field_alias = field_alias)
                            print(f"  - Set alias for field {field.name} to {field_alias}")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the OCCR main class ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OCCR(OCGD):
    """
    A class containing functions and methods for the OC Community Resilience Estimates (OCCR) Project.
    Attributes:
        None
    Methods:
        project_metadata(part: int, version: float, silent: bool = False) -> dict:
            Generates project metadata for the OCCR data processing project.
        project_directories(silent: bool = False) -> dict:
            Generates project directories for the OCCR data processing project.
    Returns:
        None
    Raises:
        None
    Examples:
        >>> metadata = project_metadata(1, 1)
        >>> prj_dirs = project_directories()
    Notes:
        This class is used to generate project metadata and directories for the project.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Class initialization ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, part: int = 0, version: float = float(datetime.datetime.now().year)):
        """
        Initializes the OCCR class.
        """
        # Initialize the OCgdm class with provided part/version
        super().__init__(part, version)

        # Create a prj_meta variable calling the project_metadata function
        self.prj_meta = self.project_metadata(silent = False)

        # Define the geographies list
        self.geographies = [
            "CO",  # County
            "TR"   # Census Tract
        ]

        # Define the CR DataFrame schema
        self.schema = {
            "GEOID": "object",
            "GEO_ID": "object",
            "SUMLEVEL": "int32",
            "GEOCOMP": "int32",
            "STATE": "int32",
            "COUNTY": "int32",
            "TRACT": "int32",
            "NAME": "object",
            "YEAR": "int32",
            "POPUNI": "int64",
            "PRED0_E": "int64",
            "PRED12_E": "int64",
            "PRED3_E": "int64",
            "PRED0_PE": "float",
            "PRED12_PE": "float",
            "PRED3_PE": "float",
            "PRED0_M": "int64",
            "PRED12_M": "int64",
            "PRED3_M": "int64",
            "PRED0_PM": "float",
            "PRED12_PM": "float",
            "PRED3_PM": "float"
        }

        # Load the codebook
        cb_path = os.path.join(self.prj_dirs["codebook"], "cr_cb.json")
        # Load the CR variables codebook
        self.cb = {}
        if os.path.exists(cb_path):
            with open(cb_path, "r", encoding = "utf-8") as f:
                self.cb = json.load(f)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Project metadata ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def project_metadata(self, silent: bool = False) -> dict:
        """
        Function to generate project metadata for the OCUP data processing project.
        Args:
            silent (bool, optional): Whether to print the metadata information. Defaults to False.
        Returns:
            prj_meta (dict): A dictionary containing the project metadata.
        Raises:
            ValueError: If part is not an integer, or if version is not numeric.
        Example:
            >>> metadata = project_metadata(1, 1)
        Notes:
            The project_metadata function is used to generate project metadata for the OCUP data processing project.
        """
        
        # Match the part to a specific step and description (with default case)
        match self.part:
            case 1:
                step = "Part 1: Create CR Feature Classes"
                desc = "Creating feature classes for the CR data from the Census API data frames and the Tiger/Line Census Tract geographies."
            case 2:
                step = "Part 2: Imported Data Geocoding"
                desc = "Geocoding the imported data and preparing it for GIS processing."
            case 3:
                step = "Part 3: GIS Data Processing"
                desc = "GIS Geoprocessing and formatting of the OCUP data."
            case 4:
                step = "Part 4: GIS Map Processing"
                desc = "Creating maps and visualizations of the OCUP data."
            case 5:
                step = "Part 5: GIS Data Sharing"
                desc = "Exporting and sharing the GIS data to ArcGIS Online."
            case _:
                step = "Part 0: General Data Processing"
                desc = "General data processing and analysis (default)."
        
        # Create a dictionary to hold the metadata
        metadata = {
            "name": "OC Community Resilience Estimates (OCCR) Data Processing",
            "title": step,
            "description": desc,
            "version": self.version,
            "date": self.data_date,
            "author": "Dr. Kostas Alexandridis, GISP",
            "years": self.cr_years
        }

        # If not silent, print the metadata
        if not silent:
            print(
                f"\nProject Metadata:\n- Name: {metadata['name']}\n- Title: {metadata['title']}\n- Description: {metadata['description']}\n- Version: {metadata['version']}\n- Author: {metadata['author']}\n- Date: {metadata['date']}\n- Available CR Years: {metadata['years']}\n"
            )

        # Return the metadata
        return metadata


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Load CR codebook ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def generate_cr_codebook(self, year: int, write_to_file: bool = False) -> dict:
        """
        Generate CR codebook for a given year and list of headers.
        Args:
            year (int): The CR year (e.g., 2020, 2021, 2022).
        Returns:
            Dictionary containing the CR variable metadata.
        Raises:
            RuntimeError: If the CENSUS_API_KEY1 environment variable is not set.
        Example:
            >>> cr_cb = generate_cr_codebook(2020)
        Notes:
            This function fetches CR variable metadata from the Census API.
        """
        # Define a dictionary to hold variable metadata
        cr_cb = dict()

        # Define the headers to fetch metadata for
        var_list = ["GEO_ID", "SUMLEVEL", "GEOCOMP", "NAME", "POPUNI", "PRED0_E", "PRED12_E", "PRED3_E", "PRED0_PE", "PRED12_PE", "PRED3_PE", "PRED0_M", "PRED12_M", "PRED3_M", "PRED0_PM", "PRED12_PM", "PRED3_PM", "STATE", "COUNTY", "TRACT"]

        # Loop through each CR variable and fetch its metadata
        for cr_var in var_list:
            # Define the URL for the variable metadata
            cr_info_url = f"https://api.census.gov/data/{year}/cr/variables/{cr_var}.json"

            # Make the API request for variable metadata
            info_response = requests.get(cr_info_url, timeout = 60)
            
            # Check for valid JSON response
            try:
                info_data = info_response.json()
            except Exception as exc:
                raise RuntimeError(f"Invalid JSON response from Census API (status={info_response.status_code}): {info_response.text[:500]}") from exc
            
            # Add the variable metadata to the dictionary
            cr_cb[cr_var] = info_data

        # Write the codebook to a JSON file
        cr_cb_path = os.path.join(self.prj_dirs["codebook"], f"cr_cb_{year}.json")
        if write_to_file:
            with open(cr_cb_path, "w", encoding = "utf-8") as f:
                json.dump(cr_cb, f, indent = 4)
            print(f"CR codebook for year {year} written to {cr_cb_path}")

        # Return the codebook dictionary
        return cr_cb

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Fetch CR tables ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def fetch_cr_tables(self, year: int) -> pd.DataFrame:
        """
        Fetch CR data for a given year and geography.
        Args:
            year (int): The CR year (e.g., 2020, 2021, 2022).
        Returns:
            DataFrame containing the requested CR data for each geography.
        Raises:
            RuntimeError: If the CENSUS_API_KEY1 environment variable is not set.
        Example:
            >>> df_cr = fetch_cr_tables(2020)
        Notes:
            This function fetches CR data from the Census API.
        """
        print(f"Fetching CR data for year: {year}...")
        
        # Get Census API key from environment variable
        api_key = os.getenv("CENSUS_API_KEY1")
        if not api_key:
            raise RuntimeError("Environment variable CENSUS_API_KEY1 is not set")

        # Base URL for ACS5 API
        cr_api_url = f"https://api.census.gov/data/{year}/cr?get=GEO_ID,SUMLEVEL,GEOCOMP,NAME,POPUNI,PRED0_E,PRED12_E,PRED3_E,PRED0_PE,PRED12_PE,PRED3_PE,PRED0_M,PRED12_M,PRED3_M,PRED0_PM,PRED12_PM,PRED3_PM&for=tract:*&in=state:06&in=county:059&key={api_key}"

        # Make the API request
        api_response = requests.get(cr_api_url, timeout = 60)
        # Check for valid JSON response
        try:
            api_data = api_response.json()
        except Exception as exc:
            raise RuntimeError(f"Invalid JSON response from Census API (status={api_response.status_code}): {api_response.text[:500]}") from exc

        # Extract headers from the first row of the api_data
        headers = api_data[0]

        # Convert headers to lowercase
        headers = [h for h in headers]

        # Iterate over the api_data rows and create a list of dictionaries and add them to a list
        records = []
        for row in api_data[1:]:
            rec = dict(zip(headers, row))
            records.append(rec)

        # Convert the list of records to a pandas DataFrame
        records_df = pd.DataFrame.from_records(records)

        # if the records_df does not contain all the columns in the schema, add the missing columns with default values. Iterate using the items so that we have access to both the column name and the api_data type
        for col, dtype in self.schema.items():
            
            # If the column is in the api_dataFrame, set the api_data type
            if col in records_df.columns:
                records_df[col] = records_df[col].astype(dtype)
            elif col not in records_df.columns:
                # Set the default value and add the column to the api_dataFrame based on the api_data type
                if dtype == "object":
                    records_df[col] = ""
                elif dtype in ["int32", "int64"]:
                    records_df[col] = 0
                elif dtype in ["float32", "float64"]:
                    records_df[col] = 0.0

        # Reorder the columns of the api_dataFrame to match the schema
        records_df = records_df[list(self.schema.keys())]

        # Set the year column to the current year
        records_df["YEAR"] = year

        # Set the geoid column by removing the '1400000US' prefix from the GEO_ID column
        records_df["GEOID"] = records_df["GEO_ID"].str.replace("1400000US", "", regex=False)

        # Rename the "NAME" column to "CR_NAME"
        records_df = records_df.rename(columns={"NAME": "CR_NAME"})

        # Return the final DataFrame
        return records_df


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Create CR feature class ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_cr_feature_class(self, year: int):
        """
        Create CR feature class for the specified year.
        Args:
            year (int): The CR year (e.g., 2020, 2021, 2022).
        Returns:
            None
        Raises:
            None
        Example:
            >>> create_cr_feature_class(2020)
        Notes:
            This function creates a CR feature class by joining CR data with TL tract data.
        """
        # Geoid of the ocean side tract to remove
        remove_geoid = "06059990100"

        print(f"Creating CR feature class for year: {year}...")
        # Fetch the CR tables for the specified year
        cr_db = self.fetch_cr_tables(year= year)

        print(f"- Removing ocean side tract GEOID: {remove_geoid} if it exists...")
        # Remove specific GEOID record if it exists
        cr_db = cr_db[cr_db["GEOID"] != remove_geoid]
        # Path to TL geodatabase
        tl_gdb = os.path.join(self.prj_dirs["gis"], f"tl{year}.gdb")

        print(f"- Setting arcpy environment to TL geodatabase: tl{year}.gdb...")
        # Set the arcpy environment to the TL geodatabase
        arcpy.env.workspace = tl_gdb
        arcpy.env.overwriteOutput = True

        # Path to TL tract feature class
        tl_tract = os.path.join(tl_gdb, "TR")

        print("- Loading TL tract feature class into a spatial DataFrame...")
        # Load TL tract feature class into a spatial DataFrame
        tl_sdf = pd.DataFrame.spatial.from_featureclass(tl_tract)
        print(f"- Removing ocean side tract GEOID: {remove_geoid} from TL SDF if it exists...")
        # Remove specific GEOID record if it exists
        tl_sdf = tl_sdf[tl_sdf["GEOID"] != remove_geoid]

        # Ensure GEOID columns are comparable (strings without extra whitespace)
        tl_sdf["GEOID"] = tl_sdf["GEOID"].astype(str).str.strip()
        cr_db["GEOID"] = cr_db["GEOID"].astype(str).str.strip()

        print("- Checking if the number of records between TL SDF and CR DB match before join...")
        diff_count = tl_sdf.shape[0] - cr_db.shape[0]
        if diff_count == 0:
            print(f"The number of records in TL SDF and CR DB match: {tl_sdf.shape[0]} records each.")
        elif diff_count > 0:
            print(f"Warning: TL SDF has {diff_count} more records ({tl_sdf.shape[0]}) than CR DB ({cr_db.shape[0]}).")
        elif diff_count < 0:
            print(f"Warning TL SDF has {-diff_count} fewer records ({tl_sdf.shape[0]}) than CR DB ({cr_db.shape[0]}).")
        
        print("- Joining CR data with TL SDF on GEOID...")
        # Perform a left join: keep all tl_sdf records and add matching cr_db columns
        # If there are overlapping column names besides `GEOID`, keep tl_sdf's versions
        cols_to_merge = [c for c in cr_db.columns if c != "GEOID"]
        tl_sdf = tl_sdf.merge(cr_db[ ["GEOID"] + cols_to_merge ], on="GEOID", how="left")
        print(f"- After join, tl_sdf shape: {tl_sdf.shape}")
        # Path to output CR geodatabase
        cr_gdb = self.prj_dirs["gis_occr_gdb"]

        print(f"- Setting up CR geodatabase: {os.path.basename(cr_gdb)}...")
        # Set the arcpy environment to the feature dataset
        arcpy.env.workspace = cr_gdb
        arcpy.env.overwriteOutput = True

        # Path to output CR feature class
        cr_fc = os.path.join(cr_gdb, f"CRTR{year}")
        print(f"- Creating CR feature class: CRTR{year}...")
        # Remove the output feature class if it already exists
        if arcpy.Exists(cr_fc):
            print(f"  - Deleting existing feature class: CRTR{year}")
            arcpy.Delete_management(cr_fc)
            print(f"  - Deleted existing feature class: CRTR{year}")

        print(f"- Converting merged DataFrame to feature class: CRTR{year}...")
        # Convert the merged DataFrame to a feature class in the geodatabase
        tl_sdf.spatial.to_featureclass(location = cr_fc, overwrite = True, has_z = None, has_m = None, sanitize_columns = False)

        print("- Setting aliases for CR feature class and fields...")
        # Set a friendly alias for the output feature class
        alias_name = f"OC Community Resilience Estimates {year} Census Tracts"
        try:
            # Change the alias name
            arcpy.AlterAliasName(cr_fc, alias_name)
            print(f"  - Alias for 'CRTR{year}' successfully changed to '{alias_name}'.")
        except arcpy.ExecuteError:
            # ArcPy-specific errors
            print("  - ArcPy Error:", arcpy.GetMessages(2))
        except (RuntimeError, OSError, ValueError, TypeError, AttributeError) as e:
            # Specific Python errors
            print("  - Error:", e)

        print("- Setting field aliases based on CR codebook...")
        # Set field aliases on the output feature class from the CR codebook
        for field_key, info in self.cb.items():
            # `cb_cr` entries should have an `alias` value
            alias = info.get("alias") if isinstance(info, dict) else None
            if not alias:
                continue
            try:
                # Only attempt to alter the field if it exists in the output feature class
                fields = arcpy.ListFields(cr_fc, field_key)
                if not fields:
                    # Field not present; skip
                    # (sanitize_columns=False above should preserve names but some fields may be absent)
                    continue
                # Use AlterField to change only the alias (keep the same field name)
                arcpy.AlterField_management(cr_fc, field_key, field_key, alias)
                print(f"  - Field alias for '{field_key}' set to '{alias}'.")
            except arcpy.ExecuteError:
                print(f"  - ArcPy Error altering alias for field {field_key}:", arcpy.GetMessages(2))
            except (RuntimeError, OSError, ValueError, TypeError, AttributeError) as e:
                print(f"  - Error altering alias for field {field_key}:", e)

        print("- Defining metadata for CR feature class...")
        # Define a metadata object for the feature class
        cr_md = md.Metadata(cr_fc)
        cr_md.title = alias_name
        cr_md.tags = "Orange County, California, Community Resilience Estimates, CR, OCCR, Census Tracts"
        cr_md.summary = f"Orange County Community Resilience Estimates for year {year} at Census Tracts geography level."
        cr_md.description = f"Orange County Community Resilience Estimates (OCCR) for year {year} at Census Tracts geography level. The data contains composite social vulnerability indicators derived from U.S. Census data. Version: {self.version}, last updated on {self.data_date}."
        cr_md.credits = "Dr. Kostas Alexandridis, GISP, Data Scientist, OC Public Works Geospatial Services"
        cr_md.accessConstraints = """The feed data and associated resources (maps, apps, endpoints) can be used under a <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">Creative Commons CC-SA-BY</a> License, providing attribution to OC Public Works Geospatial Services. <div><br /></div><div>We make every effort to provide the most accurate and up-to-date data and information. Nevertheless the data feed is provided, 'as is' and OC Public Work's standard <a href="https://www.ocgov.com/contact-county/disclaimer" target="_blank">Disclaimer</a> applies.</div><div><br /></div><div>For any inquiries, suggestions or questions, please contact:</div><div><br /></div><div style="text-align:center;"><a href="https://www.linkedin.com/in/ktalexan/" target="_blank"><b>Dr. Kostas Alexandridis, GISP</b></a><br /></div><div style="text-align:center;">GIS Analyst | Spatial Complex Systems Scientist</div><div style="text-align:center;">OC Public Works Geospatial Services</div><div style="text-align:center;"><div>601 N. Ross Street, P.O. Box 4048, Santa Ana, CA 92701</div><div>Email: <a href="mailto:kostas.alexandridis@ocpw.ocgov.com" target="_blank">kostas.alexandridis@ocpw.ocgov.com</a> | Phone: (714) 967-0826</div></div>"""
        cr_md.thumbnailUri = "https://ocpw.maps.arcgis.com/sharing/rest/content/items/67ce28a349d14451a55d0415947c7af3/data"
        cr_md.save()

        print(f"CR feature class for year {year} created successfully at {cr_fc}.")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
