# Molly Iverson

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "yelpDatasetProject.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class yelpDatasetProject(QMainWindow):
    def __init__(self):
        super(yelpDatasetProject, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()

        # Connects user input events with functions
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.searchButton.clicked.connect(self.searchButtonClicked)
        self.ui.clearButton.clicked.connect(self.clearButtonClicked)
        self.ui.refreshButton.clicked.connect(self.refreshButtonPressed)
        self.justClear = False

        self.updateTables()

    # Executes a query in the database
    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='mustafa'")
            # adjust username/password as needed
        except:
            print("Unable to connect to the database")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()

        if cur.description is None:
            # there are no results for this query
            conn.close()
            return

        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM BusinessTable ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("State query failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    # Loads all business categories for a specific zipcode
    def loadCategories(self):
        self.ui.categoryList.clear()
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.selectedItems()[0].text()
        zipcode= self.ui.zipList.selectedItems()[0].text()

        sql_str = "SELECT distinct C.category_name FROM CategoryTable as C, BusinessTable as B" \
                  " WHERE B.state='" + state + "' AND B.city='" + city + "' AND B.postal_code='" + zipcode + "' AND " \
                  "C.business_id=B.business_id ORDER BY C.category_name;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.categoryList.addItem(row[0])
        except:
            print("Category query failed!")

    # Clears results when user changes the selected state. Shows the new cities
    def stateChanged(self):
        if self.justClear:
            return
        self.justClear = True
        self.ui.cityList.clear()
        self.justClear = False
        state = self.ui.stateList.currentText()
        if self.ui.stateList.currentIndex() >= 0:
            sql_str = "SELECT distinct city FROM BusinessTable WHERE state='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("State changed query has failed")
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            self.clearStatsAndAnalysis()

    # Clears results and shows the new zipcodes when user changes the city
    def cityChanged(self):
        self.ui.zipList.clear()
        self.ui.categoryList.clear()
        if self.justClear:
            return
        if self.ui.stateList.currentIndex() >= 0:
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT distinct postal_code FROM BusinessTable WHERE state='" + state + "' AND city='" + \
                      city + "' ORDER BY postal_code;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print("City changed query has failed")
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            self.clearStatsAndAnalysis()

    # Clears results and shows the categories of the new zipcode
    def zipChanged(self):
        if self.justClear:
            return
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and \
                len(self.ui.zipList.selectedItems()) > 0:
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            self.clearStatsAndAnalysis()
            self.loadCategories()

    # Shows the number of businesses, average review stars, and number of reviews for a zipcode
    def loadStats(self, state, city, zipcode):
        sql_str_businessCount = "SELECT COUNT(*) FROM BusinessTable WHERE state='" + state + "' AND city='" + \
                  city + "' AND postal_code='" + zipcode + "';"
        sql_str_avgStars = "SELECT AVG(B.stars) FROM BusinessTable as B WHERE " \
                           "B.state='" + state + "' AND B.city='" + city + \
                           "' AND B.postal_code='" + zipcode + "';"
        sql_str_reviewCount = "SELECT COUNT(*) FROM ReviewTable as R, BusinessTable as B WHERE " \
                           "B.business_id=R.business_id AND B.state='" + state + "' AND B.city='" + city + \
                           "' AND B.postal_code='" + zipcode + "';"
        try:
            results = self.executeQuery(sql_str_businessCount)
            self.ui.sumBusLabel.setText(str(results[0][0]))

            results = self.executeQuery(sql_str_avgStars)
            self.ui.averageStarLabel.setText(str(results[0][0]))

            results = self.executeQuery(sql_str_reviewCount)
            self.ui.reviewCountLabel.setText(str(results[0][0]))
        except:
            print("Load zipcodestats query has failed")


    # Loads the categories for a businesses from most common to least common
    def loadTopCategories(self, state, city, zipcode):
        sql_str = "SELECT COUNT(*) as category_count, C.category_name FROM BusinessTable as B, CategoryTable as C " \
                  "WHERE state='" + state + "' AND city='" + city + "' AND postal_code='" + zipcode + "' AND " \
                  "C.business_id=B.business_id GROUP BY C.category_name ORDER BY category_count DESC;"
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.categoryTable.horizontalHeader().setStyleSheet(style)
            self.ui.categoryTable.setColumnCount(len(results[0]))
            self.ui.categoryTable.setRowCount(len(results))
            self.ui.categoryTable.setHorizontalHeaderLabels(['# of Businesses', 'Category'])
            self.ui.categoryTable.resizeColumnsToContents()
            self.ui.categoryTable.setColumnWidth(0, 150)
            self.ui.categoryTable.setColumnWidth(1, 300)

            currentRowCount = 0
            for row in results:
                for columnCount in range(0, len(results[0])):
                    self.ui.categoryTable.setItem(currentRowCount, columnCount, QTableWidgetItem(str(row[columnCount])))
                currentRowCount += 1
        except:
            print("Top category query has failed.")

    # Displays the businesses that are in the state, city, and zipcode selected by the user
    def searchButtonClicked(self):
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and \
                len(self.ui.zipList.selectedItems()) > 0:

            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipList.selectedItems()[0].text()

            if len(self.ui.categoryList.selectedItems()) > 0:  # Will check if searching by category too
                category = self.ui.categoryList.selectedItems()[0].text()

                sql_str = "SELECT name, address, city, stars, review_count, review_rating, num_checkins FROM " \
                          "BusinessTable as B, CategoryTable as C WHERE B.state='" + state + "' AND B.city='" + city + \
                          "' AND B.postal_code='" + zipcode + "' AND B.business_id=C.business_id AND " \
                          "C.category_name='" + category + "' ORDER BY name;"
            else:
                sql_str = "SELECT name, address, city, stars, review_count, review_rating, num_checkins FROM " \
                          "BusinessTable WHERE state='" + state + "' AND city='" + city + "' AND postal_code='" \
                          + zipcode + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars',
                                                                 'Review Count', 'Review Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 200)
                self.ui.businessTable.setColumnWidth(3, 150)
                self.ui.businessTable.setColumnWidth(4, 150)
                self.ui.businessTable.setColumnWidth(5, 150)
                self.ui.businessTable.setColumnWidth(6, 200)

                currentRowCount = 0
                for row in results:

                    for columnCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, columnCount, QTableWidgetItem(str(row[columnCount])))
                    currentRowCount += 1
            except:
                print("Business query has failed.")
            self.loadStats(state, city, zipcode)
            self.loadTopCategories(state, city, zipcode)

    # Clears business results
    def clearButtonClicked(self):
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

        self.justClear = True
        self.ui.cityList.clear()
        self.ui.zipList.clear()
        self.ui.categoryList.clear()
        self.justClear = False

        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)

        for i in reversed(range(self.ui.popularBusiness.rowCount())):
            self.ui.popularBusiness.removeRow(i)

        for i in reversed(range(self.ui.successfulBusiness.rowCount())):
            self.ui.successfulBusiness.removeRow(i)

        self.clearStatsAndAnalysis()

    # Clears the statistic table
    def clearStatsAndAnalysis(self):
        for i in reversed(range(self.ui.categoryTable.rowCount())):
            self.ui.categoryTable.removeRow(i)
        self.ui.reviewCountLabel.clear()
        self.ui.sumBusLabel.clear()
        self.ui.averageStarLabel.clear()

    # Refreshes the table of businesses
    def refreshButtonPressed(self):
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and \
                len(self.ui.zipList.selectedItems()) > 0:

            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipList.selectedItems()[0].text()

            for i in reversed(range(self.ui.popularBusiness.rowCount())):
                self.ui.popularBusiness.removeRow(i)

            for i in reversed(range(self.ui.successfulBusiness.rowCount())):
                self.ui.successfulBusiness.removeRow(i)
            self.createPopularTable(state, city, zipcode)
            self.createSuccessfulTable(state, city, zipcode)

    # Updates the business tables with number of reviews, number of check ins, and average review rating
    def updateTables(self):
        sql_str_reviewCount = "UPDATE BusinessTable SET review_count = Reviews.review_count " \
                              "FROM (SELECT ReviewTable.business_id, COUNT(ReviewTable.business_id) " \
                              "AS review_count FROM ReviewTable GROUP BY (ReviewTable.business_id)) AS Reviews " \
                              "WHERE BusinessTable.business_id = Reviews.business_id;"

        sql_str_numCheckins = "UPDATE BusinessTable SET num_checkins = CheckIns.checkin_sum " \
                              "FROM (SELECT CheckInTable.business_id, SUM(CheckInTable.customers) AS " \
                              "checkin_sum FROM CheckInTable GROUP BY (CheckInTable.business_id)) AS CheckIns " \
                              "WHERE BusinessTable.business_id = CheckIns.business_id;"

        sql_str_reviewRating = "UPDATE BusinessTable SET review_rating = Reviews.avg_review " \
                               "FROM (SELECT ReviewTable.business_id, AVG(ReviewTable.stars) AS avg_review " \
                               "FROM ReviewTable GROUP BY (ReviewTable.business_id)) AS Reviews " \
                               "WHERE BusinessTable.business_id = Reviews.business_id;"

        try:
            self.executeQuery(sql_str_reviewCount)
            self.executeQuery(sql_str_reviewRating)
            self.executeQuery(sql_str_numCheckins)
        except:
            print("Update reviewCount, reviewRating, numCheckins has failed")

    # Analyzes businesses in the city, state, and zipcode to find the most popular ones using an algorithm
    def createPopularTable(self, state, city, zipcode):
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and \
                len(self.ui.zipList.selectedItems()) > 0:

            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipList.selectedItems()[0].text()

            sql_str = "SELECT B.name, B.stars, B.review_rating, B.review_count FROM BusinessTable as B," \
                      "((SELECT B.business_id FROM BusinessTable as B WHERE B.review_rating >= 3.0 " \
                      "AND review_count > 20)" \
                      "UNION" \
                      "(SELECT B.business_id FROM CategoryTable AS C, BusinessTable AS B, (SELECT C.category_name, " \
                      "MAX(B.num_checkins) AS max_checkins FROM CategoryTable AS C, BusinessTable as B WHERE " \
                      "B.business_id = C.business_id AND B.review_rating >= 3 GROUP BY C.category_name) AS subquery " \
                      "WHERE B.business_id=C.business_id AND C.category_name=subquery.category_name AND " \
                      "B.num_checkins=subquery.max_checkins)) as Popular WHERE B.business_id=Popular.business_id " \
                      "AND B.state='" + state + "' AND B.city='" + city + "' AND B.postal_code='" + zipcode + "' " \
                      "ORDER BY B.name;"

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popularBusiness.horizontalHeader().setStyleSheet(style)
                if results == []:
                    self.ui.popularBusiness.setColumnCount(4)
                else:
                    self.ui.popularBusiness.setColumnCount(len(results[0]))
                self.ui.popularBusiness.setRowCount(len(results))
                self.ui.popularBusiness.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Review Rating',
                                                                   '# of Reviews'])
                self.ui.popularBusiness.resizeColumnsToContents()
                self.ui.popularBusiness.setColumnWidth(0, 200)
                self.ui.popularBusiness.setColumnWidth(1, 150)
                self.ui.popularBusiness.setColumnWidth(2, 150)
                self.ui.popularBusiness.setColumnWidth(3, 150)

                currentRowCount = 0
                for row in results:
                    for columnCount in range(0, len(results[0])):
                        self.ui.popularBusiness.setItem(currentRowCount, columnCount, QTableWidgetItem(str(row[columnCount])))
                    currentRowCount += 1
            except:
                print("Popular Business query has failed.")

    # Analyzes businesses in the city, state, and zipcode to find the most successful ones using an algorithm
    def createSuccessfulTable(self, state, city, zipcode):
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and \
                len(self.ui.zipList.selectedItems()) > 0:

            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipList.selectedItems()[0].text()

            sql_str = "SELECT B.name, B.review_count, B.num_checkins FROM BusinessTable as B, " \
                      "((SELECT B.business_id FROM BusinessTable as B, ReviewTable as R " \
                      "WHERE B.business_id=R.business_id AND B.is_open=True " \
                      "GROUP BY B.business_id HAVING MIN(R.date) < '2010-01-01') " \
                      "UNION " \
                      "(SELECT B.business_id FROM BusinessTable as B, CategoryTable as C, " \
                      "(SELECT B.postal_code, C.category_name, AVG(B.num_checkins) as average_checkins " \
                      "FROM CategoryTable as C, BusinessTable as B WHERE C.business_id=B.business_id " \
                      "GROUP BY B.postal_code, C.category_name " \
                      "ORDER BY C.category_name) as AverageCheckins	WHERE B.postal_code=AverageCheckins.postal_code " \
                      "AND B.business_id=C.business_id AND C.category_name=AverageCheckins.category_name " \
                      "AND B.num_checkins > AverageCheckins.average_checkins)) as Successful " \
                      "WHERE B.business_id=Successful.business_id AND B.state='" + state + "' AND B.city='" + city + \
                      "' AND B.postal_code='" + zipcode + "' ORDER BY B.name;"

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.successfulBusiness.horizontalHeader().setStyleSheet(style)
                if results == []:
                    self.ui.successfulBusiness.setColumnCount(3)
                else:
                    self.ui.successfulBusiness.setColumnCount(len(results[0]))
                self.ui.successfulBusiness.setRowCount(len(results))
                self.ui.successfulBusiness.setHorizontalHeaderLabels(['Business Name', '# of Reviews', '# of Checkins'])
                self.ui.successfulBusiness.resizeColumnsToContents()
                self.ui.successfulBusiness.setColumnWidth(0, 200)
                self.ui.successfulBusiness.setColumnWidth(1, 150)
                self.ui.successfulBusiness.setColumnWidth(2, 150)

                currentRowCount = 0
                for row in results:
                    for columnCount in range(0, len(results[0])):
                        self.ui.successfulBusiness.setItem(currentRowCount, columnCount, QTableWidgetItem(str(row[columnCount])))
                    currentRowCount += 1
            except:
                print(sql_str)
                print("Successful Business query has failed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = yelpDatasetProject()
    window.show()
    sys.exit(app.exec_())
