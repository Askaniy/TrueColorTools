# True Color Tools
Astronomy-focused set of Python tools with GUI that use spectra construction and eye absorption to calculate realistic colors.

Input data is accepted in the form of channel measurements, color indices, magnitudes, physical parameters and even images. 
Customizable output in RGB, Hex, image or spectra database table.

![TCT preview](ViewMe.png)


## Installation

**Basic installation way**

Tested on Windows 10/11 and Linux (openSUSE).

1. Clone the repository or download archive by the GitHub web interface (press the button `Code`, then I recommend choosing `Download ZIP`, unpack the archive after downloading);
2. Make sure you have Python (recommended 3.10 or higher) and the required libraries: [NumPy](https://numpy.org/), [SciPy](https://www.scipy.org/), [Pillow](https://pillow.readthedocs.io/), [Plotly](https://plotly.com/python/) and [PySimpleGUI](https://pysimplegui.readthedocs.io/) (4.29 or higher). If you use Anaconda, the first 4 libraries are already preinstalled. You can install the libraries all at once using [`requirements.txt`](requirements.txt): `python -m pip install -r requirements.txt`;
3. Run [TCT.py](Scripts/TCT.py)

Note: Python 3.7 was the main version until July 2022, when I decided to upgrade to 3.10. Requirements are set at this point, but you can try using older versions for a while.

**Executable file (Windows)**

This installation way supports by [SevenSpheres](https://github.com/SevenSpheres) and the relevance of updates is not guaranteed.

1. Go to [releases of SevenSpheres' fork](https://github.com/SevenSpheres/TrueColorTools/releases);
1. Select, download and unpack the desired archive from the assets;
1. Run TCT.exe


## How it works?

The key processing method is converting the data into a continuous (5 nm step) spectrum and applying the absorption function of the eye to it. The key idea is to apply this method to a variety of use cases. Summarizing the standard steps:
1. Reading data, converting to the form "wavelength — brightness value". Built-in filter information is used to work with color indices and spacecraft images.
2. The obtained values ​​are interpolated (and extrapolated if required). There are two modes, fast linear (built-in) and slow Akima interpolator (imported from SciPy) with linear extrapolation. I know this is a bit of a simplification, but developing full spectrum reconstruction from absorption curves would be at the expense of other features.
3. Stiles & Burch 1959 10 Degree RGB CMFs are used to convert spectrum to color. Directly, without converting to a XYZ color space, since this caused additional problems. If you want to try, sRGB mode is for you, but I don't recommend it.


## How to use?

[`TCT.py`](Scripts/TCT.py) is functionally divided into 4 tabs: *Spectra*, *Images*, *Table* and *Blackbody & Redshifts*. No internet connection is required.

**Spectra tab** provides access to the built-in spectra database and allows to calculate a color with the selected settings just by clicking on an object.

For example, you can get colors formatted for [Celestia](https://github.com/CelestiaProject/Celestia), which uses chromaticity values from 0 to 1 for each color channel, where 1 is the value of the brightest channel. Make sure that the `chromaticity` mode is used and `Decimal places` is greater than zero (by default it is), and then set the `Color (bit) depth` parameter to zero.

**Images tab** allows you to load image(s), specify wavelengths and save a processed image, for each pixel of which a spectrum was built. It takes a long time, so you can check out the preview. The wavelength values can be set by the choice of spacecraft filters and they should always increase. Input can be in form of color image (`Single image mode`) or ≥2 b/w images.

**Table tab** generates an image of all the colors of the selected category and their sources. You can see examples [here](Tables/).

Notes: sources are renumbered by usage in the processed category; to use the *Table* tab on Linux, the NotoSans font family must be installed in `/usr/share/fonts/truetype/`.

**Blackbody & Redshifts tab** calculates the influence of physical phenomena on color. Based on the blackbody spectrum, the program displays the changes in color and brightness from Doppler and gravitational redshifts. You can lock the exposure through the logarithmic spectral irradiance scale. It is measured in energy from 1 m² on 550 nm in the 1 nm range.

### Auxiliary
- [`calculations.py`](Scripts/calculations.py) is the mathematical core. It contains most of functions and some zero points of photometric systems;
- [`cmf.py`](Scripts/cmf.py) contains sensitivity of human perception and used curve of color space;
- [`database.py`](Scripts/database.py) contains spectra, color indices and their sources;
- [`filters.py`](Scripts/filters.py) is a database of spacecraft photometric systems;
- [`strings.py`](Scripts/strings.py) contains almost all used inscriptions of other scripts in supported languages.

### Important notes
- Tag system. Each object in the database can be assigned an arbitrary set of tags. They form lists of categories in the *Spectra* and *Table* tabs, which makes it easier to work with a huge database.
- System of sources. Each object in the database can be easily linked to one or several sources by its number. You can see the list in `File`→`Sources`. Also, after an object's name there can be abbreviations, the decoding of which is indicated in `File`→`Notes`.
- The language can be changed through the top menu. Runtime translation is not available only for tab titles (due to PySimpleGUI limitations). For full localization, you can change the `lang` variable in the [`TCT.py`](Scripts/TCT.py) code. TCT supports English, German and Russian. If you want to add support for your language, you can do it by analogy in [`strings.py`](Scripts/strings.py).


## Database modification
Format of spectra database is just a dictionary in a Python file. You can modify it with your own spectra, and, if you want, share data for TCT. There are many examples in the database and the easiest way is to do by analogy. Note that any parameters must increase with wavelength.

### Dictionary keys
- `nm`: list of wavelengths in nanometers
- `br`: same-size list of reflectivity
- `mag`: same-size list of magnitudes
- `filters`: filter system, linked with [`filters.py`](Scripts/filters.py)
- `indices`: dictionary of color indices, use only with `filters`
- `bands`: list of filters' names, use only with `filters`
- *(optional)* `albedo`: bool (`True` if reflectivity was set by albedo values) or float (in V band or on 550 nm)
- *(optional)* `sun`: bool (`True` if spectrum contains the solar reflection)
- *(optional)* `tags`: list of strings, categorizes a spectrum