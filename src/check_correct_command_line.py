import sys, getopt
import math

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'error, usage, *.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for option, argument in opts:
      if option == '-help':
         print 'help you, *.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif option in ("-i", "--inputfile"):
         inputfile = argument
      elif option in ("-o", "--outputfile"):
         outputfile = argument
#   print 'Input file is "', inputfile
#   print 'Output file is "', outputfile


def take_standard_data(predictedclass):
    if (predictedclass== posture1):
#        standard_data = posture1_standard_data # loaded data

    if (predictedclass== posture2):
        standard_data = posture2_standard_data

    if (predictedclass== posture3):
        standard_data = posture3_standard_data

    if (predictedclass== posture4):
        standard_data = posture4_standard_data

    if (predictedclass== posture5):
        standard_data = posture5_standard_data

    if (predictedclass== posture6):
        standard_data = posture6_standard_data
    print 'standard_data:', standard_data


def distance(testingdata,standard_data):
    
#    fruits = ['banana', 'apple',  'mango']
    for i in range(len(standard_data)):
        sum_distance + =(standard_data[i]-testingdata[i])*(standard_data[i]-testingdata[i])

#       error_square_sum + =(standard_data[i]-testingdata[i])*(standard_data[i]-testingdata[i])
#    error = math.sqrt (x)(error_square_sum)
    distance = math.sqrt (x)(sum_distance)
#    print 'distance :', distance
#    print 'error :', error

def correct(testingdata,standard_data):
    err1 = math.abs(standard_data[i]-testingdata[i])/distance(testingdata,standard_data)
   max_err = math.max(err1)
    for i in range(11):
        if (max_err == err1[i]):
            print 'the #',i, 'err,  need to modify'


#print "Good bye!"


def check(testingdata, predictedclass):
        standard_data = take_standard_data(predictedclass)
        distance = distance(testingdata,standard_data)
        if (distance <= error_boundory):
            print 'right'
            break
        else :
            correct(testingdata,standard_data)
            print 'the #',i, 'err, succeed modifying'
            raw_input("Press enter to continue to learn the modified posture  ... \n")
#            testingdata = kinect_functione_get_data() ##### call the extracted data from kinect

#            predictedclass = SVM(testingdata) #####
             check(testingdata, predictedclass)



if __name__ == "__main__":
    main(sys.argv[1:])
    print"Welcome IIS project, we are group 5"
    raw_input("Press enter to train SVM... \n")
    standard_data = inputfile
    SVM = train_SVM(standard_data)#call the train funtion
    raw_input("Press enter to train SVM... \n")

    raw_input("Press enter to continue... \n")
    
    count = 1
    while (count <= 6):
        print 'The count is:', count
#        testingdata = kinect_functione_get_data()
#        predictedclass = SVM(testingdata)
        check(testingdata, predictedclass)
        print "succeed in this porture "
        count = count + 1
        if (count<=6):
            raw_input("Press enter to continue to learn next posture  ... \n")
        else:
            raw_input("Congratulations, Press enter to stop  ... \n")



