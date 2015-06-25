import os

thisversion = "$Id: mkversion.py 550 2012-11-27 19:17:46Z schelle $"
#vers=os.popen('svnversion -n').read().replace(":","-")
vers='a1'
# SET THESE
###################################
manualversion = "2015.01." + vers
manualmainversion = "2015.01"
###################################
a = open("_version.py","w")

a.write("VERSION=\"" + vers + " " + thisversion + "\"\n")
a.write("MVERSION=\"" + manualversion +"\"\n")

a.close()

a = open("wflow/__init__.py","w")
a.write("__all__ = [\"wflow_funcs\",\"wflow_adapt\",\"wflow_lib\",\"pcrut\",\"wf_DynamicFramework\",\"stats\"]\n")
a.write("__version__=\"" + manualmainversion + "\"\n")
a.write("__release__=\"" + manualversion + "\"\n")
a.write("import osgeo.gdal as gdal")


print "============================================================================="
print "Now install wflow using setup.py install and regenerate the documentation...."
print "============================================================================="
