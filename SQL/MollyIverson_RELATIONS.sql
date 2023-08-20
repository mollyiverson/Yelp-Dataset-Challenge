CREATE TABLE BusinessTable (
    business_id CHAR(22),
    name VARCHAR(100) NOT NULL,
    address VARCHAR(80),
    state CHAR(2),
    city VARCHAR(50),
    postal_code CHAR(5),
    stars DECIMAL(2, 1) DEFAULT 0 CHECK (stars >= 0),
    review_count INTEGER DEFAULT 0 CHECK (review_count >= 0),
    is_open BOOLEAN,  
    num_checkins INTEGER DEFAULT 0 CHECK (num_checkins >= 0),
    review_rating DECIMAL(2, 1) DEFAULT 0 CHECK (review_rating >= 0),
    
    PRIMARY KEY (business_id)
);

CREATE TABLE UserTable (
    user_id CHAR(22),
    name VARCHAR(60) NOT NULL,
    average_stars DECIMAL(2, 1) DEFAULT 0,
    review_count INTEGER DEFAULT 0 CHECK (review_count >= 0),
    fans INTEGER DEFAULT 0 CHECK (fans >= 0),
    funny INTEGER DEFAULT 0 CHECK (funny >= 0),
    cool INTEGER DEFAULT 0 CHECK (cool >= 0),  

    PRIMARY KEY (user_id)
);

CREATE TABLE ReviewTable (
    user_id CHAR(22) NOT NULL,
    business_id CHAR (22) NOT NULL,
    review_id CHAR(22),
    date DATE,
    text VARCHAR(1500),
    stars DECIMAL(2, 1) DEFAULT 0 CHECK (stars >= 0),
    useful INTEGER DEFAULT 0 CHECK (useful >= 0),
    funny INTEGER DEFAULT 0 CHECK (funny >= 0),
    cool INTEGER DEFAULT 0 CHECK (cool >= 0),  
      
    FOREIGN KEY (business_id) REFERENCES BusinessTable (business_id),
    FOREIGN KEY (user_id) REFERENCES UserTable (user_id),
    PRIMARY KEY (review_id)
);

CREATE TABLE CheckInTable (
    day VARCHAR (9),
    time VARCHAR (5),
    business_id CHAR (22),
    customers INTEGER DEFAULT 0 CHECK (customers >= 0),
      
    PRIMARY KEY (business_id, day, time)
);

CREATE TABLE IsFriendsWith (
    user_id1 CHAR (22),
    user_id2 CHAR (22),

    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES UserTable (user_id),
    FOREIGN KEY (user_id2) REFERENCES UserTable (user_id)
);

CREATE TABLE AttributeTable (
    business_id CHAR(22),
    attr_name VARCHAR(50),
    value VARCHAR(20),

    PRIMARY KEY (business_id, attr_name),
    FOREIGN KEY (business_id) REFERENCES BusinessTable(business_id)
);

CREATE TABLE CategoryTable (
    business_id CHAR(22),
    category_name VARCHAR(50),

    PRIMARY KEY (business_id, category_name),
    FOREIGN KEY (business_id) REFERENCES BusinessTable(business_id)
);

