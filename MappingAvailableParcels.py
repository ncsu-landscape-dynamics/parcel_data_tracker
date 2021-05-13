# Author: Samantha Whisenant

import arcpy

directory = 'E:/PEP/'  # Change to your local directory where data folder will be stored

# Convert csv to dbase and join to shapefile

arcpy.env.workspace = directory + 'data'
arcpy.env.overwriteOutput = True

Input_Table = 'Parcels.csv'
Output_Folder = directory + 'data'
Parcel_dbase = arcpy.TableToDBASE_conversion(Input_Table, Output_Folder)

copyInData = 'US_Counties.shp'
copyOutData = directory + 'data/parcelCountyJoin.shp'

arcpy.Copy_management(copyInData, copyOutData)

inFeature = directory + 'data/parcelCountyJoin.shp'
joinFeature = directory + 'data/Parcels.dbf'
inField = "COUNTY2"
joinField = "County2"

joinCsv = arcpy.JoinField_management(inFeature, inField, joinFeature, joinField)

# Add joined shapefile to map, assign symbology, and export to PNG

myMap = directory + 'data/parcelsMap.mxd'

mxd = arcpy.mapping.MapDocument(myMap)

dfs = arcpy.mapping.ListDataFrames(mxd)
df = dfs[0]
layerObj = arcpy.mapping.Layer(directory + 'data/parcelCountyJoin.shp')
arcpy.mapping.AddLayer(df, layerObj, 'BOTTOM')

lyrs = arcpy.mapping.ListLayers(mxd, '', df)
layerToModify = lyrs[1]

srcLay = directory + 'data/US_Counties.lyr'
srcLayObj = arcpy.mapping.Layer(srcLay)
arcpy.mapping.UpdateLayer(df, layerToModify, srcLayObj)

arcpy.RefreshActiveView()

parcelLayer = arcpy.mapping.ListLayers(mxd, "parcelCountyJoin", df)[0]
arcpy.SelectLayerByAttribute_management(parcelLayer, "NEW_SELECTION", "Location = 'Mainland'")
df.extent = parcelLayer.getSelectedExtent(False)
df.scale = df.scale * 1.1
arcpy.SelectLayerByAttribute_management(parcelLayer, "CLEAR_SELECTION")

imageName1 = 'Parcels_by_Counties1'
arcpy.mapping.ExportToPNG(mxd, imageName1)

parcelLayer = arcpy.mapping.ListLayers(mxd, "parcelCountyJoin", df)[0]
arcpy.SelectLayerByAttribute_management(parcelLayer, "NEW_SELECTION", "Location = 'Alaska'")
df.extent = parcelLayer.getSelectedExtent(False)
df.scale = df.scale * 1.1
arcpy.SelectLayerByAttribute_management(parcelLayer, "CLEAR_SELECTION")

imageName2 = 'Parcels_by_Counties2'
arcpy.mapping.ExportToPNG(mxd, imageName2)

parcelLayer = arcpy.mapping.ListLayers(mxd, "parcelCountyJoin", df)[0]
arcpy.SelectLayerByAttribute_management(parcelLayer, "NEW_SELECTION", "Location = 'Hawaii'")
df.extent = parcelLayer.getSelectedExtent(False)
df.scale = df.scale * 1.1
arcpy.SelectLayerByAttribute_management(parcelLayer, "CLEAR_SELECTION")

imageName3 = 'Parcels_by_Counties3'
arcpy.mapping.ExportToPNG(mxd, imageName3)

copyName = directory + 'data/parcelsMap2.mxd'
mxd.saveACopy(copyName) 
del mxd

# Create HTML report

image1 = directory + imageName1 + '.png'
image2 = directory + imageName2 + '.png'
image3 = directory + imageName3 + '.png'


beginning = '''<!DOCTYPE html>
 <html>
 <body>'''

middle = '''
 <h1>Mapping Available Parcels in the United States</h1>
 <img src='{0}' width="100%" >\n
 <img src='{1}' width="100%" >\n
 <img src='{2}' width="100%" >\n'''.format(image1, image2, image3)


end = ''' </body>
 </html>
 '''

htmlfile =  directory + 'data/Parcels_HTML.html'
with open(htmlfile,'w') as outf:
    outf.write(beginning)
    outf.write(middle)
    outf.write(end)
    
print '{0} created.'.format(htmlfile)
