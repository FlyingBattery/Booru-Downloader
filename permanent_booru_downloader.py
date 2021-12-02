from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import threading
import time
import sqlite3
import os
import pyautogui
from selenium.webdriver import ActionChains

con = sqlite3.connect('.\\data\\images.db')
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS images (link text, direct text, tags text)')
con.commit()

binary = FirefoxBinary(r".\\tor\\Tor Browser\\Browser\\firefox.exe")
profile = FirefoxProfile(r".\\tor\\Tor Browser\\Browser\\TorBrowser\Data\Browser\profile.default")

# Disable images for performance
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
profile.set_preference("browser.download.manager.focusWhenStarting", False)
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.useDownloadDir", True)
profile.set_preference("browser.helperApps.alwaysAsk.force", False)
profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
profile.set_preference("browser.download.manager.closeWhenDone", True)
profile.set_preference("browser.download.manager.showAlertOnComplete", False)
profile.set_preference("browser.download.manager.useWindow", False)
profile.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
profile.set_preference("pdfjs.disabled", True)
# Create webdriver
driver = webdriver.Firefox(profile, binary)
# Create actionchains
actionChain = ActionChains(driver)
time.sleep(20)
count = 0
offset = 1

searchTerms = [
    '/creator:roy arashi?',
    '/creator:darkmirage?'
]
for search in searchTerms:
    print("Current search term {}".format(search))
    while True:
        skipped = 0
        added = 0
        driver.get("http://owmvhpxyisu6fgd7r2fcswgavs7jly4znldaey33utadwmgbbp4pysad.onion/posts/{}{}".format(str(count+offset), search))
        print("Currently on page {}".format(count+offset))
        count += 1
        # Get Posts
        elems = driver.find_element_by_id("posts").find_elements_by_tag_name("a")
        if not elems:
            break
        # If there are no results, exit.
        links = []
        ids = []
        # Store Links for page
        for e in elems:
            # Skip links that are already in db.
            cur.execute("SELECT * FROM images WHERE `link` = '" + e.get_attribute('href') + "'")

            row = cur.fetchone()

            # Add the link to be archived if it does not exist.
            if row is None:
                # Save the link for access.
                links.append(e.get_attribute('href'))
                added += 1
            else:
                skipped += 1
        # Collect data per link
        for e in links:
            tagList = []
            # Get post link
            link = e
            # Go to post
            driver.get(link)
            # Get download link
            download = driver.find_element_by_xpath('//a[@download=""]')
            # Get Tags
            try:
                table = driver.find_element_by_id("tags").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
                for t in table:
                    # Get tag text
                    tag = t.find_element_by_tag_name("a").find_element_by_tag_name("span").text
                    # Add tag to list
                    tagList.append(tag)
            except:
                a = 1
            # Save data
            cur.execute("INSERT INTO images VALUES (?,?,?)", (link, download.get_attribute('href'), ", ".join(tagList) ))
            con.commit()
            # Get file url
            imageUrl = download.get_attribute('href')
            driver.get('http://xbzszf4a4z46wjac7pgbheizjgvwaf3aydtjxg7vsn3onhlot6sppfad.onion/')
            # Create a tag with download attribute
            exe = '''
            var s = document.createElement('a')
            s.href = '{imageLink}';
            s.download = '';
            s.text="download"
            document.body.appendChild(s)
            '''.format(imageLink = imageUrl)
            driver.execute_script(exe)
            # Scroll into view
            driver.execute_script("return arguments[0].scrollIntoView()", driver.find_element_by_tag_name("a"))
            # Download file.
            try:
                driver.find_element_by_tag_name("a").click()
            except:
                a=1
con.close()

driver.quit()

import create_searchable_tags

create_searchable_tags