![Header logo](logo_header.webp)

An astronomy-focused set of tools with a GUI that uses spectrum construction and eye absorption to compute realistic colors.

Input data is accepted in the form of filters measurements (such as color indices) or continuous spectra, in irradiance units or in magnitudes. Stores a comprehensive catalog of photometry in a proprietary format. Can process spectral cubes, multiband spacecraft images and correct images in enhanced colors.

To calibrate the color of maps based on TCT data, I recommend using [Cylindrical Texture Calibrator](https://github.com/Askaniy/CylindricalTextureCalibrator).

![TCT screenshot](screenshot.png)


## Installation

TrueColorTools works on Windows and Linux (the GUI library might be unstable on macOS). Python version 3.11 or higher is required.

1. Clone the repository or download the archive using the GitHub web interface;
2. Open the console in the project root folder;
3. Create a virtual environment with `python3 -m venv .venv`;
4. Install the dependencies with `.venv/bin/pip install -r requirements.txt`;
5. Execute `.venv/bin/python runTCT.py`.

### Executable file

An alternative way for Windows 8/10/11. Stable versions are compiled into an executable file, Python installation is not required.

1. Go to [the latest release page](https://github.com/Askaniy/TrueColorTools/releases/latest);
2. Download and unpack the first archive;
3. Launch the `runTCT.exe`.


## How it works?

TCT converts photometric measurements into a continuous spectrum (if it isn't already a spectrum) and convolves it with eye color matching functions (CMFs). A set of photographs (e.g. taken by a spacecraft) is counted and processed in the same way as photometry.

According to a common color processing procedure, after convolution from CMF to CIE 1931 XYZ color space, the color is converted by a 3×3 matrix to the selected color system.
The matrix is formed from the specified color space and (optional) white point for chromatic adaptation. The default is the most common color space (sRGB) with a natural-looking white point, equal-energy spectrum (illiminant E).

The photometric measurements read from the database are calibrated at runtime using the specified calibration system and filter profiles. Zero points are not required. Spectra and filter profiles are stored on a grid with a 5-nm step in energy spectral density units (e.g., W/(m² nm)).

Interpolation is not used to reconstruct the spectrum from the photometry because it is not a solution to the inverse problem (i.e., looking at the spectrum through the filters does not give exactly the original photometry). Therefore, the Tikhonov regularization method is applied, which (almost) guarantees the solution of the ill-posed problem. A combination of first-order and second-order differential operators is chosen for the Tikhonov matrix (tries to minimize height variations and curvature in the spectrum) with a restriction to negative values.


## How to use?

Interaction with TrueColorTools is implied through the GUI. However, if you are an advanced Python user, you can import the core (`from src.core import *`) and use it as a spectral processing library.

If you are running the GUI from the command line, you can set the startup language <!--- and CLI verbosity level--> (run with `--help` for details). No Internet connection is required, the databases are stored in the appropriate repository folders, and you can replenish them.

Program interface is functionally divided into tabs: *Database viewer*, *Image processing* and *Blackbody & Redshifts*. Color output formatting, often common to tabs, is located in the sidebar settings.

The **Database viewer** tab provides access to the spectra database and allows you to calculate a color with the selected settings by simply clicking on an object. It is possible to plot one or more spectra from the database in a pop-up window. You can process the colors of an entire category at once and get the output in text form or as a graphical table ([examples](tables/)).

The **Image processing** tab accepts regular images, a series of black and white images, or a spectral cube as input. Using the wavelength information, the image is "reshot" in true color. The internal operations are similar to reconstructing the spectrum for each pixel, but use efficient operations on arrays.

The **Blackbody & Redshifts** tab calculates the influence of physical phenomena on color. Based on the blackbody spectrum, the program displays the color and brightness changes due to Doppler and gravitational redshifts. Surface brightness is tied to the `Maximize brightness` checkbox, otherwise can be adjusted with the slider.

### Features
- Tag system: Any spectrum in the database can be assigned any set of tags. They form lists of categories for the *Database viewer* tab, which makes working with the database easier.
- Reference system: Each object in the database can be easily linked to one or more data sources by its short name. You can see the list in `Menu`→`References`.
- Multilingual support: The language can be changed from the top menu at runtime. TCT supports English, German and Russian. If you want to add support for your language, you can do it similar to [`strings.py`](src/strings.py) and make a commit or contact me.


## Databases

### Spectra database structure
The JSON5-formatted database stores two types of data: references and (photo)spectral objects. There are no restrictions on their order and relative position (data block and its reference block can be in different files), it is usually more convenient to list the sources at the beginning of the file or right before the spectra they describe.

The object name may contain formatting indicators for the GUI and the color table, the template is `(index) name: note (info) | reference`. The contents of the brackets are placed in the upper left corner; colon followed by a note; what appears after a vertical bar is reference(s) and is placed in the upper right corner. The naming conventions in the GUI may vary and try to follow naming standards in astronomy.

The brightness scale is not strictly tied to physical quantities. Using one of the logical albedo keys (`is_geometric_albedo`, `is_spherical_albedo`, `is_albedo`), you can indicate that the appropriate spectrum is scaled and the brightness should be treated as reflectance factor. You can also tell the program to scale the spectrum by albedo in a band through the following keys: `geometric_albedo`, `spherical_albedo`, `albedo`.

Geometric albedo is a reflection coefficient at the zero phase angle (normal albedo is now not distinguished from geometric albedo). It is usually brighter than the spherical albedo, the ratio of all incident light to all reflected light. If one is not specified in the database or can't be calculated from the phase function, TCT uses a [theoretical model](https://ui.adsabs.harvard.edu/abs/2019A%26A...626A..87S/abstract) to convert one to the other for the appropriate brightness display mode. If no albedo is specified, the object will not be displayed in albedo modes (exception for the `star` tag). The `albedo` key indicates both albedos at once, but it is not recommended.

Phase functions are used to calculate phase integral, which is used to convert between spherical and geometric albedo. The name and function parameters are stored as `[name, {param1: value1, ...}]`, each value can go with uncertainty. `Hapke` model also calculates albedo, therefore `[filter/nm, name, params]` format is supported to indicate reference spectral range (it will have no effect for other models).

The following phase functions are supported:
- `phase coefficient`: requires `beta`, the logarithmic slope parameter;
- `exponentials`: requires `A_1`, `mu_1`, …, `A_n`, `mu_n`, see [Velikodsky et al. 2011](https://www.sciencedirect.com/science/article/abs/pii/S0019103511001564);
- `HG`: requires `G` parameter (`H` is optional), see [Bowell et al. 1989](https://ui.adsabs.harvard.edu/abs/1989aste.conf..524B/abstract);
- `HG1G2`: requires `G_1` and `G_2` (`H` is optional), see [Muinonen et al. 2010](https://ui.adsabs.harvard.edu/abs/2010Icar..209..542M/abstract);
- `Hapke`: requires `w`, `bo`, `h`, `b`, `c` and `theta`, see [Hapke, B. 1984](https://www.sciencedirect.com/science/article/abs/pii/001910358490054X).

For photometry, it is necessary to specify calibration spectrum if it's not an equal-energy irradiance density by wavelengths ([this link](https://hst-docs.stsci.edu/acsdhb/chapter-5-acs-data-analysis/5-1-photometry#id-5.1Photometry-5.1.15.1.1PhotometricSystems,Units,andZeropoints) may help). Typically you need to specify `calibration_system: 'AB'` when working with Sloan filters (u, g, r, i, z) and `calibration_system: 'Vega'` for all other cases. For absolute magnitudes, use `is_reflecting_sunlight: false`.

Supported input keys of a database unit:
- `tags` (list): strings categorizing the spectral data, optional
- `nm` (list): list of wavelengths in nanometers
- `br` (list): same-size list of "brightness" in energy spectral density per wavelength units
- `mag` (list): same-size list of magnitudes
- `sd` (list/number): same-size list of standard deviations (or a common value)
- `nm_range` (dict): wavelength range definition in the format `{start: …, stop: …, step: …}`
- `slope` (dict): spectrum definition in the format `{start: …, stop: …, power/percent_per_100nm: …}`
- `file` (str): path to a text or FITS file, recommended placing in `spectra` or `spectra_extras` folder
- `filters` (list): list of filter names present in the `filters` folder (can be mixed with nm values)
- `color_indices` (list): dictionary of color indices, formatted `{'filter1-filter2': …, …}`
- `photometric_system` (str): a way to parenthesize the photometric system name (separator is a dot)
- `calibration_system` (str): `Vega` or `AB` filters zero points calibration, `ST` is assumed by default
- `geometric_albedo` (list): scales the data to geometric albedo spectrum, syntax is `[filter/nm, value]`
- `spherical_albedo` (list): scales the data to spherical albedo spectrum, syntax is `[filter/nm, value]`
- `albedo` (list): scales the data to both geom. and sphe. albedo spectra, syntax is `[filter/nm, value]`
- `bond_albedo` (number): scales the data to spherical albedo spectrum using known Solar spectrum
- `phase_integral` (number/list): transition factor from geometric albedo to spherical albedo
- `phase_function` (list): phase function name and its parameters to compute phase integral
- `br_geometric`, `br_spherical` (list): specifying unique spectra for different albedos
- `sd_geometric`, `sd_spherical` (list/number): corresponding standard deviations or a common value
- `is_geometric_albedo` (bool): `true` to interpret the data as a geometric albedo spectrum
- `is_spherical_albedo` (bool): `true` to interpret the data as a spherical albedo spectrum
- `is_albedo` (bool): `true` to interpret the data as a both geom. and sphe. albedo spectra
- `is_reflecting_sunlight` (bool): `true` to divide the data by the reflected Solar spectrum
- `is_emission_spectrum` (bool): `true` to interpret the data points as spectral lines
- `is_emissive` (bool): `true` not expect albedo data and always render in the chromaticity mode

Standard deviations are syntactically supported (but not always processed). Any brightness value in any of the data types can be replaced by a corresponding list of `[value, sd]` (or `[value, +sd, -sd]` for asymmetric standard deviation).

You can store the file with the spectrum outside of JSON5, and include a link in it. Text (`*.txt`, `*.dat`) and FITS (`*.fits`, `*.fit`) formats are supported for external files. A text file must contain at least wavelengths in the first column, irradiance in the second column, and optionally standard deviations in the third column and a mask in the fourth column ("good" rows in SMASS data marked with "1"). Data is assumed to be in the second HDU in FITS files. If you have problems reading FITS, contact me, I'll improve the parsing of the provided example.

As in JSON5, the default wavelengths for external files are in nanometers and the spectrum is in energy density. For FITS files, TCT attempt to determine the wavelength unit from internal data. You can also force the data type by using letters in the file extension (`.txt` for example):
- `.txtN` for nanometers (by default), `.txtA` for ångströms, `.txtU` for micrometers;
- `.txtE` for energy counters per wavelength (by default), `.txtJ` for energy counters per frequency (like jansky), `.txtP` for photon counters.

### Spectra database extension
The data in the `/spectra` folder can be modified by the user (except for [Sun](spectra/files/CALSPEC/sun_reference_stis_002.fits) and [Vega](spectra/files/CALSPEC/alpha_lyr_stis_011.fits), which are used for calibration). The display order in the *Database viewer* is determined by the file names and the order within the file. If the spectrum header is repeated in the database, the last spectrum will replace the previous one. The tag list is created and completed while reading files. `/spectra_extras` is recommended as the storage location for user files and add-ons; they will be shown last in the GUI. There is a [pinned issue](https://github.com/Askaniy/TrueColorTools/issues/26) for sharing "official" and user add-ons. Pull requests are welcome too.

### Filters database extension
TCT uses filter sensitivity profiles for accurate spectrum restoration. They are provided by the [SVO Filter Profile Service](http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php) and stored [here](/filters). To replenish the database, select a filter on the site, select the "ascii" data file and place it in the folder. You need also specify the wavelength unit (usually ångströms, so you get the `.datA` extension). If you see "Detector Type: **P**hoton counter" in the filter description there (instead of "Energy counter", which we need) you need to add `P` to the extension. (Do not edit the [V band filter](filters/Generic_Bessell.V.dat), it is needed for the program to work.)

Short help on the UBVRI photometric system implementations:
- `Generic_Johnson` takes into account the sensitivity of photomultiplier tubes, mostly affected on R and I bands. Use **only** if the measurements were actually taken on a PMT.
- `Generic_Cousins` contains only R and I bands. Can be used directly with the U, B, V from the Johnson system, but the error is expected to be large.
- `Generic_Bessell` is actually Johnson—Cousins system for CCD receivers. Recommended by default.


## Acknowledgements

My thanks to *arbodox* for the creation of the project logo.
Thanks to *SevenSpheres* for the Windows releases compilation.
Thanks to the Celestia community for the support.

This research has made use of:
- [Spanish Virtual Observatory](https://svo.cab.inta-csic.es) project funded by MCIN/AEI/10.13039/501100011033/ through grant PID2020-112949GB-I00
    - [The SVO Filter Profile Service. Rodrigo, C., Solano, E., Bayo, A., 2012](https://ui.adsabs.harvard.edu/abs/2012ivoa.rept.1015R/abstract);
    - [The SVO Filter Profile Service. Rodrigo, C., Solano, E., 2020](https://ui.adsabs.harvard.edu/abs/2020sea..confE.182R/abstract);
- [Colour & Vision Research laboratory and database](http://www.cvrl.org/)
    - [CIE 1931 2-deg, XYZ colour matching functions](http://www.cvrl.org/cie.htm);
    - [Stiles & Burch (1955) 2-deg colour matching functions](http://www.cvrl.org/stilesburch2_ind.htm).
