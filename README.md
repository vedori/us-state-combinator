# Data preprocessing
## GDP and Population Data
Had to clean up raw data from government excel doc
Once cleaned up, I exported the data as a CSV file
Expects a csv file formatted as follows:
1.
`COUNTY_NAME,STATE_NAME,VALUE\n`
2.
`COUNTY_NAME+CITY_NAME,STATE_NAME,VALUE\n`
3.
`COUNTY_NAME+CITY_NAME+CITY_NAME,STATE_NAME,VALUE\n`
# Notable data information
## GDP DATA
- [The data comes from the 2023 section of the US census](https://www.bea.gov/data/gdp/gdp-county-metro-and-other-areas)
- The specific unit is Thousands of dollars (chained to 2017), so 1,000 is $1 mil 2017 dollars
### Virginia combination areas
- Virginia combination areas consist of one or two independent cities with populations of less than 100,000, combined with an adjacent county. 
- The county name appears first, followed by the city name(s).
### Indepencdent cities (Virginia)
Virginia also has Independent cities, unsure whether to ignore this and list them as counties,
but if it shows up as its own thing then that's what it is.
### Hawaii
Maui and Kalawao are combined
### Idaho
Fremont includes Yellowstone National Park
## POP DATA
- [The data comes from the 2023 section of the US census](https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-total.html)
### Suggested citation
Annual Estimates of the Resident Population for Counties in the United States: April 1, 2020 to July 1, 2024 (CO-EST2024-POP)
Source: U.S. Census Bureau, Population Division
Release Date: March 2025
