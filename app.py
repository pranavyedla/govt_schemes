from flask import Flask, request, jsonify, render_template 
import os
import google.generativeai as genai 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.form.get("prompt") or request.json.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing 'prompt' in request"}), 400
    
    reply = get_responses(prompt, schemes)
    reply = format_reply(reply) 
    if request.form: 
        return render_template("index.html", reply=reply)

    return jsonify({"reply": reply})


schemes = [
    "Pradhan Mantri Jan Dhan Yojana (PMJDY)",
    "Pradhan Mantri Swasthya Suraksha Yojana (PMSSY)",
    "Pradhan Mantri Mudra Yojana (PMMY)",
    "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
    "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
    "Atal Pension Yojana (APY)",
    "Kisan Vikas Patra (KVP)",
    "Gold Monetisation Scheme (GMS)",
    "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
    "Pradhan Mantri Krishi Sinchai Yojana (PMKSY)",
    "Deen Dayal Upadhyaya Gram Jyoti Yojana (DDUGJY)",
    "Rashtriya Gokul Mission (RGM)",
    "Digital India",
    "Skill India",
    "Pradhan Mantri Kaushal Vikas Yojana (PMKVY)",
    "Make in India",
    "Startup India",
    "Stand-Up India",
    "Beti Bachao Beti Padhao",
    "Swachh Bharat Abhiyan",
    "Ayushman Bharat Yojana",
    "Ujjwala Yojana",
    "Saubhagya Scheme",
    "Smart Cities Mission",
    "National Health Mission (NHM)",
    "National Digital Health Mission",
    "National Solar Mission",
    "Unnat Jyoti by Affordable LEDs for All (UJALA)",
    "AMRUT (Atal Mission for Rejuvenation and Urban Transformation)",
    "National Rural Employment Guarantee Act (MGNREGA)",
    "PM Awas Yojana (PMAY)",
    "National Pension Scheme (NPS)",
    "PM Garib Kalyan Anna Yojana (PMGKAY)"
]

additional_schemes = [
    "Bharatmala Pariyojna",
    "National Social Assistance Programme (NSAP)",
    "Pradhan Mantri Matritva Vandana Yojana (PMMVY)",
    "Deen Dayal Upadhyaya Antyodaya Yojana (DAY)",
    "Pradhan Mantri Adarsh Gram Yojana (PMAGY)",
    "Antyodaya Anna Yojana (AAY)",
    "ASPIRE (A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship)",
    "MUDRA Bank (Micro Units Development and Refinance Agency Bank)",
    "Multiplier Grants Scheme (MGS)",
    "Swamitva Yojana",
    "National Rural Health Mission (NRHM)",
    "National Urban Health Mission (NUHM)",
    "Integrated Child Development Services (ICDS)",
    "Rashtriya Madhyamik Shiksha Abhiyan (RMSA)",
    "Sarva Shiksha Abhiyan (SSA)",
    "National Literacy Mission Programme",
    "Mid-Day Meal Scheme",
    "National Programme for Health Care of the Elderly (NPHCE)",
    "Rashtriya Swasthya Bima Yojana (RSBY)",
    "National Rural Drinking Water Programme (NRDWP)",
    "Namami Gange Programme",
    "Heritage City Development and Augmentation Yojana (HRIDAY)",
    "Shyama Prasad Mukherji Rurban Mission",
    "National Handloom Development Programme (NHDP)",
    "Solar Energy Corporation of India (SECI)",
    "National Electric Mobility Mission Plan (NEMMP)",
    "Faster Adoption and Manufacturing of Hybrid and Electric Vehicles (FAME)",
    "National Adaptation Fund for Climate Change (NAFCC)",
    "Soil Health Card Scheme",
    "Paramparagat Krishi Vikas Yojana (PKVY)",
    "National Agroforestry Policy",
    "Rashtriya Pashudhan Vikas Yojana",
    "National Livestock Mission",
    "Dairy Entrepreneurship Development Scheme (DEDS)",
    "National Programme for Organic Production (NPOP)",
    "National Mission for Sustainable Agriculture (NMSA)",
    "National Mission on Oilseeds and Oil Palm (NMOOP)",
    "National Food Security Mission (NFSM)",
    "National Horticulture Mission (NHM)",
    "National Mission on Agricultural Extension and Technology (NMAET)",
    "National Mission on Micro Irrigation (NMMI)",
    "Pradhan Mantri Gram Sadak Yojana (PMGSY)",
    "Rural Infrastructure Development Fund (RIDF)",
    "Sansad Adarsh Gram Yojana (SAGY)",
    "National Rural Livelihood Mission (NRLM)",
    "National Urban Livelihoods Mission (NULM)",
    "Pradhan Mantri Rojgar Protsahan Yojana (PMRPY)",
    "National Career Service (NCS)",
    "Pradhan Mantri Yuva Yojana (PMYY)",
    "Standup India Scheme",
    "National Apprenticeship Promotion Scheme (NAPS)",
    "Udaan Scheme",
    "Rashtriya Uchchatar Shiksha Abhiyan (RUSA)",
    "Unnat Bharat Abhiyan",
    "Global Initiative of Academic Networks (GIAN)",
    "Impacting Research Innovation and Technology (IMPRINT)",
    "Smart India Hackathon",
    "National Digital Library of India (NDLI)",
    "National Academic Depository (NAD)",
    "Study Webs of Active Learning for Young Aspiring Minds (SWAYAM)",
    "National Institutional Ranking Framework (NIRF)",
    "Pradhan Mantri Vidya Lakshmi Karyakram",
    "National Programme on Technology Enhanced Learning (NPTEL)",
    "Self-Employed Women's Association (SEWA)",
    "Support to Training and Employment Programme for Women (STEP)",
    "Mahila E-Haat",
    "Working Women Hostel Scheme",
    "One Stop Centre Scheme",
    "Swadhar Greh Scheme",
    "Ujjawala Scheme",
    "Nari Shakti Puraskar",
    "Rashtriya Mahila Kosh (RMK)",
    "Sukanya Samriddhi Yojana",
    "Pradhan Mantri Mahila Shakti Kendra (PMMSK)",
    "National Creche Scheme",
    "Beti Bachao Beti Padhao Scheme",
    "Pradhan Mantri Matru Vandana Yojana (PMMVY)",
    "Indira Gandhi Matritva Sahyog Yojana (IGMSY)",
    "Janani Suraksha Yojana (JSY)",
    "Rashtriya Kishor Swasthya Karyakram (RKSK)",
    "Kishori Shakti Yojana (KSY)",
    "Rajiv Gandhi Scheme for Empowerment of Adolescent Girls (RGSEAG) - Sabla",
    "Integrated Child Protection Scheme (ICPS)",
    "National Child Labour Project (NCLP)",
    "Balika Samriddhi Yojana",
    "Integrated Programme for Street Children",
    "Childline India Foundation",
    "National Policy for Children",
    "National Plan of Action for Children",
    "Operation Smile",
    "Operation Muskaan",
    "PENCIL Portal",
    "Mid Day Meal Scheme",
    "Sarva Shiksha Abhiyan",
    "Rashtriya Madhyamik Shiksha Abhiyan",
    "Saakshar Bharat Programme",
    "Padhe Bharat Badhe Bharat",
    "Unnat Jyoti by Affordable LEDs for All (UJALA)",
    "Street Lighting National Programme (SLNP)",
    "National Biogas and Manure Management Programme (NBMMP)",
    "Off-Grid Solar PV Programme",
    "Solar Parks Scheme",
    "Development of Solar Cities Programme",
    "Wind Resource Assessment Programme",
    "Small Hydro Power Programme",
    "National Electric Mobility Mission Plan (NEMMP)",
    "Faster Adoption and Manufacturing of Hybrid and Electric Vehicles (FAME)",
    "National Adaptation Fund for Climate Change (NAFCC)",
    "State Action Plan on Climate Change (SAPCC)",
    "National Action Plan on Climate Change (NAPCC)",
    "Perform Achieve and Trade (PAT) Scheme",
    "Renewable Energy Development Programme",
    "National Bio-Energy Mission",
    "National Offshore Wind Energy Policy",
    "National Policy on Biofuels",
    "National Electric Mobility Mission Plan (NEMMP)",
    "Faster Adoption and Manufacturing of Hybrid and Electric Vehicles (FAME)",
    "National Adaptation Fund for Climate Change (NAFCC)",
    "State Action Plan on Climate Change (SAPCC)",
    "National Action Plan on Climate Change (NAPCC)",
    "Perform Achieve and Trade (PAT) Scheme",
    "Renewable Energy Development Programme",
    "National Bio-Energy Mission",
    "National Offshore Wind Energy Policy",
    "National Policy on Biofuels",
    "National Electric Mobility Mission Plan (NEMMP)",
    "Faster Adoption and Manufacturing of Hybrid and Electric Vehicles (FAME)",
    "National Adaptation Fund for Climate Change (NAFCC)"
]

schemes = schemes + additional_schemes 
api_key = os.getenv("api_key") 
genai.configure(api_key=api_key) 
chat_history = [] 

def get_responses(prompt, data):
    # Add past history into the conversation
    history_text = ""
    for idx, (old_prompt, old_response) in enumerate(chat_history, 1):
        history_text += f"\n[Query {idx}]: {old_prompt}\n[Response {idx}]: {old_response}\n"
    

    formatted_prompt = f"""
You are an assistant that reads a list of Indian government schemes and answers user queries.
- Response must be short yet informative.
- Provide the information in point format(1,2,3...) without using bold formatting. (only if he ask any query).
- If prompt needs external sources, ask them to look in 'Scheme Portal'.
- At the end, ask if they have any further queries.

Below is the conversation history followed by the current user query.
{history_text}

User's Prompt: {prompt}
Data: {data}
""" 
    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(formatted_prompt)
        reply_text = response.text if response and hasattr(response, "text") else "Sorry, I couldn't find relevant information."

        # Save current query + response into history
        chat_history.append((prompt, reply_text))
        return reply_text

    except Exception as e:
        return f" Unable to fetch explanation: {str(e)}"

def format_reply(text): 
    import re
    
    for scheme in schemes:
        # Use re.sub to replace the scheme text with bold tags
        text = re.sub(rf"({re.escape(scheme)})", r"<b>\1</b>", text)
        
    # Add additional formatting or customizations if necessary
    text = f"<div class='response-container'>{text}</div>"
    return text


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
