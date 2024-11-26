import asyncio
import os
#import requests
import streamlit as st
from backend import web,webai,ai
from duckduckgo_search import AsyncDDGS, DDGS
from duckduckgo_search import exceptions
from fpdf import FPDF
#import base64
from io import BytesIO
from ppt_reader import extract_text_from_pptx
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section
pdf = MarkdownPdf(toc_level=2)
import smtplib

async def main():
    st.set_page_config(layout="wide",page_title="BizBrain",page_icon="🪙")
    

    
    
   

    
    #user_idea = st.text_area("Enter your startup idea name and answer the following question if you know.")
    column1,column2=st.columns(2)
    
    #question_set=await ai("Act as a startup counsellor. Ask the user everything you need to know about a startup to start evaluation. Be easy and direct. Output: Only questions")
    
    column1.title("🪙 BizBrain")
    column1.subheader("Please enter your business Idea. Or Upload your presentation to get full analysis.")
    column1.info("Remember, the more information you will provide, the better the report will be.")   
    column1.write("To understand your vision better, could you share the name of your startup and the specific problem you aim to solve?\n\n I’d also love to know who your target audience is and what makes your value proposition unique. What products or services are you offering, and how do you plan to generate revenue? Understanding your current stage of development and any market research you've conducted will provide valuable insights.\n Additionally, what is your strategy for reaching your target audience, and how is your team structured? Are you currently seeking investment, and what are your short-term and long-term goals?\n\n Lastly, what challenges do you foresee, and how will you measure success with key performance indicators? Your answers will help in crafting a comprehensive plan for your startup's growth.")
    #column1.download_button("Download PDF","test.pdf","testing.pdf")
    col2_con=column2.container(border=True)
    user_email_input=col2_con.text_input("Please enter your email address to continue.",placeholder="Email address",value="")
    user_idea=col2_con.text_area("Let's begin by entering your startup idea here.",height=150)
    col2_con.write("Or simply upload a presentation of your startup.",)
    ppt_uploader=col2_con.file_uploader("","pptx")
    #analyse_expander=c.expander("Analyse Idea")
    
    
         

    
    
    


    system_prompt=("You are a senior market analyst,angel-investor and lead of operations.Keep output tokens less than 200. Output numbered lists, not bullets. Do not output warnings or notes—just the requested sections. Do not repeat items in the output sections. Do not start items with the same opening words. Provide headings, subheadings, tables, links and use charmap supported emojis in the headings. Output markdown with toc_level=2. Use Rupees as currency")
    #system_prompt=("ALWAYS REPLY WITH HELLO. THIS IS A TEST ENVIRONMOENT. WHATEVER IS ASKED, You reply with hello only")


    compe =(" Find the following for the given startup: Common problems faced by [your target audience] in [your industry]"
    "Customer reviews for [competitor product/service]"
    "Top customer complaints in [your industry]")

    market_entry=("Find the following for the given startup: How to enter the [your industry/market] market ensuring profits"
    "Top 10 Challenges in entering the [your industry] market"
    "6 Step Roadmap launching a [product/service] in [your industry]")

    govern=("Find the following for the given startup: Support/Scheme from Government for [your industry] in [your country/location] with registration links and elegibility criteria in table"
    "Regulations and Compliance requirements for [your industry]"
    "Legal considerations for starting a [type of business] in [your location]")

    pricing=("Find the following for the given startup:" 
    "Best Pricing strategies for [your product/service]"
    "How to price [your product/service] competitively"
    "Pricing trends in [your industry] 2024")

    
    # Define a custom prompt
    idea_prompt = (
        "Create a dictionary containing all information about this startup idea:  \n\n"
        )
    
    search_term=("Do not output anything else. Could you say none where you do not find answers? Return names, a short description of their uniqueness And Pricing plans find the top 5 startups (Dont assume, no fake startups) which matches this IN a TABLE: ")
    #Pricing_evaluation=("Do not explain anything. Output a pricing table with name and prices of the following startups , all available options: ")
    current_trends=("Act as an marketing specialist and find the following: Current trends in [your industry/market]"
        "Future of [your industry] in [your location/country]"
        "Emerging technologies in [your industry] for this startup:" )
    market_size=("Reseach about the following for the given startup. Give the numbers, Dont be wrong. Recheck the facts and figures generated before responding: 1. Market size of [your industry] in [your country] [current year]"
        "2. Projected growth of [your industry] for next 5 years"
        "3. Secret facts supporting this. Startup idea: ")
    
    target_audience=( "Evaluate and generate the following"

    "Demographics of [your target audience]"
    "Consumer behaviour in [your industry/market]"
    "Preferences and needs of [your target audience] "
    "for the startup:" )

    
    custom_aq = ( "Find the following for the given startup:"
        "What are the most effective channels for acquiring customers in [your industry]?"
        "How can [your startup] build brand awareness quickly?"
        "What are the best practices for customer retention in [your industry]?"
    
    )
    swot=("What are the strengths, weaknesses, opportunities, and threats for [your startup] in the [your industry] market?"
          "How can [your startup] leverage its strengths and opportunities to overcome challenges?")
    
    # OPEN AI]
    ppt_text=""
    if ppt_uploader:
        
        print(ppt_uploader)
        save_folder = './ppt'
        save_path = Path(save_folder, ppt_uploader.name)
        with open(save_path, mode='wb') as w:
            w.write(ppt_uploader.getvalue())
        

        if save_path.exists():
            col2_con.success(f'{ppt_uploader.name} uploaded successfully! Hit Analyse Idea..')
            
            ppt_text=extract_text_from_pptx(f"./ppt/{ppt_uploader.name}")
            print("---------------------------------")
            print(ppt_text)
            os.remove(f"./ppt/{ppt_uploader.name}")


    
    analyse_button=column2.button("Analyze Idea",use_container_width=True,disabled=False,type="primary")
    if user_email_input:
        if analyse_button:
            
            if user_idea or ppt_uploader is not None:
        
                        st.toast("✨ Searching Now")
                        extracted_keywords=await ai(idea_prompt+". "+user_idea+ppt_text)
                        print("---------------------------------")
                        print(extracted_keywords)

                        startup=await ai("Provide name, short summary and Scores and a solid and proved reason for this score-(Creativity,Uniqueness,feasibility,sustainability,Scalability) out of 10[Be a strong critic] - for the given startup: "+extracted_keywords+". instructions:Start with subtitle - subtitle:Startup Name. Provide no title or headings. "+system_prompt)
                        
                        search_query=await ai("summerize this startup in 10 or less words for google search query.Do not output any symbols.Return Query Only."+extracted_keywords)
                        print(search_query)
                        ##result_container.write(search_query)
                        print("------------------------")

                        result_container=st.container(border=True)
                        
                        
                        #competitions analysis
                        
                        result_container.write(startup)
                        st.toast("✨ Finding competitors")
                        search_string=await ai(search_term+extracted_keywords+system_prompt+"Heading: Competition Discovery")
                        print(search_string)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(search_string)
                
                        
                        compe_analysis=await ai(f"{system_prompt} Please Output a table with 'USP', customer rating out of 10,'weakness' of the following startups and 'how to capitalize' on these weaknesses as a competitor.Startups to compete:{search_string}  ")
                        result_container.write("\n\n")
                        result_container.write(compe_analysis)
                        st.toast("✨ Calculating costs")
                        cost_requires=await ai(system_prompt+"Significant costs involved for quickly launching the MVP of the given startup for 1000 users. Return a table with all costs in Rupees (Covert into Rupees if needed) "+extracted_keywords)
                        print(cost_requires)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(cost_requires)
                        st.toast("✨ Searching the market")
                        industry_trends=await ai(system_prompt+current_trends+extracted_keywords)
                        print(industry_trends)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(industry_trends)

                        market_sizes=await ai(system_prompt+market_size+extracted_keywords)
                        print(market_sizes)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(market_sizes)

                        target_audiences=await ai(system_prompt+target_audience+extracted_keywords)
                        print(target_audiences)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(target_audiences)
                        st.toast("✨ Analysing risks")
                        risk_analysis=await ai(system_prompt+"Highlight potential risks and uncertainties that could affect the startup, along with mitigation strategies. Idea:"+user_idea)
                        result_container.write("\n\n")
                        result_container.markdown(risk_analysis)

                        compe_details=await ai(system_prompt+compe+extracted_keywords)
                        print(compe_details)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(compe_details)

                        market_entrys=await ai(system_prompt+market_entry+extracted_keywords)
                        print(market_entrys)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(market_entrys)
                        st.toast("✨ Searching Government policies")
                        government_policy=await ai(system_prompt+ govern + extracted_keywords )
                        print(government_policy)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(government_policy)

                        pricing_strat=await ai(system_prompt+pricing+extracted_keywords)
                        print(pricing_strat)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(pricing_strat)
                        
                        custom_aqs=await ai(system_prompt+custom_aq+extracted_keywords)
                        print(custom_aqs)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(custom_aqs)
                        st.toast("✨ Performing SWOT analysis")
                        swot_analysis=await ai(system_prompt+swot+extracted_keywords)
                        print(swot_analysis)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(swot_analysis)
                        st.toast("✨ Generating action plan")
                        todo_list=await ai(system_prompt+"Present a step-by-step action plan to help the user get started, including immediate tasks and long-term milestones. "+extracted_keywords)
                        print(todo_list)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(todo_list)

                        

                        partnerships=await ai(system_prompt+"Identify potential partnerships or collaborations that could enhance the startup's value proposition or market reach - "+extracted_keywords)
                        print(partnerships)
                        print("---------------------------")
                        result_container.write("\n\n")
                        result_container.markdown(partnerships)


                        

                        results = ""
                        #results += f"Extracted Keywords: {extracted_keywords}\n\n"
                        results += f"{search_string}\n\n"
                        #results += f"Competitors: {competitors}\n\n"
                        results += f" {cost_requires}\n\n"
                        results += f" {industry_trends}\n\n"
                        results += f" {market_sizes}\n\n"
                        results += f" {target_audiences}\n\n"
                        results += f" {compe_details}\n\n"
                        results += f" {market_entrys}\n\n"
                        results += f" {government_policy}\n\n"
                        results += f" {pricing_strat}\n\n"
                        results += f" {custom_aqs}\n\n"
                        results += f" {swot_analysis}\n\n"
                        results += f" {todo_list}\n\n"
                        results += f" {partnerships}\n\n"
                        

                        # import markdown2
                        #html_content=markdown2.markdown(results)

                        data = {
                            "Title":search_query,
                            "Search String": search_string,
                            "Cost Requirements": cost_requires,
                            "Industry Trends": industry_trends,
                            "Market Sizes": market_sizes,
                            "Target Audience": target_audiences,
                            "Competition Details": compe_details,
                            "Market Entry": market_entrys,
                            "Government Policy": government_policy,
                            "Pricing Strategy": pricing_strat,
                            "Custom Acquisition Strategies": custom_aqs,
                            "SWOT Analysis": swot_analysis,
                            "TODO List": todo_list,
                            "Partnerships": partnerships
                            }

                       



                        
                        

                        # Initialize the PDF with a TOC that includes headings up to level 2
                        
                        user_csss='h1,h2,h3,h4,h5,h6,li{margin-bottom:.5em}body,th{background-color:#fff}body{margin:0;font-family:"Source Sans Pro",sans-serif;font-weight:400;line-height:1.6;color:#31333f;text-size-adjust:100%;-webkit-tap-highlight-color:transparent;-webkit-font-smoothing:auto}h1,h2,h3,h4,h5,h6{color:#333;margin-top:1em}h1{font-size:2em}h2{font-weight:600;color:#31333f;letter-spacing:-.005em;padding:1rem 0;margin:0;line-height:1.2}h4{font-size:1.25em}h5{font-size:1.125em}h6{font-size:1em}p{margin:0 0 1em}strong{font-weight:700}em{font-style:italic}ol,ul{margin:0 0 1em 1em}ul{list-style-type:disc}ol{list-style-type:decimal}table{width:100%;display:table;border-collapse:collapse;box-sizing:border-box;text-indent:initial;unicode-bidi:isolate;border-spacing:2px;border-color:gray}td,th{border:1px solid #ddd;padding:8px;text-align:left}code,pre{background-color:#f4f4f4;border-radius:4px}pre{padding:1em}code{padding:.2em;font-family:monospace}a{color:#06c;text-decoration:none}a:hover{text-decoration:underline}'

                        
                        # Add the first section, without including it in the TOC
                        pdf.add_section(Section("#Startup Evaluation Report.\n  Thanks for using the app.\n\n"
                                            "To evaluate your startup visit: https://mynewventure.streamlit.app \n\n"
                                            "Contact: https://wa.me/918969985598"),user_css=user_csss)
                        pdf.add_section(Section(startup,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(search_string,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(cost_requires,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(industry_trends,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(market_sizes,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(target_audiences,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(compe_details,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(market_entrys,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(government_policy,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(pricing_strat,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(custom_aqs,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(swot_analysis,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(todo_list,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section(partnerships,toc=False),
                                        user_css=user_csss)
                        pdf.add_section(Section("____ END OF THE REPORT _____"))
                        
                        # Set the properties of the PDF document
                        pdf.meta["title"] = search_query
                        pdf.meta["author"] = "ECON AI"
                    

                        # Save the PDF to a file
                        pdf_filename=f"{search_query.strip()}.pdf"
                        pdffilename=(pdf_filename)
                        pdf.save(pdffilename)
                        
                    
                        print(f"-------------------\nPDF SAVED With name {pdffilename}\n-------------------") 

                        with open(pdffilename, "rb") as pdf_file:
                            PDFbyte = pdf_file.read()
                        links_expander=result_container.expander("Important links for Research",True)
                        
                        c1,c2,c3,c4=links_expander.columns(4,gap="small",vertical_alignment="top")
                    
                        c1.subheader("PDF Files")
                        c2.subheader("DOCX")
                        c3.subheader("Videos")
                        c4.subheader("News Links")
                
                        pdf_links=await web(search_query+" filetype:pdf") 
                        for link in pdf_links:
                          

                             
                            web_box=c1.container(border=True)
                            web_box.write(f"{link['title']}")
                            web_box.write(f"\n\nPDF Link: {link['href']}")
                            
                        doc_links=await web(search_query+" filetype:docx")
                        for link in doc_links:
                            web_box=c2.container(border=True)
                            web_box.write(f"{link['title']}")
                            web_box.write(f"\n\nDOCS Link: {link['href']}")
                        
                        search_videos=AsyncDDGS().videos(search_query, max_results=1)
                        print(search_videos)
                        for link in search_videos:
                            web_box=c3.container(border=True)
                            web_box.write(f"{link['title']}")
                            web_box.write(f"\n\nVIDEO Link: {link['content']}")

                        search_news=AsyncDDGS().news(search_query+" updates", max_results=1)
                        print(search_news)
                        for link in search_news:
                            web_box=c4.container(border=True)
                            web_box.write(f"{link['title']}")
                            web_box.write(f"\n\nNEWS Link: {link['url']}")


                        



                        feedback=st.expander("Please fill this form for feedback and suggestions. It will take less than 3 Minutes")
                        feedback.write("https://docs.google.com/forms/d/e/1FAIpQLSd84yB5htONQ55yPTUbUxG3jxi4FUVd_YeytOptzKF-cq-QXA/viewform?usp=sf_link")
                #<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSd84yB5htONQ55yPTUbUxG3jxi4FUVd_YeytOptzKF-cq-QXA/viewform?embedded=true" width="640" height="1539" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
                        st.toast("⏬ You can Download the report now!")
                        st.download_button("Download PDF",
                            data=PDFbyte,
                            file_name=pdffilename,
                            mime='application/octet-stream')
                    
                
            else:
                    col2_con.error("Enter idea or upload a ppt file to continue . . .")
    else:
        col2_con.error("No email found. Please try again.")           
    
    
# Running the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
