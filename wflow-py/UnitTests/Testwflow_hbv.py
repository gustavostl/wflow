__author__ = 'schelle'

import unittest
import wflow.wflow_hbv as wf
import os
"""

Run wflow_hbv for 30 steps and checks if the outcome is approx that of the reference run

"""

class MyTest(unittest.TestCase):

    def testapirun(self):
        startTime = 1
        stopTime = 30
        currentTime = 1

          # set runid, clonemap and casename. Also define the ini file
        runId = "unittest"
        configfile="wflow_hbv.ini"
        wflow_cloneMap = 'wflow_catchment.map'
        caseName="wflow_hbv"

        myModel = wf.WflowModel(wflow_cloneMap, caseName,runId,configfile)
         # initialise the framework
        dynModelFw = wf.wf_DynamicFramework(myModel, stopTime,startTime)

          # Load model config from files and check directory structure
        dynModelFw.createRunId(NoOverWrite=False)
        # Run the initial part of the model (reads parameters and sets initial values)
        dynModelFw._runInitial() # Runs initial part

        dynModelFw._runResume() # gets the state variables
        sump = 0.0
        for ts in range(startTime,stopTime):
            if ts <10:
                dynModelFw.wf_setValues('P', 0.0)
            elif ts <= 15:
                dynModelFw.wf_setValues('P', 10.0)
                sump = sump + 10.0
            else:
                dynModelFw.wf_setValues('P', 0.0)

            dynModelFw.wf_setValues('PET', 2.0)
            dynModelFw.wf_setValues('TEMP', 10.0)
            dynModelFw._runDynamic(ts,ts) # runs for all timesteps
            dynModelFw.logger.info("Doing step: " + str(ts))
        dynModelFw._runSuspend() # saves the state variables
        dynModelFw._wf_shutdown()

        # nore read the csv results acn check of they match the first run
        # Sum should be approx c 4.569673676
        my_data = wf.genfromtxt(os.path.join(caseName,runId,"watbal.csv"), delimiter=',')

        print("Checking  water budget ....")
        self.assertAlmostEquals( 0.00018204912482389091,my_data[:,2].sum())

        print("Checking precip sum ....")
        my_data = wf.genfromtxt(os.path.join(caseName,runId,"P.csv"), delimiter=',')
        self.assertAlmostEquals(sump,my_data[:,2].sum())


if __name__ == '__main__':
    unittest.main()