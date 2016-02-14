# appstore scraper functions

1) get_rating_summary: given an app_id, this function returns the app's rating summary: number of total ratings, number of total text reivews as well as the distribution of stars of the ratings.

2) get_static_info: given an app_id, this function returns some static or near-static information for the app. The app's category, it's price, description and size in MB.

3) reviews_scraper: given an app_id and a store_id (the country code for the store) this function returns all available text reviews for that app in that country's store. Each observation has the date of the reivew, it's text, star rating and the version of the app. 
You can save the reviews in a database or a csv file.


