from savatemplate import template

# gotovo
if __name__ == "__main__":
    section = "https://savacoop.rs/sr/category/veleprodaja/masine-i-alati/bastenski-alati-i-masine/kosacice"
    scroll = 0
    items = 11
    template(section, scroll, items)
    driver.quit()
