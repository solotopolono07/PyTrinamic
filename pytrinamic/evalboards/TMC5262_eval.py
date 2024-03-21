################################################################################
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

from pytrinamic.evalboards import TMCLEval
from pytrinamic.ic import TMC5262
from pytrinamic.features import MotorControlModule


class TMC5262_eval(TMCLEval):
    """
    This class represents a TMC5262 Evaluation board.
    """
    def __init__(self, connection, module_id=1):
        """
        Constructor for the TMC5262 evalboard instance.

        Parameters:
        connection: TMCL connection interface instance.
        module_id: Module ID to identify the evalboard module. This is used to differentiate
        between different modules on shared busses. Default is set to 1, different
        values have to be configured with the module first.
        """
        TMCLEval.__init__(self, connection, module_id)
        self.motors = [self._MotorTypeA(self, 0)]
        self.ics = [TMC5262(self)]

    # Use the motor controller functions for register access

    def write_register(self, register_address, value):
        return self._connection.write_mc(register_address, value, self._module_id)

    def read_register(self, register_address, signed=False):
        return self._connection.read_mc(register_address, self._module_id, signed)

    # Motion control functions

    def rotate(self, motor, value):
        self._connection.rotate(motor, value)

    def stop(self, motor):
        self._connection.stop(motor)

    def move_to(self, motor, position, velocity=None):
        if velocity and velocity != 0:
            # Set maximum positioning velocity
            self.motors[motor].set_axis_parameter(self.motors[motor].AP.MaxVelocity, velocity)
        self._connection.move_to(motor, position, self._module_id)

    class _MotorTypeA(MotorControlModule):
        """
        Motor class for the generic motor.
        """
        def __init__(self, eval_board, axis):
            MotorControlModule.__init__(self, eval_board, axis, self.AP)

        class AP:
            TargetPosition = 0
            ActualPosition = 1
            TargetVelocity = 2
            ActualVelocity = 3
            MaxVelocity = 4
            MaxAcceleration = 5
            MaxCurrent = 6
            StandbyCurrent = 7
            PositionReachedFlag = 8
            RightEndstop = 10
            LeftEndstop = 11
            AutomaticRightStop = 12
            AutomaticLeftStop = 13
            SW_MODE = 14
            MaxDeceleration = 15
            StartVelocity = 16
            A1 = 17
            V1 = 18
            D1 = 19
            StopVelocity = 20
            RampWaitTime = 21
            V2 = 22
            D2 = 23
            A2 = 24
            TVMax = 25
            VDCMIN = 27
            HighSpeedChopperMode = 28
            HighSpeedFullstepMode = 29
            MeasuredSpeed = 30
            CurrentP = 31
            CurrentI = 32
            CurrentLimit = 37
            CurrentAmplMeas = 40
            MicrostepResolution = 140
            ChopperBlankTime = 162
            ConstantTOffMode = 163
            DisableFastDecayComparator = 164
            ChopperHysteresisEnd = 165
            ChopperHysteresisStart = 166
            TOff = 167
            SEIMIN = 168
            SECDS = 169
            smartEnergyHysteresis = 170
            SECUS = 171
            smartEnergyHysteresisStart = 172
            SG5FilterEnable = 173
            SG4Threshold = 174
            SG2FilterEnable = 175
            SG2Threshold = 176
            smartEnergyActualCurrent = 180
            smartEnergyStallVelocity = 181
            smartEnergyThresholdSpeed = 182
            SG4FilterEnable = 183
            SGAngleOffset = 184
            ChopperSynchronization = 185
            PWMThresholdSpeed = 186
            MSCNT = 194
            MEAS_SD_EN = 195
            LoadValue = 206
            EncoderPosition = 209
            EncoderResolution = 210
            CurrentRange = 212
            ADCTemperature = 213
            ADCIN = 214
            FSR_IREF = 215
            ADCOvervoltageLimit = 216
            ADCOvertemperatureWarningLimit = 217
            Temperature = 218
            AIN = 219
            VSupply = 220
            OvervoltageLimit = 221
            OvertemperatureWarningLimit = 222
            nSLEEP = 223