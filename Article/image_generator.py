# Unsplash API + Nider + Pillow
# Finetuning Cartoon GAN
# Generate from Cartoon GAN
# Find top relevant sentence with keyword by yake
# get the sentence put to cartoonze image
# put the image after paragraph
from pyunsplash import PyUnsplash
api_key = 'l9gjJyfyMA97_nu1IjHxFlpP43DT_XQRSoWwtjVA-7c'

# Get Photo
py_un = PyUnsplash(api_key=api_key)
search = py_un.search(type_='photos', query='data science')
for photo in search.entries:
    print(photo.id, photo.link_download)
