The README provides a short summary of the project.
Where applicable, the README provides instructions for obtaining the necessary packages or libraries needed to run the code.
Where applicable, the README mentions any changes necessary to the code required to successfully run it.
The README provides instructions for obtaining similar or identical data to that used in the project.
The README provides instructions for how to generate plots similar or identical to those shown in the project computational essay.

## Overview

The goal of this project was to understand the quantity and characteristics of
repeat customers of Andrew's Etsy shop, ADesignsDenver. We did this by
connecting to Etsy API to pull all of the order reciepts into a JSON. Then we
processed the data to find key metrics such as repeat order rate, the sizes
of those orders, orders broken down by state, and time between repeat orders.
Finally we visualized the data using matplotlib.

## Dependencies


## How to run

To successfully run the code on your machine, you will need to clone the repo,
then install the necessary dependencies mentioned above. 

## Obtaining Similar Data

While it isn't possible to obtain the same data we have for Andrew's Etsy shop
due to privacy, if you have managing access to another Etsy shop you can
access the order data for that shop. Here are the steps to follow:

1. Request access to Etsy API from Etsy website [using this link](https://www.etsy.com/developers/register).
It typically takes a few weeks to a month for your request to be reviewed.

2. Follow [this tutorial](https://medium.com/@anastasia.bizyayeva/a-comprehensive-guide-to-oauth-2-0-setup-for-etsy-v3-open-api-f514e63b436f)
to authenticate through the OAuth 2.0 system and gain access to personal shop
data

3. Clone this repo if you haven't already

4. With the keys form the tutorial create a file in the cloned directory called
'keys.json' with the following format: 
{
    "access_token": "YOUR ACCESS TOKEN HERE",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "YOUR REFRESH TOKEN HERE",
    "keystring": "YOUR SHOP KEYSTRING HERE"
}

## Generating Similar Plots

