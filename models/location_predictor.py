import re

from typing import List, Dict
from optimum.pipelines import pipeline

from models.consants import EMOJI_PATTERN, CITY_VILLAGE_PATTERN, STREET_PATTERN, DELIMETERS, PUNCTUATION, NAME_WORDS

class LocationPredictor:
    """
    Wrapper for Location Prediction NER model.
    """

    def __init__(self, chkp_path: str, device: str, thresh: float = 0.83):
        self.model = pipeline(
            "token-classification", model=chkp_path, aggregation_strategy="simple", batch_size=32, device=device,
            accelerator="ort"
        )
        self.thresh = thresh

    @staticmethod
    def _final_string_cleaning(text: str) -> str:
        """
        Delete some unneccessary separators.
        """
        return text.replace('\xa0', ' ').replace('\n', ' ')

    @staticmethod
    def _clean_text_sentences(text: str) -> str:
        """
        Delete sentences with channel name.
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

    # TODO: refactor this one into many separate functions, maybe in the separate class
    def _postprocess_one(self, text:str, row_labels: List[Dict]) -> List[str]:
        """
        Process one specific text input.

        Args:
            text (str): input text.
            row_labels (List[Dict]): the results of the model prediction.
        Returns:
            List[str]: list of locations.
        """
        res = []
    
        # row_labels = self.model(text)
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
                            res.append(LocationPredictor._final_string_cleaning(text[street_before.start():end]))
                            added = True
                            break
                        search_start += street_before.end()
                        street_before = STREET_PATTERN.search(text[search_start:start])
                    
                    search_start = 0
                    # Searching for a city word right before ours 
                    while city_before:
                        if start - city_before.end() <= 2:
                            res.append(LocationPredictor._final_string_cleaning(text[city_before.start():end]))
                            added = True
                            break
                        search_start += city_before.end()
                        city_before = CITY_VILLAGE_PATTERN.search(text[search_start:start])
                            
                # If we have found nothing to prepend
                if not added:
                    res.append(LocationPredictor._final_string_cleaning(text[start:end]))
                
        return res

    def predict(self, texts: List[str]) -> List[List[str]]:
        """
        Process texts input.

        Args:
            texts (List[str]): input texts.
        Returns:
            List[List[str]]: list of lists of locations.
        """
        cleaned_texts = [LocationPredictor._clean_text_sentences(text) for text in texts]
        labels = self.model(cleaned_texts) # Actual prediction
        return [self._postprocess_one(text, row_label) for text, row_label in zip(cleaned_texts, labels)]