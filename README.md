# Web-Crawling-and-Information-Extraction

RottenTomatoes is an IMDb like website, where we can find an online database of information related to films, television programs, including cast, production crew,
personal biographies, plot summaries, trivia, ratings, critic and fan reviews.

we are provided with a file named “rotten tomatoes movie genre link.txt,” which contains URL links for ten different genre-wise top 100 movie lists.
Our task is following:

* Reads each of the URLs, saves the pages in HTML format.
* Given a user input of any of the ten genres, it should list all the movies in that genre and wait for user input of a particular movie name from the list.
* Given a movie name as the input, it should download and save the corresponding movie page’s HTML file.
* After saving movie pages in HTML format, create grammar using the syntax of the HTML file to extract following fields:

  * **Movie Name**
  * **Director**
  * **Producer**
  * **Writers**
  * **Original Language**
  * **Cast and Crew Members**
  * **Storyline**
  * **Box Office Collection**
  * **Runtime**
  * **You Might Also Like**
  * **Where to Watch**

For any selected film user can ask for any of the above field to show and our program will show the information after extractng using grammar we created. For example if user asks for "Movie Name" then user will get movie title,if user asks for "Director" then it will show director name(s) to user and so on..

After completion of above task we need to do two more extra tasks to add some special features with two fields "You Might Also Like" and "Cast and Crew Members" :

**Task-1:**   when user selects "You Might Also Like" option then it will show movie names given in this field,and then it will wait for user input to selects any of            the shown movie name,and when user selects any it will download HTML page for that movie and show the above list for selected movie....

**Task-2:**   If user selects "Cast and Crew Members" then it will show list of memebers with their role(or responsibility),then wait for user input of any one of the listed cast member, given the input we need to download and save that actor/actress profile and write grammar to extract the below fields: 
 - **Highest Rated film**
 - **Lowest Rated film**
 - **Birthday**
 - **His/Her other movies**

Then wait for the user to select from any of the above options and show the result as per selection and for the ‘His/Her other movies’ further ask for a year and use it as a filter to show all the movies on or after that year.
