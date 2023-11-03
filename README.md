# Star classification with Machine Learning

The purpose of this project is to use photometric and spectroscopy data observations to train a machine learning model that classifies objects into three different classes: stars, galaxies, and quasars. The trained model is wrapped into a prediction service that can be used locally or deployed to the cloud using AWS Elastic Beanstalk.

The project is organzied as follows:
- [Data explanation](#what-type-of-data-are-we-dealing-with)
- [Environment setup](#)
- [Exploring the data](#)
- [Training the model](#)
- [Runing the service](#)

## What type of data are we dealing with? 

The dataset is provided by the [SDSS project (Sloan Digital Sky Survey)](https://en.wikipedia.org/wiki/Sloan_Digital_Sky_Survey). The data contains thousands of photometric observations of astronomical objects. Each observation is labeled with the type of objects which can be galaxies, stars, and quasars.

The SDD telescopes are equipped with imaging cameras that measure the intensity of incoming radiation in the electromagnetic spectrum. In the cameras, different type of filters are placed to measure the radiation at different frequencies. This intensities are available as features in the dataset:

-  **u**: ultraviolet light
-  **g**: blue and green visible light
-  **r**: yellow and red visible light
-  **i**: near-infrared light
-  **z**: near-infrared light

In addition to the above filters, the dataset includes a measurement of the redshift (**z**). For a celestial body, this value is defined as the difference between observed and emitted wavelength, divided by the emitted wavelength. [Read this](https://voyages.sdss.org/preflight/light/redshift/) for a more extended explanation.

Furthremore, we also have the data for the coordinates of the celestial objects. These are the **alpha** and **delta** and represent the coordinates on the celestial sphere. This [post](https://voyages.sdss.org/preflight/locating-objects/ra-dec/) describes how they are measured. For the purpose of this analysis it is useful to understand that they represent coordinates in degrees.

All the previously described data measurements are used to create a model for star classification. 

## Environment setup

In order to run the notebooks and scripts provied in this repositoy, you should download [this dataset](https://www.kaggle.com/datasets/fedesoriano/stellar-classification-dataset-sdss17) and save it to the folder **data** in the root of this repository.

For managing the python dependencies and virtual environments I chose poetry. To set it up, follow [these installing instructions](https://python-poetry.org/docs/).

With poetry installed in your system, you can run the command:

```console 
poetry install
```

Which will read from the [pyproject.toml](pyproject.toml) to install the required dependencies. 

Finally, make sure that you have Docker setup in your system and the aws-cli if you want to deploy the service to the cloud.

## Exploring the data

With the python poetry environment setup, you can run the [notebook](./star_classification.ipynb). It contains an exploratory data analysis as well as the training and finetuning of different ML models and several evaluation metrics. The analysis suggest that the best performance is obtained using an XGboost model giving a macro accuracy of 98%.

## Training the model

The optimal hyperparameters found in the notebook are used to train the model directly using the [training script](./model_training.py). To execute the script use:

```console 
make run-training
```

This will create a model json file in the /models folder which can be used in the service to make predictions.

## Running the service

wWith the previous step you should have an Xgboost model json file available and next it can be used to make predictions.
I use the framework **quart** instead of **flask** as it provides much better support for asynchronous calls and has basically the same usage as flask. 

The make file has several commands to run the service using different methods:

**Run the service locally**

```console 
make run-server-local
```

**Run the service with docker**

first make sure you build the docker image with 

```console
make build-image
``` 

and then use 

```console 
make run-server-docker
```

To test the service we can use a POST call to the predict endpoint:

```console
curl --location 'http://star-prediction-env.eba-g3cym73c.eu-central-1.elasticbeanstalk.com/predict' \
--header 'Content-Type: application/json' \
--data '{
    "alpha": 118.66,
    "delta": 39.642,
    "u": 22.857,
    "g": 22.188,
    "r": 21.355,
    "i": 21.265,
    "z": 20.939,
    "redshift": 1.174
}'
```

Change any of the body parameters to observe how the model predicts different classes


## Deploying to AWS Elastic Beanstalk

Make sure you have an aws account configured in your system. 

Initialize the project

```console
eb init -p docker --profile {your_aws_profile} -r {aws_region} star-model-serving
```

Test locally

```console 
eb local run --port 8000
```

If everything works, it can be deployed to aws with:

```console
make aws-deploy
```

It can take up a few minutes until the neccesary resources are create and initialized. When it is done, the console output will provide an url where the service is available.

Finally, clean up all the resources to avoid undesired aws costs:

```console
make aws-delete-env
```


