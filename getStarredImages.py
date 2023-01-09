import os
from PIL import Image
from PIL.ExifTags import TAGS

SELECTED_IMAGES = 'selected_file_names.txt'

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
def getStarredImages(directory):
    stared_images = []
    image_files = getImages(directory)
    # print image name and star count
    for image_file in image_files:
        metadata = getImageDetails(image_file)
        if metadata:
            # print rating stars
            if 'Rating' in metadata:
                # print(image_file, metadata['Rating'])
                if metadata['Rating'] > 0:
                    stared_images.append(image_file)
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
        directory = input('Enter directory: ')
        # if q is entered, quit
        if directory == 'q':
            break
        # check if directory exists
        if not os.path.exists(directory):
            print('Directory does not exist\n')
            continue
        stared_images = getStarredImages(directory)
        print('Number of stared images: ', len(stared_images))
        writeImageList(directory, stared_images)
        print('=====Done=====\n')
   
    

if __name__ == '__main__':
    main()
