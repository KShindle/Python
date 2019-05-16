#   -----------------------------------------------------------------------------------------------------
#   | 		PYTHON                          Public PRC Extract Script.py |
#   |  		      				Property Record Card Creation Tool     			|
#   | 		                                        By                                         			|
#   | 		                                    Kara Shindle                                   			|
#   |  		                                County of Franklin                                			|
#   |               		                                                                    		|
#   |               		                Built:  03/13/2019                                    		|
#   -----------------------------------------------------------------------------------------------------


##Script Tool to be published as GP Service for generating Property Recorad Cards from data updated daily.


## import modules & set environment
import arcpy.mapping
import os

##set overwrite option to True
arcpy.env.overwriteOutput = True

##set variable to get parameters for Universal Parcel Identifer (UPI)
UPI = arcpy.GetParameterAsText(0).strip()                               #remove whitespace.  Parcel Adminstrator adds trailing whitespaces to parcel numbers when linked to ArcMap due to UPI Format

#makes sure UPI is all uppercase so record can be located
formatedUPI = UPI.upper()

#Set path for Data Driven Pages MXD - PRC Page 1
parMXD1 = arcpy.mapping.MapDocument(r"S:\\PUBLIC_RECORDS.mxd")          

#specify location user wants PDF saved to on their comupter
outputPath = arcpy.GetParameterAsText(1)

arcpy.AddMessage('PRC will be saved at: ' + outputPath)




#If then else staement for handling a UPI that has an incorrect number of characters
if len(UPI) < 20:
	arcpy.AddError("UPI doesn't have enough characters")
elif len(UPI) > 23:
	arcpy.AddError("UPI has too many characters.")
else:
	try:

		#store final PDF path in variable for exporting
		finalPDF = os.path.join(outputPath, formatedUPI) + ".pdf"

		#sets Page ID from UPI & exports first DDP
		pageID = parMXD1.dataDrivenPages.getPageIDFromName(formatedUPI)
		parMXD1.dataDrivenPages.currentPageID = pageID
		parMXD1.dataDrivenPages.exportToPDF(finalPDF, "CURRENT")

		arcpy.AddMessage("Card Generated for {}".format(formatedUPI))

	except Exception:
		e = sys.exc_info()[1]
		print(e.args[0])
		arcpy.AddError(e.args[0])
