from savatemplate import template

# gotovo
if __name__ == "__main__":
    section = "https://savacoop.rs/sr/category/veleprodaja/agro-program/dubriva-i-oplemenjivaci-zemljista"
    scroll = 6
    items = 124
    template(section, scroll, items)
    driver.quit()
