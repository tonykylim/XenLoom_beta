import glob, cv2
import numpy as np

# load contrail files
contrail_file_list = glob.glob("*.jpg")
contrail_dict = {}

# put all contrails from single animal into a new group
for contrail in contrail_file_list:
    filename = contrail[:-4]
    animalID, timepoint, treatment, trial = filename.split("_")
    trial_num = int(trial[-1:])
    try:
        contrail_dict[animalID]
    except:
        contrail_dict[animalID] = []
    contrail_dict[animalID].append(contrail)

# trial colours
color = [ [75, 25, 230], [48, 130, 245], [25, 225, 255], [60, 245, 210], [75, 180, 60], [240, 240, 70], [200, 130, 0], [180, 30, 145], [230, 50, 240], [128, 128, 128] ]

# loop through animals
for animal in contrail_dict:
    count = 0
    merge_image = np.zeros((480,640,3), np.uint8)
    #loop through trials
    for file in contrail_dict[animal]:
        # designate colour
        animal_color = color[count]
        # open contrail
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        # colourize contrail
        img[np.where((img > [200,200,200]).all(axis = 2))] = animal_color
        # merge
        merge_image = cv2.add(merge_image, img)
        # show the merged contrails
        cv2.imshow(file , merge_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # filename data
        filenameZ = file[:-4]
        animalIDZ, timepointZ, treatmentZ, trialZ = filenameZ.split("_")
        trial_numZ = int(trial[-1:])
        count += 1
    # save the merged contrails
    cv2.imwrite(animalIDZ + '_' + timepointZ + '_' + treatmentZ + '.jpg', merge_image)