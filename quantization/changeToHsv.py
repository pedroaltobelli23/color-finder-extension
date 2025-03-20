import os
import re
import colorsys

def changeToHsv(file, variable_name):
    # Read the JavaScript file
    with open(file, "r", encoding="utf-8") as file:
        js_content = file.read()

    # Regular expression to match color names and hex values
    pattern = re.compile(r"{\s*name:\s*'([^']+)'\s*,\s*hex:\s*'([^']+)'\s*}")

    # Function to convert hex to HSV
    def hex_to_hsv(hex_color):
        print(hex_color)
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        print(h, s, v)
        return [int(h * 255), int(s * 255), int(v * 255)]

    # Extract color names and convert hex to HSV
    HSV_COLORS = {match[0]: hex_to_hsv(match[1]) for match in pattern.findall(js_content)}
    with open("parameters.py", "a") as f:
        f.write(variable_name + "=" + str(HSV_COLORS) + "\n\n")

if __name__=="__main__":
    path = "/home/pedro/Documents/color-finder-extension/backend/color_js"
    changeToHsv(os.path.join(path, "basic.js"), "BASIC_HSV_COLORS")
    changeToHsv(os.path.join(path, "html.js"), "HTML_HSV_COLORS")
    changeToHsv(os.path.join(path, "x11.js"), "X11_HSV_COLORS")