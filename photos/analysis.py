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
        black_std =[]
        rgb_std = []
        b_mean = []
        b_std = []
        g_mean = []
        g_std = []

        if self.imagem_path is None:
          raise ValueError('Imagem is None')

        

        imagem_black = cv2.cvtColor(self.imagem_path, cv2.COLOR_BGR2GRAY)

        imagem_rgb = cv2.normalize(self.imagem_path,None,0,256,
                            cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        imagem_cortada = imagem_rgb[int(len(imagem_rgb)/2)-300:int((len(imagem_rgb)/2)+600),int(len(imagem_rgb[0])/2)-300:int((len(imagem_rgb[0])/2)+500)]
        imagem_cortada_black = imagem_black[int(len(imagem_black)/2)-300:int((len(imagem_black)/2)+600),int(len(imagem_black[0])/2)-300:int((len(imagem_black[0])/2)+500)]

        (B, G, R) = cv2.split(imagem_cortada)

        if self.filename == None:
           raise ValueError('Filename is None')

        black_std =[]
        rgb_std = []
        b_mean = []
        b_std = []
        g_mean = []
        g_std = []
        dados_foto = []
                ## Nome
        black_std.append(np.std(imagem_cortada_black))
        rgb_std.append(np.std(imagem_rgb))
        b_mean.append(np.mean(B))
        b_std.append(np.std(B))
        g_mean.append(np.mean(G))
        g_std.append(np.std(G))
        dados_foto.append(1)

        black_std.append(9.24232424245032) 
        black_std.append(87.04032748460934) 
        rgb_std.append(85.873146) 
        rgb_std.append(30.12307929992676) #Valor minimo rgb_std
        b_mean.append(3.8900719)
        b_mean.append(169.6479949951172) 
        b_std.append(85.48547)
        b_std.append(7.284865)
        g_mean.append(51.643063)
        g_mean.append(210.3330993652344)
        g_std.append(92.25825)
        g_std.append(8.36779)
        dados_foto.append(0)
        dados_foto.append(0)

        df = pd.DataFrame()
        df['black_std'] = black_std
        df['rgb_std'] = rgb_std
        df['b_mean'] = b_mean
        df['b_std'] = b_std
        df['g_mean'] = g_mean
        df['g_std'] = g_std
        df['dados_foto']= dados_foto
        return df

    def __trata_df(self,df):
        scaler = MinMaxScaler()
        df_ajuste = scaler.fit_transform(df)
        df_ajuste = pd.DataFrame(df_ajuste,columns=df.columns)
        df_ajuste = df_ajuste.loc[df_ajuste['dados_foto']==1][['black_std','rgb_std','b_mean','b_std','g_mean','g_std']]
        return df_ajuste
    

    def __usage_model(self,df):
        modelo = self.filename
        loaded_model = joblib.load(modelo)
        return loaded_model.predict(df)

    def predict(self):
        imagem_todata = self.__read_imagem()
        df_tratado = self.__trata_df(imagem_todata)
        predict = self.__usage_model(df_tratado)
        return predict
