This is a small LinuxCNC setup for controlling a single stepper motor
over the network.  (It does not use 99% of the LinuxCNC stuff, only a
minimal HAL setup with a software step generator.)

It's intended to run on a Raspberry Pi with the Pi image from
<http://linuxcnc.org/downloads/>.


There are two parts:

First, a HAL file named `stepper.hal` loads the three components needed:
a software step generator, the driver for the Raspberry Pi GPIO pins,
and the thread manager.  It makes one "slow" thread (1 ms period) and one
"fast" thread (500 µs period).  It adds the functions from the components
to the threads.

It next configures the stepgen with the step & direction waveform timing
parameters, and the max allowed velocity and acceleration.

It finally connects the step and direction "pins" of the stepgen component
to the gpio "pins" of the hal_pi_gpio component.

Note that we're limited by the realtime performance of the Raspberry
Pi to a 2 kHz "fast" thread, which means the step and direction signals
can not change any more rapidly than that.  The max step rate with this
setup is thus 1 kHz.


Second, a Python script named `netstep.py` connects to HAL, makes an
output pin, makes a signal named "position-cmd", connects its pin to the
new signal, and also connects the stepgen's "position-cmd" input pin to
the new signal.

It then listens for connections on port 9999, and reads string-encoded
floats, and writes those floats to its "position-cmd" pin.


To start:

`$ halrun -I stepper.hal`

That starts LinuxCNC's realtime environment and executes the HAL file.

`$ ./netstep.py`

That starts the non-realtime network application running.

