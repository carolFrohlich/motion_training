HOW TO RUN

1) turn off firewall
sudo ufw disable

2) open afni real time
export PATH=$PATH:/usr/lib/afni/bin
sudo afni -rt

check Talairach VIew

define datamode
plugins
RT options

check registration
3D: realtime

check Graph
Realtime

check mask
choose mask MNI_EPI+tlrc
Vals to Send: Motion Only

set+close


Misc
Edit environment
AFNI_REALTIME_MP_HOST_PORT = localhost:53214
set+close


3)listen motion parameters
open other terminal
export PATH=$PATH:/usr/lib/afni/bin
realtime_receiver.py -show_data yes
listen port 53214
or 
python motion_tracker.py


4) send motion parameters
open other terminal
export PATH=$PATH:/usr/lib/afni/bin
cd Documents/projects/NKI-tabs/bin
rtfeedme -3D -dt 100 -host localhost ../sim/original_brik__002+orig


