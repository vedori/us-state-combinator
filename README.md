# Data preprocessing

**ALL DATA** collected from 2020

## GDP and Population Data

Had to clean up raw data from government excel doc
Once cleaned up, I exported the data as a CSV file
Some cities are independent of any counties and will end in "City" instead of "County"
Expects a csv file formatted as follows:
1.
`COUNTY_NAME,STATE_NAME,VALUE\n`
2.
`COUNTY_NAME+COUNTY_NAME+...,STATE_NAME,VALUE\n`

## Connecticut

This state has councils of governments (COGs) that function similarly to a county but
was only fully recognized as equivalent by the US census bureau in 2022.
The **GDP** data from BEA still uses the traditional county divisions.

# GDP DATA

**The next GDP by county release is February 5, 2026**

- [The data comes from the US Bureau of Economic Analysis (BEA)](https://www.bea.gov/data/gdp/gdp-county-metro-and-other-areas)
- The specific unit is Thousands of dollars (chained to 2017), so 1,000 is $1 mil 2017 dollars

## Virginia combination areas

- Virginia combination areas consist of one or two independent cities with populations of less than 100,000, combined with an adjacent county.
- The county name appears first, followed by the city name(s).

## Hawaii

Maui and Kalawao are combined

## Idaho

Fremont includes Yellowstone National Park

# POP DATA

- [The data comes from the 2020 decennial US census](https://data.census.gov/table/DECENNIALPL2020.P1?q=Decennial+Census&g=010XX00US$0500000&y=2020&tp=true)
