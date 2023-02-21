import requests
from bs4 import BeautifulSoup
import csv
import time

site = 'Apple_Stackexchange'

# Create and open the CSV files
questions_file = open(f'{site}-questions.csv', mode='w', newline='', encoding='utf-8')
answers_file = open(f'{site}-answers.csv', mode='w', newline='', encoding='utf-8')

# Create the CSV writers
questions_writer = csv.writer(questions_file)
answers_writer = csv.writer(answers_file)

# Write the column names to the CSV files
questions_writer.writerow(['Question_Title', 'Question_ID', 'Author_Name', 'Author_ID', 'Author_Rep', 'Question_Post_Time',
                           'Question_Score', 'Number_Of_Views', 'Number_Of_Answers', 'Number_Of_Comments', 'Edited', 
                           'Answer_Accepted', 'Tag_1', 'Tag_2', 'Tag_3', 'Tag_4', 'Tag_5', 'Question_Closed'])

answers_writer.writerow(['Question_ID', 'Answer_Score', 'Author_Name', 'Author_ID', 'Author_Rep', 
                         'Number_Of_Comments', 'Answer_Accepted'])

# Loop through the pages of newest questions
for page_num in range(1, 10): 
    page_url = f'https://apple.stackexchange.com/questions?tab=Newest'
    page_html = requests.get(page_url).text
    page_soup = BeautifulSoup(page_html, 'html.parser')

    # Extract the links to each question's individual page
    question_links = page_soup.find_all('a', class_='question-hyperlink')
    question_urls = [link.get('href') for link in question_links]

    # Loop through each question's individual page and extract the required data
    for question_url in question_urls:
        question_html = requests.get(question_url).text
        question_soup = BeautifulSoup(question_html, 'html.parser')

        # Extract data using beautifulsoup and store them
        question_id = question_soup.find('div', {'class': 'question js-question'})['data-questionid']
        
        
        # Find the div with class 'user-details'
        user_details = question_soup.find('div', {'class': 'user-details'})
        # Extract the name
        try:
            name = user_details.find('a').text
        except AttributeError:
            name = "N/A"
        # Extract the ID
        try:
            user_id = user_details.find('a')['href'].split('/')[-2]
        except Exception:
            user_id = "N/A"
        # Extract the reputation score
        try:
            reputation_score = user_details.find('span', {'class': 'reputation-score'}).text.replace(',', '')
        except Exception:
            reputation_score = "N/A"
            
        # Find time the original post
        timestamp = question_soup.find('span', {'class': 'relativetime'})['title']
        # Find the question score
        try:
            score = int(question_soup.find('span', {'class': 'vote-count-post'}).text)
        except Exception:
            score = "N/A"
        # Find the number of views
        try:
            views = int(question_soup.find('div', {'class': 'js-gps-track'}).text.replace(' views', '').replace(',', ''))
        except Exception:
            views = "N/A"
        # Find the number of answers
        try:
            answers = int(question_soup.find('h2', {'class': 'mb0'}).span.text)
        except Exception:
            answers = "N/A"
        # Find whether an answer was accepted
        accepted = question_soup.find('div', {'class': 'js-accepted-answer-indicator'}) is not None
        # Find the tag elements with class "post-tag" (which contains the question tags)
        tag_elements = question_soup.find_all('a', {'class': 'post-tag'})
        # Extract the tag text from the tag elements
        tags = [tag.text for tag in tag_elements]
        
        # Check if the question is closed
        closed_element = question_soup.find('div', {'class': 'js-question-closed'})
        is_closed = closed_element is not None
        
        # Check if the "edited" class is present in the question's post history
        edited_class = question_soup.select_one('.post-signature.owner .user-action-time .relativetime.edited')
        has_been_edited = edited_class is not None
        # Find the tag element with class "js-comment-count" (which contains the number of comments)
        comment_element = question_soup.find('a', {'class': 'js-comment-count'})
        

        # Loop through each answer div element
        if question_soup.find('div', {'class': 'js-answers-header'}):
            # Find all the answer div elements
            answer_divs = question_soup.find_all('div', {'class': 'answer'})
            for answer_div in answer_divs:
                # Extract the answer score
                ans_score = int(answer_div.find('div', {'class': 'data-answercount'}).text)
                # Extract the poster's name, ID, and reputation score
                poster_div = answer_div.find('div', {'class': 'user-details'})
                ans_name = poster_div.find('a').text
                profile_url = poster_div.find('a')['href']
                ans_user_id = profile_url.split('/')[2]
                ans_reputation_score = int(answer_div.find('span', {'class': 'reputation-score'}).text.replace(',', ''))
    
                # Extract the number of comments for the answer
                comment_divs = answer_div.find_all('div', {'class': 'js-comment-container'})
                num_comments = len(comment_divs)
                
                # Check if the answer is accepted or not
                is_accepted = answer_div.find('div', {'class': 'js-accepted-answer-indicator'}) is not None
        else: ans_score = poster_div = ans_name = profile_url = ans_user_id = ans_reputation_score = "NA"
        

    
    answer_data_list = []

    # Write the extracted data to the CSV files
    questions_writer.writerow([...])
    for answer_data in answer_data_list:
        answers_writer.writerow(answer_data)
    # Delay for 1 second before downloaDing the next page
    time.sleep(1)

# Close the CSV files
questions_file.close()
answers_file.close()
