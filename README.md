
# AI Updates Newsletter Platform  

## Project Description  
AI Updates makes it easy to stay up-to-date with everything in the world of artificial intelligence. From the latest news to new tools and product updates, we bring it all straight to your inbox. Simple, convenient, and made for anyone who wants to stay in the know.

link to the website:-https://ai-and-tech.onrender.com/
---
## Features and Functionality  
- **User-Friendly Interface**  
  A clean interface for browsing AI news and subscribing to updates.  
   
- **Dynamic Carousel**  
  Interactive carousel showcasing example newsletters.  

- **OTP Verification**  
  Secure OTP integration for protecting subscription forms.  

- **Subscriber Management**  
  Database-backed subscription and email storage.  

- **FAQs Section**  
  A detailed FAQ section addressing common user queries.  

- **Responsive Design**  
  Fully responsive across devices.  

---

## Instructions for Usage or Setup  

### Prerequisites  
- Python (version 3.8 or higher)  
- Flask  
- PostgreSQL  
- `dotenv` package for environment variable management  

### Setup Steps  
1. **Clone the Repository**  
   ```bash  
   git clone <repository_url>  
   cd <repository_name>
   
2.**Install Dependencies**  
  pip install -r requirements.txt  
  
3.**create .env file with details below**
  
  SENDER_EMAIL='aiandtechnewsletter@gmail.com'
  
  SENDER_PASSWORD='xspo mmpk gmqs ujpu'
  
  DATABASE_URL='postgresql://newsletter_g6ru_user:KREKfq0nY4817cJpYjPYZ9kRIxJTEWyh@dpg-ctoccktumphs73cdgfi0-a.singapore-postgres.render.com/newsletter_g6ru'

  
4.**Run the Application**

  python app.py

5.**go to the link**

  in terminal it will show link like this  [Running on http://127.0.0.1:5000] ctrl+click on the link it will open  website locally in your default browser.

    
6.**Subscribing**

  now hit sign up or Get started for free button to subscribe,enter details and enter otp(note-check for the otp in spam mails and report it as not spam)

   
7.**sending updates to subscribers**

  run python file named mailer.py to send AI updates to subscribers, instead of doing this manually, we can upload this python file in "python anywhere" 
  and can set the timer to run the file automatically.

  note:- if requests and lxml are not already available in your Python environment.
     
     install them using these commands :-
     
     pip install requests
     
     pip install lxml

    

### Details of Group Members
  Jhansi(cs23i1021)  yaswitha(cs23i1037)

 

