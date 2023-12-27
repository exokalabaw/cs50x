
# Kabisote
#### Video demo: https://youtu.be/b7uH-VwTiDQ
#### DESCRIPTION:
Kabisote is a web app where I have used the skills I have learned in CS50X, and some additional Javascript and CSS, to build a web app that allows users to take and make practice quizzes. Users can create accounts and make quizzes that they can either make private to use themselves, or publicly available for others to take. When creating Quizzes, users have the option to use two types of questions: multiple choice, or a text box answer where they can set multiple possible answers.

The following page types exist on the web app

+ ##### public quizzes - A table of quizzes that have been set to public by the author. users and take the practice tests without logging in
+ ##### quiz - This is a webform that contains the quiz. quizzess have two different types of questions: a textbox answer question and a multiple choice question. On the header of each quiz is a JSON answer key embedded via FLASK. When a user submits a test, the user has three options: to see the results, to re take the test, or to just return to the test without seeing the results. When the user clicks to see the results, the user will see which answers are correct and incorrect. To see the correct possible answer/s for each incorrect answer, the user has to click on one more link right below the question. All of this is handled via quiz.js and is all processed on the front end.
+ ##### login and signup -  these pages are the same forms that I used on the Finance project, with the only difference of the error messages being shown via flash instead.
+ ##### user quizzes - a list of publicly available quizzes from a specific user
+ ##### home page(logged in) -  this shows a list of the logged in user's own quizzes, with links to either take, edit, or delete the quiz.All of this is processes via Flask via POST and routes from the url designating quiz id's on the url parameter.
+ ##### edit quiz - this displays the quiz title, quiz items, links to re-order the quiz items.
+ ##### edit quiz details - this page takes the title, description text, and a tickbox to control wether the quiz is public or private. Form vaildation is handled via editquiz.js and makes sure all of the pertinent fields are filled up before the submit button is active. The form is submitted via post and saved on an SQL database.
+ ##### add/edit textbox - these are similar pages that edit the textbox type of question, providing users a title field and one or more possible answers to the question. validation is also handled on the front via addtextbox.js and is submitted via FLASK through POST requests
+ ##### add/edit multi - these are similar pages that edit the multiple choice type of question. similar functionality as add/edit textbox with js catered to making sure the pertinent fields are correct before the submit button is active.

Form validation is handled via Javascript on the front end. The way it works is that the submit button will be disabled as long as all of the required fields of the form are not met. Each page that uses Javascript has it's own separate JS file. Answers to the practice questions are embedded as a JSON answer key on the quiz page.

Error and Sucess messages are shown through the flash feature of FLASK, JINJA.

Additional server side validation has been added via flask to prevent users from editing other user's content. Flask has also been used to prevent non-public quizzes to be taken or viewed by users other than the owner.

Editing and taking of quizzes, quiz items, teaser pages are handled via routes directed by node id's added to the url parameters.

I plan to take this minimum viable project and make improvements by using it as my final project when I take the CS50W course. The goal is to be able to launch it as a publicly available web app.
