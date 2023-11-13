# True Color Tools
Astronomy-focused set of Python tools with GUI that use spectra construction and eye absorption to calculate realistic colors.

Input data is accepted in the form of channel measurements, color indices, or magnitudes. Customizable output in floating point or hexadecimal formats. Multiband image processing and blackbody/redshifts colors calculating are also supported.

**Note**: images processing is temporarily not works. Go to the commit #13cd296 for something stable.

![TCT screenshot](screenshot.png)


## Installation

### Basic installation way

True Color Tools has been tested on Windows 10/11, macOS and Linux. It requires Python 3.10 or higher version, which do not support Windows 7. [This](https://github.com/adang1345/PythonWin7) launch tool can be used for the case.

1. Clone the repository or download archive by the GitHub web interface (press the button `Code`, then choose `Download ZIP` and unpack the archive after downloading);
2. Ensure that you have libraries listed in [requirements.txt](requirements.txt). You can install them all at once using the following command: `python3 -m pip install -r requirements.txt`;
3. Execute `python3 -u runTCT.py`.

### In a virtual environment

2. Open the folder in terminal and create a virtual environment with `python3 -m venv .venv`;
3. Install the libraries needed by `.venv/bin/pip install -r requirements.txt` (versions were frozen as of November 12, 2023);
4. Execute `.venv/bin/python3 -u runTCT.py`.

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

Program interface is functionally divided into tabs: *Database viewer*, *Multiband processing* and *Blackbody & Redshifts*. Color output formatting, often common to tabs, is located in the sidebar settings.

**Database viewer** provides access to the spectra database and allows you to calculate a color with the selected settings just by clicking on an object. It is possible to plot one or several spectra from the database in a pop-up window. You can process the colors of an entire category at once, and get the output in the text form or a graphic table ([examples](tables/)).

**Multiband processing** allows you to directly access photometry calculations. Single measurements or set of images in different filters, or spectral cubes are accepted as input. For each pixel of an image, its spectrum is restored and converted into color.

**Blackbody & Redshifts tab** calculates the influence of physical phenomena on color. Based on the blackbody spectrum, the program displays the changes in color and brightness from Doppler and gravitational redshifts. You can lock the exposure on the apparent magnitude logarithmic scale, adjusting the overexposure limit for a tuned blackbody object if it was in the sky replacing the Sun (with the angular size).

### Features
- Tag system: Each spectrum in the database can be assigned an arbitrary set of tags. They form lists of categories for the *Database viewer* tab, which makes working with the database easier.
- Reference system: Each object in the database can be easily linked to one or several data sources by its short name. You can see the list in `File`→`References`. Also, object name can contain abbreviations, the decoding of which is indicated in `File`→`Notes`.
- Multilingual support: The language can be changed through the top menu in runtime. TCT supports English, German and Russian. If you want to add support for your language, you can do it by analogy in [`strings.py`](src/strings.py) and make a commit or contact me.


## Databases

### Spectra database structure
Data listed in a JSON5 file can be of two types: reference and photometry. There are no restrictions on their order and relative position at all (source and data can be in different files), but it is usually convenient to list the sources at the beginning of the file, then the spectra.

The brightness scale is not strictly tied to physical quantities. Using the `albedo` flag, you can indicate that the incoming spectrum is scaled and the brightness in the range 0 to 1 should be treated as reflectance. The scaling task can be left to the program by specifying a wavelength or filter for which the albedo is known. Optional internal standard is flux spectral density measured in W / (m² nm).

It is assumed that all data is indicated in ascending wavelength order, and for measurements that are calibrated according to Vega, a flag about this is required! TCT doesn't store information about which photometric systems use Vega as a white standard and which do not.

You can store the file with the spectrum outside of JSON5, and put a link in it. Text and FITS (*.fits, *.fit) formats are supported for external files. The text file must be in two columns without a header, and the first column of wavelengths must be in angstroms. In FITS files assumed data containing in the second HDU. If you have problems reading FITS, contact me, I'll improve the parsing on this example.

Supported input keys of a database unit:
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

### Spectra database extension
The data in the `/spectra` folder can be modified by user (except for the "vital" spectra of the [Sun](spectra/files/CALSPEC/sun_reference_stis_002.fits) and [Vega](spectra/files/CALSPEC/alpha_lyr_stis_011.fits)). The display order in the *Database viewer* is determined by the file names and the order within the file. When repeating the spectrum header in the database, the last spectrum replaces the previously specified one. Tags can be anything, nothing will break. Their list is formed after reading the files. `"/spectra extras"` is recommended as a storage location for user files; they will be shown first in the GUI. You can help the project by creating and sharing database files.

100 stellar spectra of [CALSPEC database](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec) (as of August 12, 2023) are stored as FITS files in the [spectra/files/CALSPEC](spectra/files/CALSPEC) folder. If you add spectrum from the database, it is recommended to take the "stis" version and pay attention to the presence of the B−V color index in the table.

### Filters database extension
TCT use filter sensitivity profiles for accurate spectrum restoration. They are provided by [SVO Filter Profile Service](http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php) and stored [here](/filters). To replenish the database, select a filter on the site, choose the "ascii" data file and place it in the folder. If you see "Detector Type: Photon counter" in the filter description there (instead of "Energy counter" we need) rename the file by putting `-` at the beginning.

Some of files in the `/filters` folder are "vital": [V band filter](filters/Generic_Bessell.V.dat) and human eye's color matching functions. You can create `"/filter extras"` folder for personal use.

Brief help on the UBVRI photometric system implementations:
- `Generic_Johnson` takes into account the sensitivity of photomultiplier tubes, mostly affected on R and I bands. Use **only** if the measurements were actually recorded on a PMT.
- `Generic_Cousins` contains only R and I bands. Can be used with the U, B, V from Johnson system directly, but the error is expected to be large.
- `Generic_Bessell` is actually Johnson—Cousins system for CCD receiver. Recommended by default.