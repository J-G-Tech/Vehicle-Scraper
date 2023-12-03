How to use:

1)You will need python 3.12 to run this program but any python 3.x should work.

2)Install all the requirements in the requirements.txt file using the command:

pip3 install -r requirements.txt

in your terminal.

3)Go to the accounts.json file and fill in all your facebook details. (dont need to change the id value)

4) You must have google chrome and Firefox installed to run the program

5)After you made sure to install the packages, go to test.py and run it. 


It will download all the listings first from the site.
Then it will 1 by 1 post each vehicle listing to facebook. Once you get rate limited, stop and resume in 3 days. 
If it does not allow more listings, then rerun the program in a week. 
When you rerun the program, it will not redownload listings that have been downloaded already and it will not post listings that have been posted already. 
Each time you rerun the program, the program will scrape your new and old listings for newly added listings and post them to facebook.