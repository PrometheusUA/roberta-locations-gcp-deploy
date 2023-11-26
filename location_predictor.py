import re

from typing import List
from transformers import pipeline

from consants import EMOJI_PATTERN, CITY_VILLAGE_PATTERN, STREET_PATTERN, DELIMETERS, PUNCTUATION, NAME_WORDS

class LocationPredictor:
    """
    Wrapper for Location Prediction NER model.
    """

    def __init__(self, chkp_path: str, device: str, thresh: float = 0.83):
        self.model = pipeline(
            "token-classification", model=chkp_path, aggregation_strategy="simple", batch_size=32, device=device
        )
        self.thresh = thresh

    def _final_string_cleaning(self, text:str) -> str:
        return text.replace('\xa0', ' ').replace('\n', ' ')

    def _clean_text_sentences(self, text):
        """
        Delete sentences with channel name
        """ 
        
        lines = text.split('\n')
                
        while '' in lines:
            lines.remove('')
        while ' ' in lines:
            lines.remove(' ')
        
        # Delete last rows which iclude any of name_words
        while any([name_word in lines[-1].lower() for name_word in NAME_WORDS]) and len(lines[-1]) < 50:
            lines.pop()
        
        return ' '.join(lines)

    def _predict_one(self, text: str) -> List[str]:
        """
        Process one specific text input.

        Args:
            text (List[str]): input text.
        Returns:
            List[str]: list of locations.
        """
        res = []
    
        row_labels = self.model(text)
        for found_info in row_labels:
            if found_info['entity_group'] == 'LOC' and found_info['score'] > self.thresh:
                # Deleting "столиц" where we don't need it
                if re.search(r"район.? столиц.", found_info['word'].lower()):
                    res.append(re.sub('столиц.', '', found_info['word'].lower()))
                    continue
                
                start = found_info['start']
                end = found_info['end']
                # Increasing found words bounds if not full word is returned by the model
                while (start > 0 and text[start - 1] not in DELIMETERS and
                        not EMOJI_PATTERN.match(text[start - 1]) and
                        text[start - 1] not in PUNCTUATION):
                    start -= 1
                while (end < len(text) and text[end] not in DELIMETERS and
                        not EMOJI_PATTERN.match(text[end]) and
                        text[end] not in PUNCTUATION):
                    end += 1
                added = False
                # Increasing found words by specific words meaning it is a street or a city etc 
                # if it is in the text and not in the proposed return
                street_in = STREET_PATTERN.search(text[start:end])
                city_in = CITY_VILLAGE_PATTERN.search(text[start:end])
                if not street_in and not city_in and start > 0:
                    street_before = STREET_PATTERN.search(text[:start])
                    city_before = CITY_VILLAGE_PATTERN.search(text[:start])
                    search_start = 0
                    
                    # Searching for a street word right before ours 
                    while street_before:
                        if start - street_before.end() <= 2:
                            res.append(self._final_string_cleaning(text[street_before.start():end]))
                            added = True
                            break
                        search_start += street_before.end()
                        street_before = STREET_PATTERN.search(text[search_start:start])
                    
                    search_start = 0
                    # Searching for a city word right before ours 
                    while city_before:
                        if start - city_before.end() <= 2:
                            res.append(self._final_string_cleaning(text[city_before.start():end]))
                            added = True
                            break
                        search_start += city_before.end()
                        city_before = CITY_VILLAGE_PATTERN.search(text[search_start:start])
                            
                # If we have found nothing to prepend
                if not added:
                    res.append(self._final_string_cleaning(text[start:end]))
                
        return res

    def predict(self, texts: List[str]) -> List[List[str]]:
        """
        Process texts input.

        Args:
            texts (List[str]): input texts.
        Returns:
            List[List[str]]: list of lists of locations.
        """
        cleaned_texts = [self._clean_text_sentences(text) for text in texts]
        return [self._predict_one(text) for text in cleaned_texts]