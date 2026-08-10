from .models import Financial_Year

def session_financial_year(request):
    financial_years = Financial_Year.objects.all()
    print('financial_years',financial_years)
    selected_financial_year = request.session.get('financial_year')
    print('selected_financial_year',selected_financial_year)
    financial_yr = Financial_Year.objects.order_by('-id').first()
    
    if selected_financial_year == None:
        selected_financial_year = financial_yr.financial_year
    
    print('selected_financial_yearselected_financial_year=======',selected_financial_year)
      
    return {
        'financial_years': financial_years,
        'selected_financial_year_id': selected_financial_year
    }

    