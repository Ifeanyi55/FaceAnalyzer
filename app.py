from deepface import DeepFace
import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt
import tempfile
import os

def faceAnalyzer(image_path):
    def analyze(image_path, attribute):
        analysis = DeepFace.analyze(img_path=image_path, actions=['gender', 'race', 'emotion', 'age'])
        df = pd.DataFrame(analysis[0])
        plot = df[attribute].plot(kind='line', figsize=(9, 5), title=attribute).get_figure()
        _, temp_filename = tempfile.mkstemp(suffix=".png")
        plot.savefig(temp_filename, dpi=600)
        plt.close(plot)
        return temp_filename

    attributes = ['gender', 'race', 'emotion']
    images = [analyze(image_path, attribute) for attribute in attributes]

    return [gr.Image(image) for attribute, image in zip(attributes, images)]


def faceAnalyzer2(image_path, attribute):

  analysis = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race', 'emotion'])
    # convert the resulting dictionary to a DataFrame
  df = pd.DataFrame(analysis[0])

  if attribute == "gender":
    gender = df['gender'].plot(kind = 'line', figsize = (9, 5), title = 'Gender').get_figure()
    return gender

  elif attribute == "race":
    race = df['race'].plot(kind = 'line', figsize = (9, 5), title = 'Race').get_figure()
    return race
  
  elif attribute == "emotion":
    emotion = df['emotion'].plot(kind = 'line', figsize = (9, 5), title = 'Emotion').get_figure()
    return emotion


app1 = gr.Interface(faceAnalyzer,
                   inputs=gr.Image(label="Upload Photo"),
                   outputs=[gr.Image(label="Gender Analysis"),
                            gr.Image(label="Race Analysis"),
                            gr.Image(label="Emotion Analysis")],
                   theme=gr.themes.Soft())

app2 = gr.Interface(faceAnalyzer2,
                    inputs=[gr.Image(label="Upload Photo"),gr.Radio(choices=["gender","race","emotion"],
                                                                    value="gender",
                                                                    label="Attributes",
                                                                    info="Select an attribute")],
                    outputs=gr.Plot(label="Analysis Output"),
                    theme=gr.themes.Soft())

application = gr.TabbedInterface([app1,app2],["Full Analysis","Select Analysis"],theme=gr.themes.Soft())


application.launch()
