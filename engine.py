from serpapi.google_search import GoogleSearch
import google.generativeai as genai
from openai import OpenAI
#from rapidfuzz import fuzz
#import spacy
import json
import re

client = genai.GenerativeModel('gemini-1.5-flash')

params = {
  "api_key": "c89c60c5b258294355be4b089813ae5b34f593bb76a37c293bb3d905a12ec568",
  "engine": "google",
  "start": "0",
  "q": 'rohan raval ucsd site:linkedin.com/in',  
  "google_domain": "google.com",      
  "gl": "us",                         
  "hl": "en",                         
  "location": "India",       
  "num": "15",                      
  "no_cache": True                    
}

api_key = 'AIzaSyCeV1KXz-arpRDq2PnyzqFO66Wm5rQidTY'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')


client = OpenAI(api_key="sk-1d7703f788414eb589b1a6d99ef30677", base_url="https://api.deepseek.com")


def search(query):

  system_prompt = """
You are an expert Search Optimizer. Your task is to convert natural language queries into powerful Google search queries, specifically targeting LinkedIn profiles.

*Rules*:
•⁠  ⁠Always include: ⁠ site:linkedin.com/in ⁠
•⁠  ⁠Break complex terms into categories and use boolean operators like ⁠ AND ⁠, ⁠ OR ⁠, and ⁠ () ⁠ properly.
•⁠  ⁠For educational institutions or companies, expand known synonyms.
•⁠  ⁠Use quotes around exact matches like "Harvard" or "software engineer".
•⁠  ⁠Only output the final search string. No explanations.

*Examples*:

Input: Ivy League students working at FAANG
Output: site:linkedin.com/in ("Harvard" OR "Yale" OR "Princeton" OR "Columbia" OR "Brown" OR "Dartmouth" OR "Cornell" OR "University of Pennsylvania" OR "UPenn") AND ("student" OR "graduate" OR "alumni" OR "intern") AND ("Meta" OR "Facebook" OR "Amazon" OR "Apple" OR "Netflix" OR "Google" OR "Alphabet")

Input: Aman working at tntra.io
Output: site:linkedin.com/in "Aman" AND ("TNTRA" OR "tntra.io") AND ("developer" OR "engineer" OR "employee")


Input: incoming freshman at usc in fall 2025 doing ms in supply chain
Output: site:linkedin.com/in ("University of Southern California" OR "USC") 
        AND ("MS" OR "Master of Science") 
        AND ("Supply Chain" OR "SCM" OR "Logistics") 
        AND ("Fall 2025" OR "incoming" OR "admit" OR "class of 2025")


Now process this query and return only the optimized string:
"""

  response = client.chat.completions.create(
      model="deepseek-chat",
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": query},
      ],
      stream=False
  )

  return response.choices[0].message.content

def execute_search(query):
  params['q'] = query
  search = GoogleSearch(params)
  results = search.get_dict()
  try:
    return results['organic_results']
  except:
    return ['empty']


#nlp = spacy.blank('en')
#nlp.add_pipe('gliner_spacy')


#def extract_person_names_list(profiles):
 #   extracted = []
  #  for idx, profile in enumerate(profiles):
   #     if not isinstance(profile, dict):
    #        continue
     #   if 'title' not in profile:
      #      continue

       # doc = nlp(profile['title'])
       # name = None
       # for ent in doc.ents:
       #     if ent.label_.lower() == "person":
       #         name = ent.text.strip()
       #         break
       # extracted.append((idx, name))
    #return extracted


#def match_profiles_by_extracted_names(linkedin_list, researchgate_list, threshold=95):
    #linkedin_names = extract_person_names_list(linkedin_list)
    #researchgate_names = extract_person_names_list(researchgate_list)

    #matches = []
    #used_rg = set()

    #for li_idx, li_name in linkedin_names:
     #   if not li_name:
      #      continue

      #  best_match = None
      #  best_score = 0

      #  for rg_idx, rg_name in researchgate_names:
      #      if rg_idx in used_rg or not rg_name:
      #          continue

      #      score = fuzz.ratio(li_name.lower(), rg_name.lower())

      #      if score > best_score:
      #          best_score = score
      #          best_match = rg_idx

      #  if best_score >= threshold and best_match is not None:
      #      matches.append({
      #          "name": li_name,
      #          "linkedin": linkedin_list[li_idx],
      #          "researchgate": researchgate_list[best_match],
      #          "match_score": best_score
      #      })
      #      used_rg.add(best_match)

   # return matches



def linkedin_profiles(natural_query):
    search_query = search(natural_query)
    print("search query: ",search_query)
    sub_answer = []
    sub_ans1 = []
    sub_ans2 = []


    sub_answer.append(execute_search(search_query))
    #urls = url_replace(search_query)


    #print("\n Total queries being searched: ")
    #for q in urls:
    #  print("→", q)


    #sub_ans1.append(execute_search(urls[0]))
    #if len(urls) > 1:
    #  sub_ans2.append(execute_search(urls[1]))
     # matched = match_profiles_by_extracted_names(sub_ans1, sub_ans2)
      #if matched:
      #  sub_answer.append(matched)
      #else:
      #  sub_answer.append(sub_ans2)


    answers = [item for sublist in sub_answer for item in sublist]
    return map_to_profile_card_format(answers)



def link_check(links):
  linkedin_pattern = r'^https?://(www\.)?linkedin\.com/in/[^/\s]+'
  researchgate_pattern = r'^https?://(www\.)?researchgate\.net/profile/[^/]+/$'
  crunchbase_pattern = r'^https?://(www\.)?crunchbase\.com/person/[^/]+/$'

  correct_profiles = []
  for i in range(0, len(links)):
    url = links[i]['link']

    if (re.match(linkedin_pattern, url)):
      correct_profiles.append(links[i])
    elif (re.match(researchgate_pattern, url)):
      correct_profiles.append(links[i])
    elif (re.match(crunchbase_pattern, url)):
      correct_profiles.append(links[i])
    else:
      pass

  return correct_profiles


def url_replace(search_query):
    queries = []

    if "site:" not in search_query:
        base_query = search_query + " site:linkedin.com/in"
    elif "site:linkedin.com/in" not in search_query:
        base_query = search_query + " site:linkedin.com/in"
    else:
        base_query = search_query

    queries.append(base_query)

    service = service_decider(search_query)

    if service == 'crunchbase':
        crunch_query = base_query.replace("site:linkedin.com/in", "site:crunchbase.com/person")
        queries.append(crunch_query)
    elif service == 'researchgate':
        research_query = base_query.replace("site:linkedin.com/in", "site:researchgate.net/profile")
        queries.append(research_query)

    return queries





def service_decider(google_query):

  SERVICE_DECIDER_PROMPT = f"""
    You are a classification assistant. Given a user query, return which service is best suited to search for relevant people:

    - Use "crunchbase" if the query is about startups, investors, or founders.
    - Do not classify queries about corporate professionals, students, or interns at large tech companies as "crunchbase" unless the query directly mentions startups, founders, or investors.
    - Use "researchgate" if the query is about academic researchers, PhDs, publications, or scientific work.
    - If neither applies, return "unknown".

    User query: {google_query}

    Return only one word: "crunchbase", "researchgate", or "unknown".
    """


  classifier = model.generate_content(SERVICE_DECIDER_PROMPT)

  return classifier.text.strip().replace('"', '').lower()


def map_to_profile_card_format(results):
    mapped = []
    for item in results:
        mapped.append({
            "name": item.get("title", "Unknown"),
            "title": "",  # You can try to extract a title if available
            "company": "",  # You can try to extract a company if available
            "snippet": item.get("snippet", ""),
            "linkedinUrl": item.get("link", ""),
            "avatarUrl": "",  # You can add logic to fetch avatars if you want
        })
    return mapped
