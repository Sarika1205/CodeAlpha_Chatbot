import json
import random
import re
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Load intents
# -----------------------------
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

all_patterns = []
pattern_tags = []
pattern_topics = []
responses_map = {}
tag_to_topic = {}

for intent in data["intents"]:
    tag = intent["tag"]
    topic = intent["topic"]
    responses_map[tag] = intent["responses"]
    tag_to_topic[tag] = topic

    for pattern in intent["patterns"]:
        all_patterns.append(pattern)
        pattern_tags.append(tag)
        pattern_topics.append(topic)

# -----------------------------
# Text cleaning
# -----------------------------
def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

cleaned_patterns = [clean_text(pattern) for pattern in all_patterns]

# -----------------------------
# Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
pattern_vectors = vectorizer.fit_transform(cleaned_patterns)

# -----------------------------
# Topic FAQs for safe guidance
# -----------------------------
topic_related_questions = {
    "Internship": [
        "What domains are available for internship?",
        "Will I get internship certificate?",
        "How do I submit project?",
        "Is there any internship fee?"
    ],
    "Company & Services": [
        "Tell me about your company",
        "What services do you offer?"
    ],
    "Support": [
        "How can I contact support?",
        "What are your working hours?",
        "I have an issue"
    ],
    "General": [
        "Hi",
        "Help",
        "Thank you"
    ]
}

generic_fallback = (
    "I’m not fully sure about that yet. I can currently help with internship domains, certificate, project submission, fees, support/contact, working hours and company/services."
)

# -----------------------------
# Similarity helper
# -----------------------------
def fuzzy_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

# -----------------------------
# Main response function
# -----------------------------
def get_bot_response(user_message):
    original_text = user_message.strip()
    user_message = clean_text(user_message)

    if not user_message:
        return {
            "response": "Please type a valid message.",
            "matched_tag": None,
            "matched_topic": None,
            "related_questions": []
        }

    # TF-IDF similarity
    user_vector = vectorizer.transform([user_message])
    similarity_scores = cosine_similarity(user_vector, pattern_vectors)
    best_index = similarity_scores.argmax()
    best_score = float(similarity_scores[0][best_index])

    matched_tag = pattern_tags[best_index]
    matched_topic = pattern_topics[best_index]

    # Fuzzy similarity with best matched pattern
    fuzzy_score = fuzzy_ratio(user_message, cleaned_patterns[best_index])

    # Strong match
    if best_score >= 0.34 or fuzzy_score >= 0.82:
        response = random.choice(responses_map[matched_tag])
        related = topic_related_questions.get(matched_topic, [])
        related = [q for q in related if clean_text(q) != user_message][:3]
        return {
            "response": response,
            "matched_tag": matched_tag,
            "matched_topic": matched_topic,
            "related_questions": related
        }

    # Medium confidence: only answer if topic is clearly relevant and not risky
    if best_score >= 0.20 or fuzzy_score >= 0.68:
        safe_topics = {"Internship", "Company & Services", "Support"}
        if matched_topic in safe_topics:
            response = (
                f"I’m not completely certain, but this seems related to **{matched_topic}**.\n\n"
                f"{random.choice(responses_map[matched_tag])}"
            )
            related = topic_related_questions.get(matched_topic, [])[:3]
            return {
                "response": response,
                "matched_tag": matched_tag,
                "matched_topic": matched_topic,
                "related_questions": related
            }

    # Low confidence → do NOT bluff. Give safe help + related FAQ from nearest topic
    related = topic_related_questions.get(matched_topic, [])[:4]
    response = (
        generic_fallback
        + f"\n\nYour question seems closest to **{matched_topic}**. You can try one of these:"
    )

    return {
        "response": response,
        "matched_tag": None,
        "matched_topic": matched_topic,
        "related_questions": related
    }