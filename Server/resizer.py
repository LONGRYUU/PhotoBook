import argparse
import os
from PIL import Image


def resize_images(image_dir, output_dir, size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    images = os.listdir(image_dir)
    num_images = len(images)
    for i, image in enumerate(images):
        resize_image(os.path.join(image_dir, image), os.path.join(output_dir, image), size)
        if i % 100 == 0:
            print("[%d/%d] Resized the images and saved in '%s'" % (i, num_images, output_dir))

def resize_image(image_path, save_path, size):
    with(open(image_path, 'r+b')) as f:
        with Image.open(f) as img:
            img = img.resize((size,size), Image.ANTIALIAS)
            img.save(save_path, img.format)


def main(args):
    resize_images(args.train_image_dir,args.train_output_dir,args.image_size)
    # resize_images(args.val_image_dir, args.val_output_dir, image_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    '''
    parser.add_argument('--train_image_dir', type=str,
                        default='D:\\COCO\\train2017')
    parser.add_argument('--train_output_dir', type=str,
                        default='D:\\COCO\\resized\\train2017')
    parser.add_argument('--val_image_dir', type=str,
                        default='D:\\COCO\\val2017')
    parser.add_argument('--val_output_dir', type=str,
                        default='D:\\COCO\\resized\\val2017')
    '''
    parser.add_argument('--train_image_dir', type=str,
                        default='D:\\MMQ')
    parser.add_argument('--train_output_dir', type=str,
                        default='D:\\resized')
    parser.add_argument('--image_size', type=int, default=256)
    args = parser.parse_args()
    main(args)
