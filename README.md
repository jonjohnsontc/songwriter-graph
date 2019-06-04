# Songwriter Graph

The Songwriter Graph has been created with the idea to better connect listeners to songwriters. Often underappreciated and overlooked, this recommender system is designed to give listeners more information about how their favorite songs are written. There will eventually be a front end interface to deliver this information to users, but in the meantime, you can check out how the sausage is made or help contribute.

## Updates to Come

In the near future, I plan on adding a number of additions, including:

- A web interface to query the recommender (you can view the code so far [here](https://github.com/jonjohnsontc/si_app))
- Adding song lyrics as an additional set of features
- Recommending songwriters given a particular song of interest
- Incorporating songwriter credits into the model

## Layout 

You'll find this project currently spread over 3 different folders, though this is subject to change with the inclusion of additional content.

- [data](./data) - Where all of the datasets generated are stored
- [pickle](./pickle) - Where all of the pickled/interim variables are stored
- [notebooks](./notebooks) - The notebooks which the work to build the model. Please note that these are still quite messy.
  - [library](./notebooks/library) - Where you can find all of the re-usable functions utilized to collect and transform the data used in the recommender
- [`data_dictionary.md`](data_dictionary.md) - Where you can find definitions of all the features used in the recommender
- [`requirements.txt`](requirements.txt) - All of the libraries necessary to run through each notebook
