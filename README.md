# Joggling Results Archive

I've created a streamlit web app to present a compilation of joggling results from around the world, from the 1980's to the present day. This resource exists to serve the joggling community with regard to all-time rankings over different distances, along with being a place to host other joggling fun, such as the Joggler network visualisation, and the quarterly Joggler's Jottings Newsletter.

The app can be accessed here: https://jogglingresults.streamlit.app/ 


#### Developer Notes
On around a monthly basis, I add the latest results to the results.csv file. Jogglers submit their results here: https://docs.google.com/forms/u/0/d/e/1FAIpQLSekhuhhZKzYHdS-hN9owER17PPRgxAfC_DODLKGuwZyXHPkOQ/viewform?pli=1

To update the app:
- Update the `results.csv` file in the data directory of the repo.
- Run the `data/z-prepare_data.py` script to update all of the artifacts (csv, figures, etc.) used by the app.
- Update the update_date in `home.py`


#### Azure Deployment
- Deployed at https://jogglingresultsarchive.azurewebsites.net/ as an Azure web app.
- Though some dependency issues with plotly, yet to be resolved, mean the joggler map isn't working.