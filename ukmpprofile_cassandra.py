#!/usr/bin/env python3


# DISCLAIMER: The Application code scrpt and tool is intended to facilitate research, by authorised and approved parties, pursuant to the ideals of libertarian democracy in the UK, by Campaign Lab membership. Content subject-matter and results can be deemed sensitive and thus confidential. Therefore illicit and authorisation for any other use, outside these terms, is hereby not implied pursuant to requisite UK Data Protection legislation and the wider GDPR enactments within the EU.

# CODE REVISION: Ejimofor Nwoye, Newspeak House, London, England, @ 27/01/2025

import requests
from bs4 import BeautifulSoup
import re
import json
from cassandra.cluster import Cluster
import os

os.system('clear') 

# Define URLs
urls = [
    "https://www.theyworkforyou.com/mps/",
    "https://members.parliament.uk/constituencies"
]

# Function to scrape individual MP links
def scrape_mp_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    mp_links = []

    if "theyworkforyou" in url:
        for link in soup.select('a[href^="/mp/"]'):
            mp_links.append("https://www.theyworkforyou.com" + link['href'])

    elif "parliament" in url:
        for link in soup.select('a[href^="/member/"]'):
            mp_links.append("https://members.parliament.uk" + link['href'])

    return mp_links

# Extract policy interests and other details using regex
def extract_mp_details(mp_url):
    response = requests.get(mp_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    text_content = soup.get_text(separator=' ', strip=True)
    
    details = {
        "policy_interests": re.findall(r'\b(policy|interest|priority|focus):?\b.*?\.', text_content, re.IGNORECASE),
        "statements": re.findall(r'"(.*?)"', text_content),
        "standpoint": re.findall(r'\b(oppose|support|neutral|favor)\b.*?\.', text_content, re.IGNORECASE),
        "political_views": re.findall(r'\b(conservative|labour|liberal|green|ukip|independent)\b', text_content, re.IGNORECASE),
        "ipp_positions": re.findall(r'\b(IPP sentences?|indeterminate sentences?)\b.*?\.', text_content, re.IGNORECASE)
    }

    return details

# Main scraping logic
all_mp_data = []

for url in urls:
    mp_links = scrape_mp_links(url)
    for mp_link in mp_links:
        try:
            mp_details = extract_mp_details(mp_link)
            mp_data = {
                "mp_url": mp_link,
                **mp_details
            }
            all_mp_data.append(mp_data)
        except Exception as e:
            print(f"Error processing {mp_link}: {e}")

# Save to JSON file
output_file = "ukmpprofile.json"
with open(output_file, 'w') as f:
    json.dump(all_mp_data, f, indent=4)

print(f"Data saved to {output_file}")

# Insert data into Apache Cassandra
def insert_into_cassandra(data):
    cluster = Cluster(["127.0.0.1"])
    session = cluster.connect()

    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS uk_mps
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """)

    session.set_keyspace('uk_mps')

    session.execute("""
    CREATE TABLE IF NOT EXISTS mp_profiles (
        mp_url text PRIMARY KEY,
        policy_interests list<text>,
        statements list<text>,
        standpoint list<text>,
        political_views list<text>,
        ipp_positions list<text>
    )
    """)

    for mp in data:
        session.execute(
            """
            INSERT INTO mp_profiles (mp_url, policy_interests, statements, standpoint, political_views, ipp_positions)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                mp['mp_url'],
                mp['policy_interests'],
                mp['statements'],
                mp['standpoint'],
                mp['political_views'],
                mp['ipp_positions']
            )
        )

    print("Data inserted into Cassandra")

insert_into_cassandra(all_mp_data)

