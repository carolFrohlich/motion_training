HOW TO RUN

#turn off firewall
sudo ufw disable

#open afni real time
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


#open other terminal
export PATH=$PATH:/usr/lib/afni/bin
realtime_receiver.py -show_data yes
#listen port 53214
or python motion_tracker.py



#open other terminal
export PATH=$PATH:/usr/lib/afni/bin
cd Documents/projects/NKI-tabs/bin
rtfeedme -dt 1 -host localhost ../sim/original_brik__002+orig


