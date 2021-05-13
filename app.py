import streamlit as st
import pandas as pd
import json
import requests
import time


from time import sleep
import random

from seleniumwire import webdriver

from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.chrome.options import Options





def main():
	ddf = pd.DataFrame()

	

	st.title("Get Linkedⓘⓝ Employee Data")
	st.sidebar.title("Provide your details here:")

	li_at = st.sidebar.text_input('Your li_at cookie:')

	JSESSIONID = st.sidebar.text_input('Your JSESSIONID:')

	company = st.sidebar.text_input('(Single) Linkedin Company Name (lowercase):')


	if st.sidebar.button('Get Data for Single Company'):
		all_requests = get_data(li_at, JSESSIONID, company)
		df = build_data(all_requests, ddf)
		write_data(df)



def get_data(li_at, JSESSIONID, company):

	options = Options()
	options.add_argument("window-size=1920,1080")
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')

	driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


	driver.get('https://www.linkedin.com/404?_l=en_US')


	if(driver.find_element_by_id('error404').text):
		st.write("Starting Session")

	else:
		st.write("Couldn't start a session. Exiting...")
		driver.quit()


	# sleep(random.uniform(2.5, 4.5))

	# driver.delete_cookie("JSESSIONID")

	driver.add_cookie({'name': 'li_at', 'value': li_at,'domain':'linkedin.com'})

	driver.add_cookie({'name': 'JSESSIONID', 'value': JSESSIONID,'domain':'linkedin.com'})

	# sleep(random.uniform(5.5, 6.5))

	




	url = "https://www.linkedin.com/company/"+str(company)+"/people/"

	driver.get(url)

	sleep(random.uniform(5.5, 6.5))

	if(driver.find_element_by_class_name('mt1').text):
		st.write("Sesssion Created")
		st.write(driver.find_element_by_class_name('mt1').text)
		sleep(random.uniform(1, 2.5))
		st.write("Now Fethching Employee Data...")

	else:
		st.write("Couldn't create a session. Exiting...")
		driver.quit()



	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
	    SCROLL_PAUSE_TIME = random.uniform(2.5, 4.5)
	    
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	    # Wait to load page
	    sleep(SCROLL_PAUSE_TIME)

	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	        break
	    last_height = new_height


	fetched_requests = driver.requests

	driver.quit()

	return(fetched_requests)

	

def build_data(all_requests, ddf):

	for request in all_requests:
	    if request.response:
	        if 'voyager/api/search/hits' in request.path:

	            
	            y = json.loads(request.response.body.decode("utf-8")) 
	            
	            for ele in y["data"]["elements"]:

	                try:
	                    LinkedIn_ID_AlphaNumeric = ele["hitInfo"]["id"]
	                except:
	                    LinkedIn_ID_AlphaNumeric = "NA" 

	                for inc in y["included"]:
	                    if (inc["entityUrn"].split(":")[3] == LinkedIn_ID_AlphaNumeric):

	                        try:

	                            First_Name = inc["firstName"]
	                            break # If you don't break the loop after finding a firstName , then any other later LinkedIn_ID_AlphaNumeric match that doesn't have required field will result in executing except and hence an NA assignment

	                        except:

	                            First_Name = "NA"
	                            
	                if bool(First_Name)==0:
	                    First_Name = "NA"

	                for inc in y["included"]:
	                    if (inc["entityUrn"].split(":")[3] == LinkedIn_ID_AlphaNumeric):

	                        try:

	                            Last_Name = inc["lastName"]
	                            break # If you don't break the loop after finding a lastName , then any other later LinkedIn_ID_AlphaNumeric match that doesn't have required field will result in executing except and hence an NA assignment
	                        except:

	                            Last_Name = "NA"
	                            
	                if bool(Last_Name)==0:
	                    Last_Name = "NA"
	                    
	                if First_Name == "NA" and Last_Name == "NA":
	                    Name = "NA"
	                else:
	                    Name = First_Name+" "+Last_Name 

	                try:
	                    LinkedIn_ID_No = ele["hitInfo"]["backendUrn"].split(":")[3]
	                except:
	                    LinkedIn_ID_No = "NA"         

	                for inc in y["included"]:
	                    if (inc["entityUrn"].split(":")[3] == LinkedIn_ID_AlphaNumeric):

	                        try:

	                            Linkedin_Public_ID = inc["publicIdentifier"]
	                            break #important
	                        except:

	                            Linkedin_Public_ID = "NA"

	                if Linkedin_Public_ID == "NA":
	                    LinkedIn_URL = "NA"
	                else:
	                    LinkedIn_URL = "linkedin.com/in/"+str(Linkedin_Public_ID)

	                try:
	                    Facebook_URL = "NA"
	                except:
	                    Facebook_URL = "NA"      

	                try:
	                    Twitter_URL = "NA"
	                except:
	                    Twitter_URL = "NA"  

	                try:
	                    External_Id = "NA"
	                except:
	                    External_Id = "NA"

	                try:
	                    Address = "NA"
	                except:
	                    Address = "NA" 

	                try:
	                    Suite = "NA"
	                except:
	                    Suite = "NA"        

	                try:
	                    City = ele["hitInfo"]["location"].split(",")[0] #WIP what is there is no comma ; is input city or country
	                except:
	                    City = "NA"          

	                try:
	                    try:

	                        Country = ele["hitInfo"]["location"].split(",")[1].strip()

	                    except:
	                        Country = ele["hitInfo"]["location"].split(",")[0].strip()         
	                except:
	                    Country = "NA"

	                if Country == "Canada Area": #WIP - May have to build multiple cleanup cases
	                    Country = "Canada"

	                try:
	                    State = "NA"
	                except:
	                    State = "NA"  


	                try:
	                    Postal_Code = "NA"
	                except:
	                    Postal_Code = "NA"


	                try:
	                    Phone = "NA"
	                except:
	                    Phone = "NA"  

	                for inc in y["included"]:
	                    if (inc["entityUrn"].split(":")[3] == LinkedIn_ID_AlphaNumeric):

	                        try:

	                            rootURL = inc["picture"]["rootUrl"].split("/")[5]
	                            fileIdentifyingUrlPathSegment = inc["picture"]["artifacts"][2]["fileIdentifyingUrlPathSegment"]

	                            Profile_image_URL = "https://media-exp1.licdn.com/dms/image/"+str(rootURL)+("/profile-displayphoto-shrink_")+str(fileIdentifyingUrlPathSegment)

	                            break
	                        except:

	                            Profile_image_URL = "NA"


	                try:
	                    Current = "WIP"
	                except:
	                    Current = "WIP"


	                try:
	                    Job_Title = ele["hitInfo"]["snippets"][0][heading][text].split("at")[0].strip()

	                except:
	                    for inc in y["included"]:
	                        if (inc["entityUrn"].split(":")[3] == LinkedIn_ID_AlphaNumeric):

	                            try:
	                                Job_Title = inc["occupation"].split("at")[0].strip()

	                                break # Important
	                            except:

	                                Job_Title = "NA"     

	                try:
	                    Job_Type = "WIP"
	                except:
	                    Job_Type = "WIP"

	                try:
	                    Present_State = "NA"
	                except:
	                    Present_State = "NA"

	                try:
	                    Started_On = "NA"
	                except:
	                    Started_On = "NA"

	                try:
	                    Organization_Identifier = "WIP"
	                except:
	                    Organization_Identifier = "WIP"

	                try:
	                    Ended_On = "NA"
	                except:
	                    Ended_On = "NA"                

	                data = {
	                    "First_Name" : [First_Name],
	                    "Last_Name" : [Last_Name],
	                    "Name" : [Name],
	                    "LinkedIn_ID_No" : [LinkedIn_ID_No],
	                    "Linkedin_Public_ID" : [Linkedin_Public_ID],
	                    "LinkedIn_ID_AlphaNumeric" : [LinkedIn_ID_AlphaNumeric],
	                    "LinkedIn_URL" : [LinkedIn_URL],
	                    "Facebook_URL" : [Facebook_URL],
	                    "Twitter_URL" : [Twitter_URL],
	                    "External_Id" : [External_Id],
	                    "Address" : [Address],
	                    "Suite" : [Suite],
	                    "City" : [City],
	                    "Country" : [Country],
	                    "State" : [State],
	                    "Postal_Code" : [Postal_Code],
	                    "Phone" : [Phone],
	                    "Profile_image_URL" : [Profile_image_URL],
	                    "Current" : [Current],
	                    "Job_Title" : [Job_Title],
	                    "Job_Type" : [Job_Type],
	                    "Present_State" : [Present_State],
	                    "Started_On" : [Started_On],
	                    "Organization_Identifier" : [Organization_Identifier],
	                    "Ended_On" : [Ended_On],
	                }

	                t = pd.DataFrame(data=data)
	                ddf = ddf.append(t,ignore_index=True)


	return ddf



def write_data(dframe):
	st.write(dframe)
	st.write("Sesssion Closed")




if __name__ == '__main__':
	main()
 
