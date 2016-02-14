def get_static_info(app_id):
    try:
        app_id=str(int(app_id))
        r=requests.get('https://itunes.apple.com/us/app/id'+app_id, timeout=3)
        page=BeautifulSoup(r.text)

        category=page.find('span', {'itemprop':"applicationCategory"})
        if category is not None:
            category=category.get_text(strip=True)
        else:
            category=None

        description=page.find('p',{'itemprop':"description"})
        if description is not None:
            description=description.get_text(strip=True)
        else:
            description=None
        description_len=len(description)

        price=page.find('div', {'itemprop':"price"})
        if price is not None:
            price=price.get_text(strip=True).replace('$','')
        else:
            price=None
        #size
        t=page.find_all('li')
        for elem in t:
            if elem.find_next('span',{'class':"label"}) is not None:
                if elem.find_next('span',{'class':"label"}).get_text(strip=True).replace(' ','')=='Size:':
                    size=elem.get_text(strip=True).replace('Size:','')
        return [app_id, category, description_len, price, size]
    except:
        return [None]*5
