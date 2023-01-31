from django.db import models
from .utils import pega_img_mod
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.

ACTION_CHOICES=(
    ('FATIAMENTO1','Desenho sobre a imagem'),
    ('COLOR_BGR2GRAY','Imagem CINZA'),
    ('COLOR_BGR2HSV','Imagem BGR'),
    ('COLOR_BGR2LAB','Imagem LAB'),
    ('SUAVE1','Suavização por cálculo da média'),
    ('SUAVE2','Suavização pela Gaussiana'),
    ('SUAVE3','Suavização pela mediana'),
    ('BINARIZACAO1','Binarização com limiar'),
    ('BINARIZACAO2','Threshold adaptativo'),
    ('BINARIZACAO3','Threshold com Otsu e Riddler-Calvard'),
    ('SEGMENTACAO1','Sobel'),
    ('SEGMENTACAO2','Filtro Laplaciano'),
    ('SEGMENTACAO3','Detector de bordas Canny'),
)

class Upload(models.Model):
    imagem = models.ImageField(upload_to='images')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return str(self.id)

    def save(self,*args, **kwargs):
        #abrir imagem
        pil_img = Image.open(self.imagem)
        #converter imagem para array e fazer os edits
        cv_img=np.array(pil_img)
        img = pega_img_mod(cv_img,self.action)
        #converter imagem para pil
        img_pil = Image.fromarray(img)
        #salvar
        buffer = BytesIO()
        img_pil.save(buffer, format='png')
        image_png = buffer.getvalue()
        self.imagem.save(str(self.imagem),ContentFile(image_png), save=False)
        super().save(*args, **kwargs)
