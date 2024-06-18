################################################################################
# Copyright © 2023 Analog Devices Inc. All Rights Reserved.
# This software is proprietary to Analog Devices, Inc. and its licensors.
################################################################################

"""
Dump all register values of the TMC2262 IC.

The connection to a Landungsbrücke is established over USB. TMCL commands are used for communicating with the IC.
"""

import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.evalboards import TMC2262_eval
import time

pytrinamic.show_info()

my_interface = ConnectionManager().connect()
print(my_interface)
eval_board = TMC2262_eval(my_interface)
drv = eval_board.ics[0]
motor = eval_board.motors[0]

print("Driver info: " + str(drv.get_info()))
print("Register dump for " + str(drv.get_name()) + ":")
time.sleep(2)
print("GCONF                     0x{0:08X}".format(eval_board.read_register(drv.REG.GCONF)))
print("GSTAT                     0x{0:08X}".format(eval_board.read_register(drv.REG.GSTAT)))
print("DIAG_CONF                 0x{0:08X}".format(eval_board.read_register(drv.REG.DIAG_CONF)))
print("DIAG_DAC_CONF             0x{0:08X}".format(eval_board.read_register(drv.REG.DIAG_DAC_CONF)))
print("IOIN                      0x{0:08X}".format(eval_board.read_register(drv.REG.IOIN)))
print("DRV_CONF                  0x{0:08X}".format(eval_board.read_register(drv.REG.DRV_CONF)))
print("PLL                       0x{0:08X}".format(eval_board.read_register(drv.REG.PLL)))
print("IHOLD_IRUN                0x{0:08X}".format(eval_board.read_register(drv.REG.IHOLD_IRUN)))
print("TPOWERDOWN                0x{0:08X}".format(eval_board.read_register(drv.REG.TPOWERDOWN)))
print("TSTEP                     0x{0:08X}".format(eval_board.read_register(drv.REG.TSTEP)))
print("TPWMTHRS                  0x{0:08X}".format(eval_board.read_register(drv.REG.TPWMTHRS)))
print("TCOOLTHRS                 0x{0:08X}".format(eval_board.read_register(drv.REG.TCOOLTHRS)))
print("THIGH                     0x{0:08X}".format(eval_board.read_register(drv.REG.THIGH)))
print("TSGP_LOW_VEL_THRS         0x{0:08X}".format(eval_board.read_register(drv.REG.TSGP_LOW_VEL_THRS)))
print("T_RCOIL_MEAS              0x{0:08X}".format(eval_board.read_register(drv.REG.T_RCOIL_MEAS)))
print("TUDCSTEP                  0x{0:08X}".format(eval_board.read_register(drv.REG.TUDCSTEP)))
print("UDC_CONF                  0x{0:08X}".format(eval_board.read_register(drv.REG.UDC_CONF)))
print("STEPS_LOST                0x{0:08X}".format(eval_board.read_register(drv.REG.STEPS_LOST)))
print("SW_MODE                   0x{0:08X}".format(eval_board.read_register(drv.REG.SW_MODE)))
print("SG_SEQ_STOP_STAT          0x{0:08X}".format(eval_board.read_register(drv.REG.SG_SEQ_STOP_STAT)))
print("ENCMODE                   0x{0:08X}".format(eval_board.read_register(drv.REG.ENCMODE)))
print("X_ENC                     0x{0:08X}".format(eval_board.read_register(drv.REG.X_ENC)))
print("ENC_CONST                 0x{0:08X}".format(eval_board.read_register(drv.REG.ENC_CONST)))
print("ENC_STATUS                0x{0:08X}".format(eval_board.read_register(drv.REG.ENC_STATUS)))
print("ENC_LATCH                 0x{0:08X}".format(eval_board.read_register(drv.REG.ENC_LATCH)))
print("ENC_DEVIATION             0x{0:08X}".format(eval_board.read_register(drv.REG.ENC_DEVIATION)))
print("CURRENT_PI_REG            0x{0:08X}".format(eval_board.read_register(drv.REG.CURRENT_PI_REG)))
print("ANGLE_PI_REG              0x{0:08X}".format(eval_board.read_register(drv.REG.ANGLE_PI_REG)))
print("CUR_ANGLE_LIMIT           0x{0:08X}".format(eval_board.read_register(drv.REG.CUR_ANGLE_LIMIT)))
print("ANGLE_LOWER_LIMIT         0x{0:08X}".format(eval_board.read_register(drv.REG.ANGLE_LOWER_LIMIT)))
print("CUR_ANGLE_MEAS            0x{0:08X}".format(eval_board.read_register(drv.REG.CUR_ANGLE_MEAS)))
print("PI_RESULTS                0x{0:08X}".format(eval_board.read_register(drv.REG.PI_RESULTS)))
print("COIL_INDUCT               0x{0:08X}".format(eval_board.read_register(drv.REG.COIL_INDUCT)))
print("R_COIL                    0x{0:08X}".format(eval_board.read_register(drv.REG.R_COIL)))
print("R_COIL_USER               0x{0:08X}".format(eval_board.read_register(drv.REG.R_COIL_USER)))
print("SGP_CONF                  0x{0:08X}".format(eval_board.read_register(drv.REG.SGP_CONF)))
print("SGP_IND_2_3               0x{0:08X}".format(eval_board.read_register(drv.REG.SGP_IND_2_3)))
print("SGP_IND_0_1               0x{0:08X}".format(eval_board.read_register(drv.REG.SGP_IND_0_1)))
print("INDUCTANCE_VOLTAGE        0x{0:08X}".format(eval_board.read_register(drv.REG.INDUCTANCE_VOLTAGE)))
print("SGP_BEMF                  0x{0:08X}".format(eval_board.read_register(drv.REG.SGP_BEMF)))
print("COOLSTEPPLUS_CONF         0x{0:08X}".format(eval_board.read_register(drv.REG.COOLSTEPPLUS_CONF)))
print("COOLSTEPPLUS_PI_REG       0x{0:08X}".format(eval_board.read_register(drv.REG.COOLSTEPPLUS_PI_REG)))
print("COOLSTEPPLUS_PI_DOWN      0x{0:08X}".format(eval_board.read_register(drv.REG.COOLSTEPPLUS_PI_DOWN)))
print("COOLSTEPPLUS_RESERVE_CONF 0x{0:08X}".format(eval_board.read_register(drv.REG.COOLSTEPPLUS_RESERVE_CONF)))
print("COOLSTEPPLUS_LOAD_RESERVE 0x{0:08X}".format(eval_board.read_register(drv.REG.COOLSTEPPLUS_LOAD_RESERVE)))
print("TSTEP_VELOCITY            0x{0:08X}".format(eval_board.read_register(drv.REG.TSTEP_VELOCITY)))
print("ADC_VSUPPLY_TEMP          0x{0:08X}".format(eval_board.read_register(drv.REG.ADC_VSUPPLY_TEMP)))
print("ADC_I                     0x{0:08X}".format(eval_board.read_register(drv.REG.ADC_I)))
print("OTW_OV_VTH                0x{0:08X}".format(eval_board.read_register(drv.REG.OTW_OV_VTH)))
print("MSLUT_0                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_0)))
print("MSLUT_1                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_1)))
print("MSLUT_2                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_2)))
print("MSLUT_3                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_3)))
print("MSLUT_4                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_4)))
print("MSLUT_5                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_5)))
print("MSLUT_6                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_6)))
print("MSLUT_7                   0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_7)))
print("MSLUTSEL                  0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUTSEL)))
print("MSLUTSTART                0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUTSTART)))
print("MSCNT                     0x{0:08X}".format(eval_board.read_register(drv.REG.MSCNT)))
print("MSCURACT                  0x{0:08X}".format(eval_board.read_register(drv.REG.MSCURACT)))
print("CHOPCONF                  0x{0:08X}".format(eval_board.read_register(drv.REG.CHOPCONF)))
print("COOLCONF                  0x{0:08X}".format(eval_board.read_register(drv.REG.COOLCONF)))
print("DRV_STATUS                0x{0:08X}".format(eval_board.read_register(drv.REG.DRV_STATUS)))
print("PWMCONF                   0x{0:08X}".format(eval_board.read_register(drv.REG.PWMCONF)))
my_interface.close()

print("\nReady.")
