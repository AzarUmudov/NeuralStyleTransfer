# Neural Style Transfer

Neural Style Transfer is one of applications of Convolutional Neural Network. The main idea of Neural Style Transfer optimization technique is to provide an image by applying style reference to content image. This code is implementation of the style transfer method that is outlined in the paper, [Image Style Transfer Using Convolutional Neural Networks, by Gatys](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf) in PyTorch.

## Theory
Neural Style Transfer uses VGG-19 extract content or style features from a passed in image. Neural Style Transfer uesd to take 2 images: **a content image** and **a style reference image**, and blend them together so the output image looks like the content image, but “painted” in the style of the style reference image.

Architecture of VGG-19:
<p align="center">
  <img width="660" height="300" src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Notebook/vgg%2019.png">
</p>

Referring to [ the paper ](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf),  ‘conv1_1’, ‘conv2_1’, ‘conv3_1’, ‘conv4_1’ and ‘conv5_1’ are used for style representation layers where ‘conv4_2’ for content representation. 

To optimize result image, Style Transfer uses 3 losses: **Content loss**, **Style Loss** and **Total Loss**

### Content Loss
Content loss consists of squared error between feature representations of original image and generated image:
<p align="center">
  <img src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Notebook/Contentloss.jpg">
</p>

### Style Loss
In order to compute style loss, we need the correlations between the different filter responses, which get by passing style reference image through the layers. These feature correlations are given by the Gram matrix where it is the inner product between the vectorised feature maps i and j in layer 
<p align="center">
  <img src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Notebook/Grammatrix.png">
</p>
 
Total style loss is 
<p align="center">
  <img src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Notebook/totalstyleloss.png">
</p>

where w_l are weighting factors of the contribution of each layer to the total loss andd E_l is the contribution of layer l to the total loss 
<p align="center">
  <img src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Notebook/styleloss.png">
</p>

### Total Loss
<p align="center">
  <img src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Notebook/totalloss.png">
</p>

where α and β are the weighting factors for content and style reconstruction, respectively.

Representation of style transfer algorithm in [ the paper ](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf):
<p align="center">
  <img src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Notebook/styletransferalgoritm.png">
</p>

## Usage
Clone the repo:
```
git clone https://github.com/AzarUmudov/NeuralStyleTransfer.git
cd <path of NeuralStyleTransfer project in your computer>
pip install -r requirements.txt
```
Running neuralstyletransfer.py:
```
Example: neuralstyletransfer.py -c "content path" -s "style path" -r "result path"
```
Recommended paramaters in the paper:

| Parameters | Values |
| ---------- |:------:| 
| alpha      | 1      | 
| beta       | 1e6    |
| lr         | 0.003  | 
| epoch      | 2000   | 

If you want to change the parameters, you can use following guide:
```
-e for epoch count
-a for alpha
-b for beta
-lr for learning_rate
```

## Examples 
<p align="left">
  <img width="280" height="220" src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Examples/content1.jpg">
  <img width="280" height="220" src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Examples/style1.jpg">
  <img width="280" height="220" src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Examples/result1.jpg">
</p>


<p align="left">
  <img width="280" height="220" src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Examples/content2.jpg">
  <img width="280" height="220" src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Examples/style2.jpg">
  <img width="280" height="220" src="https://github.com/AzarUmudov/NeuralStyleTransfer/blob/master/Examples/result2.jpg">
</p>
