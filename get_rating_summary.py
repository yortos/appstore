def get_rating_page(app_id):
    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent', 'iTunes/11.3.1 (Macintosh; Intel Mac OS X 10.7.8)'),] 
    link="https://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s=143441&displayable-kind=11&id="+str(int(app_id))+"&page=1&sort=4"
    r=opener.open(link).read()
    page=str(r)
    page=page[2:len(page)-1]
    j=json.loads(page)
    return j
    
    
def get_rating_summary(app_id, store_id):
    link="https://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s="+str(store_id)+"&displayable-kind=11&id="+str(int(app_id))+"&page=1&sort=4"

    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent', 'iTunes/11.3.1 (Macintosh; Intel Mac OS X 10.7.8)'),] #AppleWebKit/533.21.1
    #open the page
    #time.sleep(1)
    while True:
        try:
            response = opener.open(link)
            break
        except (ValueError, RuntimeError):
            print ('Problem')
    page = response.read()
    temp=ast.literal_eval(page)

    num_text_reviews=temp['totalNumberOfReviews']
    total_ratings=temp['ratingCount']
    mean=temp['ratingAverage']
    dist=temp['ratingCountList']
    one=dist[0]
    two=dist[1]
    three=dist[2]
    four=dist[3]
    five=dist[4]
    return [total_ratings, num_text_reviews, mean, one, two, three, four, five]
