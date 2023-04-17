import time
import math
import imu_package.IMU as IMU
import datetime
import os
import sys

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

class BIMU:
    def __init__(self):
        self.magXmin =  0
        self.magYmin =  0
        self.magZmin =  0
        self.magXmax =  0
        self.magYmax =  0
        self.magZmax =  0

        ############### END Calibration offsets #############self.####

        self.gyroXangle = 0.0
        self.gyroYangle = 0.0
        self.gyroZangle = 0.0
        self.CFangleX = 0.0
        self.CFangleY = 0.0

    def detect_imu_connection(self):
        IMU.detectIMU()     #Detect if BerryIMU is connected.
        if(IMU.BerryIMUversion == 99):
            print(" No BerryIMU found... exiting ")
            sys.exit()
        IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

        

    def getgyroXangle(self):
        return self.gyroXangle

    def getgyroYangle(self):
        return self.gyroYangle

    def getgyroZangle(self):
        return self.gyroZangle

    def getCFangleX(self):
        return self.CFangleX

    def getCFangleY(self):
        return self.CFangleY

    def read(self):
        a = datetime.datetime.now()
        #Read the accelerometer,gyroscope and magnetometer values
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()
        MAGx = IMU.readMAGx()
        MAGy = IMU.readMAGy()
        MAGz = IMU.readMAGz()

        #Apply compass calibration
        MAGx -= (self.magXmin + self.magXmax) /2
        MAGy -= (self.magYmin + self.magYmax) /2
        MAGz -= (self.magZmin + self.magZmax) /2

        ##Calculate loop Period(LP). How long between Gyro Reads
        b = datetime.datetime.now() - a
        a = datetime.datetime.now()
        LP = b.microseconds/(1000000*1.0)
        outputString = "Loop Time %5.2f " % ( LP )


        #Convert Gyro raw to degrees per second
        rate_gyr_x =  GYRx * G_GAIN
        rate_gyr_y =  GYRy * G_GAIN
        rate_gyr_z =  GYRz * G_GAIN


        #Calculate the angles from the gyro.
        self.gyroXangle+=rate_gyr_x*LP
        self.gyroYangle+=rate_gyr_y*LP
        self.gyroZangle+=rate_gyr_z*LP


        #Convert Accelerometer values to degrees
        AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
        AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

        #convert the values to -180 and +180
        if AccYangle > 90:
            AccYangle -= 270.0
        else:
            AccYangle += 90.0



        #Complementary filter used to combine the accelerometer and gyro values.
        self.CFangleX=AA*(self.CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
        self.CFangleY=AA*(self.CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle



        #Calculate heading
        heading = 180 * math.atan2(MAGy,MAGx)/M_PI

        #Only have our heading between 0 and 360
        if heading < 0:
            heading += 360

        ####################################################################
        ###################Tilt compensated heading#########################
        ####################################################################
        #Normalize accelerometer raw values.
        accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


        #Calculate pitch and roll
        pitch = math.asin(accXnorm)
        roll = -math.asin(accYnorm/math.cos(pitch))


        #Calculate the new tilt compensated values
        #The compass and accelerometer are orientated differently on the the BerryIMUv1, v2 and v3.
        #This needs to be taken into consideration when performing the calculations

        #X compensation
        if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
            magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
        else:                                                                #LSM9DS1
            magXcomp = MAGx*math.cos(pitch)-MAGz*math.sin(pitch)

        #Y compensation
        if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
            magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)
        else:                                                                #LSM9DS1
            magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)




        #Calculate tilt compensated heading
        tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

        if tiltCompensatedHeading < 0:
            tiltCompensatedHeading += 360


        ##################### END Tilt Compensation ########################


        # if 1:                       #Change to '0' to stop showing the angles from the accelerometer
        #     outputString += "#  ACC_X Angle %5.2f ACC_Y Angle %5.2f  #  " % (AccXangle, AccYangle)

        # if 1:                       #Change to '0' to stop  showing the angles from the gyro
        #     outputString +="\t# GYR_X Angle %5.2f  GYR_Y Angle %5.2f  GYR_Z Angle %5.2f # " % (self.gyroXangle,self.gyroYangle,self.gyroZangle)

        # if 1:                       #Change to '0' to stop  showing the angles from the complementary filter
        #     outputString +="\t#  CFangle_X Angle %5.2f   CFangle_Y Angle %5.2f  #" % (self.CFangleX,self.CFangleY)

        # if 1:                       #Change to '0' to stop  showing the heading
        #     outputString +="\t# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)


        if 1:                       #Change to '0' to stop  showing the angles from the gyro
            outputString +="\t# GYR_X Angle %5.2f" % (self.gyroXangle)
        print(outputString)



        #slow program down a bit, makes the output more readable
        time.sleep(0.03)
    
    # def start(self):
    #     self.detect_imu_connection()
    #     self.read()
    
if __name__ == "__main__":
    imu = BIMU()
    imu.start()
    imu.getgyroXangle()
    imu.getgyroYangle()
    imu.getgyroZangle()
    imu.getCFangleX()
    imu.getCFangleY()
