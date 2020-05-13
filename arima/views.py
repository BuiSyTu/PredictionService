import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from arima.models import Arima

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import numpy as np

from rpy2.robjects import pandas2ri


@csrf_exempt
def arima(request):
    if request.method == "POST":
        params = json.loads(request.body)
        name_forecast = params['nameForeCast']
        data = params['data']
        if name_forecast == "arimas":
            ts = robjects.r('ts')
            package_name = "forecast"

            try:
                forecast = importr(package_name)
            except:
                robjects.r(f'install.packages("{package_name}")')
                forecast = importr(package_name)

            forecast

            pandas2ri.activate()
            rstring = """
                function(data){
                    library(forecast)
                    model<-auto.arima(data)
                    forecast<-forecast(model,h=5,level=c(95))
                    mean <- as.vector(forecast[['mean']])
                    lower <- as.vector(forecast[['lower']])
                    upper <- as.vector(forecast[['upper']])
                    output <- data.frame(mean, lower, upper)
                    output
                }
            """
            rfunc = robjects.r(rstring)
            a = np.array(data)
            rdata = ts(a)
            r_df = rfunc(rdata)
            means = list(r_df.rx('mean'))[0]
            uppers = list(r_df.rx('upper'))[0]
            lowers = list(r_df.rx('lower'))[0]
            predicts = []
            for i in range(5):
                predict = dict()
                predict = {
                    'Time': i + 1,
                    'Lower': lowers[i],
                    'Upper': uppers[i],
                    'Mean': means[i],
                    'Percent': 80
                }
                predicts.append(predict)
            output = {
                'p': 1,
                'q': 1,
                'd': 1,
                'Coefficients': '',
                'AIC': 1,
                'BIC': 1,
                'AICC': 1,
                'Sigma2': 1,
                'LogLikelihood': 1,
                'Predicts': predicts,
                'ImagePredict': '',
                'TimeRun': 1
            }

            arimas = list(Arima.objects.values())
            ok = True
            for a in arimas:
                if a['input'] == json.dumps(data):
                    ok = False
                    break
            if ok:
                Arima.objects.create(
                    input=json.dumps(data),
                    type='arima',
                    output=json.dumps(output),
                    total_time='',
                    status='',
                    log_file='',
                    created_time='',
                    resolved_time='',
                )
                print(" ok ok")
            else:
                print("-_-")
            output1 = list(Arima.objects.filter(input=json.dumps(data)))[0]

            _arima = {
                'id': output1.id,
                'type': 'arimas',
                'status': 1
            }

            return JsonResponse(_arima, safe=False)

@csrf_exempt
def arima_detail(request, id):
    if request.method == "GET":
        arimas = list(Arima.objects.filter(id=id).values())
        arima = arimas[0]
        data = {
            'id': arima['id'],
            'input': arima['input'],
            'type': arima['type'],
            'output': arima['output'],
            'createdAt': arima['created_time'],
            'resolvedAt': arima['resolved_time'],
            'status': arima['status'],
            'totalTime': arima['total_time'],
            'logFile': arima['log_file']

        }
        return JsonResponse(data, safe=False)
