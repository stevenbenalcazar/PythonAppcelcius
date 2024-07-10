from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    fahrenheit = None
    if request.method == 'POST':
        celsius = request.form['celsius']
        url = "https://www.w3schools.com/xml/tempconvert.asmx"
        SOAPEnvelope = f"""
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <CelsiusToFahrenheit xmlns="https://www.w3schools.com/xml/">
              <Celsius>{celsius}</Celsius>
            </CelsiusToFahrenheit>
          </soap:Body>
        </soap:Envelope>"""

        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "https://www.w3schools.com/xml/CelsiusToFahrenheit"
        }

        response = requests.post(url, data=SOAPEnvelope, headers=headers)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for child in root.iter("{https://www.w3schools.com/xml/}CelsiusToFahrenheitResult"):
                fahrenheit = child.text
        else:
            fahrenheit = f"Error: {response.status_code}"

    return render_template('index.html', fahrenheit=fahrenheit)

if __name__ == '__main__':
    app.run(debug=True)

