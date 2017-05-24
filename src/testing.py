"""
An example that shows how to draw tracked skeletons
It also use joint filtering
"""

import itertools
import pygame
import pygame.color
import csv


from pygame.color import THECOLORS
from pykinect import nui
from pykinect.nui import JointId
from pykinect.nui import SkeletonTrackingState
from pykinect.nui.structs import TransformSmoothParameters

KINECTEVENT = pygame.USEREVENT
WINDOW_SIZE = 640, 480

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

SMOOTH_PARAMS_SMOOTHING = 0.7
SMOOTH_PARAMS_CORRECTION = 0.4
SMOOTH_PARAMS_PREDICTION = 0.7
SMOOTH_PARAMS_JITTER_RADIUS = 0.1
SMOOTH_PARAMS_MAX_DEVIATION_RADIUS = 0.1
SMOOTH_PARAMS = TransformSmoothParameters(SMOOTH_PARAMS_SMOOTHING,
                                          SMOOTH_PARAMS_CORRECTION,
                                          SMOOTH_PARAMS_PREDICTION,
                                          SMOOTH_PARAMS_JITTER_RADIUS,
                                          SMOOTH_PARAMS_MAX_DEVIATION_RADIUS)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

def post_frame(frame):
    """Get skeleton events from the Kinect device and post them into the PyGame
    event queue."""
    try:
        pygame.event.post(
            pygame.event.Event(KINECTEVENT, skeleton_frame=frame)
        )
    except:
        # event queue full
        pass

def draw_skeleton_data(dispInfo, screen, pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def draw_skeletons(dispInfo, screen, skeletons):
    # clean the screen
    screen.fill(pygame.color.THECOLORS["black"])

    for index, skeleton_info in enumerate(skeletons):
        # test if the current skeleton is tracked or not
        if skeleton_info.eTrackingState == SkeletonTrackingState.TRACKED:
            # draw the Head
            HeadPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h)
            SCPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.ShoulderCenter], dispInfo.current_w, dispInfo.current_h)
            LWPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.WristLeft], dispInfo.current_w, dispInfo.current_h)
            RWPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.WristRight], dispInfo.current_w, dispInfo.current_h)
            REPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.ElbowRight], dispInfo.current_w, dispInfo.current_h)
            LEPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.ElbowLeft], dispInfo.current_w, dispInfo.current_h)
            RSPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.ShoulderRight], dispInfo.current_w, dispInfo.current_h)
            LSPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.ShoulderLeft], dispInfo.current_w, dispInfo.current_h)
            HCPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.HipCenter], dispInfo.current_w, dispInfo.current_h)
            RHPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.HipRight], dispInfo.current_w, dispInfo.current_h)
            LHPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.HipLeft], dispInfo.current_w, dispInfo.current_h)
            RKPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.KneeRight], dispInfo.current_w, dispInfo.current_h)
            LKPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.KneeLeft], dispInfo.current_w, dispInfo.current_h)
            RAPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.AnkleRight], dispInfo.current_w, dispInfo.current_h)
            LAPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.AnkleLeft], dispInfo.current_w, dispInfo.current_h)

            draw_skeleton_data(dispInfo, screen, skeleton_info, index, SPINE, 10)
            pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
           
            position= [[HeadPos[0],HeadPos[1]],[SCPos[0],SCPos[1]],[LWPos[0],LWPos[1]],[RWPos[0],RWPos[1]],[LEPos[0],LEPos[1]],[RSPos[0],RSPos[1]],[LSPos[0],LSPos[1]],[HCPos[0],HCPos[1]],[RHPos[0],RHPos[1]],[LHPos[0],LHPos[1]],[RKPos[0],RKPos[1]],[LKPos[0],LKPos[1]],[RAPos[0],RAPos[1]],[LAPos[0],LAPos[1]]]
            # print position
            if pygame.time.get_ticks() == 100:
                with open("position.csv","wb") as f :
                    writer = csv.writer(f)
                    writer.writerows(position)
    
            # drawing the limbs
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_ARM)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_ARM)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_LEG)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_LEG)

def main():
    """Initialize and run the game."""
    pygame.init()
    # Initialize PyGame
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
    pygame.display.set_caption('PyKinect Skeleton Example')
    screen.fill(pygame.color.THECOLORS["black"])

    with nui.Runtime() as kinect:
        kinect.skeleton_engine.enabled = True
        kinect.skeleton_frame_ready += post_frame

        # Main game loop
        while True:
           event = pygame.event.wait()
           # time = pygame.time.get_ticks()
           if event.type == pygame.QUIT:
               break
           elif event.type == KINECTEVENT:
               # apply joint filtering
               kinect._nui.NuiTransformSmooth(event.skeleton_frame, SMOOTH_PARAMS)               
               draw_skeletons(pygame.display.Info(), screen, event.skeleton_frame.SkeletonData)
               pygame.display.update()
   
           pass
if __name__ == '__main__':
    main()