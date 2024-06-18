################################################################################
# Copyright © 2023 Analog Devices Inc. All Rights Reserved.
# This software is proprietary to Analog Devices, Inc. and its licensors.
################################################################################

import time
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.evalboards import TMC2262_eval

pytrinamic.show_info()

with ConnectionManager().connect() as my_interface:
    print(my_interface)

    eval_board = TMC2262_eval(my_interface)
    motor = eval_board.motors[0]
    mc = eval_board.ics[0]
    eval_board.set_axis_parameter(motor.AP.MaxAcceleration, 0, 25000)

    print("Rotating...")
    motor.rotate(10000)
    time.sleep(5)

    print("Stopping...")
    motor.stop()
    time.sleep(1)

print("\nReady.")

