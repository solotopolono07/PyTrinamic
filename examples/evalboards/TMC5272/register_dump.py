################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################
"""
Dump all register values of the TMC5272 IC.

The connection to a Landungsbrücke is established over USB. TMCL commands are used for communicating with the IC.
"""

import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.evalboards import TMC5272_eval

pytrinamic.show_info()

my_interface = ConnectionManager().connect()
print(my_interface)
eval_board = TMC5272_eval(my_interface)
drv = eval_board.ics[0]
motor = eval_board.motors[0]

print("Driver info: " + str(drv.get_info()))
print("Register dump for " + str(drv.get_name()) + ":")

print("GCONF:               0x{0:08X}".format(eval_board.read_register(drv.REG.GCONF)))
print("GSTAT:               0x{0:08X}".format(eval_board.read_register(drv.REG.GSTAT)))
print("IFCNT:               0x{0:08X}".format(eval_board.read_register(drv.REG.IFCNT)))
print("SLAVECONF:           0x{0:08X}".format(eval_board.read_register(drv.REG.SLAVECONF)))
print("IOIN:                0x{0:08X}".format(eval_board.read_register(drv.REG.IOIN)))
print("DRV_CONF:            0x{0:08X}".format(eval_board.read_register(drv.REG.DRV_CONF)))
print("GLOBAL_SCALER:       0x{0:08X}".format(eval_board.read_register(drv.REG.GLOBAL_SCALER)))
print("RAMPMODE:            0x{0:08X}".format(eval_board.read_register(drv.REG.RAMPMODE)))
print("MSLUT_ADDR:          0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_ADDR)))
print("MSLUT_SEL_START:     0x{0:08X}".format(eval_board.read_register(drv.REG.MSLUT_SEL_START)))
# Motor_01
print("MOTOR 01")
print("M0_X_COMPARE:        0x{0:08X}".format(eval_board.read_register(drv.REG.M0_X_COMPARE)))
print("M0_X_COMPARE_REPEAT: 0x{0:08X}".format(eval_board.read_register(drv.REG.M0_X_COMPARE_REPEAT)))
print("M0_IHOLD_IRUN:       0x{0:08X}".format(eval_board.read_register(drv.REG.M0_IHOLD_IRUN)))
print("M0_TPOWERDOWN:       0x{0:08X}".format(eval_board.read_register(drv.REG.M0_TPOWERDOWN)))
print("M0_TSTEP:            0x{0:08X}".format(eval_board.read_register(drv.REG.M0_TSTEP)))
print("M0_TPWMTHRS:         0x{0:08X}".format(eval_board.read_register(drv.REG.M0_TPWMTHRS)))
print("M0_TCOOLTHRS:        0x{0:08X}".format(eval_board.read_register(drv.REG.M0_TCOOLTHRS)))
print("M0_THIGH:            0x{0:08X}".format(eval_board.read_register(drv.REG.M0_THIGH)))
print("M0_XACTUAL:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_XACTUAL)))
print("M0_VACTUAL:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_VACTUAL)))
print("M0_AACTUAL:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_AACTUAL)))
print("M0_VSTART:           0x{0:08X}".format(eval_board.read_register(drv.REG.M0_VSTART)))
print("M0_A1:               0x{0:08X}".format(eval_board.read_register(drv.REG.M0_A1)))
print("M0_V1:               0x{0:08X}".format(eval_board.read_register(drv.REG.M0_V1)))
print("M0_A2:               0x{0:08X}".format(eval_board.read_register(drv.REG.M0_A2)))
print("M0_V2:               0x{0:08X}".format(eval_board.read_register(drv.REG.M0_V2)))
print("M0_AMAX:             0x{0:08X}".format(eval_board.read_register(drv.REG.M0_AMAX)))
print("M0_VMAX:             0x{0:08X}".format(eval_board.read_register(drv.REG.M0_VMAX)))
print("M0_DMAX:             0x{0:08X}".format(eval_board.read_register(drv.REG.M0_DMAX)))
print("M0_D2:               0x{0:08X}".format(eval_board.read_register(drv.REG.M0_D2)))
print("M0_D1:               0x{0:08X}".format(eval_board.read_register(drv.REG.M0_D1)))
print("M0_VSTOP:            0x{0:08X}".format(eval_board.read_register(drv.REG.M0_VSTOP)))
print("M0_TVMAX:            0x{0:08X}".format(eval_board.read_register(drv.REG.M0_TVMAX)))
print("M0_TZEROWAIT:        0x{0:08X}".format(eval_board.read_register(drv.REG.M0_TZEROWAIT)))
print("M0_XTARGET:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_XTARGET)))
print("M0_VDCMIN:           0x{0:08X}".format(eval_board.read_register(drv.REG.M0_VDCMIN)))
print("M0_SW_MODE:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_SW_MODE)))
print("M0_RAMP_STAT:        0x{0:08X}".format(eval_board.read_register(drv.REG.M0_RAMP_STAT)))
print("M0_XLATCH:           0x{0:08X}".format(eval_board.read_register(drv.REG.M0_XLATCH)))
print("M0_POSITION_PI_CTRL: 0x{0:08X}".format(eval_board.read_register(drv.REG.M0_POSITION_PI_CTRL)))
print("M0_X_ENC:            0x{0:08X}".format(eval_board.read_register(drv.REG.M0_X_ENC)))
print("M0_ENCMODE:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_ENCMODE)))
print("M0_ENC_CONST:        0x{0:08X}".format(eval_board.read_register(drv.REG.M0_ENC_CONST)))
print("M0_ENC_STATUS:       0x{0:08X}".format(eval_board.read_register(drv.REG.M0_ENC_STATUS)))
print("M0_ENC_LATCH:        0x{0:08X}".format(eval_board.read_register(drv.REG.M0_ENC_LATCH)))
print("M0_ENC_DEVIATION:    0x{0:08X}".format(eval_board.read_register(drv.REG.M0_ENC_DEVIATION)))
print("M0_VIRTUAL_STOP_L:   0x{0:08X}".format(eval_board.read_register(drv.REG.M0_VIRTUAL_STOP_L)))
print("M0_VIRTUAL_STOP_R:   0x{0:08X}".format(eval_board.read_register(drv.REG.M0_VIRTUAL_STOP_R)))
print("M0_MSCNT:            0x{0:08X}".format(eval_board.read_register(drv.REG.M0_MSCNT)))
print("M0_MSCURACT:         0x{0:08X}".format(eval_board.read_register(drv.REG.M0_MSCURACT)))
print("M0_CHOPCONF:         0x{0:08X}".format(eval_board.read_register(drv.REG.M0_CHOPCONF)))
print("M0_COOLCONF:         0x{0:08X}".format(eval_board.read_register(drv.REG.M0_COOLCONF)))
print("M0_DCCTRL:           0x{0:08X}".format(eval_board.read_register(drv.REG.M0_DCCTRL)))
print("M0_DRV_STATUS:       0x{0:08X}".format(eval_board.read_register(drv.REG.M0_DRV_STATUS)))
print("M0_PWMCONF:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_PWMCONF)))
print("M0_PWM_SCALE:        0x{0:08X}".format(eval_board.read_register(drv.REG.M0_PWM_SCALE)))
print("M0_PWM_AUTO:         0x{0:08X}".format(eval_board.read_register(drv.REG.M0_PWM_AUTO)))
print("M0_SG4_THRS:         0x{0:08X}".format(eval_board.read_register(drv.REG.M0_SG4_THRS)))
print("M0_SG4_RESULT:       0x{0:08X}".format(eval_board.read_register(drv.REG.M0_SG4_RESULT)))
print("M0_SG4_IND:          0x{0:08X}".format(eval_board.read_register(drv.REG.M0_SG4_IND)))
# Motor_02
print("MOTOR 02")
print("M1_X_COMPARE:        0x{0:08X}".format(eval_board.read_register(drv.REG.M1_X_COMPARE)))
print("M1_X_COMPARE_REPEAT: 0x{0:08X}".format(eval_board.read_register(drv.REG.M1_X_COMPARE_REPEAT)))
print("M1_IHOLD_IRUN:       0x{0:08X}".format(eval_board.read_register(drv.REG.M1_IHOLD_IRUN)))
print("M1_TPOWERDOWN:       0x{0:08X}".format(eval_board.read_register(drv.REG.M1_TPOWERDOWN)))
print("M1_TSTEP:            0x{0:08X}".format(eval_board.read_register(drv.REG.M1_TSTEP)))
print("M1_TPWMTHRS:         0x{0:08X}".format(eval_board.read_register(drv.REG.M1_TPWMTHRS)))
print("M1_TCOOLTHRS:        0x{0:08X}".format(eval_board.read_register(drv.REG.M1_TCOOLTHRS)))
print("M1_THIGH:            0x{0:08X}".format(eval_board.read_register(drv.REG.M1_THIGH)))
print("M1_XACTUAL:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_XACTUAL)))
print("M1_VACTUAL:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_VACTUAL)))
print("M1_AACTUAL:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_AACTUAL)))
print("M1_VSTART:           0x{0:08X}".format(eval_board.read_register(drv.REG.M1_VSTART)))
print("M1_A1:               0x{0:08X}".format(eval_board.read_register(drv.REG.M1_A1)))
print("M1_V1:               0x{0:08X}".format(eval_board.read_register(drv.REG.M1_V1)))
print("M1_A2:               0x{0:08X}".format(eval_board.read_register(drv.REG.M1_A2)))
print("M1_V2:               0x{0:08X}".format(eval_board.read_register(drv.REG.M1_V2)))
print("M1_AMAX:             0x{0:08X}".format(eval_board.read_register(drv.REG.M1_AMAX)))
print("M1_VMAX:             0x{0:08X}".format(eval_board.read_register(drv.REG.M1_VMAX)))
print("M1_DMAX:             0x{0:08X}".format(eval_board.read_register(drv.REG.M1_DMAX)))
print("M1_D2:               0x{0:08X}".format(eval_board.read_register(drv.REG.M1_D2)))
print("M1_D1:               0x{0:08X}".format(eval_board.read_register(drv.REG.M1_D1)))
print("M1_VSTOP:            0x{0:08X}".format(eval_board.read_register(drv.REG.M1_VSTOP)))
print("M1_TVMAX:            0x{0:08X}".format(eval_board.read_register(drv.REG.M1_TVMAX)))
print("M1_TZEROWAIT:        0x{0:08X}".format(eval_board.read_register(drv.REG.M1_TZEROWAIT)))
print("M1_XTARGET:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_XTARGET)))
print("M1_VDCMIN:           0x{0:08X}".format(eval_board.read_register(drv.REG.M1_VDCMIN)))
print("M1_SW_MODE:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_SW_MODE)))
print("M1_RAMP_STAT:        0x{0:08X}".format(eval_board.read_register(drv.REG.M1_RAMP_STAT)))
print("M1_XLATCH:           0x{0:08X}".format(eval_board.read_register(drv.REG.M1_XLATCH)))
print("M1_POSITION_PI_CTRL: 0x{0:08X}".format(eval_board.read_register(drv.REG.M1_POSITION_PI_CTRL)))
print("M1_X_ENC:            0x{0:08X}".format(eval_board.read_register(drv.REG.M1_X_ENC)))
print("M1_ENCMODE:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_ENCMODE)))
print("M1_ENC_CONST:        0x{0:08X}".format(eval_board.read_register(drv.REG.M1_ENC_CONST)))
print("M1_ENC_STATUS:       0x{0:08X}".format(eval_board.read_register(drv.REG.M1_ENC_STATUS)))
print("M1_ENC_LATCH:        0x{0:08X}".format(eval_board.read_register(drv.REG.M1_ENC_LATCH)))
print("M1_ENC_DEVIATION:    0x{0:08X}".format(eval_board.read_register(drv.REG.M1_ENC_DEVIATION)))
print("M1_VIRTUAL_STOP_L:   0x{0:08X}".format(eval_board.read_register(drv.REG.M1_VIRTUAL_STOP_L)))
print("M1_VIRTUAL_STOP_R:   0x{0:08X}".format(eval_board.read_register(drv.REG.M1_VIRTUAL_STOP_R)))
print("M1_MSCNT:            0x{0:08X}".format(eval_board.read_register(drv.REG.M1_MSCNT)))
print("M1_MSCURACT:         0x{0:08X}".format(eval_board.read_register(drv.REG.M1_MSCURACT)))
print("M1_CHOPCONF:         0x{0:08X}".format(eval_board.read_register(drv.REG.M1_CHOPCONF)))
print("M1_COOLCONF:         0x{0:08X}".format(eval_board.read_register(drv.REG.M1_COOLCONF)))
print("M1_DCCTRL:           0x{0:08X}".format(eval_board.read_register(drv.REG.M1_DCCTRL)))
print("M1_DRV_STATUS:       0x{0:08X}".format(eval_board.read_register(drv.REG.M1_DRV_STATUS)))
print("M1_PWMCONF:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_PWMCONF)))
print("M1_PWM_SCALE:        0x{0:08X}".format(eval_board.read_register(drv.REG.M1_PWM_SCALE)))
print("M1_PWM_AUTO:         0x{0:08X}".format(eval_board.read_register(drv.REG.M1_PWM_AUTO)))
print("M1_SG4_THRS:         0x{0:08X}".format(eval_board.read_register(drv.REG.M1_SG4_THRS)))
print("M1_SG4_RESULT:       0x{0:08X}".format(eval_board.read_register(drv.REG.M1_SG4_RESULT)))
print("M1_SG4_IND:          0x{0:08X}".format(eval_board.read_register(drv.REG.M1_SG4_IND)))
my_interface.close()

print("\nReady.")
