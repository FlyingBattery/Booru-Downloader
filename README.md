# booru_downloader
 Becuase hugging servers is fun.
 
To run this program, first open TOR and connect.

Download geckodriver from https://github.com/mozilla/geckodriver/releases, extract the file from the .zip and add to the system path.

Run pip install -r requirements.txt to install python packages.

Open tor and connect, keep this window open during operation.

Run permanent_booru_downloader.py using python3 ./main.py to download from the Permanent Booru on the .onion site.

After you download content, run create_searchable_tags.py using python3 ./create_searchable_tags.py

Using NodeJS, run npm install.

Run main.js using node main.js or pm2 start main.js

Go to localhost:3007 and enjoy your personal archive!
