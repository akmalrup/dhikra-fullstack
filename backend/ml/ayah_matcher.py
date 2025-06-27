import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.ayah_matcher import find_most_similar_ayah

def match_ayah(sentence: str, top_k: int = 1, surah_filter=None):
    """
    Wrapper function for the existing find_most_similar_ayah function
    to match the API specification.
    
    Args:
        sentence (str): The input sentence/transcription
        top_k (int): Number of matches to return (default 1 for best match)
        surah_filter: Optional surah filter
        
    Returns:
        dict: Best matched ayah with similarity score and metadata
    """
    results = find_most_similar_ayah(sentence, top_k=top_k, surah_filter=surah_filter)
    
    if not results:
        return {
            "matched_ayah": None,
            "similarity_score": 0.0,
            "surah": None,
            "ayah": None,
            "arabic_text": "",
            "english_text": ""
        }
    
    # Return the best match (first result)
    best_match = results[0]
    
    # Convert NumPy types to Python native types for JSON serialization
    similarity_score = float(best_match["similarity"])
    surah = int(best_match["surah"])
    ayah = int(best_match["ayah"])
    
    return {
        "matched_ayah": f"{surah}:{ayah}",
        "similarity_score": similarity_score,
        "surah": surah,
        "ayah": ayah, 
        "arabic_text": best_match.get("arabic_text", ""),
        "english_text": best_match.get("english_text", "")
    } 