import csv #to write in to csv files
import requests #to scrape the pages
import urllib
from bs4 import BeautifulSoup #to read the html


def get_page(link, num_tries=3, sleep=3, timeout): #
    for i in range(num_tries): #three tries
        try:
            opener = urllib.request.build_opener()
            opener.addheaders=[('User-Agent', 'iTunes/10.2.2 (Macintosh; Intel Mac OS X 10.9.1) AppleWebKit/533.21.1'),]
                   #('Accept-Language, en-us, en;q=0.50'),
            response = opener.open(link, timeout=timeout)
            
        except KeyboardInterrupt:
            break
        except:   #if the response times out 
            time.sleep(sleep) #wait a littl
            continue          #and try again
            
        if response.status!=200: #or 'not currently available' in r.text.lower(): #if you do get a response and it's not the right response
            #print('sleeping')
            #print('not 200')
            time.sleep(10) #if it didn't succeded, wait a little and try again
        else:
            return response
            break #if it succeded, don't try again
    return None

def get_version_date(string):#returns the version of the app and the date the review was written
    ind=findOccurences(string, '-')
    #we have to take care the case when the username has a '-' in their name. So we want to keep only the last occurences.
    if len(ind)>=2:
        ind=ind[len(ind)-2:]
    else:
        #print('something')
        return [string, string] #we have to take into account the case that there are less than two '-'

    temp=string[ind[0]:ind[1]].replace(' ','').replace('\n','')#between the first and the second '-', remove ' '  and '\n' just for ease
    version=str(temp[8:len(temp)]).replace('\\n','').replace('on','')

    sec_half=string[ind[1]+1:] #the date is here
    spaces=findOccurences(sec_half,' ') #find all the spaces
    date=sec_half[spaces[len(spaces)-3]+1:] #and keep everything right of the third space from the end. This is because the format of the date is 'Mon DD, YYYY' and it could be D or DD
    return [version, date]

def clean_reviews_db(app_id, soup, df): #takes df, and a page. Adds the reviews from the page to the df
    #
    #soup=BeautifulSoup(html, 'lxml')
    for elem in soup.find_all('div',{'class':'customer-review'}):
        
        #print(elem)
        #rev_title=elem.find('span',{'class':'customerReviewTitle'}).get_text(strip=True).encode('utf-8')
        rating=int(elem.find('div', {'class':'rating'})['aria-label'][0])
        
        #user_name=elem.find('a', {'class':'reviewer'}).get_text(strip=True).encode('utf-8')
        review_body=elem.find('p',{'class':'content'}).get_text(strip=True).encode('utf-8')
        
        if review_body is not None:
            review_body_len=len(review_body)  #just the rev_body_len
        string=elem.find('span',{'class':'user-info'}).get_text(strip=True).encode('utf-8')
        [version, date]=get_info(str(string))
        
        df.loc[len(df)]=[app_id, rating, review_body, len(review_body), version, date]
    return df


def clean_reviews_csv(app_id, soup, fp): #takes df, and a page. Adds the reviews from the page to the df
    a=csv.writer(fp)
    
    for elem in soup.find_all('div',{'class':'customer-review'}):
        #rev_title=elem.find('span',{'class':'customerReviewTitle'}).get_text(strip=True).encode('utf-8')
        rating=int(elem.find('div', {'class':'rating'})['aria-label'][0])
        #user_name=elem.find('a', {'class':'reviewer'}).get_text(strip=True).encode('utf-8')
        review_body=elem.find('p',{'class':'content'}).get_text(strip=True).encode('utf-8')
        
        if review_body is not None:
            review_body_len=len(review_body)  #just the rev_body_len
        string=elem.find('span',{'class':'user-info'}).get_text(strip=True).encode('utf-8')
        [version, date]=get_info(str(string))
        
        a.writerow([app_id, rating, review_body, len(review_body), version, date])
        fp.close()

def get_reviews_db(app_id, engine, store_id='143441', table_name="customer_reviews"):#app_id of the 
    customer_reviews=pandas.DataFrame(columns=['app_id', 'rating', 'reviewText', 'reviewTextLen','version', 'date'])

    link_1="https://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s="+str(store_id)+"&displayable-kind=11&id="+str(int(app_id))"&page="
    link_2="&sort=4"

    page_num=0 #we start from page 1 and then determine whether we should keep going
    
    #df=pandas.DataFrame(columns=['app_id', 'page_num', 'html_file', 'date_scraped'])
    
    while True:
        page_num+=1
        link=link_1+str(page_num)+link_2
        r=get_page(link)
        
        if r is not None:
            try:#try to read the page
                page=r.read()
                soup = BeautifulSoup(page)
                if len(soup.find_all('div',{'class':'customer-review'}))==0: #on the first page we find that has no reviews
                        #print(page_num)
                    break #stop
                else:
                    
                    customer_reviews=clean_reviews(app_id, soup, customer_reviews)
                    customer_reviews.to_sql(table_name, engine, if_exists='append')
            except KeyboardInterrupt:
                break
            except:
                continue
    #df.to_sql(table_name, engine, if_exists='append') #save the db


def get_reviews_csv(app_id, engine, store_id='143441', table_name="customer_reviews"):#app_id of the 
    fp=open(table_name+".csv", 'w')
    a=csv.writer(fp)
    a.writerow(['app_id', 'rating', 'reviewText', 'reviewTextLen','version', 'date'])
    fp.close()

    link_1="https://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s="+str(store_id)+"&displayable-kind=11&id="+str(int(app_id))"&page="
    link_2="&sort=4"

    page_num=0 #we start from page 1 and then determine whether we should keep going
    
    #df=pandas.DataFrame(columns=['app_id', 'page_num', 'html_file', 'date_scraped'])
    
    while True:
        page_num+=1
        link=link_1+str(page_num)+link_2
        r=get_page(link)
        
        if r is not None:
            try:#try to read the page
                page=r.read()
                soup = BeautifulSoup(page)
                if len(soup.find_all('div',{'class':'customer-review'}))==0: #on the first page we find that has no reviews
                        #print(page_num)
                    break #stop
                else:
                    fp=open(table_name+'.csv','a') #open the file
                    clean_reviews_csv(app_id, soup,fp) #and let the function write all the reviews in it
            except KeyboardInterrupt:
                break
            except:
                continue
