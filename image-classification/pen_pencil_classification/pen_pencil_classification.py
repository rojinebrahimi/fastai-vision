# -*- coding: utf-8 -*-
"""pen\pencil-classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kHduoC-cptdchAZbsc55GlNrNHP8wzS9
"""

from fastai import *
from fastai.vision import *

# urls=Array.from(document.querySelectorAll('.rg_i')).map(el=> el.hasAttribute('data-src')?el.getAttribute('data-src'):el.getAttribute('data-iurl'));
# window.open('data:text/csv;charset=utf-8,' + escape(urls.join('\n')));

folder = 'pen'
file = 'pens.txt'

folder = 'pencil'
file = 'pencils.txt'

path = Path('data/write')
dest = path/folder
dest.mkdir(parents=True, exist_ok=True)

path.ls()

classes = ['pen', 'pencil']

download_images(path/folder/file, dest, max_pics=250)

for c in classes:
  print(c)
  verify_images(path/c, delete=True, max_size=500)

data = ImageDataBunch.from_folder(path, train='.', valid_pct=0.2, ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)

len(data.classes), data.c

data.classes

data.show_batch(row=5, figsize=(8, 8))

len(data.train_ds), len(data.valid_ds)

learn = cnn_learner(data, models.resnet34, metrics=[accuracy, error_rate])

learn.fit_one_cycle(7)

learn.save('stage-1')

learn.unfreeze()

learn.lr_find()

learn.recorder.plot()

learn.load('stage-1')
learn.fit_one_cycle(7, max_lr=1e-05)

learn.save('stage-2')

learn.load('stage-2')
interp = ClassificationInterpretation.from_learner(learn)

interp.plot_confusion_matrix()

interp.plot_multi_top_losses()

learn.export()

defaults.device = torch.device('cpu')

image = open_image(path/'pen'/'00000017.jpg')
image

learn = load_learner(path)

pred_class, indx, outputs = learn.predict(image)

pred_class
