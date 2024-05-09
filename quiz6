import arcpy
arcpy.env.overwriteOutput = True

def calculate_percent_area_of_polygon_a_in_polygon_b(input_geodatabase, fcPolygonA, fcPolygonB, idFieldPolygonB):
    try:
        # workspace
        arcpy.env.workspace = input_geodatabase
        
        # Area of fcPolygon A
        arcpy.AddField_management(fcPolygonA, "PARK_AREA", "DOUBLE")
        arcpy.CalculateGeometryAttributes_management(fcPolygonA, [["PARK_AREA", "AREA"]], area_unit="SQUARE_METERS")
        
        # Area of fcPolygonB
        arcpy.AddField_management(fcPolygonB, "Area_Blockgroup", "DOUBLE")
        arcpy.CalculateGeometryAttributes_management(fcPolygonB, [["Area_Blockgroup", "AREA"]], area_unit="SQUARE_METERS")
        
        # Spatial join to calculate intersection area
        arcpy.analysis.SpatialJoin(fcPolygonB, fcPolygonA, "intersection", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT")
        
        # Calculate percentage area
        arcpy.AddField_management("intersection", "Percentage_Area", "DOUBLE")
        expression = "!PARK_AREA! / !Area_Blockgroup! * 100" 

        arcpy.CalculateField_management("intersection", "Percentage_Area", expression, "PYTHON")
        # Join the calculated percentage area to the block-grpups
        arcpy.JoinField_management(fcPolygonB, idFieldPolygonB, "intersection", idFieldPolygonB, ["Percentage_Area"])
        #delete the temporary layer
        arcpy.Delete_management("intersection")
      #arcpy exception
    except arcpy.ExecuteError:
        print("ArcPy error occurred")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#TEST
input_geodatabase = "C:/Users/nwajiaku/Downloads/ASSIGNMENT6/ASSIGNMENT6.gdb"
fcPolygonA = "parks"
fcPolygonB = "block_groups"
idFieldPolygonB = "OBJECTID"  # Change this to your actual ID field name

# Call the function
calculate_percent_area_of_polygon_a_in_polygon_b(input_geodatabase, fcPolygonA, fcPolygonB, idFieldPolygonB)
