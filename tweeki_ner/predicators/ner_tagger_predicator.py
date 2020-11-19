

from typing import Tuple
from overrides import overrides

from allennlp.data.fields import TextField,SequenceLabelField
from allennlp.common.util import JsonDict
from allennlp.data import DatasetReader, Instance
from allennlp.data.tokenizers.word_splitter import SpacyWordSplitter
from allennlp.models import Model
from allennlp.service.predictors.predictor import Predictor
from allennlp.data.tokenizers import Token
from allennlp.data.token_indexers import SingleIdTokenIndexer
from allennlp.training.metrics import SpanBasedF1Measure
from allennlp.data.vocabulary import Vocabulary

@Predictor.register('tweeki-ner-tagger')
class SentenceTaggerPredictor(Predictor):
    """
    Predictor for any model that takes in a sentence and returns
    a single set of tags for it.  In particular, it can be used with
    the :class:`~allennlp.models.crf_tagger.CrfTagger` model
    and also
    the :class:`~allennlp.models.simple_tagger.SimpleTagger` model.
    """
    def __init__(self, model: Model, dataset_reader: DatasetReader) -> None:
        super().__init__(model, dataset_reader)
        self._tokenizer = SpacyWordSplitter(language='en_core_web_sm', pos_tags=True)
        self._token_indexers =  {'tokens': SingleIdTokenIndexer()} 
       
    def predict_json(self, sentence: str) -> JsonDict:
        try:
                instance = self._json_to_instance(sentence)
                pred = self.predict_instance(instance)
                return pred	
        except:
            token = sentence["sentence"].split(" ")
            return {"words":token,"tags":sentence["tags"]}

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        """
        Expects JSON that looks like ``{"sentence": "..."}``.
        Runs the underlying model, and adds the ``"words"`` to the output.
        """
        sentence = json_dict["sentence"]
        tags = json_dict["tags"]
        tokens = self._tokenizer.split_words(sentence)
        instance = self._dataset_reader.text_to_instance(tokens,None,None,tags)

        return instance
