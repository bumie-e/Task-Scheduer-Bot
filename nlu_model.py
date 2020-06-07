from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

#nlp = spacy.load('en_core_web_sm')

def train_taskbot(data_json, config_file, model_dir):
    training_data = load_data(data_json)
    trainer = Trainer(RasaNLUConfig(config_file))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name='taskbot')
    
def predict_intent(text):
    interpreter = Interpreter.load('./models/nlu/default/taskbot', RasaNLUConfig('config.json'))
    print(interpreter.parse(text))
    
if __name__ == '__main__':
    train_taskbot('./data/data.json', 'config.json', './models/nlu')
    predict_intent(u"so, what task do you have for me?")