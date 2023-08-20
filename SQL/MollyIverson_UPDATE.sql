-- "review_count" should be updated to the number of reviews made to the business.
UPDATE BusinessTable
SET review_count = Reviews.review_count
    FROM (SELECT ReviewTable.business_id, COUNT(ReviewTable.business_id) AS review_count FROM ReviewTable GROUP BY (ReviewTable.business_id)) AS Reviews
WHERE BusinessTable.business_id = Reviews.business_id;

-- "num_checkins" value for a business should be updated to the count of all check-in counts for that business.
UPDATE BusinessTable
SET num_checkins = CheckIns.checkin_sum
    FROM (SELECT CheckInTable.business_id, SUM(CheckInTable.customers) AS checkin_sum FROM CheckInTable GROUP BY (CheckInTable.business_id)) AS CheckIns
WHERE BusinessTable.business_id = CheckIns.business_id;

-- "review_rating" value for a user should be updated average rating for a business.
UPDATE BusinessTable
SET review_rating = Reviews.avg_review
    FROM (SELECT ReviewTable.business_id, AVG(ReviewTable.stars) AS avg_review FROM ReviewTable GROUP BY (ReviewTable.business_id)) AS Reviews
WHERE BusinessTable.business_id = Reviews.business_id;
