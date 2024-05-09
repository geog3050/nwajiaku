############################################################################################################

#######################  -  GEOG 3050 Quiz 5  -  #######################

### Upload a python file (py) that creates variable buffers around airport facilities. ###
## Buffers are based on the 'FEATURE' field and 'TOT_ENP' (total enplanements). ##
## 'Airport' features with > 10,000 enplanements receive a 15,000-meter buffer; those below have a 10,000-meter buffer. ##
## 'Seaplane base' facilities with > 1,000 enplanements get a 7,500-meter buffer. ##
## No buffers for facilities not matching these criteria or with minimal activity. ##
## Save buffers into a separate shapefile named buffer_airports. ###

############################################################################################################ 

def hawkid():
    return(["Loretta Nwajiaku", "nwajiaku"])

def createBufferAirport(fcPoint, featureFieldName, enpFieldName, workspace):
    # Import system modules
    import os
    import arcpy
    import sys
    
    # Create the buffer analysis
    try:
        # Check the shape type
        desc_fcPoint = arcpy.Describe(fcPoint)
        if desc_fcPoint.shapeType != "Point":
            print("ERROR: Feature class " + fcPoint + " is NOT a Point type!")
            sys.exit(-1)
        
        distanceUnit = "Meters" # Assuming shapefile is in meters to simplify
        
        # Add buffer distance field
        arcpy.AddField_management(fcPoint, "bufferDist", "TEXT")
        with arcpy.da.UpdateCursor(fcPoint, [featureFieldName, enpFieldName, "bufferDist"]) as cursor:
            for row in cursor:
                featureType = row[0].lower()
                totEnp = row[1]

                if featureType == "airport" and totEnp > 10000:
                    row[2] = "15000 Meters"
                elif featureType == "airport" and totEnp <= 10000:
                    row[2] = "10000 Meters"
                elif featureType == "seaplane base" and totEnp > 1000:
                    row[2] = "7500 Meters"
                else:
                    row[2] = None  # Exclude from buffer creation
                    
                cursor.updateRow(row)

        # Exclude features without a buffer distance defined
        query = "bufferDist IS NOT NULL"
        arcpy.SelectLayerByAttribute_management(fcPoint, "NEW_SELECTION", query)
        
        # Create buffer feature class
        fcBuffer = "buffer_" + fcPoint
        arcpy.Buffer_analysis(fcPoint, fcBuffer, "bufferDist")
        print("Buffers based on feature type and enplanement levels were created and saved in " + fcBuffer)

        # Change feature class to shapefile
        arcpy.FeatureClassToShapefile_conversion(fcBuffer, workspace)
        
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
