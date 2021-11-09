##Data description:

###Files description:
Live Data (ending with _lv) - Data Recorded each Frame of the application. Data at Runtime. Captures, 



####Variables description:
HMD related - Camera Attached to the player (In first person and thirdperson) - your Head position
Global - Global space, related to the complete world
local - relative to the SteamVR player Object
NoseVector  -> Tranform foward of the Camera, a Vector pointing in the Heads "direction"
HMDPositionGlobal
HMDRotationGlobal
HMDPositionLocal  
HMDRotationLocal

Hands in embodied condition or controller in non embodied Condition
!Check if Blob condition really has their Left hand and Right Positions there
LeftHand 

Righthand


!Missing Controller model position (Always relative to the camerea!) -> (needs to be stored) 
----------


Movement Input 
Vector 2 containing X and Y
X LeftRight Movement 0 -> no movement, >0 -> left , 0< -> right
Y FowardBackwards 0 -> no movement , >0 -> foward, <0 -> backward

!Missing Rotation Input  single float
X Left and Right Rotation
---------
CharacterController , where the player is located in the VR environment , always global


!Adjusted Character Position is missing

----------
Puppet-  visual Avatar

Puppet Head Position -> Where is the Avatar 

!Arm transforms are missing could be beneficial to have
!Maybe Knee , and feet 



static Data

application start time (Unix Time Stamp)- the moment the application was started

Conditions : Hybrid, Firstperson, Blob, or Bodiless 

StationID: 0 is Tutorial , 1-4 real stations

Station 1: Horizontal Volentary movement
Station 2: Interaction and locomotion in Room
Station 3: Involentary movement horizontal and vertically
Station 4: Volentary vertical movement


Timestamp: 
Pakour StartTimeStamp : Pakour was entered
Pakour EndTimetsamp : Pakour ended (NOT including Datagathering)
Pakour Duration : End - Start time
Abort Teleport: when participant was not able to finish pakour, it is set to the end of it.
was teleported : 
DataGatheringentered: Door entered from Datagathering room
Data gathering board reached, reached blue circle of the rating board
AudioStarted: The moment  the button for datagathering was pressed
AudioEnded: The moment the recording stopped.  (NOTE the file is always 3 Minutes long, and has to be cut with these time stamps)
Name of Audio file : - 
MotionsicknessScoreRatingBegin: Begin of Sickness Sickness
MotionsicknessScoreRatingEnd: End of sickness rating
Motion sickness Score: chosen value
PosturalStabilityBegin: The moment (after 2 seconds delay) of the postural stability measurement
PosturalStabilityEnd: After 5 seconds of the Begin, the stability measurement End.













