from io import BytesIO 
import base64
import matplotlib.pyplot as plt
from fractions import Fraction
import re

def get_graph():
   #create a BytesIO buffer for the image
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   #set cursor to the beginning of the stream
   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   #free up the memory of buffer
   buffer.close()

   #return the image/graph
   return graph

#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
   #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
   #AGG is preferred solution to write PNG files
   plt.switch_backend('AGG')

   #specify figure size
   fig=plt.figure(figsize=(6,3))

   #select chart_type based on user input from the form
   if chart_type == '#1':
       (print(data))
       plt.bar(data['ingredient__name'], data['ingredient__price'])
       plt.xlabel('Ingredient')
       plt.xticks(rotation=45, ha='right')
       plt.ylabel('Price ($)')
       plt.title('Ingredient Prices')
       
   elif chart_type == '#2':
       plt.plot(data['ingredient__name'], data['ingredient__calories'])
       plt.xlabel('Ingredient')
       plt.xticks(rotation=45, ha='right')
       plt.ylabel('Calories')
       plt.title('Ingredient Calories')
       
   elif chart_type == '#3':
       labels=kwargs.get('labels')
       # Parse quantities - handles fractions like 1/4, decimals, and whole numbers
       quantities = []
       for qty in data['quantity']:
           # Extract first number or fraction from string
           match = re.search(r'(\d+/\d+|\d+\.?\d*)', str(qty))
           if match:
               num_str = match.group(1)
               # Convert fraction to float
               if '/' in num_str:
                   quantities.append(float(Fraction(num_str)))
               else:
                   quantities.append(float(num_str))
           else:
               quantities.append(1.0)  # default if no number found
       
       plt.pie(quantities, autopct='%1.1f%%')
       plt.title('Ingredient Quantity Distribution')
       plt.legend(labels, loc='upper right', bbox_to_anchor=(1.7, 0.9))
   else:
       print ('unknown chart type')

   #specify layout details
   plt.tight_layout()

   #render the graph to file
   chart =get_graph() 
   return chart