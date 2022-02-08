
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def pagination(request, result):
    """"
    Description: The function is designed to make pages for the results passed as parameter.
    Input: The list of results whose pagination is to be done
    Output: It return a page object of results passed.
    """
    p=Paginator(result,20)
    page_number=request.GET.get('page',1)
    try:
        page_obj = p.page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    return page_obj