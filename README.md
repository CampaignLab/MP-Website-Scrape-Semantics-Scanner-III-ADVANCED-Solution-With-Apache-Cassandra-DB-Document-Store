 MP-Website-Scrape-Semantics-Scanner-III-ADVANCED-Solution-With-Apache-Cassandra-DB-Document-Store

 DISCLAIMER: The Application code scrpt and tool is intended to facilitate research, by authorised and approved parties, pursuant to the ideals of libertarian democracy in the UK, by Campaign Lab membership. Content subject-matter and results can be deemed sensitive and thus confidential. Therefore illicit and authorisation for any other use, outside these terms, is hereby not implied pursuant to requisite UK Data Protection legislation and the wider GDPR enactments within the EU.

The Python script code provides a solution to scrape the URLs provided, extract the required data, and store the results in a JSON file and an Apache Cassandra database. This script uses libraries like requests, BeautifulSoup, re, and cassandra-driver. Internet access is mandatory
 
Steps in the Script:
Scrape URLs: Scrapes the MP links from the two provided URLs.
Extract Details: Extracts information like policy interests, statements, standpoints, and political views using regular expressions.
Store in JSON: Saves the extracted data into a JSON file (ukmpprofile.json).
Insert into Cassandra: Creates a keyspace and table in Apache Cassandra and inserts the data.
Prerequisites:
Install required libraries: pip install requests beautifulsoup4 cassandra-driver.
Ensure Apache Cassandra is running locally or replace 127.0.0.1 with your Cassandra server's IP.

 
