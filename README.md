# Sumthing Summarize
https://devpost.com/software/490889  
Placed 3rd overall at HackUIOWA 2022!  
This is the Python/Flask backend, the React frontend and Google Chrome Extension can be found at https://github.com/paaatrrrick/sumthingsummarize

# Inspiration
Years of studying in high school and college has taken its toll. The brain can only hold so much so fast. We've devised a solution that not only records important information you come across while studying, but also uses modern machine learning language processing to summarize it!

# What it does
Processes many highlighted paragraphs into summarized excerpts, then displays them on an additional website.  
It also summarizes the summaries for a big picture overview!

# How we built it
A Chrome Extension adds a button to you right click field when highlighting text.  
`Click Add to Text Summary` to send it to the Python/Flask backend which manipulates the data and summarizes it with OpenAI's GPT-3.  
Finally, when you load sumthingsummarize.com, you can find all your saved summaries on our React frontend!

# Challenges we ran into
We had to learn Flask from scratch, and we ran into a lot of issues with CORS when sending PUSH requests to the backend. We managed to get it all sorted out and working with some help from the organizers.

# Accomplishments that we're proud of
Hooking a frontend to a backend to a different frontend.
Learning a backend framework and implementing it in just a few hours.
Building a Chrome Extension for the first time.
Participating in our first Hackathon!

# What we learned
* Flask
* Chrome Extensions
* How to work over multiple machines
* How to connect Git repos

# What's next for Sumthing Summarized
To move forward we would host the frontend on Heroku, backend on AWS, and get our Chrome Extension hosted on the app store.  
We would also have to register for a more reliable OpenAI key instead of a personal free trial.

# Built With
`chrome extensions`
`flask`
`javascript`
`python`
`react`
