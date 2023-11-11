# True Color Tools
Astronomy-focused set of Python tools with GUI that use spectra construction and eye absorption to calculate realistic colors.

Input data is accepted in the form of channel measurements, color indices, or magnitudes. Customizable output in floating point or hexadecimal formats. Multiband image processing and blackbody/redshifts colors calculating are also supported.

![TCT screenshot](screenshot.png)


## Installation

### Basic installation way

True Color Tools has been tested on Windows 10/11, macOS and Linux. It requires Python 3.10 or higher version, which do not support Windows 7. [This](https://github.com/adang1345/PythonWin7) launch tool can be used for the case.

1. Clone the repository or download archive by the GitHub web interface (press the button `Code`, then choose `Download ZIP` and unpack the archive after downloading);
2. Ensure that you have libraries listed in [requirements.txt](requirements.txt). You can install them all at once using the following command: `python3 -m pip install -r requirements.txt`;
3. Execute `python3 -u runTCT.py`.

### Executable file

[SevenSpheres](https://github.com/SevenSpheres) compiles stable versions of True Color Tools for Windows 8/10/11. Thus, Python is not required in this installation way.

1. Go to [releases of SevenSpheres' fork](https://github.com/SevenSpheres/TrueColorTools/releases);
2. Select, download and unpack the desired archive from the assets;
3. Run `TCT.exe`.


## How it works?

The key processing method is converting a photometry data into a continuous spectrum and convolve it with color matching functions of an eye. Summarizing the standard steps:

1. Reading data, converting to the form "wavelength: brightness value". Built-in filter information is used to work with color indices and spacecraft images.
2. The obtained values ​​are interpolated (and extrapolated if required). The program uses its own functions for this, which work faster and more reliably than from SciPy. In plans replacing interpolation with a multidimensional minimum search.
3. There are two ways to get color. The first (default) convolve spectrum with experimentally obtained sensitivity curves directly. In the sRGB mode the calculations are more complex, but generally accepted: processing a spectrum first into the XYZ space, from which it transformed into sRGB with illuminant E (the equal energy white point is much better for our purposes than the standard D65).


## How to use?
GUI is the only way to interact with True Color Tools. When running it from the command line, you can set the startup language and CLI verbosity level (run with `--help` for details). No internet connection is required, the databases are stored in the appropriate folders of the repository, and you can replenish them.

Program interface is functionally divided into tabs: *Spectra*, *Images*, *Table* and *Blackbody & Redshifts*. Color output formatting, often common to tabs, is located in the sidebar settings.

**Spectra tab** provides access to the spectra database and allows you to calculate a color with the selected settings just by clicking on an object. It is possible to plot one or several spectra from the database in a pop-up window.

**Images tab** allows you to load one color or several monochrome images, specify wavelengths, and save a processed image, for each pixel of which a spectrum was built. It takes a long time, so you can check out the preview. The wavelength values can be set by the choice of spacecraft filters, and they should always increase.

**Table tab** generates an image of all the colors of the selected category. You can see examples [here](tables/).

**Blackbody & Redshifts tab** calculates the influence of physical phenomena on color. Based on the blackbody spectrum, the program displays the changes in color and brightness from Doppler and gravitational redshifts. You can lock the exposure on the apparent magnitude logarithmic scale, adjusting the overexposure limit for a tuned blackbody object if it was in the sky replacing the Sun (with the angular size).

### Features
- Tag system: Each object in the database can be assigned an arbitrary set of tags. They form lists of categories in the *Spectra* and *Table* tabs, which makes it easier to work with a huge database.
- Reference system: Each object in the database can be easily linked to one or several data sources by its short name. You can see the list in `File`→`Sources`. Also, after an object's name there can be abbreviations, the decoding of which is indicated in `File`→`Notes`.
- Multilingual support: The language can be changed through the top menu in runtime. TCT supports English, German and Russian. If you want to add support for your language, you can do it by analogy in [`strings.py`](src/strings.py) and make a commit or contact me.


## Database Extension
The data in the [spectra folder](spectra/) can be modified by the user (except for the "vital" spectra of the [Sun](spectra/files/CALSPEC/sun_reference_stis_002.fits) and [Vega](spectra/files/CALSPEC/alpha_lyr_stis_011.fits), they cannot be edited). Also, an `extras` folder can be created nearby, the contents of which will also be replenished with the database, at the top of the first tab's list. Spectrum and reference information is stored in JSON5 files. The program reads all the JSON5 files in the folder. The display order within TCT is determined by the file names and the order within the file. When duplicating, the last spectrum replaces the previously specified one. Tags can be anything, nothing will break. Their list is formed after reading the files. You can help the project by creating and sharing database files.

Spectrum brightness scale does not affect anything. If you know that the spectrum is reflectivity (where 0 is total absorption and 1 is total reflection), then you can set `albedo=true` and TCT will be able to show the true brightness. Specifying a floating point number will require TCT to make this spectrum in Bessell V filter give such an albedo. Optional internal standard (e.g. for "vital" Solar and Vegan spectra, *Blackbody & Redshifts* tab) is flux spectral density measured in W / (m² nm).

You can store the file with the spectrum outside of JSON5, and put a link in it. Text and FITS (*.fits, *.fit) formats are supported for external files. The text file must be in two columns without a header, and the first column of wavelengths must be in angstroms. In FITS files assumed data containing in the second HDU. If you have problems reading FITS, contact me, I'll improve the parsing on this example.

100 stellar spectra of [CALSPEC database](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec) (as of August 12, 2023) are stored as FITS files in the [spectra/files/CALSPEC](spectra/files/CALSPEC) folder. If you add spectrum from the database, it is recommended to take the "stis" version and pay attention to the presence of the B−V color index in the table.

TCT will use filter sensitivity profiles for more accurate spectrum restoration. They are provided by [SVO Filter Profile Service](http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php) and stored [here](/filters). To replenish the database, select a filter on the site, choose the `ascii` data file and place it in the folder.

### Database keys
Note that any parameters must increase with wavelength.
- `nm` (list): list of wavelengths in nanometers
- `br` (list): same-size list of "brightness" of an energy counter detector (not photon counter)
- `mag` (list): same-size list of magnitudes
- `nm_range` (list): list of [`start`, `stop`, `step`] integer values with including endpoint
- `file` (str): path to a text or FITS file, recommended placing in `spectra` or `extras` folder
- `filters` (list): list of filter names that can be found in the `filters` folder
- `indices` (list): dictionary of color indices, formatted `{'filter1-filter2': *float*, ...}`
- `system` (str): a way to bracket the name of the photometric system
- `albedo` (bool): `true` if brightness in the [0, 1] range represents scaled (reflective) spectrum
- `scale` (list): sets the (reflectivity) at the wavelength, formatted `[*nm or filter name*, *float*]`
- `sun` (bool): `true` to remove Sun as emitter
- `vega` (bool): `true` to untie from the white standard according to Vega
- `tags` (list): strings, categorizes a spectrum