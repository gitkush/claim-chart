import streamlit as st


import yagmail

import os

from docx import Document


import requests
from bs4 import BeautifulSoup


def main():

	st.sidebar.title("Get a claim chart to start mapping")
	st.title("Provide your details in the sidebar")

	patent_number = st.sidebar.text_input('Patent Number:')

	email = st.sidebar.text_input('Your email:')

	if st.sidebar.button('Get Claim-Chart'):
		if(patent_number=="" or email==""):
			st.write("Please enter patent_number and email")
		
		else:

			try:

				user = 'data@ankushgaur.com'
				app_password = 'njwyiovhniepufxy' # a token for gmail
				to = email

				url = "https://patents.google.com/patent/"+str(patent_number)+"/en"

				response = requests.get(url)

				soup = BeautifulSoup(response.content, 'html.parser')

				clm = []
				claims = soup.find("section",{"itemprop":"claims"} ).find_next("div",{"itemprop":"content"}).find_all("div",{"class":"claim"})
				for claim in claims:
				    if(claim.has_attr("num")):
				        split_text = claim.text.split(";")
				        for ctext in split_text:
				            clm.append(ctext.strip())
				
				document = Document()

				table = document.add_table(rows=1, cols=2)
				hdr_cells = table.rows[0].cells
				hdr_cells[0].text = 'Claim'
				hdr_cells[1].text = 'Mapping'
				for c in clm:
				    row_cells = table.add_row().cells
				    row_cells[0].text = str(c)
				    row_cells[1].text = ""

				table.style = 'Table Grid'

				file_name = "Claim-Chart-"+str(patent_number)+".docx"
				document.save(file_name)



				subject = 'Data from Ankush Gaur - Claim chart for '+patent_number
				content = ['Hi \n Here is the claim-chart for you to start mapping. \nPlease find the attachment.',file_name]

				with yagmail.SMTP(user, app_password) as yag:
				    yag.send(to, subject, content)
				    
				    st.write('Sent email successfully')
				    st.write("Please find an email from data@ankushgaur.com with patent number in the subject")
				    st.write("Make sure to check the spam/junk folder and move emails to inbox.")
				    st.write("Time to get to work! 🙂")

				if os.path.exists(file_name):
				  os.remove(file_name)
				  # st.write("File deleted")
				else:
					pass
				  # st.write("The file does not exist")

			except:
				st.write("Unable to process request. Report this to Ankush [ankushgaur@live.com]")

if __name__ == '__main__':
	main()	
