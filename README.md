## Star classification dataset

The purpose of this project is to use photometric and spectroscopy data observations to classify three types of objects: stars, galaxies, and quasars.

The dataset is provided by the [SDSS project (Sloan Digital Sky Survey)](https://en.wikipedia.org/wiki/Sloan_Digital_Sky_Survey). The data contains thousands of photometric observations of astronomical objects. Each observation is labeled with the type of objects which can be galaxies, stars, and quasars.

What type of data are we dealing with? 

The SDD telescopes are equipped with imaging cameras that measure the intensity of incoming radiation in the electromagnetic spectrum. In the cameras, different type of filters are placed to measure the radiation at different frequencies. This intensities are available as features in the dataset:

-  **u**: ultraviolet light
-  **g**: blue and green visible light
-  **r**: yellow and red visible light
-  **i**: near-infrared light
-  **z**: near-infrared light

In addition to the above filters, the dataset includes a measurement of the redshift (**z**). For a celestial body, this value is defined as the difference between observed and emitted wavelength, divided by the emitted wavelength. [Read this](https://voyages.sdss.org/preflight/light/redshift/) for a more extended explanation.

Furthremore, we also have the data for the coordinates of the celestial objects. These are the **alpha** and **delta** and represent the coordinates on the celestial sphere. This [post](https://voyages.sdss.org/preflight/locating-objects/ra-dec/) describes how they are measured. For the purpose of this analysis it is useful to understand that they represent coordinates in degrees.

All the previously described data measurements are used to create a model for star classification.