# Masterwork

Generative Art in the style of Jackson Pollock and Piet Mondrian.

## Command Line Arguments:

All examples are default values except `-mc`, which defaults to `none`. If `-mc` is `none`, colors will be chosen randomly based on `-c`, otherwise they will be taken from the file.

### pollock.py

| Flag | Argument Type | Example | Description |
| ---- | ------------- | ------- | ----------- |
| --width | int | --width 1920 | Width of image in pixels |
| --height | int | --height 1080 | Height of image in pixels |
| -c, --colors | int | -c 10 | Number of random colors to use |
| -d, --depth | int | -d 1000 | Number of iterations to perform | 
| -bg, --background | str | -bg none | Background color. Valid options: none, white, grey, black |
| -op, --operations | int | -op 3 | Approximate number of operations per iteration, varies by up to 50% |
| -o, --output | str | -o pollock | Output filename, do not include .png |
| -mc, --manualcolor | str | -mc pollockcolor.txt | Manually define colors with a file |

### mondiran.py

| Flag | Argument Type | Example | Description |
| ---- | ------------- | ------- | ----------- |
| -r, --resolution | str | -r 1000x1000 | Set the resolution of the image in pixels. "widthxheight" | 
| -g, --grid | str | -g 10x10 | Set the resolution of the grid in tiles. "widthxheight" |
| -c, --colors | int | -c 3 | Number of random colors to use |
| -o, --output | str | -o mondrian | Output filename, do not include .png |
| -mc, --manualcolor | str | -mc mondcolor.txt | Manually define colors with a file |
| -cd, --colordensity | int | -cd 30 | Probability of a tile being colored as an integer percentage (30 = 30% chance) |

## Color File Format

Each line represents an RGB color expressed as three floats from 0 to 1 separated by commas. (e.g. 0,0,0 is black, 1,1,1 is white, and .5,.5,.5 is grey)
