# SpaceColorsCalculator
A set of Python scripts for calculating human-visible colors of celestial bodies by spectra and color indices

### List of Python libraries for all scripts to work:
* [NumPy](https://numpy.org/)
* [SciPy](https://www.scipy.org/)
* [Plotly](https://plotly.com/python/)
* [Pillow](https://pillow.readthedocs.io/)
* [PySimpleGUI](https://pysimplegui.readthedocs.io/)

### Description of scripts:
* `color_calc.py` is written to calculate the color of one or several objects and build their spectra;
* `color_calc_GUI.py` allows you to calculate colors much more conveniently with a graphical interface and visualization;
* `color_table.py` generates a table-poster of the colors of celestial bodies;
* `mapper_single.py` calibrates a set of maps in different ranges and calculates a spectrum for each pixel to calculate true colors;
* `mapper_batch.py` is used to process all the specified maps in `spectra.py` (they are not in this repository);
* `convert.py` contains everything that is directly related to processing (functions, zero points of photometric systems, used curves of color space and sensitivity of human perception);
* `spectra.py` is a database of spectra, color indices, sources and all other information used;
* `translator.py` contains almost all used inscriptions of `spectra.py`, `color_table.py`, `color_calc.py` and `color_calc_GUI.py` in supported languages.

### FAQ:
> How can I get formatted colors for Celestia?

Celestia uses chromaticity values from 0 to 1 for each color channel, where 1 is the value of the brightest channel. In the GUI version, you need to make sure that the `chromaticity` mode is used and `Decimal places` is greater than zero (by default it is), and then set the `Color (bit) depth` parameter to zero.


> How do I add my own spectrum?

Add it to the dictionary `objects` in `spectra.py`. It can be in two forms, but I don't yet recommend getting the spectrum from color indices. 
```py
"Object name": {
  "nm": [], # list of wavelengths in nm
  "br": [], # same-size list of reflectivity
  "albedo": # True (if reflectivity values are albedo values), False, or value (in V band or on 550 nm)
}
"Object name": {
  "filters": "", # one from convert.py → filters
  "indices": {"": 0, …, "": 0} # min wavelength color index → max wavelength color index
}
```

> Why it crashes if I choose German?

German is a stub in the file for storing titles in different languages, `translator.py`. If someone wants to add support for any language, this can be done simply.
