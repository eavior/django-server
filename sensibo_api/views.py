from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sensibo_api import serializers
import requests
import json


# Create your views here.

_SERVER = 'https://home.sensibo.com/api/v2'

def processResponse(acId, data1, data2):
    result = {
      'id': acId,
      'status': data1.get('status'),
      'on': data1['acState'].get('on'),
      'mode': data1['acState'].get('mode'),
      'targetTemperature': data1['acState'].get('targetTemperature'),
      'temperatureUnit': data1['acState'].get('temperatureUnit'),
      'fanLevel': data1['acState'].get('fanLevel'),
      'swing': data1['acState'].get('swing'),
      'light': data1['acState'].get('light'),
      'changedProperties': data1.get('changedProperties'),
      'reason': data1.get('reason'),
      'failureReason': data1.get('failureReason'),
      'currentTemperature': data2['temperature'][-1]['value'],
      'currentHumidity': data2['humidity'][-1]['value'],
    };
    return result

class SensiboGetDevicesView(APIView):
    """Test API View"""
    # serializer_class = serializers.SensiboSerializer

    def get(self, request, apiKey, format=None):
        """Returns a list of APIView features"""
        response = requests.get(_SERVER + "/users/me/pods?apiKey=" + apiKey)

        if response.status_code == 200:
            data = response.json()
            return Response({'success': True, 'sensibo': data['result']})
        else:
            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

class SensiboGetDeviceData(APIView):
    def get(self, request, itemId, apiKey, format=None):
        """Returns a list of APIView features"""
        response1 = requests.get(_SERVER + "/pods/" + itemId + "/acStates?limit=1&apiKey=" + apiKey)
        response2 = requests.get(_SERVER + "/pods/" + itemId + "/historicalMeasurements?apiKey=" + apiKey)

        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            print(data1)
            # print(data2)
            result = processResponse(itemId, data1['result'][0], data2['result'])
            return Response({'success': True, 'sensibo': result})
        else:
            return Response(
                response1,
                # response2,
                status=status.HTTP_400_BAD_REQUEST
            )

class SensiboPatchDeviceData(APIView):
    serializer_class = serializers.SensiboPatchSerializer

    def patch(self, request, itemId, property, apiKey, format=None):
        """Returns a list of APIView features"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            newValue = request.data.get('newValue')
            payload = {
            "headers": {
                "Accept": "application/json",
                "Content-Type": "application/json",
                },

            "newValue": newValue
            }
            url = _SERVER + "/pods/" + itemId + "/acStates/" + property + "?apiKey=" + apiKey
            response1 = requests.patch(url, data=json.dumps(payload))
            response2 = requests.get(_SERVER + "/pods/" + itemId + "/historicalMeasurements?apiKey=" + apiKey)
            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()
                result = processResponse(itemId, data1['result'], data2['result'])
                return Response({'success': True, 'sensibo': result})
            else:
                return Response(
                    response1,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
