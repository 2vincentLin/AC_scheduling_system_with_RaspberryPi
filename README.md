# AC_scheduling_system_with_RaspberryPi

The purpose of this project is to use Raspberry pi to control relays to achieve automatic on/off (scheduling) certain relay.

## how to use

there're two file you need, 

1. ac_control_gui.py, it's a gui written using Tkinter and Tkcalendar, it'll call the schedule functio nfrom relay_class.py every second and update the interface.
2. relay_class.py, classes that controls relay with a schedule function.
