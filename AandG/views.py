from django.shortcuts import render
import pandas as pd
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
import pickle
import re
import joblib
from django.conf import settings
import os


from sklearn.ensemble import RandomForestClassifier
import numpy as np
from catboost import CatBoostClassifier

catb_file = os.path.join(settings.BASE_DIR, 'templates/catboost.pkl')
mdl1 = joblib.load(catb_file)

randomforest_file = os.path.join(settings.BASE_DIR, 'templates/randomforesttest.pkl')
mdl2 = joblib.load(randomforest_file)

imported_sklearn_ohe = joblib.load(os.path.join(settings.BASE_DIR, 'templates/encoder.pkl'))

df_statename = pd.read_csv(os.path.join(settings.BASE_DIR, 'templates/name-list.csv'))
df_stateabbr = pd.read_csv(os.path.join(settings.BASE_DIR, 'templates/abbr-list.csv'))
df_codes = pd.read_excel(os.path.join(settings.BASE_DIR, 'templates/codes.xlsx'))
df_sample = pd.read_excel(os.path.join(settings.BASE_DIR, 'templates/sampledata.xlsx'))
df_category = pd.read_excel(os.path.join(settings.BASE_DIR, 'templates/category.xlsx'))
df_statename = pd.DataFrame(df_statename)
df_codes = pd.DataFrame(df_codes)
df_stateabbr = pd.DataFrame(df_stateabbr)
res1 = dict(df_statename)
res2 = dict(df_codes)
res3 = dict(pd.DataFrame(df_sample))
res4 = dict(pd.DataFrame(df_category))
res5 = dict(df_stateabbr)

def proc_code(procedure_code):
    if procedure_code.isdigit() and int(procedure_code)>=100:
        procedure_code= int(procedure_code)
        cpt = [[100, 1999], [10004, 69990], [70010, 79999], [80047, 89398], [99201, 99499], [90281, 99756]]
        cpt_desc = {0: 'Anesthesia', 1: 'Surgery', 2: 'Radiology Procedures', 3: 'Pathology and Laboratory Procedures',
                    4: 'Evaluation and Management Services', 5: 'Medicine Services and Procedures'}
        for i in range(len(cpt)):
            if procedure_code in range(cpt[i][0],cpt[i][1]):
                return cpt_desc[i]
        procedure_code=str(procedure_code)
    if not re.search('[a-zA-Z]', procedure_code):
        procedure_code = float(procedure_code)
        icd_proc = [[0, 1], [1, 6], [6, 8], [8, 17], [18, 21], [21, 30], [30, 35], [35, 40],
                    [40, 42], [42, 55], [55, 60], [60, 65], [65, 72], [72, 76], [76, 85], [85, 87], [87, 99]]

        icd_desc = {0: 'Procedures and interventions', 1: 'Operations on the nervous system',
                    2: 'Operations on the endocrine system', 3: 'Operations on the eye',
                    4: 'Operations on the ear', 5: ' Operations on the nose, mouth and pharynx',
                    6: 'Operations on the respiratory system', 7: 'Operations on the cardiovascular system',
                    8: 'Operations on the hemic and lymphatic system', 9: 'Operations on the digestive system',
                    10: 'Operations on the urinary system', 11: 'Operations on the male genital organs',
                    12: 'Operations on the female genital organs', 13: 'Obstetrical procedures',
                    14: 'Operations on the musculoskeletal system', 15: 'Operations on the integumentary system',
                    16: 'Miscellaneous diagnostic and therapeutic procedures'}
        for i in range(len(icd_proc)):
            if (procedure_code>=list(icd_proc[i])[0] and procedure_code<=list(icd_proc[i])[1]):
                return icd_desc[i]
    elif procedure_code.isalnum():
        if re.match(r'^A....', procedure_code):
            return 'A';
        if re.match(r'^B....', procedure_code):
            return 'B';
        if re.match(r'^C....', procedure_code):
            return 'C';
        if re.match(r'^E....', procedure_code):
            return 'E';
        if re.match(r'^G....', procedure_code):
            return 'G';
        if re.match(r'^H....', procedure_code):
            return 'H';
        if re.match('^J....', procedure_code):
            return 'J';
        if re.match('^K....', procedure_code):
            return 'K';
        if re.match('^L....', procedure_code):
            return 'L';
        if re.match('^M....', procedure_code):
            return 'M';
        if re.match('^P....', procedure_code):
            return 'P';
        if re.match('^Q....', procedure_code):
            return 'Q';
        if re.match('^R....', procedure_code):
            return 'R';
        if re.match('^S....', procedure_code):
            return 'S';
        if re.match('^T....', procedure_code):
            return 'T';
        if re.match('^V....', procedure_code):
            return 'V';
        if re.match('....F$', procedure_code):
            return 'Cat II';
        if re.match('....T$', procedure_code):
            return 'Cat III';
        if re.match('....U$', procedure_code):
            return 'Laboratory Analyses';
        if re.match('....M$', procedure_code):
            return 'Multianalyte Assay';

def login_page(request):
    if request.POST:
        a=request.POST
        form = AuthenticationForm(data=a)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return render(request,"nav.html",{'form':form})
        else:
            return render(request,"login.html",{'form':form})
    else:
        form = AuthenticationForm
        if request.user.is_authenticated:
            return render(request, "nav.html", {'form': form})
    return render(request,"nav.html",{'form':form})
def logout_page(request):
    logout(request)
    return render(request,"login.html",{'form':AuthenticationForm})
def index(request):
    if not request.user.is_authenticated:
        return render(request,'login.html',{'form':AuthenticationForm})
    return render(request,'home.html',request.POST)
def index1(request):
    if not request.user.is_authenticated:
        return render(request,'login.html',{'form':AuthenticationForm})
    res={}
    res['code'] = res2['HCPC']
    res['category'] = res4['Category']
    res['state'] = zip(res5['abbr'],res1['state'])
    return render(request,'Aform.html',context=res)
def min_max(x,mn,mx):
    x=float(x)
    return ((x-mn)/(mx-mn))
def index2(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'form': AuthenticationForm})
    req = request.POST
    a=dict(req)
    print(a)
    a.pop('csrfmiddlewaretoken')
    a['cat'] = a['cat'][0]
    a['part'] = a['part'][0]
    a['state'] = a['state'][0]
    a['otr'],a['psc'],a['rac'] = a['otr'][0],a['psc'][0],a['rac'][0]
    a['procedurecode']=proc_code(a['procedurecode'][0])
    a['noofclaims'] = min_max(a['noofclaims'][0],0,15)
    a['noofdays'] = min_max(a['noofdays'][0],0,365)
    a['amount'] = min_max(a['amount'][0],160.0,1634.95)
    if(a['approach'][0]=='Approach 1'):
        b = {'Appeal Category': a['cat'], 'Medicare Part': a['part'], 'State': a['state'], 'OTR': a['otr'],
             'PSC/ZPIC': a['psc'], 'RAC': a['rac'], 'Hearing Type': a['htype'], 'Procedure Code': a['procedurecode'],
             'Claims': a['noofclaims'], 'Processing_Days': a['noofdays'], 'Claims Amount': a['amount']}
        b = pd.DataFrame(b)
        loaded_sklearn_dummies = imported_sklearn_ohe.transform(
            b[['Appeal Category', 'Medicare Part', 'State', 'OTR', 'PSC/ZPIC', 'RAC',
               'Hearing Type', 'Procedure Code']])

        df = pd.DataFrame(data=loaded_sklearn_dummies.toarray(),
                          columns=imported_sklearn_ohe.get_feature_names())
        b = b.join(df)
        b.drop(columns=['Appeal Category', 'Medicare Part', 'State', 'OTR', 'PSC/ZPIC', 'RAC',
                        'Hearing Type', 'Procedure Code'], inplace=True)
        perc = mdl1.predict_proba(b)
    elif(a['approach'][0]=='Approach 2'):
        b = {'Appeal Category': a['cat'], 'Medicare Part': a['part'], 'State': a['state'], 'OTR': a['otr'],
             'PSC/ZPIC': a['psc'], 'RAC': a['rac'], 'Hearing Type': a['htype'], 'Procedure Code': a['procedurecode'],
             'Claims': a['noofdays'], 'Processing_Days': a['noofclaims'], 'Claims Amount': a['amount']}
        b = pd.DataFrame(b)
        loaded_sklearn_dummies = imported_sklearn_ohe.transform(
            b[['Appeal Category', 'Medicare Part', 'State', 'OTR', 'PSC/ZPIC', 'RAC',
               'Hearing Type', 'Procedure Code']])

        df = pd.DataFrame(data=loaded_sklearn_dummies.toarray(),
                          columns=imported_sklearn_ohe.get_feature_names())
        b = b.join(df)
        b.drop(columns=['Appeal Category', 'Medicare Part', 'State', 'OTR', 'PSC/ZPIC', 'RAC',
                        'Hearing Type', 'Procedure Code'], inplace=True)
        perc =mdl2.predict_proba(b)
    print(b)
    b.to_csv('file.csv')
    print(perc)
    result = {'denied':perc[0][0]*100,'accepted':perc[0][1]*100,'appno':a['appno']}
    return render(request,'output.html',context=result)
def index3(request):
    if not request.user.is_authenticated:
        return render(request,'login.html',{'form':AuthenticationForm})
    a=request.POST
    return render(request,'AformA.html',context=res3)
def index4(request):
    if not request.user.is_authenticated:
        return render(request,'login.html',{'form':AuthenticationForm})
    a=request.POST
    return render(request,'AformA2.html',context=res3)
def index5(request):
    if not request.user.is_authenticated:
        return render(request,'login.html',{'form':AuthenticationForm})
    a=request.POST
    return render(request,'AformD.html',context=res3)
def index6(request):
    if not request.user.is_authenticated:
        return render(request,'login.html',{'form':AuthenticationForm})
    a=request.POST
    return render(request,'AformD2.html',context=res3)

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request,'login.html',{'form':AuthenticationForm})
    return render(request,'dashboard.html')
