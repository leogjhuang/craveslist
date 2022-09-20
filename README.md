# CravesList

Have a dream meal? Turn that dream into a reality using just your voice! Feel blissed using CravesList!

## Inspiration
As a group of computer science and software engineering students, we often find ourselves in situations where we are uncertain of how to prepare a certain meal under time constraints. With our lack of culinary knowledge, we always struggled in finding what ingredients to purchase, much less where to find that product in a supermarket. It was always a hassle to run into situations where the prices were way out of our budget, or when the store no longer had a particular ingredient. Taking inspiration from Siri, we ultimately wanted to leverage speech-to-text software to minimize the need for interpersonal interaction, better enhancing the health, safety, and well-being of our people.

## What it does
As a result, we created a program that enhances customers’ shopping experience both in and outside of stores. At its very core, our program, CravesList, takes input from the customer regarding what food they want to make and outputs the ingredients, price range for each ingredient, whether the store has the item, and even which section of the store it’s in! By using speech-to-text software, we allow users to activate the program using only their voice, effectively minimizing the amount of time spent. Our program currently uses a sample data frame that we constructed for the product inventory and location, but individual stores can use their unique organization data to provide customers with accurate and relevant information. Once a customer knows what they want, we want to help them move through the path-to-purchase as easily as possible, and capitalize on an in-stores biggest strength: immediacy.

## How we built it
First, we used the AssemblyAI Speech to Text API to do real-time speech recognition with python in order to convert the user’s verbal input to text. Afterward, we used the Selenium web scraping API in order to find the most suitable set of ingredients based on the user’s recipe request. We then web scraped the Loblaw database to give the most accurate estimation of the prices of each ingredient and constructed a sample database in CVS that determined the availability and in-store location for each ingredient using the Pandas data analysis software. Finally, we used Flask to deploy our code on a Google app engine and publish it using the Google cloud platform in order to enhance user-friendliness. 

## Challenges we ran into

From the process of using Assembly AI to deploying our code on a Google app engine, we faced many challenges throughout our project. During the process of coding a real-time speech-to-text transcriber, we found difficulty with implementing concurrent code via asynchronous functions, especially because they could not communicate with each other in the same way synchronous functions could. Furthermore, it was the first time our team members had any interaction with Selenium and other web scraping APIs, which presented many challenges with both retrieving web information and optimizing the efficiency of our search. Additionally, learning to use Assembly API and applying it to our code presented challenges in and of itself, whether it was telling the code when to stop taking user input or ensuring that the process of deploying our code on a Google app engine is compatible with Assembly AI. 

## Accomplishments that we're proud of

Despite the many challenges that we ran into, we were very happy to have been able to overcome them by working effectively as a team in order to effectuate our project idea. In particular, there were many aspects of our project that our team members had no prior knowledge of, such as how to use Assembly AI or Selenium, but we were very proud to have been able to learn how to use such powerful tools in such a short amount of time. 

## What we learned

Our project started as a simple idea to get a list of ingredients based on a customer’s requested food. However, throughout the weekend, we learned two very important things. Even with one seemingly simple idea, there are often many different components that are required in order for the project to be practical. For instance, even with the process of searching for something, the process of web scraping involves a step-by-step rigorous set of instructions that are necessary to succeed. In addition, we learned that when generating an idea, it is far easier to expand slowly upon it to make the process more effective for our team. 

## What's next for CravesList
Even though our program was able to successfully meet our initial goals, our next steps for this project would be to ensure that the ingredients match as closely as possible to what the user wants. As such, we could allow for user feedback about the outputted ingredients, and use python to incorporate machine learning, and anonymously store previous responses in a database so that the program can adjust future ingredient recommendations to improve customer satisfaction even more. 
