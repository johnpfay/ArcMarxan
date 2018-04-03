import arcpy
import os, csv, numpy, datetime

"""
/***************************************************************************
 ArcMarxan
                             -------------------
        begin                : 2016-08-29
        updated              : 2017-08-09
        copyright            : (C) 2016 by Apropos Information Systems Inc.
        email                : info@aproposinfosystems.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   any later version.                                                    *
 *                                                                         *
 ***************************************************************************/
"""

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "ArcMarxan Toolbox (1.0.3)"
        self.alias = "arcmarxan"

        # List of tool classes associated with this toolbox
        self.tools = [MarxanProject,Boundary,Features,PlanningUnits,SelectedSummary]

#
# input.dat creation tool
#
class MarxanProject(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Input File and Folders"
        self.description = "Create input.dat file and marxan project folders. This input.dat file can be edited with a text editor (eg. NotePad) after creation."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
       
        # output folder
        output_folder = arcpy.Parameter(
            displayName="Marxan project folder (folder for input.dat and input and output folders)",
            name="output_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        params = [output_folder]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        # process fields to ensure that only common fields are kept and
        # only fields of the appropriate type for the planning unit id
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        paramAsString = parameters[0].valueAsText
        baseDir = paramAsString.replace("\\","/")
        if os.path.exists(baseDir):
            iDir = os.path.join(baseDir,'input')
            if not os.path.exists(iDir):
                os.mkdir(iDir)
            oDir = os.path.join(baseDir,'output')
            if not os.path.exists(oDir):
                os.mkdir(oDir)
            puDir = os.path.join(baseDir,'pu')
            if not os.path.exists(puDir):
                os.mkdir(puDir)
            iName = os.path.join(baseDir,'input.dat')
            self.createInputFile(iName)
        else:
            arcpy.AddError('Folder now found %s' % baseDir)
        
        return

    def createInputFile(self,outFName):

        #
        # formatAsME - format as Marxan Exponent format like 
        #              Input File Editor
        #
        def formatAsME(inVal):
            outStr = "%.14E" % float(inVal)
            parts = outStr.split('E')
            sign = parts[1][:1]
            exponent = "%04d" % float(parts[1][1:])
            outStr = parts[0] + 'E' +  sign + exponent
            return(outStr)
            
        f = open(outFName, 'w')
        creditText = "Input file for Annealing program.\n\n"
        creditText += "This file generated by ArcMarxan Toolbox version 1.0.3\n" 
        creditText += "created by Apropos Information Systems Inc.\n\n"
        f.write(creditText)
        f.write("General Parameters\n")
        f.write("VERSION %s\n" % '0.1')
        f.write("BLM %s\n" % formatAsME(1.0))
        f.write("PROP %s\n" % formatAsME(0.5))
        f.write("RANDSEED %d\n" % -1)
        f.write("NUMREPS %d\n" % 100)
        f.write("\nAnnealing Parameters\n")
        f.write("NUMITNS %d\n" % 1000000)
        f.write("STARTTEMP %s\n" % formatAsME(-1.0))
        f.write("COOLFAC %s\n" % formatAsME(-1.0))
        f.write("NUMTEMP %d\n" % 10000)
        f.write("\nCost Threshold\n")
        f.write("COSTTHRESH %s\n" % formatAsME(0.0))
        f.write("THRESHPEN1 %s\n" % formatAsME(0.0))
        f.write("THRESHPEN2 %s\n" % formatAsME(0.0))
        f.write("\nInput Files\n")
        f.write("INPUTDIR %s\n" % 'input')
        f.write("SPECNAME %s\n" % 'spec.dat')
        f.write("PUNAME %s\n" % 'pu.dat')
        f.write("PUVSPRNAME %s\n" % 'puvsp.dat')
        f.write("BOUNDNAME %s\n" % 'bound.dat')
        f.write("MATRIXSPORDERNAME %s\n" % 'puvsp_sporder.dat')
        f.write("\nSave Files\n")
        f.write("SCENNAME %s\n" % 'output')
        f.write("SAVERUN %d\n" % 3)
        f.write("SAVEBEST %d\n" % 3)
        f.write("SAVESUMMARY %d\n" % 3)
        f.write("SAVESCEN %d\n" % 3)
        f.write("SAVETARGMET %d\n" % 3)
        f.write("SAVESUMSOLN %d\n" % 3)
        f.write("SAVELOG %d\n" % 3)
        f.write("SAVESNAPSTEPS %d\n" % 0)
        f.write("SAVESNAPCHANGES %d\n" % 0)
        f.write("SAVESNAPFREQUENCY %d\n" % 0)
        f.write("OUTPUTDIR %s\n" % 'output')
        f.write("\nProgram control.\n" )
        f.write("RUNMODE %d\n" % 1)
        f.write("MISSLEVEL %s\n" % formatAsME(0.95))
        f.write("ITIMPTYPE %d\n" % 1)
        f.write("HEURTYPE %d\n" % -1)
        f.write("CLUMPTYPE %d\n" % 0)
        f.write("VERBOSITY %d\n" % 2)
        f.write("SAVESOLUTIONSMATRIX %s\n\n" % '3')
        f.close()
        
#
# bound.dat creation tool
#
class Boundary(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Boundary File"
        self.description = "Create the bound.dat file. Once created this file does not require editing."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # boundary layer 
        boundary_layer = arcpy.Parameter(
            displayName="Planning unit layer (source of bound.dat file)",
            name="boundary_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        boundary_layer.filter.list = ["Polygon"]
        
        # field name 
        pu_field = arcpy.Parameter(
            displayName="Planning unit id field",
            name="pu_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        pu_field.parameterDependencies = [boundary_layer.name]
        pu_field.filter.list = ["Short","Long","Double","Float"]

        # boundary method
        boundary_method = arcpy.Parameter(
            displayName="Boundary method (how will lengths between planning units be set)",
            name="boundary_method",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        boundary_method.filter.list = ["Single Value","Measured","Weighted","Field"]
        boundary_method.value = "Single Value"
        
        # boundary treatment
        boundary_treatment = arcpy.Parameter(
            displayName="Boundary treatment (how values for PUs on perimeter of study area will be set)",
            name="boundary_treatment",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        boundary_treatment.filter.list = ["Full Value","Half Value","Exclude"]
        boundary_treatment.value = "Full Value"
            
        # boundary value
        boundary_value = arcpy.Parameter(
            displayName="Single value (value for all boundaries regardless of measured length)",
            name="boundary_value",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input",
            enabled=False)
        
        # field name 
        calc_field_name = arcpy.Parameter(
            displayName="Calculation field name (field to weight or assign boundary lengths)",
            name="calc_field_name",
            datatype="Field",
            parameterType="Optional",
            direction="Input",
            enabled=False)
        calc_field_name.parameterDependencies = [boundary_layer.name]
        calc_field_name.filter.list = ["Short","Long","Double","Float"]
        
        # field calculation
        field_calc_method = arcpy.Parameter(
            displayName="Calculation method (how to assign boundary length if values between adjacent planning units differ)",
            name="field_calc_method",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        field_calc_method.filter.list = ["Mean","Maximum","Minimum"]
        field_calc_method.value = "Mean"

        # output folder
        marxan_input_folder = arcpy.Parameter(
            displayName="Marxan input folder (place to write bound.dat file)",
            name="marxan_input_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
            
        params = [boundary_layer, pu_field, boundary_method, boundary_treatment, boundary_value, calc_field_name, field_calc_method, marxan_input_folder]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        # convert paramters array to named values for code clarity
        boundary_method = parameters[2]
        boundary_treatment = parameters[3]
        boundary_value = parameters[4]
        calc_field_name = parameters[5]
        field_calc_method = parameters[6]
        
        if boundary_method.value:
            if boundary_method.valueAsText == "Single Value":
                boundary_value.enabled = True
                if boundary_value.value is None:
                    boundary_value.value = 1.0
                calc_field_name.enabled = False
                field_calc_method.enabled = False
            else:
                boundary_value.enabled = False
                boundary_value.value = None
                if boundary_method.valueAsText in ["Weighted","Field"]:
                    calc_field_name.enabled = True
                    field_calc_method.enabled = True
                else: # is Measured
                    calc_field_name.enabled = False
                    field_calc_method.enabled = False
                    calc_field_name.value = ""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        
        # convert paramters array to named values for code clarity
        boundary_method = parameters[2]
        boundary_treatment = parameters[3]
        boundary_value = parameters[4]
        calc_field_name = parameters[5]
        field_calc_method = parameters[6]
        
        # force values for optional fields based on boundary_method
        if boundary_method.value:
            if boundary_method.valueAsText in ["Weighted","Field"]:
                if not calc_field_name.value:
                    calc_field_name.setErrorMessage(
                        "Must selected field if using weighted or field method")
            if boundary_method.valueAsText == "Single Value":
                if not boundary_value.value:
                    boundary_value.setErrorMessage(
                        "Must set value if using single value method")
                        
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        #
        # The approach is straightforward. Marxan must account for outer boundaries therefore
        # a new layer must be created which has an outer boundary. The natural way to do this is
        # to dissolve the pu layer, then buffer it and union the result with the original pu layer.
        # The next step is to set the PUID of the outer buffer to -1 as -1 is not a permitted pu id 
        # in Marxan. Then the arcpy polygon neighbors analysis runs and gives us a table. When one of 
        # the puid's equals -1 then that indicates an outer boundary and the id is set to match the 
        # other id and thus becomes the "self" boundary. The end result is sorted and written to disk.
        #
        
        # convert paramters array to named values for code clarity
        boundary_layer = parameters[0].valueAsText
        pu_field = parameters[1].valueAsText
        boundary_method = parameters[2].valueAsText
        boundary_treatment = parameters[3].valueAsText
        boundary_value = parameters[4].value
        calc_field_name = parameters[5].valueAsText
        field_calc_method = parameters[6].valueAsText
        marxan_input_folder = parameters[7].valueAsText
        
        # dissolve the pulayer
        #dissolveFeatClass = arcpy.env.workspace + "\\amt_temp_dissolve"
        #arcpy.Dissolve_management(boundary_layer, dissolveFeatClass)
        
        # buffer and dissolve layer in one step
        buffFeatClass = arcpy.env.workspace + "\\amt_temp_buffer"
        arcpy.Buffer_analysis(boundary_layer, buffFeatClass, '100 Meters', dissolve_option="ALL")
        # union buffered layer with the pulayer and delete temp source
        unionFeatClass = arcpy.env.workspace + "\\amt_temp_union"
        arcpy.Union_analysis([buffFeatClass, boundary_layer], unionFeatClass)
        arcpy.Delete_management(buffFeatClass)
        # update planning unit id to equal -1 
        # based on knowledge that FID_boundary_layer field will be set to -1 or 0 because 
        # the field didn't exist in the source layer for the boundary layer
        field_names = [f.name for f in arcpy.ListFields(unionFeatClass)]
        with arcpy.da.UpdateCursor(unionFeatClass,[field_names[5],pu_field]) as cursor:
            for row in cursor:
                if row[0] == -1 or row[0] == 0:
                    row[1] = -1
                    cursor.updateRow(row)
                    break
        # get boundaries and lengths
        outDBF = os.path.join(marxan_input_folder,'tempBound.dbf')
        if boundary_method in ["Weighted","Field"]:
            arcpy.PolygonNeighbors_analysis(unionFeatClass,outDBF,[pu_field,calc_field_name],both_sides="NO_BOTH_SIDES",out_linear_units="METERS")
        else:
            arcpy.PolygonNeighbors_analysis(unionFeatClass,outDBF,[pu_field],both_sides="NO_BOTH_SIDES",out_linear_units="METERS")
        boundList = []
        x = 0
        for row in arcpy.da.SearchCursor(outDBF,'*'):
            x += 1
            id1 = int(row[1])
            id2 = int(row[2])
            if id1 == -1:
                id1 = id2
            if boundary_method in ["Weighted","Field"]:
                nodes = row[6]
                sideLen = row[5]
            else:
                nodes = row[4]
                sideLen = row[3]
            # note: node > 0 means a touching corner, not a touching side
            if nodes == 0 and sideLen > 0:
                if boundary_method in ["Weighted","Field"]:
                    if id1 == id2 and int(row[1]) == -1:
                        # note this is for the perimeter where the buffered calc field value is zero 
                        # and so the difference method will fail
                        fValue = row[4]
                    else:
                        if field_calc_method == 'Mean':
                            fValue = (row[3]+row[4])/2.0
                        elif field_calc_method == 'Maximum':
                            if row[3] > row[4]:
                                fValue = row[3]
                            else:
                                fValue = row[4]
                        else:
                            if row[3] < row[4]:
                                fValue = row[3]
                            else:
                                fValue = row[4]
                if boundary_method == 'Measured':
                    bValue = sideLen
                elif boundary_method == 'Weighted':
                    bValue = sideLen * fValue
                elif boundary_method == 'Field':
                    bValue = fValue
                elif boundary_method == 'Single Value':
                    bValue = boundary_value
                # deal with boundary units special cases
                if id1 == id2:
                    if boundary_treatment in ["Full Value","Half Value"]:
                        if boundary_treatment == "Half Value":
                            bValue = bValue / 2.0
                        boundList.append([int(id1),int(id2),bValue])
                else:
                    boundList.append([int(id1),int(id2),bValue])
        boundList.sort()
        # convert to bound.dat file
        oFileName = os.path.join(marxan_input_folder,'bound.dat')
        oFile = open(oFileName,'w')
        oFile.write('id1\tid2\tboundary\n')
        for rec in boundList:
            oFile.write('%d\t%d\t%f\n' % (rec[0],rec[1],rec[2]))   
        oFile.close()
        arcpy.Delete_management(outDBF)
        arcpy.Delete_management(unionFeatClass)
        return

#
# spec.dat, puvsp.dat and puvsp_sporder.dat creation tool
#
class Features(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Feature Files"
        self.description = "Create spec.dat, puvsp.dat and puvsp_sporder.dat files. The spec.dat file will need to be edited manually after creation using a spreadsheet program. See documentation for more details."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
       
        # pu layer
        pu_layer = arcpy.Parameter(
            displayName="Planning unit layer (with feature / species values)",
            name="pu_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        pu_layer.filter.list = ["Polygon"]
        
        # pu field name 
        pu_field = arcpy.Parameter(
            displayName="Planning unit id field",
            name="pu_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        pu_field.parameterDependencies = [pu_layer.name]
        pu_field.filter.list = ["Short","Long","Double","Float"]

        # feauture field names
        feature_field_names = arcpy.Parameter(
            displayName="Feature fields (values for each feature / species of interest)",
            name="feature_field_names",
            datatype="Field",
            parameterType="Required",
            direction="Input",
            multiValue=True)
        feature_field_names.parameterDependencies = [pu_layer.name]
        feature_field_names.filter.list = ["Short","Long","Double","Float"]

        # output folder
        marxan_input_folder = arcpy.Parameter(
            displayName="Marxan input folder (place to write spec.dat, puvsp.dat and puvsp_sporder.dat files)",
            name="marxan_input_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        params = [pu_layer, pu_field, feature_field_names, marxan_input_folder]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        pu_layer = parameters[0].valueAsText
        pu_field = parameters[1].valueAsText
        feature_field_names = parameters[2].valueAsText.split(';')
        marxan_input_folder = parameters[3].valueAsText
        # create field list
        fldsRef = []
        flds =[]
        flds.append(pu_field)
        x = 0
        for fld in feature_field_names:
            x += 1
            fldsRef.append([x,fld])
            flds.append(fld)
        # create spec.dat file
        specFName = os.path.join(marxan_input_folder,'spec.dat')
        self.createFeatFile(fldsRef,specFName)
        # create puvsp.dat and puvsp_sporder.dat files
        f1 = os.path.join(marxan_input_folder,'puvsp.dat')
        f2 = os.path.join(marxan_input_folder,'puvsp_sporder.dat')
        self.createFeatVsPUFiles(flds,fldsRef,f1,f2,pu_layer,pu_field)
        return
        
    def createFeatFile(self,fieldRefList,specFName):

        # make copy of old spec.dat file so SPF and targets are not lost
        if os.path.exists(specFName):
            nName = specFName + '.backup_%s' % datetime.datetime.now().isoformat()[:19].replace(':','').replace('-','')
            os.rename(specFName,nName)
        header = 'id\tprop\ttarget\ttargetocc\tspf\tname\n'
        f = open(specFName,'w')
        f.write(header)
        for rec in fieldRefList:
            f.write('%d\t0.0\t0.0\t0\t1.0\t%s\n' % (rec[0],rec[1]))
        f.close()
        
    def createFeatVsPUFiles(self,flds,fieldRefList,puvFName,puvSFname,pu_layer,pu_field):
    
        unOrdered = []
        # step through file and put data into unordered list
        for row in arcpy.da.SearchCursor(pu_layer,flds):
            for rec in fieldRefList:
                if float(row[flds.index(rec[1])]) > 0:
                    unOrdered.append((rec[0],int(row[flds.index(pu_field)]),float(row[flds.index(rec[1])])))
        # use numpy to sort it quickly
        dtype = [('species', int),('pu', int),('amount', float)]
        npArray = numpy.array(unOrdered,dtype=dtype)
        # create puvsp order
        sList = list(numpy.sort(npArray, order=['pu','species']))
        # write results
        puf = open(puvFName, 'w')
        puf.write("species\tpu\tamount\n")
        for rec in sList:
            puf.write('%d\t%d\t%f\n' % (rec[0],rec[1],rec[2]))
        puf.close()
        # create puvsp_sporder order
        sList = list(numpy.sort(npArray,order=['species','pu']))
        # write results
        spf = open(puvSFname, 'w')
        spf.write("species\tpu\tamount\n")
        for rec in sList:
            spf.write('%d\t%d\t%f\n' % (rec[0],rec[1],rec[2]))
        spf.close()
    
#
# pu.dat creation tool
#
class PlanningUnits(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Planning Units File"
        self.description = "Create the pu.dat file. Once created this file does not require editing."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # pu layer 
        pu_layer = arcpy.Parameter(
            displayName="Planning unit layer",
            name="pu_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        pu_layer.filter.list = ["Polygon"]
        
        # pu field name 
        pu_field = arcpy.Parameter(
            displayName="Planning unit id field",
            name="pu_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        pu_field.parameterDependencies = [pu_layer.name]
        pu_field.filter.list = ["Short","Long","Double","Float"]

        # cost field name 
        cost_field = arcpy.Parameter(
            displayName="Planning unit cost field (costs for each planning unit)",
            name="cost_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        cost_field.parameterDependencies = [pu_layer.name]
        cost_field.filter.list = ["Short","Long","Double","Float"]

        # status field name 
        status_field = arcpy.Parameter(
            displayName="Planning unit status field (status values for each planning unit)",
            name="status_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        status_field.parameterDependencies = [pu_layer.name]
        status_field.filter.list = ["Short","Long","Double","Float"]

        # input folder
        marxan_input_folder = arcpy.Parameter(
            displayName="Marxan input folder (place to write pu.dat file)",
            name="marxan_input_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        params = [pu_layer, pu_field, cost_field, status_field, marxan_input_folder]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        pu_layer = parameters[0].valueAsText
        pu_field = parameters[1].valueAsText
        cost_field = parameters[2].valueAsText
        status_field = parameters[3].valueAsText
        marxan_input_folder = parameters[4].valueAsText
        # pull the data
        flds = []
        fld_string = ''
        for fld in arcpy.ListFields(pu_layer):
            if fld.name in [pu_field, cost_field, status_field]:
                flds.append(fld.name)
                fld_string = fld_string + ';' + fld.name
        puList = []
        for row in arcpy.da.SearchCursor(pu_layer,flds):
            cost = row[flds.index(cost_field)]
            if not cost: cost = 0
            if not status: status = 0
        # sort by puid and write file
        puList.sort()
        oFileName = os.path.join(marxan_input_folder,'pu.dat')
        oFile = open(oFileName,'w')
        #oFile.write(pu_layer + '\n')
        #oFile.write(fld_string + '\n')
        oFile.write('id\tcost\tstatus\n')
        for rec in puList:
            oFile.write('%d\t%f\t%d\n' % (rec[0],rec[1],rec[2]))   
        oFile.close()

        return
     
#
# summary report of selected features creation tool
#
class SelectedSummary(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Report Features for Selected Planning Units"
        self.description = "Create summary of results for selected planning units. The output is a .csv file that can be opened in any spreadsheet software."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # pu layer 
        pu_layer = arcpy.Parameter(
            displayName="Planning unit layer (with some of the planning units selected)",
            name="pu_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        pu_layer.filter.list = ["Polygon"]
        
        # field name 
        pu_field = arcpy.Parameter(
            displayName="Planning unit id field",
            name="pu_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        pu_field.parameterDependencies = [pu_layer.name]
        pu_field.filter.list = ["Short","Long","Double","Float"]

        # input folder
        input_folder = arcpy.Parameter(
            displayName="Marxan input folder (with spec.data and puvsp.dat files)",
            name="input_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        # output file
        output_file = arcpy.Parameter(
            displayName="Report output file name",
            name="output_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")
        output_file.filter.list = ['csv']
            
        params = [pu_layer,pu_field,input_folder,output_file]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        pu_layer = parameters[0].valueAsText
        pu_field = parameters[1].valueAsText
        input_folder = parameters[2].valueAsText
        output_file = parameters[3].valueAsText
        # 
        # step 1 - get field location and PU Id list
        #
        flds = []
        fld_string = ''
        puCount = int(arcpy.GetCount_management(pu_layer).getOutput(0))
        if puCount == 0:
            return
        for fld in arcpy.ListFields(pu_layer):
            if fld.name in [pu_field]:
                flds.append(fld.name)
                fld_string = fld_string + ';' + fld.name
        puIdList = []
        for row in arcpy.da.SearchCursor(pu_layer,flds):
            puIdList.append(int(row[flds.index(pu_field)]))
        # sort by puid 
        puIdList.sort()
        # 
        # step 2 - read spec file to get internal feature ids
        #
        specFile = os.path.join(input_folder,'spec.dat')
        if os.path.exists(specFile):
            sniffer = csv.Sniffer()
            f = open(specFile,'r')
            contents = f.readlines()
            f.close()
            dialect = sniffer.sniff(contents[0])
            if dialect.delimiter not in (',','\t'):
                messages.addErrorMessage('spec.dat format not recognized')
                raise arcpy.ExecuteError
            specRecs = {}
            for specLine in contents:
                vals = specLine.strip().split(dialect.delimiter)
                if vals[0] != 'id':
                    specRecs[int(vals[0])] = vals[5]
        else:
            raise Exception
            pass 
            # should raise error here
        # 
        # step 3 - read puvsp file 
        #
        # aggregate data
        puvspFile = os.path.join(input_folder,'puvsp.dat')
        if os.path.exists(puvspFile):
            # count lines using raw count for speed
            f = open(puvspFile, 'rb')
            lCount = 0
            buf_size = 1024 * 1024
            read_f = f.read
            buf = read_f(buf_size)
            while buf:
                lCount += buf.count(b'\n')
                buf = read_f(buf_size)
            f.close()
            # now read through the contents
            featSummary = {}
            with open(puvspFile,'r') as csvfile:
                qmdReader = csv.DictReader(csvfile,delimiter='\t')
                for line in qmdReader:
                    if int(line['pu']) in puIdList:
                        if line['species'] in featSummary:
                            featSummary[line['species']][0] += 1
                            featSummary[line['species']][1] += float(line['amount'])
                        else:
                            featSummary[line['species']] = [1,float(line['amount'])]
        else:
            pass 
            # should raise error here
        # convert to list to sort
        summaryList = [[int(key),value[0],value[1]] for key, value in featSummary.iteritems()]
        summaryList.sort()
        # 
        # step 4 - write file
        #
        # write report
        f = open(output_file,'w')
        f.write('featureId,featureName,featureCount,selectedPuCount,occurrencePercent,featureSum\n')
        for rec in summaryList:
            f.write('%d,%s,%d,%d,%f,%f\n' % (rec[0],specRecs[rec[0]],rec[1],puCount,float(rec[1])/float(puCount)*100,rec[2]) )
        f.close()

        return
        
