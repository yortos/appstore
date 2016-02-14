def get_rating_summary(app_id):
    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent', 'iTunes/11.3.1 (Macintosh; Intel Mac OS X 10.7.8)'),] 
    link="https://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s=143441&displayable-kind=11&id="+str(int(app_id))+"&page=1&sort=4"
    r=opener.open(link).read()
    page=str(r)
    page=page[2:len(page)-1]
    j=json.loads(page)
    return j
    
    
