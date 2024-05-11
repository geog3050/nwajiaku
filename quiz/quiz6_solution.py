def calculateAreaOfPolygonAInPolygonB(input_geodatabase, fcA, fcB, fcB_id_field):
   import arcpy
   import sys

   arcpy.env.overwriteOutput = True
   
   if arcpy.Exists(input_geodatabase):
      arcpy.env.workspace = input_geodatabase
      print("Environment workspace is set to: ", input_geodatabase)
   else:
      print("Workspace", input_geodatabase, "does not exist!")
      sys.exit(1)

   try:
      desc_fcA = arcpy.Describe(fcA)
      desc_fcB = arcpy.Describe(fcB)

      if desc_fcA.shapeType != "Polygon":
         print("Error shapeType: ", fcA, "need to be a polygon type!")
         sys.exit(1)

      if desc_fcB.shapeType != "Polygon":
         print("Error shapeType: ", fcB, "need to be a polygon type!")
         sys.exit(1)

      if desc_fcA.spatialReference.name != desc_fcB.spatialReference.name:
         print("Coordinate system error: Spatial reference of", fcA, "and", fcB, "should be the same.")
         sys.exit(1)

      fields = [f.name for f in arcpy.ListFields(fcB)]
      if fcB_id_field in fields:
         print(fcB_id_field, "exists in", fcB)
      else:
         print(fcB_id_field, "does NOT exist in", fcB)
         sys.exit(1)

      arcpy.AddField_management(fcB, "area_sqmi", "DOUBLE")
      print("Area field is added to", fcB)
      # calculate area in square miles
      arcpy.CalculateGeometryAttributes_management(fcB, [["area_sqmi", "AREA_GEODESIC"]], "MILES_US")
      print("Area in sq miles are calculated for", fcB)

      fcB_inters_fcA = "fcB_intersects_fcA"
      arcpy.Intersect_analysis([fcB, fcA], fcB_inters_fcA)
      print(fcB, "is intersected with", fcA)

      areaA_field = "areaA_sqmi"
      arcpy.AddField_management(fcB_inters_fcA, areaA_field, "DOUBLE")
      print("Area in sq miles field is added to the intersected feature class: ", fcB_inters_fcA)
      
      # calculate area of fcB in fcA in square miles
      arcpy.CalculateGeometryAttributes_management(fcB_inters_fcA, [[areaA_field, "AREA_GEODESIC"]], "MILES_US")
      print("Area in sq miles are calculated for the intersected feature class: ", fcB_inters_fcA)

      fcB_dict = dict()
      with arcpy.da.SearchCursor(fcB_inters_fcA, [fcB_id_field, areaA_field]) as cursor:
          for row in cursor:
              id_ = row[0]
              if id_ in fcB_dict.keys():
                  fcB_dict[id_] += row[1]
              else:
                  fcB_dict[id_] = row[1]

      arcpy.Delete_management(fcB_inters_fcA)
      print("Temporary intersection feature class", fcB_inters_fcA, "is deleted")
         
      print("Area of multiple polygons in", fcA, "is summed in a dictionary of", fcB, "with", fcB_id_field)
      arcpy.AddField_management(fcB, areaA_field, "DOUBLE")

      with arcpy.da.UpdateCursor(fcB, [fcB_id_field, areaA_field]) as cursor:
         for row in cursor:
            if row[0] in fcB_dict.keys():
               row[1] = fcB_dict[row[0]]
            else:
               row[1] = 0
            cursor.updateRow(row)
      print("Total area of polygons in", fcA, "is updated for each polygon in", fcB)

      areaA_pct_field = "areaA_pct"
      arcpy.AddField_management(fcB, areaA_pct_field, "DOUBLE")
      arcpy.CalculateField_management(fcB, areaA_pct_field, "!" +areaA_field+ "!/!area_sqmi!", "PYTHON3")
      print(areaA_pct_field, " was succesfully updated in ", fcB)

   except Exception:
      e = sys.exc_info()[1]
      print(e.args[0])

