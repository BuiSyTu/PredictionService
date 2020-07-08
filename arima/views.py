import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from arima.models import Arima

from pmdarima import auto_arima

@csrf_exempt
def arima(request):
    if request.method == "POST":
        params = json.loads(request.body)
        name_forecast = params['nameForeCast']
        data = params['data']
        if name_forecast == "arimas":
            arimas = list(Arima.objects.values())
            ok = True
            for a in arimas:
                if a['input'] == json.dumps(data):
                    ok = False
                    break
            if ok:
                step_model = auto_arima(data, start_p=1, start_q=1,
                                            max_p=3, max_q=3, m=1,
                                            start_P=0, seasonal=False,
                                            d=1, D=1, trace=True,
                                            error_action='ignore',
                                            suppress_warnings=True,
                                            stepwise=False)
                predicts = []
                outputs = step_model.predict(5)

                for i in range(5):
                    predict = dict()
                    predict = {
                        'Time': i + 1,
                        'Lower': outputs[i] * (0.9 - 0.02 * i),
                        'Upper': outputs[i] * (1.1 + 0.02 * i),
                        'Mean': outputs[i],
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
