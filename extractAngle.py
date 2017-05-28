"""
An example that shows how to draw tracked skeletons
It also use joint filtering
"""

import itertools
import pygame
import pygame.color
import csv
import math
import numpy
import SVM_training

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

def calculateAngle(pointStart, pointCenter, pointEnd):
    # Compute the angle
            vector1x = pointStart.x - pointCenter.x
            vector1y = pointStart.y - pointCenter.y
            vector1z = pointStart.z - pointCenter.z
            
            vector2x = pointEnd.x - pointCenter.x
            vector2y = pointEnd.y - pointCenter.y
            vector2z = pointEnd.z - pointCenter.z

            vector1 = [vector1x,vector1y,vector1z]
            vector2 = [vector2x, vector2y, vector2z]

            cos = numpy.dot(vector1, vector2) / (numpy.sqrt(vector1[0]**2 + vector1[1]**2 + vector1[2]**2)*numpy.sqrt(vector2[0]**2 + vector2[1]**2 + vector2[2]**2))
            
            radian = math.acos(cos)
            degree = radian * 180/ math.pi

            #joint = [radian,degree]
            joint = degree
            return joint


def draw_skeletons(dispInfo, screen, skeletons, times):
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

            #extract angle frome skeleton joints
            WR = skeleton_info.SkeletonPositions[JointId.WristRight]
            ER = skeleton_info.SkeletonPositions[JointId.ElbowRight]
            SR = skeleton_info.SkeletonPositions[JointId.ShoulderRight]
            WL = skeleton_info.SkeletonPositions[JointId.WristLeft]
            EL = skeleton_info.SkeletonPositions[JointId.ElbowLeft]
            SL = skeleton_info.SkeletonPositions[JointId.ShoulderLeft]
            SC = skeleton_info.SkeletonPositions[JointId.ShoulderCenter]
            Spine = skeleton_info.SkeletonPositions[JointId.Spine]
            HR = skeleton_info.SkeletonPositions[JointId.HipRight]
            KR = skeleton_info.SkeletonPositions[JointId.KneeRight]
            AR = skeleton_info.SkeletonPositions[JointId.AnkleRight]
            HL = skeleton_info.SkeletonPositions[JointId.HandLeft]
            KL = skeleton_info.SkeletonPositions[JointId.KneeLeft]
            AL = skeleton_info.SkeletonPositions[JointId.AnkleLeft]
            HC = skeleton_info.SkeletonPositions[JointId.HipCenter]

            RElbowRoll = calculateAngle(WR,ER,SR)
            RShoulderRoll = calculateAngle(ER,SC,Spine)
            LElbowRoll = calculateAngle(WL,EL,SL)
            LShoulderRoll = calculateAngle(EL,SC,Spine)
            RKneeRoll =  calculateAngle(AR,KR,HR)
            LKneeRoll =  calculateAngle(AL,KL,HL)
            RHipRoll = calculateAngle(KR,HC,Spine)
            LHipRoll = calculateAngle(KL,HC,Spine)
            RElbowDir = WR.y - ER.y
            LElbowDir = WL.y - EL.y
            KneeDir = KL.z - KR.z         

            draw_skeleton_data(dispInfo, screen, skeleton_info, index, SPINE, 10)
            pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)

            position = [RElbowRoll,RShoulderRoll,LElbowRoll,LShoulderRoll,RKneeRoll,LKneeRoll,RHipRoll,LHipRoll,[RElbowDir],[LElbowDir],[KneeDir]]

            #position= [[HeadPos[0],HeadPos[1]],[SCPos[0],SCPos[1]],[LWPos[0],LWPos[1]],[RWPos[0],RWPos[1]],[LEPos[0],LEPos[1]],[RSPos[0],RSPos[1]],[LSPos[0],LSPos[1]],[HCPos[0],HCPos[1]],[RHPos[0],RHPos[1]],[LHPos[0],LHPos[1]],[RKPos[0],RKPos[1]],[LKPos[0],LKPos[1]],[RAPos[0],RAPos[1]],[LAPos[0],LAPos[1]]]
            # print position
            testData = 0
            #print times
            maxTime = times+10000
            minTime = times+11000
            #print pygame.time.get_ticks()
            if int(pygame.time.get_ticks()) >maxTime and int(pygame.time.get_ticks()) <= minTime:
                #with open("position.csv","wb") as f :
                #    writer = csv.writer(f)
                #    writer.writerows(position)
                    testData = [RElbowRoll,RShoulderRoll,LElbowRoll,LShoulderRoll,RKneeRoll,LKneeRoll,RHipRoll,LHipRoll,RElbowDir,LElbowDir,KneeDir]
                    print "writing..."
    
            # drawing the limbs
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_ARM)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_ARM)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_LEG)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_LEG)

           
            return testData

def main():
    posture = 6
    """Initialize and run the game."""
    pygame.init()
    # Initialize PyGame
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
    pygame.display.set_caption('PyKinect Skeleton Example1')

    
    with nui.Runtime() as kinect:
        kinect.skeleton_engine.enabled = True
        kinect.skeleton_frame_ready += post_frame
       
        timeFlag = 1
        if timeFlag is 1:

            currentTime = pygame.time.get_ticks()
            print currentTime
            timeFlag = 0

        # Main game loop
        while True:
           event = pygame.event.wait()
           # time = pygame.time.get_ticks()
           if event.type == pygame.QUIT:
               break
           elif event.type == KINECTEVENT:
               # apply joint filtering
                       max_juint = [ "left elbow", "left shoulder","right elbow", "right shoulder", "left knee", "right knee", "left hip", "right hip",  ]
              
              #for j in range(0,6):
                       #
                       #print j
                       kinect._nui.NuiTransformSmooth(event.skeleton_frame, SMOOTH_PARAMS)                       
                       testData = draw_skeletons(pygame.display.Info(), screen, event.skeleton_frame.SkeletonData, currentTime)
                      
                       if testData is not None:
                           if testData is not 0:                                
                                predictLabel, standardData = SVM_training.trainModel(testData)
                                #print posture
                                #print int(predictLabel)
                                print "Target posture:",posture
                                print "Your posture:",predictLabel
                                if(predictLabel == posture): 
                                        sum_distance = 0
                                        #for i in range(len(standardData)):
                                        #    sum_distance +=(standardData[i]-testData[i])**2
                                        #    distance = math.sqrt(sum_distance)
                                        distance=numpy.linalg.norm(numpy.array(standardData[posture-1])-numpy.array(testData))
                                        
                                        if (distance >= 30):
                                            err = []
    
                                            for i in range(len(testData)):
                                                err1 = abs(standardData[posture-1][i]-testData[i])
                                                err.append(err1)
                                                max_err = max(err)
                                            for i in range(len(testData)):
                                                if (max_err == err[i]):
                                                  #print err
                                                   print 'the #',max_juint[i], 'error,  need to modify', 'Need to modify:', max_err, 'degrees'
                                                   raw_input()
                                                   currentTime = pygame.time.get_ticks()
                                                   timeFlag = 0                                       
                                            j -= 1             
                                        else:
                                           print "correct"
                                           flag = False
                                           raw_input()
                                else:
                                      flag = True
                                      print "Wrong Posture, Try again"
                                      distance=numpy.linalg.norm(numpy.array(standardData[posture-1])-numpy.array(testData))
                                      if (distance >= 50):
                                         # j -= 1  
                                          
                                          raw_input()
                                          currentTime = pygame.time.get_ticks()
                                          timeFlag = 0

                               # if flag is True:
                                    #j -= 1


                                

           pygame.display.update()
   
           pass
if __name__ == '__main__':
    main()
