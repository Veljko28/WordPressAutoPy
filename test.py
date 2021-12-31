from slika import resizeImage
import re

if __name__ == "__main__":
    specifikacija = "<span>hello</span>"
    CLEANR = re.compile(r'<[^>]+>')
    specifikacija = CLEANR.sub('', specifikacija)
    print(specifikacija)