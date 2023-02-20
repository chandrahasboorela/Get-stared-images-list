import os
from PIL import Image
from PIL.ExifTags import TAGS

SELECTED_IMAGES = 'selected_file_names.txt'
SELECTED_FOLDER_NAME = 'selected_images'
MIN_STAR_COUNT = 2 # windows photos app adds 4 stars when marked as favorite

# get all images from a directory
def getImages(directory):
    # get all files in directory
    files = os.listdir(directory)
    # filter for image files
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    # return full path to image files
    return [os.path.join(directory, file) for file in image_files]

# get image details metadata
def getImageDetails(image_file):
    # get image details metadata
    image_details = {}
    # get image metadata
    image = Image.open(image_file)
    # get image metadata
    image_metadata = image._getexif()
    # get image details metadata
    if image_metadata:
        for tag, value in image_metadata.items():
            # get tag name
            tag_name = TAGS.get(tag, tag)
            # get image details metadata
            image_details[tag_name] = value
    # return image details metadata
    return image_details


# return images with star rating
def getStarredImages(directory, options = None):
    stared_images = []
    image_files = getImages(directory)
    # print image name and star count
    for image_file in image_files:
        metadata = getImageDetails(image_file)
        if metadata:
            # print rating stars
            if 'Rating' in metadata:
                # print(image_file, metadata['Rating'])
                if metadata['Rating'] >= MIN_STAR_COUNT:
                    stared_images.append(image_file)
                    # if options and options['move'] == True move selected images to a SELECTED_FOLDER_NAME
                    if options and options['move'] == True:
                        # create a directory to move selected images
                        selected_folder = os.path.join(directory, SELECTED_FOLDER_NAME)
                        if not os.path.exists(selected_folder):
                            os.mkdir(selected_folder)
                        # move selected images to selected folder
                        os.rename(image_file, os.path.join(selected_folder, os.path.basename(image_file)))
    return stared_images

# write a file with the list of images
def writeImageList(directory, filenames):
    write_file_name = os.path.join(directory, SELECTED_IMAGES)
    with open(write_file_name, 'w') as f:
        for filename in filenames:
            # remove directory from filename
            filename = os.path.basename(filename)
            f.write(filename + '\n') 

def main():
    print('Enter q to quit')
    while True:
        options = {'move' : False}
        directory = input('Enter directory: ')
        move_images = input(f'Move images to {SELECTED_FOLDER_NAME}  folder? (y/n): ')
        if move_images.lower() == 'y':
            options['move'] = True
        # if q is entered, quit
        if directory == 'q':
            break
        # check if directory exists
        if not os.path.exists(directory):
            print('Directory does not exist\n')
            continue
        stared_images = getStarredImages(directory, options)
        print('Number of stared images: ', len(stared_images))
        writeImageList(directory, stared_images)
        print('=====Done=====\n')
   
    

if __name__ == '__main__':
    main()
