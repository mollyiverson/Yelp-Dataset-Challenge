# Yelp-Dataset-Challenge
A data search application for Yelp.com's business review data, using Python and SQL.
By using this project, you can:
* Search businesses based on state, city, zip code, and category
* Find popular and successful businesses in the area
* Get statistics on businesses in the selected zip code

## Project Photo
<img width="767" alt="image" src="https://github.com/mollyiverson/Yelp-Dataset-Challenge/assets/113158597/2411976a-030b-4a2e-bbb4-6aeeb324354d">

## Project Demo
TBA
## How to Use
1. Clone the project:
```bash
git clone https://github.com/mollyiverson/Yelp-Database-Challenge.git
```
2. Install an IDE that can handle Python code such as Visual Studio Code or PyCharm

3. [Set up PostgreSQL Database](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm)
   * Run MollyIverson_Relations.sql (SQL folder) to create the tables
  
4. Adjust Postgres username/password in yelpDatabaseProject.py (Application folder), and parseAndInsert.py (Parser folder)
     
5. Parse the data
   * Run parseAndInsert.py

6. Run Project!
   * Run yelpDatabaseProject.py
