import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'
    
def parse_attributes(business_id, attributes):
    try:
        conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='mustafa'")
        # adjust username/password as needed
    except:
        print('Unable to connect to the database!')
    cur = conn.cursor()

    for key, value in attributes.items():
        if isinstance(value, dict):
            parse_attributes(business_id, value)
        else:
            formatted_value = ""
            if isinstance (value, list):
                formatted_value = ''.join([str(item) for item in value])
            elif not isinstance(value, str):
                formatted_value = str(value)
            else:
                formatted_value = cleanStr4SQL(value)
            
            sql_str2 = "INSERT INTO AttributeTable (business_id, attr_name, value) " + \
            "VALUES ('" + cleanStr4SQL(business_id) + "','" + cleanStr4SQL(key) + "','" + formatted_value + "');"
            try:
                cur.execute(sql_str2)
            except:
                print("Insert to Attribute table failed!")
            conn.commit()
    cur.close()
    conn.close()
        

def insert2BusinessTable():
    #reading the JSON file
    with open('./yelp_business.JSON','r') as f:
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='mustafa'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            business_id = data["business_id"]

            sql_str = "INSERT INTO BusinessTable (business_id, name, address, state, city, postal_code, stars, review_count, num_checkins, review_rating, is_open) " + \
            "VALUES ('" + cleanStr4SQL(business_id) + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) + "','"+ cleanStr4SQL(data["state"]) + "','" + \
            cleanStr4SQL(data["city"]) + "','" + cleanStr4SQL(data["postal_code"]) + "','" + str(data["stars"]) + "','" + str(data["review_count"]) + "', '0', '0.0','" + int2BoolStr(data["is_open"]) + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to Business table failed!")
            conn.commit()

            for category in data["categories"]:
                sql_str2 = "INSERT INTO CategoryTable (business_id, category_name) " + \
                "VALUES ('" + cleanStr4SQL(business_id) + "','" + cleanStr4SQL(category) + "');"
                try:
                    cur.execute(sql_str2)
                except:
                    print("Insert to Category table failed!")
                conn.commit()

            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            parse_attributes(business_id, data['attributes'])

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2UserTable():
    #reading the JSON file
    with open('./yelp_user.JSON','r') as f: 
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='mustafa'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            sql_str = "INSERT INTO UserTable (user_id, name, average_stars, review_count, fans, funny, cool) " + \
            "VALUES ('" + cleanStr4SQL(data['user_id']) + "','" + cleanStr4SQL(data["name"]) + "','" + str(data['average_stars']) + "','" + \
            str(data['review_count']) + "','" + str(data['fans']) + "','" + str(data['funny']) + "','" + str(data['cool']) + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to User table failed!")
                print(sql_str)
                return
            
            conn.commit()

            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2CheckInTable():
    #reading the JSON file
    with open('./yelp_checkin.JSON','r') as f:
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='mustafa'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            business_id = data['business_id']
            for (dayofweek,time) in data['time'].items():
                for (hour,count) in time.items():

                    sql_str = "INSERT INTO CheckInTable (business_id, day, time, customers) " + \
                    "VALUES ('" + cleanStr4SQL(business_id) + "','" + cleanStr4SQL(dayofweek) + "','" + cleanStr4SQL(hour) + "','" + str(count) + "');"
                    try:
                       cur.execute(sql_str)
                    except:
                       print("Insert to CheckIn table failed!")
                       print(sql_str)
                       return

            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2ReviewTable():
    #reading the JSON file
    with open('./yelp_review.JSON','r') as f:
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='mustafa'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            sql_str = "INSERT INTO ReviewTable (business_id, user_id, review_id, date, text, stars, useful, funny, cool) " + \
            "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data['user_id']) + "','" + cleanStr4SQL(data['review_id']) + "','" + \
            cleanStr4SQL(data["date"]) + "','" + cleanStr4SQL(data["text"]) + "','" + str(data["stars"]) + "','" + str(data["useful"]) + "','" + \
            str(data["funny"]) + "','" + str(data["cool"]) + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to Review table failed!")
                print(sql_str)
                return
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2FriendsTable():
    with open('./yelp_user.JSON','r') as f: 
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='mustafa'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            user_id1 = data['user_id']
            for friend in data['friends']:
                sql_str2 = "INSERT INTO IsFriendsWith (user_id1, user_id2) " + \
                "VALUES ('" + cleanStr4SQL(user_id1) + "','" + cleanStr4SQL(friend) + "');"
                try:
                    cur.execute(sql_str2)
                except:
                    print("Insert to IsFriendsWith table failed!")
                    print(sql_str2)
                    return
            
                conn.commit()
            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


if __name__ == "__main__":
    # insert2BusinessTable()
    # insert2UserTable()
    # insert2CheckInTable()
    insert2ReviewTable()
    # insert2FriendsTable()