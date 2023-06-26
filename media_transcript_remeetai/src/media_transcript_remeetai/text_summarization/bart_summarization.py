# -*- coding: utf-8 -*-

# from transformers import pipeline, set_seed
# from transformers import AutoTokenizer
# from ..utils import debug
# import re

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

# def bart_sum(filename: str = None, text_base: str = None, max_length: int = 1000):
#     if not filename and not text_base:
#         raise Exception("filename or text must be specified.")
    
#     if filename:
#         with open(filename, "r") as f:
#             text = f.read()
#     else:
#         text = text_base
#     #remove non breaking space 
#     text = text.replace("\xa0", " ")
#     #remove not usefull white space 
#     text = re.sub("\s+", " ", text)
#     # Print the variable
#     debug.print_debug(text)

#     token_ids = tokenizer.encode_plus(text, max_length=max_length, truncation=True)
#     short_text_truncated = tokenizer.decode(token_ids["input_ids"]) # decode
#     short_text_truncated = short_text_truncated[3:-4]

#     #for prototype use this one 
#     summarize_high_beams = summarizer(short_text_truncated, max_length=max_length, min_length=max_length//4, do_sample=False, num_beams=7, num_return_sequences=1)
#     debug.print_debug(summarize_high_beams)
#     # summarize_low_beams = summarizer(short_text_truncated, do_sample=False, num_beams=3, num_return_sequences=2)
#     # debug.print_debug(summarize_low_beams)

#     return summarize_high_beams


from transformers import pipeline, set_seed
from transformers import AutoTokenizer
from ..utils import debug
from deep_translator import GoogleTranslator,single_detection
import re

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
my_translator = GoogleTranslator(source='auto', target='english')

def bart_sum(filename: str = None, text_base: str = None, text_length: int = 0):
    
    param_grid = []
    if text_length == 0:
        param_grid = [120,30]
    elif text_length == 1:
        param_grid = [280,65]
    elif text_length == 2:
        param_grid = [420,140]
    else:
        text_length = [560,210]
        
    if not filename and not text_base:
        raise Exception("filename or text must be specified.")
    
    if filename:
        with open(filename, "r") as f:
            text = f.read()
    else:
        text = text_base
    #remove non breaking space 
    text = text.replace("\xa0", " ")
    #remove not usefull white space 
    text = re.sub("\s+", " ", text)
    # Print the variable
    debug.print_debug(text)

    translated = my_translator.translate(text=text)
    
    if len(tokenizer.encode(translated)) > summarizer.model.config.max_position_embeddings:
        print("Warning: The article length exceeds the maximum. Some information will be lost during the summary creation")
        max_position_embeddings = summarizer.model.config.max_position_embeddings
        max_input_length = tokenizer.model_max_length - 2
        encoded_inputs = tokenizer.encode(translated, max_length=max_input_length, truncation=True, padding="longest")
        if len(encoded_inputs) > max_position_embeddings:
            print("Warning: The article length exceeds the maximum position embeddings. Splitting into smaller chunks.")

            # Split the article into smaller chunks
            chunk_size = max_position_embeddings - 2  # Subtract 2 for the special tokens [CLS] and [SEP]
            chunks = [encoded_inputs[i:i+chunk_size] for i in range(0, len(encoded_inputs), chunk_size)]

            # Generate summaries for each chunk
            summaries = []
            for chunk in chunks:
                # Convert the chunk back to a string
                decoded_chunk = tokenizer.decode(chunk, skip_special_tokens=True)

                # Generate the summary for the chunk
                summary = summarizer(decoded_chunk, max_length=param_grid[0], min_length=param_grid[1], do_sample=False, num_beams=3)
                summaries.append(summary)

            # Combine the summaries from all chunks
            combined_summary = " ".join([s[0]['summary_text'] for s in summaries])
            summary = combined_summary
            print(combined_summary)
        else:
            decoded_inputs = tokenizer.decode(encoded_inputs, skip_special_tokens=True)
            summary = summarizer(decoded_inputs, max_length=param_grid[0], min_length=param_grid[1], do_sample=False, num_beams=3)
            print(summary)
    else:
        summary = summarizer(translated, max_length=param_grid[0], min_length=param_grid[1], do_sample=False, num_beams=3)
        print(summary)

    my_translator.target = 'fr'
    result = my_translator.translate(text=summary[0]["summary_text"])
    return result
