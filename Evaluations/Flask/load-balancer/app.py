import traceback
from flask import Flask, request

class ML:
    def __init__(self):
        self.avaliable_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }

        self.loaded_models_limit = 2
        self.loaded_models = {
            model: self.load_weights(model)
            for model in list(self.avaliable_models)[:self.loaded_models_limit]
        }

        self.model_request_count = {
            model : 0 for model in self.loaded_models
        }

    def load_weights(self, model):
        return self.avaliable_models.get(model,None)

    def load_balancer(self, new_model):
        print(self.loaded_models)

        least_used_model = min(self.model_request_count, key=self.model_request_count.get)
        del self.loaded_models[least_used_model]

        self.loaded_models[new_model]=self.load_weights(new_model)
        self.model_request_count[new_model]=0
        del self.model_request_count[least_used_model]

        print(self.loaded_models)
        # your code here

app = Flask(__name__)
ml = ML()

@app.route('/get_loaded_models', methods=['GET', 'POST'])

def get_loaded_models():
    return ml.loaded_models

@app.route('/process_request', methods=['GET', 'POST'])

def process_request():
    try:
        model = request.form["model"]
        if model not in ml.loaded_models:
            ml.load_balancer(model)         #if model not loaded then call a load balancer
        else:
            ml.model_request_count[model] += 1  # Increment the request count for the model
        
        return "processed by "+ ml.loaded_models[model]
    except:
        return str(traceback.format_exc())

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)