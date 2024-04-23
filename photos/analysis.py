import pandas as pd
import cv2 
from sklearn.preprocessing import MinMaxScaler
import joblib
import numpy as np



class Analysis : 
    def __init__(self,imagem_path, filename):
        self.imagem_path = cv2.imread(imagem_path)
        self.filename = filename
        
    def __read_imagem(self):
        user_name = []

        plant_dark_std = []

        plant_B_mean = []

        plant_G_mean = []
        plant_G_std = []

        plant_R_mean =[]
        plant_R_std = []

        if self.imagem_path is None:
            raise ValueError('Imagem is None')

        imagem_rgb = cv2.normalize(self.imagem_path,None,0,256,
                    cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        (B, G, R) = cv2.split(self.imagem_path)

        if self.filename == None:
           raise ValueError('Filename is None')

            ## Nome
        user_name.append(self.filename)
        ## Preto e branco
        plant_dark_std.append(np.std(cv2.calcHist(imagem_rgb,[0],None,[256], [0, 256])))

            ## Blue
        plant_B_mean.append(np.mean(cv2.calcHist(B,[0],None,[256], [0, 256])))
            ## Gren
        plant_G_mean.append(np.mean(cv2.calcHist(G,[0],None,[256], [0, 256])))
        plant_G_std.append(np.std(cv2.calcHist(G,[0],None,[256], [0, 256])))

            ## RED
        plant_R_mean.append(np.mean(cv2.calcHist(R,[0],None,[256], [0, 256])))
        plant_R_std.append(np.std(cv2.calcHist(R,[0],None,[256], [0, 256])))

        df = pd.DataFrame()
        df['dark_std'] = plant_dark_std
        df['B_mean'] = plant_B_mean
        df['G_Mean'] = plant_G_mean
        df['G_std'] = plant_G_std
        df['R_mean'] = plant_R_mean
        df['R_std'] = plant_R_std
        return df

    def __trata_df(self,df):
        scaler = MinMaxScaler()

        df_ajuste = scaler.fit_transform(df)
        df_ajuste = pd.DataFrame(df_ajuste,columns=df.columns)
        return df_ajuste


    def __usage_model(self,df):
        loaded_model = joblib.load(self.filename)
        return loaded_model.predict(df)

    def predict(self):
        imagem_todata = self.__read_imagem()
        df_tratado = self.__trata_df(imagem_todata)
        predict = self.__usage_model(df_tratado)
        return predict

