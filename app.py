import streamlit as st
import chromadb
import uuid
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


client = chromadb.PersistentClient(path="./vectorstore")
collection = client.get_or_create_collection(name="job_portfolio")


llm = ChatGroq(
    api_key="YOUR_GROQ_API_KEY",  
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def extract_job_info(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)

    try:
        job_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text

        job_desc = None
        possible_selectors = [
            ".job-description",
            "div[data-automation-id='jobDescription']",
            "div[class*='description']"
        ]

        for selector in possible_selectors:
            try:
                job_desc = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                ).text
                if job_desc:
                    break
            except:
                continue
        
        if not job_desc:
            job_desc = "Job description not found"

        job_info = {"title": job_title, "description": job_desc}

    except Exception as e:
        job_info = {"error": f"Failed to extract job details: {str(e)}"}

    driver.quit()
    return job_info

# Function to extract job details using LLM
def extract_job_details(job_data):
    prompt_extract = PromptTemplate.from_template(
        """
        I will give you scraped text from the job posting. 
        Your job is to extract the job details & requirements in a JSON format containing the following keys: 'role', 'experience', 'skills', and 'description'. 
        Only return valid JSON. No preamble, please.
        Here is the scraped text: {job_data}
        """
    )

    chain_extract = prompt_extract | llm
    response = chain_extract.invoke(input={'job_data': job_data})

    json_parser = JsonOutputParser()
    job_json = json_parser.parse(response.content)
    return job_json

#  Store extracted job details in ChromaDB
def store_job_in_chromadb(job_json):
    job_details_str = str(job_json)

    collection.add(
        documents=[job_details_str],
        ids=[str(uuid.uuid4())],
        metadatas=[{"source": "Job Posting"}]
    )
    return "Job details stored successfully!"

# Function to match job details with stored portfolios
def match_job_to_portfolio(job_json):
    job_skills_str = str(job_json["skills"])

    results = collection.query(
        query_texts=[job_skills_str],
        n_results=1
    )

    if results["documents"]:
        return {
            "match": results["documents"][0],
            "metadata": results["metadatas"][0]
        }
    else:
        return {"error": "No matching portfolio found"}

# Function to generate a cold email using LLM
def generate_cold_email(job_json, match_result):
    job_role = job_json["role"]
    skills = ", ".join(job_json["skills"])
    experience = job_json["experience"]
    description = job_json["description"]
    
    portfolio_source = match_result["metadata"][0]["source"] if "metadata" in match_result else "N/A"

    prompt_email = PromptTemplate.from_template(
        """
        **Objective:**  
        Craft a highly professional and persuasive cold email targeted at hiring managers or recruiters.  
        The email should be personalized, highlighting how our company's experience, skills, and past projects align perfectly with the job role.  
    
        **Tone & Style:**  
        - Professional, engaging, and confident  
        - Concise and to the point (max 200 words)  
        - Friendly but not overly casual  
    
        **Email Structure:**  
    

           - A compelling and personalized subject line that grabs attention.  
           - Example: "Expert Python Developer for {job_role} – Let’s Connect!"  
     
           - Address the hiring manager or recruiter.  
           - Mention the specific job role and company name.  
           - Create a strong opening that sparks interest.  
    
           - Briefly mention relevant skills and experience based on the job posting.  
           - Show how our past projects align with their needs.  
           - Mention key technical skills that match the role.  
      
           - Highlight a relevant project from our portfolio.  
           - Explain how our experience can benefit their team.  
    
           - Politely ask for a meeting or call.  
           - Provide a direct way to contact us.  
           - Example: "Would love to discuss how we can add value to your team. Let’s schedule a quick call this week!"  
    
        **Job Details:**  
        - Role: {job_role}  
        - Skills: {skills}  
        - Experience: {experience}  
        - Description: {description}  
        - Matching Portfolio Source: {portfolio_source} 

        In saluatation don't mention hiring manager name, just give as Dear hiring manager.
        You are Ujjwal Kumar Singh [name], your email is ujjwalks2709@gmail.com, your phone number is +91 7543932088.
    
        ✨ Ensure the email feels natural, avoids generic phrasing, and maximizes impact!  
        """
    )

    chain_email = prompt_email | llm
    response_email = chain_email.invoke(input={
        "job_role": job_role,
        "skills": skills,
        "experience": experience,
        "description": description,
        "portfolio_source": portfolio_source
    })

    return response_email.content


st.title("AI-Powered Cold Email Generator")

# Input field for job URL
job_url = st.text_input("Enter Job Posting URL:")

if st.button("Generate Cold Email"):
    if job_url:
        st.write("🔍 Extracting job details... Please wait.")

        
        job_data = extract_job_info(job_url)

        if "error" in job_data:
            st.error(job_data["error"])
        else:
            
            job_json = extract_job_details(job_data["description"])

            
            store_message = store_job_in_chromadb(job_json)
            st.success(store_message)

            
            match_result = match_job_to_portfolio(job_json)

            if "error" in match_result:
                st.error(match_result["error"])
            else:
                st.write("✅ Matching portfolio found!")
                
                
                cold_email = generate_cold_email(job_json, match_result)
                
                
                st.subheader("📨 Generated Cold Email:")
                st.write(cold_email)

    else:
        st.warning("Please enter a valid job posting URL.")
