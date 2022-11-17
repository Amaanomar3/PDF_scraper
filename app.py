from PIL import ImageDraw, Image
import glob
import fitz
import pytesseract



"""convert PDF to image"""

def PDF_to_img(input_path, output_path):
    zoom_x = 2.0
    zoom_y = 2.0
    mat = fitz.Matrix(zoom_x,zoom_y)
    i = 0
    all_files= glob.glob(input_path+ "/*.pdf")
    for filename in all_files:
        
        doc = fitz.open(filename)
        i += 1
        for page in doc:
            
            pix = page.get_pixmap(matrix=mat)
            pix.save("%s/document_%i_page_%i.png" % (output_path,i,page.number))

def check_zones(file_path, coordinates):
    files= glob.glob(file_path+ "/*.PNG")
    file = files[0]
    
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    for coords in coordinates:
        draw.rectangle(coords, outline=(255, 0, 0, 255), width=3)
    print("opening file...")
    img.show()


def crop_img(input_path,coordinates):
    
    img = Image.open(input_path)
    img_crop = img.crop(coordinates)
    return img_crop

def extract_info(input_path,coordinates):
    text_list = []
    all_files = glob.glob(input_path+"/*.PNG")
    for filename in all_files:
        for coords in coordinates:
            cropped_img = crop_img(filename,coords)
            text = pytesseract.image_to_string(cropped_img)
            text_list.append(text)
    
    return text_list
    
    

doc_in = 'doc_in'
img_out = 'img_out'
zones = [
    (105,555,280,584),
    (590,550,900,580),
    (105,582,280,608),
    (588,585,724,606)
]

PDF_to_img(doc_in,img_out)
check_zones(img_out,zones)
conf = input('Would you like to proceed: (Y/N): ')
if conf.lower() == "y":
    extract = extract_info(img_out,zones)
    for field in extract:
        print(field)

else:
    print("closing...")
        
    

