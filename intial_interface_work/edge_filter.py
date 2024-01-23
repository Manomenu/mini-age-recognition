import cv2

def apply_edge_filter(img):
   min_intensity_grad, max_intensity_grad = 100, 200
   edge_img = cv2.Canny(img, min_intensity_grad, max_intensity_grad)
   return edge_img


class filterer:

   @classmethod
   def filter_data(cls, image):
      new_column = []
      edge = apply_edge_filter(image)
      edge = [[[i, i, i] for i in wiersz] for wiersz in edge]
      # row = np.sum(row, axis=-1) / 3
      new_image = image + edge
      return new_image

## filtered_image = filterer.filter_data(image)