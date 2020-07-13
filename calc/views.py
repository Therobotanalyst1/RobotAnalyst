from django.shortcuts import render
from io import BytesIO
from datetime import datetime
import FundamentalAnalysis as fa, pandas as pa, matplotlib.pyplot as plt, base64, numpy as np
# Create your views here.

api_key ="249951aad4f6272646d75bc50547168b"

def home(request):
    return render(request, 'home.html', {'name': 'trader'})

def betaCalc(request):
    ticker = request.GET['betaTicker']
    ticker.upper()
    profile = fa.profile(ticker, api_key)

    x = profile.loc["beta"]
    beta = (x[0])
    res = (ticker + " has a beta of " + str(beta))

    return render(request, "result.html", {'result': res})

def peCalc(request):
    ticker = request.GET['peTicker']
    ticker.upper()
    income_statement_annually = fa.income_statement(ticker, api_key, period="quarter")

    x = income_statement_annually.loc["eps"]

    TOTAL_EPS = x[0] + x[1] + x[2] + x[3]

    profile = fa.profile(ticker, api_key)
    price = profile.loc["price"]

    PE_RATIO = price / TOTAL_EPS
    prPE_RATIO = PE_RATIO[0]

    return render(request, "result.html", {'result': prPE_RATIO})

def avgGrowth(request):
    ticker = request.GET['growthTicker']
    startYear = request.GET['startYear']
    endYear = request.GET['endYear']
    ticker.upper()
    growth_quarterly = fa.financial_statement_growth(ticker, api_key, period="annual")

    rev_growth = growth_quarterly.loc["revenueGrowth"]
    rev_growth_range = rev_growth.loc[endYear: startYear]
    average_growth_range = rev_growth_range.mean()*100
    average_growth_range_r = round(average_growth_range, 2)

    netincome_growth = growth_quarterly.loc["netIncomeGrowth"]
    netincome_growth_range = netincome_growth.loc[endYear: startYear]
    average_netincome_growth_range = netincome_growth_range.mean()*100
    average_netincome_growth_range_r = round(average_netincome_growth_range, 2)

    if average_netincome_growth_range < -100:
        average_netincome_growth_range = 0

    GROWTH = ("The average annual growth of " + ticker + " is:\n" + 
      "revenue: " + str(average_growth_range_r) +"%" + 
      " \n" + "net income: " + str(average_netincome_growth_range_r) + "%")

    return render(request, "result.html", {'result': GROWTH})

def years(request):
    ticker = request.GET['yearsTicker']
    ticker.upper()
    dcf_annually = fa.discounted_cash_flow(ticker, api_key, period="annual")

    namesDCF_X = []
    yearDCF_X = int(datetime.now().year)

    StockPrice_DCF_X = dcf_annually.loc["Stock Price"]

    StockPrice_list_DCF_X = StockPrice_DCF_X.iloc[:].values
    StockPrice_list_DCF_X.tolist()

    for i in range(len(StockPrice_list_DCF_X)):
      namesDCF_X.append(yearDCF_X-i)

    StockPrice_DCF_Y = dcf_annually.loc["DCF"]
    StockPrice_list_DCF_Y = StockPrice_DCF_Y.iloc[:].values
    StockPrice_list_DCF_Y.tolist()

    plt.plot(namesDCF_X, StockPrice_list_DCF_X, 'r-', label = 'Stock')
    plt.plot(namesDCF_X, StockPrice_list_DCF_Y, 'b-', label = 'DCF')
    plt.legend(loc=9)

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    buffer.close()

    DiscFlow = ("The graph for discounted cash flow of " + ticker + " is: ")

    return render(request, "result.html", {'result': DiscFlow, 'graphic': graphic})

def revenueCalc(request):
    ticker = request.GET['revenueTicker']
    ticker.upper()
    income_statement_annually = fa.income_statement(ticker, api_key, period="annual")

    Stock_Revenue = income_statement_annually.loc["revenue"]

    namesREV = []
    yearDCF_REV = int(datetime.now().year)

    Stock_Revenue_List = Stock_Revenue.iloc[:].values
    Stock_Revenue_List.tolist()

    for i in range(len(Stock_Revenue_List)):
      namesREV.append(yearDCF_REV-i)

    Stock_Income = income_statement_annually.loc["netIncome"]
    Stock_Income_List = Stock_Income.iloc[:].values
    Stock_Income_List.tolist

    plt.bar(namesREV, Stock_Revenue_List)
    plt.bar(namesREV, Stock_Income_List)
    plt.legend(loc=9)
    plt.title("10 year revenue")
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png1 = buffer.getvalue()
    revGraph = base64.b64encode(image_png1)
    revGraph = revGraph.decode('utf-8')
    buffer.close()

    revenue = ("The income statement of " + ticker + " is: ")

    return render(request, "result.html", {'result': revenue, 'graphic': revGraph})