# model/predictor.py
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from collections import Counter

class BacBoPredictor:
    def __init__(self):
        self.model = self.build_model()
        self.label_encoder = LabelEncoder()
        self.onehot_encoder = OneHotEncoder(sparse=False)

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(10, 1)),
            tf.keras.layers.LSTM(64),
            tf.keras.layers.Dense(3, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def preprocess_data(self, df):
        # Normalizar y limpiar resultados
        df["Resultado"] = df["Resultado"].str.strip().str.capitalize()
        df["Resultado"] = df["Resultado"].replace({r"Tie \d+x": "Tie"}, regex=True)

        df = df[df["Resultado"].isin(["Player", "Banker", "Tie"])]

        print("Valores únicos después de limpieza:", df["Resultado"].unique())
        print("Conteo por clase:", df["Resultado"].value_counts())

        labels = self.label_encoder.fit_transform(df["Resultado"])
        label_counts = Counter(labels)

        if len(label_counts) < 3:
            raise ValueError("El conjunto de datos contiene menos de 3 clases únicas (Player, Banker, Tie).")

        for clase, count in label_counts.items():
            if count < 5:
                print(f"⚠️ Advertencia: La clase '{self.label_encoder.inverse_transform([clase])[0]}' tiene solo {count} ejemplos. El modelo puede ser inestable.")

        X, y = [], []
        for i in range(len(labels) - 10):
            X_seq = labels[i:i+10]
            y_label = labels[i+10]
            X.append(X_seq)
            y.append(y_label)

        X = np.array(X).reshape(-1, 10, 1)
        y = self.onehot_encoder.fit_transform(np.array(y).reshape(-1, 1))

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train, y_train, X_val, y_val):
        self.model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20)

    def predict_next(self, last_10_results):
        labels = self.label_encoder.transform(last_10_results)
        X_input = np.array(labels).reshape(1, 10, 1)
        pred = self.model.predict(X_input)
        index = np.argmax(pred)
        return self.label_encoder.inverse_transform([index])[0]

if __name__ == "__main__":
    import os
    csv_path = os.path.join(os.path.dirname(__file__), "../data/bacbo_data.csv")
    df = pd.read_csv(csv_path)

    try:
        predictor = BacBoPredictor()
        X_train, X_val, y_train, y_val = predictor.preprocess_data(df)
        predictor.train(X_train, y_train, X_val, y_val)

        df["Resultado"] = df["Resultado"].str.strip().str.capitalize()
        df["Resultado"] = df["Resultado"].replace({r"Tie \d+x": "Tie"}, regex=True)
        ultimos = df[df["Resultado"].isin(["Player", "Banker", "Tie"])]
        ultimos = ultimos["Resultado"].tolist()[-10:]
        if len(ultimos) == 10:
            pred = predictor.predict_next(ultimos)
            print("Predicción para la próxima ronda:", pred)
        else:
            print("No hay suficientes resultados válidos para predecir.")

    except ValueError as ve:
        print("Error durante el preprocesamiento:", ve)