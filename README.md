## Overview

The goal of this project was to understand the quantity and characteristics of
repeat customers of Andrew's Etsy shop, ADesignsDenver. We did this by
connecting to Etsy API to pull all of the order reciepts into a JSON. Then we
processed the data to find key metrics such as repeat order rate, the sizes
of those orders, orders broken down by state, and time between repeat orders.
Finally we visualized the data using matplotlib and plotly.

## Dependencies

To install the necessary dependencies to run this project you can run the
following command to install any libraries needed that aren't installed.
You may also choose to install them individually by specifying the library
one at a time.

```
pip install matplotlib pandas plotly pytest requests
```

## How to run

To successfully run the code on your machine, you will need to clone the repo,
then install the necessary dependencies mentioned above. The computational
essay ('Essay.ipynb') should run without complication if you use the preprovided data from 
Andrew's Etsy Shop because relative file paths were used. However, if you run 
into difficulty reading the data, change the data file path for 'orders.json' 
to the full path on your computer. This can be done by changing the variable 
'ORDER_PATH' in the obtaining data section of the essay.

If you would like to run the essay with your own shop data to visualize your
reapeat customer characteristics, follow the instructions in the Obtaining
Similar Data section below to pull your data.

It is important to note that some unit tests in the 'test_api_lib.py' file will
fail because they access the API which requires private keys. To obtain those
keys follow the instructions in the Obtaining Similar Data section below.
However, to rerun the computational essay using the data from my shop provided,
it is not necessary for these tests to pass.

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

5. Use the 'get_all_orders' function of the api_lib library to pull all Etsy 
orders associated with the authenticated account. You can also run this same
code in the commented out code of the computational essay in the Obtaining Data
section. Just ensure to switch the SHOP_ID variable to your own shop id. 

## Generating Similar Plots

To generate the same plots shown in the computational essay using the cleaned
ADesignsDenver data in the 'orders.json' file, simply run the computational
essay using the instructions above under How to Run. This includes cloning the
repo, installing the dependencies noted above, and running 'Essay.ipynb.' All
file paths used are relative, so it should run without complication. However,
if you run into difficulty reading the data, change the data file path for 
'orders.json' to the full path on your computer. This can be done by changing
the variable 'ORDER_PATH' in the obtaining data section of the essay.

To generate plots using your own shop's data, follow the instructions under the
Obtaining Similar Data section above, then rerun the computational essay.

