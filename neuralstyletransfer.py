import torch
from torchvision import transforms, models
from PIL import Image
import torch.optim as optim
import numpy as np
import argparse
import requests
from io import BytesIO

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

style_layers = {
    '0': 'conv1_1',
    '5': 'conv2_1',
    '10': 'conv3_1',
    '19': 'conv4_1',
    '28': 'conv5_1'
}

content_layers = {
    '21': 'conv4_2'
}

style_weights = {'conv1_1': 0.2,
                  'conv2_1': 0.2,
                  'conv3_1': 0.2,
                  'conv4_1': 0.2,
                  'conv5_1': 0.2}


def get_model():
  vgg = models.vgg19(pretrained=True).features
  for param in vgg.parameters():
    param.requires_grad_(False)
  
  return vgg.to(device)

def get_features(content, style, model):
  content_features = {}
  style_features = {}
  for index, layer in model._modules.items():
    style = layer(style)
    content = layer(content)

    if index in style_layers:
       style_features[style_layers[index]] = style
    elif index in content_layers:
      content_features[content_layers[index]] = content

  return content_features, style_features

def gram_matrix(tensor):
  _, depth, height, width = tensor.size()
  tensor = tensor.view(depth, height*width)
  gram_matrix = torch.matmul(tensor, tensor.t())
  return gram_matrix

def get_content_loss(output_features, content_features):
  content_loss = torch.mean((output_features - content_features)**2)
  return content_loss

def get_style_loss(style_weight, output_gram, style_gram):
  style_loss = style_weight*torch.mean((output_gram - style_gram)**2)
  return style_loss

def get_total_loss(content_weight, style_weight, content_loss, style_loss):
  total_loss = content_weight*content_loss + style_weight*style_loss
  return total_loss

def load_image(path, max_size = 512):
  try:
    response = requests.get(path)
    img = Image.open(BytesIO(response.content))
  except:
    img = Image.open(path).convert('RGB')
	
  size = max_size if max(img.size) > max_size else max(img.size)
  transform = transforms.Compose([
                                  transforms.Resize(size),
                                  transforms.ToTensor(),
                                  transforms.Normalize((0.485, 0.456, 0.406), 
                                             (0.229, 0.224, 0.225))
  ])

  img = transform(img)[:3,:,:].unsqueeze(0)
  return img

def im_convert(tensor):
    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze()
    image = image.transpose(1,2,0)
    image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
    image*=255
    image = image.clip(0, 255).astype(np.uint8)
    return image

def compute_loss(output, content_features, style_features, style_grams, alpha, beta, model):
  output_content_features, output_style_features = get_features(output, output, model)

  content_loss = 0
  for _, layer in  content_layers.items():
    content_loss = get_content_loss(output_content_features[layer], content_features[layer]) 
 
  style_loss = 0
  for layer in style_features:
    output_style_feature = output_style_features[layer]
    output_gram = gram_matrix(output_style_feature)
    _, depth, height, width = output_style_feature.shape
    style_gram = style_grams[layer]
    layer_style_loss = style_weights[layer] * torch.mean((output_gram - style_gram)**2)
    style_loss += layer_style_loss / (depth * height * width)

  total_loss = get_total_loss(alpha, beta, content_loss, style_loss) 
  return total_loss

def run(content_path, style_path, epoch, alpha, beta, lr):
  model = get_model() 
  content = load_image(content_path).to(device)
  style = load_image(style_path).to(device)
  content_features, _ = get_features(content, style, model)
  _, style_features = get_features(content, style, model)

  style_grams = {layer: gram_matrix(style_features[layer]) for layer in  style_features}
  
  output = content.clone().requires_grad_(True).to(device)
  optimizer = optim.Adam([output], lr=lr)

  best_result, best_loss = None, float('inf')
  show_every = int(epoch/10) + 1
  
  for ii in range(epoch):
      total_loss = compute_loss(output, content_features, style_features, style_grams, alpha, beta, model)
      optimizer.zero_grad()
      total_loss.backward()
      optimizer.step()


      if total_loss < best_loss:
        best_loss = total_loss
        best_result = im_convert(output)
	
      if ii%show_every == 0:
        print("Epoch {}/{} || Loss: {}".format(ii, epoch, best_loss))

  return best_result

def main():
  parser = argparse.ArgumentParser(description='NeuralStyleTransfer')
  parser.add_argument('-c', dest='content_path', help="content image path", required=True)
  parser.add_argument('-s', dest='style_path', help="style image path", required=True)
  parser.add_argument('-r', dest='result_path', help="result image path", required=True)
  parser.add_argument('-e', dest='epoch', help="iteration count", default=2000, type=int)
  parser.add_argument('-a', dest='alpha', help="weighting factor for content loss", default=1, type=np.uint32)
  parser.add_argument('-b', dest='beta', help="weighting factor for style loss", default=1e6, type=np.uint32)
  parser.add_argument('-lr', dest='learning_rate', help="learning_rate to use in optimization", default=0.003, type=float)

  args = parser.parse_args()
  output = run(args.content_path, args.style_path, args.epoch, args.alpha, args.beta, args.learning_rate)
  Image.fromarray(output).save(args.result_path)

if __name__ == "__main__":
  main()

