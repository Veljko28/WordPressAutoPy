from savatemplate import template

# gotovo
if __name__ == "__main__":
    section = "https://savacoop.rs/sr/category/veleprodaja/masine-i-alati/bastenski-alati-i-masine/rucni-bastenski-alat"
    scroll = 6
    items = 112
    template(section, scroll, items)
    driver.quit()
