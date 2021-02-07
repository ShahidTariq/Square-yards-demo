import os
import random
import string
import time
import requests
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import FormView

from .forms import DemoForm
import pandas as pd


class IndexView(FormView):
    form_class = DemoForm  # a demo form

    # the template for form
    template_name = "demo/index.html"

    # url to redirect after success
    success_url = "/?success=1"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            address_file = form.cleaned_data["address_file"]  # getting uploaded file from cleaned data

            filename = self.generate_lat_lng(address_file)

            # opening file to be passed in response
            with open(os.path.join(settings.MEDIA_ROOT + "/" + filename), "rb") as excel:
                data = excel.read()
            response = HttpResponse(data, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="full-address.xlsx"'
            return response
        else:
            return self.form_invalid(form, **kwargs)

    def generate_lat_lng(self, address_file):

        filename = address_file.name  # getting file name

        #  generating a random string to be appended to name
        random_string = ''.join(random.choices(string.ascii_lowercase, k=9))

        filename = random_string + "_" + filename  # append the random string to the filename

        df = pd.read_excel(address_file)

        # calculating latitude and longitude from address
        df['lat_lng'] = df['ADDRESS'].apply(self.get_coordinates)

        # adding new column for latitude and longitude
        df[['latitude', 'longitude']] = pd.DataFrame(df['lat_lng'].tolist(), index=df.index)

        # delete lat_lng column
        del df['lat_lng']

        # saving new xls file
        df.to_excel(os.path.join(settings.MEDIA_ROOT + "/" + filename), index=False)

        return filename

    def get_coordinates(self, query, from_sensor=False):

        googleGeocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?key={}'.format(
            settings.GOOGLE_PLACE_API_KEY)

        params = {
            'address': query,
            'sensor': "true" if from_sensor else "false"
        }
        url = googleGeocodeUrl
        time.sleep(.10)
        json_response = requests.get(url, params)
        response = json_response.json()
        if not response['results']:
            newurl = googleGeocodeUrl + '&address=' + query
            json_response = requests.get(newurl)
            response = json_response.json()
            if not response['results']:
                return 'N/A', 'N/A'
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        return latitude, longitude
