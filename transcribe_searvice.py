import os
# Ignore pre-production warnings
import warnings
warnings.filterwarnings('ignore')
import nemo
# Import Speech Recognition collection
import nemo.collections.asr as nemo_asr
# Import Natural Language Processing colleciton
import nemo.collections.nlp as nemo_nlp

# Instantiate pre-trained NeMo models
# Speech Recognition model - QuartzNet
quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5NR-En").cuda()
jasper = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="Jasper10x5Dr-En").cuda()
# Punctuation and capitalization model
punctuation = nemo_nlp.models.PunctuationCapitalizationModel.from_pretrained(model_name='Punctuation_Capitalization_with_DistilBERT').cuda()



def transcribe(file_name):
    # Convert our audio sample to text
    files = [file_name]
    raw_text = ''
    text = ''
    # for fname, transcription in zip(files, quartznet.transcribe(paths2audio_files=files)):
    #     raw_text = transcription
    quartznet_raw = quartznet.transcribe(paths2audio_files=files)[0] 
    jasper_raw = quartznet.transcribe(paths2audio_files=files)[0]
    # Add capitalization and punctuation
    res = punctuation.add_punctuation_capitalization(queries=[quartznet_raw, jasper_raw])
    # text = res[0]
    quartznet_text, jasper_text = res
    # print(f'\nRaw recognized text: {raw_text}. \nText with capitalization and punctuation: {text}')
    print(quartznet_text, jasper_text)
    os.remove(file_name)

    return text 