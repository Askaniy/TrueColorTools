# True Color Tools
Astronomy-focused set of Python tools with GUI that use spectra construction and eye absorption to calculate realistic colors.

Input data is accepted in the form of channel measurements, color indices, or magnitudes. Customizable output in floating point or hexadecimal formats. Multispectral image processing and blackbody/redshifts colors calculating are also supported.

![TCT preview](ViewMe.png)


## Installation

### Basic installation way

TrueColorTools has been tested on Windows 10/11 and Linux (openSUSE).

1. Clone the repository or download archive by the GitHub web interface (press the button `Code`, then choose `Download ZIP` and unpack the archive after downloading);
2. Ensure that you have Python (version 3.9 or higher) and the libraries required in [requirements.txt](requirements.txt). You can install the libraries all at once using the following command: `python -m pip install -r requirements.txt`;
3. Execute `python -u runTCT.py`.

### Executable file (Windows)

This installation way supports by [SevenSpheres](https://github.com/SevenSpheres) and the relevance of updates is not guaranteed.

1. Go to [releases of SevenSpheres' fork](https://github.com/SevenSpheres/TrueColorTools/releases);
1. Select, download and unpack the desired archive from the assets;
1. Run `TCT.exe`.


## How it works?

The key processing method is converting the data into a continuous (5 nm step) spectrum and applying the absorption function of the eye to it. The key idea is to apply this method to a variety of use cases. Summarizing the standard steps:

1. Reading data, converting to the form "wavelength: brightness value". Built-in filter information is used to work with color indices and spacecraft images.
2. The obtained values ​​are interpolated (and extrapolated if required). There are two modes, fast linear (built-in) and slow Akima interpolator (imported from SciPy) with linear extrapolation. I know this is a bit of a simplification, but developing full spectrum reconstruction from absorption curves would be at the expense of other features.
3. Stiles & Burch 1959 10 Degree RGB CMFs are used to convert spectrum to color. Directly, without converting to a XYZ color space, since this caused additional problems. If you want to try, sRGB mode is for you, but I don't recommend it.


## How to use?

[`TCT.py`](scr/TCT.py) is functionally divided into 4 tabs: *Spectra*, *Images*, *Table* and *Blackbody & Redshifts*. No internet connection is required.

**Spectra tab** provides access to the built-in spectra database and allows you to calculate a color with the selected settings just by clicking on an object. It is possible to plot one or several spectra from the database, and the figure will open in your default browser.

**Images tab** allows you to load one color or several monochrome images, specify wavelengths, and save a processed image, for each pixel of which a spectrum was built. It takes a long time, so you can check out the preview. The wavelength values can be set by the choice of spacecraft filters, and they should always increase.

**Table tab** generates an image of all the colors of the selected category. You can see examples [here](tables/).

**Blackbody & Redshifts tab** calculates the influence of physical phenomena on color. Based on the blackbody spectrum, the program displays the changes in color and brightness from Doppler and gravitational redshifts. You can lock the exposure through the spectral irradiance scale, converted into stellar magnitudes per 1 nm. The surface brightness selected by the slider is assumed to be unity.

### Features
- Tag system: Each object in the database can be assigned an arbitrary set of tags. They form lists of categories in the *Spectra* and *Table* tabs, which makes it easier to work with a huge database.
- Reference system: Each object in the database can be easily linked to one or several data sources by its short name. You can see the list in `File`→`Sources`. Also, after an object's name there can be abbreviations, the decoding of which is indicated in `File`→`Notes`.
- Multilingual support: The language can be changed through the top menu in runtime. TCT supports English, German and Russian. If you want to add support for your language, you can do it by analogy in [`strings.py`](scr/strings.py).


## Database Extension
Spectra and their references are stored in the [`core_database.py`](spectra/core_database.py) and complementary `*.json5` files. The [`core_database.py`](spectra/core_database.py) can affect internal processes, so it is not recommended to change it. However, you can add custom json5 files to the `/spectra` folder and they will be detected. Newly read spectra, if they suddenly have the same names, replace the old ones. You can help the project by creating and sharing database files. Note that any parameters must increase with wavelength.

### Database keys
- `nm`: list of wavelengths in nanometers
- `br`: same-size list of linear physical property, representing "brightness"
- `mag`: same-size list of magnitudes
- `filters`: filter system, linked with [`filters.py`](scr/filters.py)
- `indices`: dictionary of color indices, use only with `filters`
- `bands`: list of filters' names, use only with `filters`
- *(optional)* `albedo`: bool (`True` if reflectivity was set by albedo values) or float (in V band or on 550 nm)
- *(optional)* `sun`: bool (`True` if spectrum contains the solar reflection)
- *(optional)* `tags`: list of strings, categorizes a spectrum