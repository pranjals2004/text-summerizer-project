import json
import requests
import re
from textsummarizer.logging import logger

DEMO_ARTICLES = {
    "tech": {
        "title": "AI Evolution: Quantum-Neural System Breaks Turing Threshold in Logical Reasoning",
        "text": (
            "A consortium of researchers from MIT and Google DeepMind has announced a breakthrough in artificial intelligence. "
            "They developed a 'Quantum-Neural' hybrid network that successfully passed a new suite of complex logical reasoning tests, "
            "dubbed the 'Turing Threshold'. Unlike traditional large language models which rely on statistical pattern matching, "
            "this hybrid architecture uses quantum-inspired bits to solve abstract mathematical proofs and multi-step logic problems "
            "with 99.8% accuracy. Dr. Helena Vance, leading the research at MIT, stated that this marks the transition from simple semantic "
            "prediction to genuine cognitive reasoning. The research team plans to open-source the model weights next month for academic "
            "collaborators. Tech giants have already expressed interest, with Microsoft reportedly bidding for an exclusive commercial license."
        ),
        "analysis": {
            "summary": "Researchers from MIT and Google DeepMind have developed a 'Quantum-Neural' hybrid network that breaks through traditional AI reasoning limits. The model achieves 99.8% accuracy on complex logic and math proofs, shifting AI from pattern matching to genuine cognitive reasoning. The team plans to open-source the weights for academic use, while major tech companies are already competing for commercial licenses.",
            "sentiment": {
                "label": "Positive",
                "score": 92,
                "emotions": {"Joy": 60, "Trust": 30, "Fear": 5, "Anger": 0, "Sadness": 5},
                "explanation": "The text displays high optimism and excitement regarding a monumental scientific breakthrough, offset slightly by potential commercial bidding wars."
            },
            "entities": [
                {"name": "MIT", "type": "Organization", "relevance": "Academic research institute co-developing the technology."},
                {"name": "Google DeepMind", "type": "Organization", "relevance": "Collaborator and industry leader in AI research."},
                {"name": "Dr. Helena Vance", "type": "Person", "relevance": "Lead researcher at MIT directing the project."},
                {"name": "Microsoft", "type": "Organization", "relevance": "Tech giant bidding for commercial licensing rights."},
                {"name": "Quantum-Neural System", "type": "Technology", "relevance": "The novel hybrid AI architecture developed."}
            ]
        },
        "qa": {
            "who lead": "The research was led by Dr. Helena Vance at MIT.",
            "accuracy": "The system solved abstract mathematical proofs and logic problems with 99.8% accuracy.",
            "open source": "Yes, the research team plans to open-source the model weights next month for academic collaborators.",
            "who bidding": "Microsoft is reportedly bidding for an exclusive commercial license.",
            "what is the name of the system": "It is called the 'Quantum-Neural' hybrid network/system."
        }
    },
    "space": {
        "title": "NASA's Lunar Explorer Confirms Vast Subsurface Water Ice on Moon's South Pole",
        "text": (
            "NASA's VIPER lunar explorer has successfully mapped a massive underground deposit of water ice in the Shackleton Crater "
            "at the Moon's South Pole. Data transmitted from the rover indicates the ice sheet is located just 1.5 meters beneath the surface "
            "and spans over 150 square kilometers. The discovery is a major triumph for the Artemis Program, which aims to establish a "
            "sustainable human presence on the Moon. Project Director Marcus Thorne confirmed that this ice can be harvested to produce "
            "drinking water, breathable oxygen, and liquid hydrogen rocket fuel. This eliminates the need to transport water from Earth, "
            "slashing mission costs by billions. However, international space agencies are already raising concerns about lunar resource rights "
            "under the Outer Space Treaty, prompting calls for an urgent diplomatic summit."
        ),
        "analysis": {
            "summary": "NASA's VIPER rover has mapped a huge subsurface water ice deposit (150 sq km) near the Moon's South Pole. This discovery is a major milestone for the Artemis Program, as the ice can supply astronauts with water, oxygen, and rocket fuel, drastically lowering lunar base operations costs. While a massive success, the discovery has triggered debate over resource rights, prompting diplomatic tension.",
            "sentiment": {
                "label": "Positive",
                "score": 78,
                "emotions": {"Joy": 50, "Trust": 25, "Fear": 10, "Anger": 5, "Sadness": 10},
                "explanation": "Strong positive tone regarding the scientific discovery and its capability to slash mission costs, balanced by geopolitical concern over lunar territory rights."
            },
            "entities": [
                {"name": "NASA", "type": "Organization", "relevance": "The US space agency conducting the VIPER rover mission."},
                {"name": "VIPER", "type": "Technology", "relevance": "The lunar explorer rover that mapped the subsurface water ice."},
                {"name": "Shackleton Crater", "type": "Location", "relevance": "The location on the Moon's South Pole containing the ice deposit."},
                {"name": "Artemis Program", "type": "Organization", "relevance": "NASA's program to return humans to the Moon and establish bases."},
                {"name": "Marcus Thorne", "type": "Person", "relevance": "Project Director who confirmed the extraction and utility of the ice."}
            ]
        },
        "qa": {
            "what rover": "NASA's VIPER lunar explorer made the discovery.",
            "where ice": "The water ice was found in the Shackleton Crater at the Moon's South Pole, 1.5 meters beneath the surface.",
            "how big": "The underground ice deposit spans over 150 square kilometers.",
            "uses of ice": "The ice can be harvested to produce drinking water, breathable oxygen, and liquid hydrogen rocket fuel.",
            "concerns": "International space agencies are raising concerns about lunar resource rights under the Outer Space Treaty, calling for a diplomatic summit."
        }
    },
    "business": {
        "title": "Global Renewable Energy Production Overtakes Coal for First Time in History",
        "text": (
            "In a historic milestone for the global climate transition, renewable energy sources—primarily solar, wind, and hydro—generated "
            "more electricity than coal globally in the last fiscal year. According to the International Energy Agency (IEA) annual report, "
            "renewables accounted for 31.5% of total power generation, compared to coal's 30.2%. This transition was accelerated by massive "
            "solar installations in China, a wind surge in Europe, and tax incentives in the United States. IEA Director Fatih Birol called it "
            "an irreversible turning point for the power sector. Despite the positive news, energy analysts warn that grid infrastructure is "
            "strugg Struggling to keep pace with this green surge, leading to frequent curtailment where clean power is wasted because transmission lines "
            "cannot support the load. Furthermore, coal-dependent communities are facing severe job losses, sparking protests in several regions."
        ),
        "analysis": {
            "summary": "For the first time ever, renewable energy surpassed coal in global electricity generation, accounting for 31.5% of the power sector. The shift was driven by major solar expansions in China, wind growth in Europe, and US subsidies. Despite this climate milestone, analysts warn of major grid congestion causing clean energy waste, and rising social protests in coal-mining regions due to job losses.",
            "sentiment": {
                "label": "Neutral",
                "score": 55,
                "emotions": {"Joy": 35, "Trust": 20, "Fear": 20, "Anger": 15, "Sadness": 10},
                "explanation": "A monumental environmental victory is heavily balanced by structural grid failures and critical economic hardships/protests in coal-dependent communities."
            },
            "entities": [
                {"name": "International Energy Agency", "type": "Organization", "relevance": "Global energy watchdog that published the annual power report."},
                {"name": "IEA", "type": "Organization", "relevance": "Abbreviation for the International Energy Agency."},
                {"name": "Fatih Birol", "type": "Person", "relevance": "IEA Director who characterized the shift as an irreversible turning point."},
                {"name": "China", "type": "Location", "relevance": "Country leading major solar capacity installations."},
                {"name": "Europe", "type": "Location", "relevance": "Region experiencing a major wind energy surge."}
            ]
        },
        "qa": {
            "what percentage": "Renewables generated 31.5% of total electricity, while coal generated 30.2%.",
            "who published": "The report was published by the International Energy Agency (IEA).",
            "what problems": "The main problems are that grid infrastructure is struggling to keep pace, leading to clean power waste (curtailment), and coal-dependent communities are experiencing job losses.",
            "what driven by": "The transition was driven by solar installations in China, wind power in Europe, and tax incentives in the United States."
        }
    },
    "science": {
        "title": "Deep-Ocean Expedition Discovers 50 New Species Near Mariana Trench",
        "text": (
            "A research expedition led by the Schmidt Ocean Institute has returned from a 30-day mission near the Mariana Trench with "
            "findings that have shocked the scientific community. Utilizing the robotic underwater vehicle 'SuBastian', scientists mapped "
            "previously unexplored hydrothermal vent fields and discovered at least 50 new marine species. Among the discoveries is a glowing "
            "bioluminescent jellyfish with fractal-like tentacles and an unusual species of 'ghost crab' that feeds on sulfur-eating bacteria. "
            "Dr. Jyotika Virmani, the expedition's chief scientist, stated that these findings reveal how little we understand about deep-ocean "
            "ecosystems. However, researchers noted with alarm that microplastic fibers were recovered in water samples taken at depths of "
            "8,000 meters. This discovery proves that human pollution has penetrated even the deepest and most remote ecosystems on the planet."
        ),
        "analysis": {
            "summary": "A 30-day Schmidt Ocean Institute expedition near the Mariana Trench using the ROV SuBastian has discovered 50 new marine species, including a bioluminescent jellyfish and a new 'ghost crab'. While showcasing rich and unexplored deep-sea biodiversity, the expedition also found microplastics at 8,000 meters, highlighting the alarming spread of human pollution into Earth's deepest trenches.",
            "sentiment": {
                "label": "Neutral",
                "score": 52,
                "emotions": {"Joy": 40, "Trust": 20, "Fear": 20, "Anger": 15, "Sadness": 5},
                "explanation": "Excitement and wonder over discovering 50 new deep-sea species is immediately shadowed by the discovery of microplastics in Earth's most pristine depths."
            },
            "entities": [
                {"name": "Schmidt Ocean Institute", "type": "Organization", "relevance": "The scientific organization that funded and led the deep-sea expedition."},
                {"name": "Mariana Trench", "type": "Location", "relevance": "The location of the underwater expedition, the deepest trench on Earth."},
                {"name": "SuBastian", "type": "Technology", "relevance": "The advanced robotic underwater vehicle used to map and capture deep-sea specimens."},
                {"name": "Dr. Jyotika Virmani", "type": "Person", "relevance": "The chief scientist leading the expedition and analyzing biological samples."}
            ]
        },
        "qa": {
            "how many species": "Scientists discovered at least 50 new marine species.",
            "what vehicle": "They used the robotic underwater vehicle named 'SuBastian'.",
            "jellyfish description": "The jellyfish is glowing, bioluminescent, and has fractal-like tentacles.",
            "concerning discovery": "They recovered microplastic fibers in water samples taken at extreme depths of 8,000 meters, indicating human pollution has reached the deep ocean."
        }
    }
}

POSITIVE_WORDS = {"breakthrough", "success", "triumph", "discover", "increase", "growth", "positive", "win", "good", "great", "excellent", "advanced", "innovative", "power", "clean", "sustainable", "support", "benefit", "boost", "improve", "save"}
NEGATIVE_WORDS = {"struggle", "loss", "waste", "protest", "alarm", "pollution", "fear", "anger", "sadness", "difficult", "problem", "threat", "danger", "crisis", "fail", "drop", "decline", "protest", "hazard", "concern", "damage", "harm"}

def local_sentiment_analysis(text):
    text_lower = text.lower()
    pos_count = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg_count = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    
    total = pos_count + neg_count
    if total == 0:
        label = "Neutral"
        score = 50
        emotions = {"Joy": 20, "Trust": 30, "Fear": 20, "Anger": 10, "Sadness": 20}
    elif pos_count > neg_count:
        label = "Positive"
        diff = pos_count - neg_count
        score = min(95, 50 + int((diff / pos_count) * 45))
        emotions = {
            "Joy": int(score * 0.6),
            "Trust": int(score * 0.3),
            "Fear": int((100 - score) * 0.5),
            "Anger": 0,
            "Sadness": 100 - int(score * 0.6) - int(score * 0.3) - int((100 - score) * 0.5)
        }
    else:
        label = "Negative"
        diff = neg_count - pos_count
        score = min(95, 50 + int((diff / neg_count) * 45))
        emotions = {
            "Joy": 0,
            "Trust": 10,
            "Fear": int(score * 0.4),
            "Anger": int(score * 0.3),
            "Sadness": 100 - 10 - int(score * 0.4) - int(score * 0.3)
        }
        
    return {
        "label": label,
        "score": score,
        "emotions": emotions,
        "explanation": f"Calculated using local NLP heuristic matching. Found {pos_count} positive triggers and {neg_count} negative triggers."
    }

def local_entity_extraction(text):
    candidates = re.findall(r'\b[A-Z][a-zA-Z\-\.]+(?:\s+[A-Z][a-zA-Z\-\.]+)*\b', text)
    ignored = {"A", "The", "In", "On", "It", "They", "He", "She", "We", "This", "Moreover", "However", "Consequently", "Therefore", "Furthermore", "Although", "But", "And", "NASA", "MIT", "IEA"}
    
    unique_candidates = list(set([c for c in candidates if c not in ignored]))
    
    entities = []
    for name in unique_candidates[:8]:
        name_lower = name.lower()
        if "institute" in name_lower or "agency" in name_lower or "association" in name_lower or "corp" in name_lower or "inc" in name_lower or "co." in name_lower or "company" in name_lower:
            etype = "Organization"
        elif "dr." in name_lower or "prof." in name_lower or len(name.split()) == 2:
            etype = "Person"
        elif "ocean" in name_lower or "trench" in name_lower or "crater" in name_lower or "pole" in name_lower or "china" in name_lower or "europe" in name_lower:
            etype = "Location"
        else:
            etype = "Technology" if len(name) > 3 else "Organization"
            
        entities.append({
            "name": name,
            "type": etype,
            "relevance": "Extracted via local NLP capitalization pattern matching."
        })
    return entities

def local_qa_search(text, question):
    question_lower = question.lower()
    q_words = [w.lower() for w in re.findall(r'\w+', question) if len(w) > 3]
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    best_sent = ""
    max_matches = 0
    
    for sent in sentences:
        matches = sum(1 for qw in q_words if qw in sent.lower())
        if matches > max_matches:
            max_matches = matches
            best_sent = sent
            
    if best_sent and max_matches > 0:
        return f"Based on local document search: \"{best_sent.strip()}\""
    else:
        return "I could not find a clear match in the article text for your question. To get deep semantic answers, please add a Gemini API Key in the settings."

def analyze_article_with_gemini(text, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = (
        "You are an expert NLP and news analysis assistant. Analyze the following news article text. "
        "Provide your analysis STRICTLY in JSON format. Do not write any markdown wrappers (like ```json) in your response, return a raw JSON string only. "
        "The JSON object must contain exactly three keys:\n"
        "1. \"summary\": A concise summary of the article (3 to 4 sentences).\n"
        "2. \"sentiment\": An object containing:\n"
        "   - \"label\": must be exactly \"Positive\", \"Negative\", or \"Neutral\".\n"
        "   - \"score\": an integer between 0 and 100 representing confidence or intensity.\n"
        "   - \"emotions\": an object with keys \"Joy\", \"Trust\", \"Fear\", \"Anger\", \"Sadness\", where values are integers that sum to 100 representing the emotional distribution.\n"
        "   - \"explanation\": a brief sentence explaining why the sentiment label was assigned.\n"
        "3. \"entities\": An array of objects, up to 6 entities, each having:\n"
        "   - \"name\": Name of the entity.\n"
        "   - \"type\": Must be one of \"Organization\", \"Person\", \"Location\", \"Date\", or \"Technology\".\n"
        "   - \"relevance\": A short sentence describing why this entity is relevant in the context of this article.\n\n"
        f"Article Text:\n{text}"
    )
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        res_json = response.json()
        
        output_text = res_json['candidates'][0]['content']['parts'][0]['text']
        if "```json" in output_text:
            output_text = re.sub(r'```json\s*|\s*```', '', output_text)
        elif "```" in output_text:
            output_text = re.sub(r'```\s*|\s*```', '', output_text)
            
        data = json.loads(output_text.strip())
        return data
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        return {
            "error": True,
            "message": str(e),
            "summary": "Failed to analyze with Gemini API. Fallback extractive summary will be loaded.",
            "sentiment": local_sentiment_analysis(text),
            "entities": local_entity_extraction(text)
        }

def answer_question_with_gemini(text, question, chat_history, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    history_context = ""
    if chat_history:
        history_context = "Previous conversation history:\n"
        for msg in chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_context += f"{role}: {msg['content']}\n"
        history_context += "\n"
        
    prompt = (
        "You are an interactive QA assistant. Answer the user's question based strictly on the provided news article.\n"
        "Keep your answer concise (2-3 sentences), professional, and easy to read. "
        "If the answer cannot be found in the article, state that clearly but try to offer whatever helpful context you can from the text.\n\n"
        f"Article Context:\n{text}\n\n"
        f"{history_context}"
        f"User Question: {question}\n\n"
        "Your Answer:"
    )
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        response.raise_for_status()
        res_json = response.json()
        output_text = res_json['candidates'][0]['content']['parts'][0]['text']
        return {"answer": output_text.strip()}
    except Exception as e:
        logger.error(f"Gemini Q&A API Error: {e}")
        return {"answer": f"Error communicating with Gemini: {str(e)}. Fallback search: " + local_qa_search(text, question)}
