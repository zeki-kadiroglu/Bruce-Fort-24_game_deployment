Find 24
SOLUTION
With this postman documentation, you can test API's requests.


https://documenter.getpostman.com/view/14217994/TzRNDpAY#32628ecd-2e9e-4667-9c57-c252210e69d2.


request links: http://18.216.105.216/user  ---->POST

                    http://18.216.105.216/login   ----->GET


                    http://18.216.105.216/user    ------> GET


                    http://18.216.105.216/test     --------->GET


                    http://18.216.105.216/numbers -----------> POST


                    http://18.216.105.216/numbers ---------------> GET


                    http://18.216.105.216/user/8d7b240a ----------> DELETE





--  this is the postman collection link. https://www.getpostman.com/collections/96dfd0b26d9ebbc23334


# TASK
The most important part of this puzzle is your approach. We are not looking for an answer, we are looking at your method. So feel very free, and encouraged to think out loud. Ask questions, or even for advice. Commit as often as you usually would, working on any standard project.
The first task is essential, and oft overlooked as an important and difficult quality of advanced engineering. Spend some preliminary drawing board time, even if just a few minutes, to break this small assessment into smaller pieces, and estimate how long each will take you. Commit a CSV with that information as your first commit. Time yourself carefully. Update this file as time goes on, with a new column showing logged time so it can be compared to the initial guess. Even good engineers are bad at this sometimes, because of the notoriously unknowable nature of unknown unknowns. Again, we are looking at your process, and promise we will not be phased by poor estimates.
The Puzzle:
Use each of the numbers 1, 3, 4, and 6 exactly once with any of the four basic math operations (addition, subtraction, multiplication, and division) to total 24. Each number must be used once, and only once, and you may define the order of operations; for example, 3 * (4 + 6) = 31 is valid, however, incorrect, since it doesn’t total 24.
# Guidelines and requirements:
-Write your algorithm in a pythonic, readable way.
-Generalize the solution. Instead of 1, 3, 4, 6, accept any user input for n integers. Instead of 24, accept any user input for 1 integer
-Output a count of total permutations your algorithm considers
-Output all solutions, and a count of how many solutions exist
# The API:
Once upon a time, before the auspicious day you decided to interview with us, we were completely technology agnostic in our approach to this puzzle, and to the interview. We are still technology agnostic by philosophy, but we would like to see how you approach solving problems using the stack of the project you’ll be immediately helpful on.
With that: use Flask to build a simple REST API wherein users can be added to a Postgres database. Users can choose the parameters of their game:
-What are the input integers (in our example 1, 3, 4, 6)? Do not limit these to four possibilities.

-What is the end goal we are searching for (in our example 24)? 
The API should also retrieve information about the solutions to a specific user's puzzle.
You can choose to do any of the extras below if you find them to be useful, low-hanging fruit, a good way to show off your mad skills, or find yourself twiddling your thumbs with far too much existential dread.
# The Extras, In Some Sort of Order:
-Thoughts on the puzzle?
-Share a postman doc for the API
-Dockerize flask api server and postgres db as two containers that can be built with a docker-compose.yml
-Barebones web interface
-Some form of simple user authentication
-Basic form validation
-Users can have more than a single set of preferences, creating a one to many map between users and puzzle parameters (i.e. multiple puzzle objects per user).
-Create an endpoint wherein users can delete themselves
-Graph all the permutations so the y axis increases in value.
-Find out how long your program takes for each permutation on average.
