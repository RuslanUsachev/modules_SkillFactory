import requests
# from requests_toolbelt.multipart.encoder import MultipartEncoder
from bs4 import BeautifulSoup
import time
import sys
from multiprocessing import Pool
from datetime import datetime
import csv
import pandas as pd


def get_soup(session, url):
    r = session.get(url)
    
    if r.status_code != 200: # not OK
        print('[get_soup] status code:', r.status_code)
        return
    else:
        return BeautifulSoup(r.text, 'html.parser')

    
def post_soup(session, url, params):
    '''Read HTML from server and convert to Soup'''

    r = session.post(url, data=params)
    
    if r.status_code != 200: # not OK
        print('[post_soup] status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')
    

def scrape(url, lang='ALL'):
    # create session to keep all cookies (etc.) between requests
    session = requests.Session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'cookie': 'TADCID=c6wDZwJOGo_EJlnsABQCjnFE8vTET66GHuEzPi7KfV4bec-95jgfanhbIdjWeTmA3bEUOgl-_M0V08Cu40tFI4wI2L0pIW36Sbs; TAUnique=%1%enc%3AnLaZ8ThTJaxOBsR59lkVciYRpDXbJ8CxA0%2FfIr8KTBkY1BzG0pZatA%3D%3D; TASSK=enc%3AAOsne0fV%2FyiomBk3YZ3fC2x4eSydXMrrvzDA7hG4vRVMuXGoz3W7QzuO970gpEsWNt3KP43SRPq%2BpBcLwsPuqvyJFQOiSZ8uIwvKIw7re0BstfSuLt%2BgQpaW2vVOsAiMjw%3D%3D; ServerPool=A; TART=%1%enc%3ATgbEefZZFXKhlJ26odlyHO8f7cs8AGpi1lXM0y8eVKxQ6NHSyozzw2j0Di%2F6XSjfBI5T9yE%2BVkU%3D; _ym_uid=1592059002891463273; _ym_d=1592059002; _ym_wasSynced=%7B%22time%22%3A1592059001677%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; CM=%1%PremiumMobSess%2C%2C-1%7Csesswifi%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7Csesstch15%2C%2C-1%7CRCPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CCYLPUSess%2C%2C-1%7Ctvsess%2C%2C-1%7CTBPers%2C%2C-1%7Cperstch15%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7Cpershours%2C%2C-1%7C%24%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CTrayspers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CMCPPers%2C%2C-1%7Csesshours%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cmdpers%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmds%2C1592059003260%2C1592145403%7CRestAds%2FRSess%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7Csesslaf%2C%2C-1%7CCYLPUPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7Cperslaf%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C%2C-1%7CTBSess%2C%2C-1%7Cb2bmcsess%2C%2C-1%7Cperswifi%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CMCPSess%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CTrayssess%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CPremiumORPers%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7Cbooksticks%2C%2C-1%7Cbookstickp%2C%2C-1%7Cmdsess%2C%2C-1%7C; __gads=ID=b57b03c324354e82:T=1592059002:S=ALNI_MZ8IHnPW6wVLseC8D6-Z872n_L1cQ; TATravelInfo=V2*AY.2020*AM.6*AD.21*DY.2020*DM.6*DD.22*A.2*MG.-1*HP.2*FL.3*DSM.1592067612926*RS.1*RY.2020*RM.6*RD.13*RH.20*RG.2; health_notice_dismissed=1; TALanguage=ALL; PMC=V2*MS.52*MD.20200613*LD.20200614; PAC=AKxGmgrabPNSDYln_H7F_GmnO4jdNKqEJ64yiQN0KzKmRraPEOfgN3CFiIeOVUagkedosvB5VvC90E6VMfsRecGIqyS0fKtN5cKctoGB339reIjKhXUlR30hApGIOlKKT5MBuppUYa8WAIe_8PN7N1jO-vc-fTwmcEZcyMo15_vKIpyAd5uf4J9x0L73efusC0o3s2sIDOP0uiBOtEgu1P69HHM8BseKT3y-iEdCFwtBJGOYFO4M8TG8Afzhx6veyA%3D%3D; VRMCID=%1%V1*id.12082*llp.%2FRestaurant_Review-g189852-d7992032-Reviews-Buddha_Nepal-Stockholm-m12082*e.1592735778220; _ym_isad=2; roybatty=TNI1625!ANxWgMoP7UKZ7OuThPCfwVSV1z0tsD1OIOnIqXvkh5V7w9Xv%2FKMrYIfvD%2FZ1ItrDghVu3jxLdWgr2%2FePZJaelf8FCYsHABzj1GKjk6IhcLi6AFCvFGfXvukMZ6%2Bkrx8xg054cnd60V84mozLFOh%2BTEsVHglQm14V49QpK1APLC3J%2C1; SRT=%1%enc%3ATgbEefZZFXKhlJ26odlyHO8f7cs8AGpi1lXM0y8eVKxQ6NHSyozzw2j0Di%2F6XSjfBI5T9yE%2BVkU%3D; __vt=YrZ9am5F6hyb0VhSABQCq4R_VSrMTACwWFvfTfL3vw3-B2GlKva9P5VCKE-jEF5RtKAUxCtDMtZl6Nz77LPRPOlgTqv0gdiajvhKidWRZb4xh04ficMi7UEnQ2fo5YUt3GjVCtLuW1mKp0CIX_jtRX_Uxg; TAReturnTo=%1%%2FRestaurant_Review%3Fg%3D189852%26reqNum%3D1%26puid%3DXuYG0wokHZEAA-yHf2sAAAGB%26isLastPoll%3Dfalse%26d%3D7992032%26waitTime%3D30%26paramSeqId%3D0%26changeSet%3DREVIEW_LIST; TASession=V2ID.93191757F7F78F6064651DA61A5FB0EE*SQ.163*LS.DemandLoadAjax*GR.37*TCPAR.66*TBR.27*EXEX.55*ABTR.81*PHTB.24*FS.37*CPU.57*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.ALL*FA.1*DF.0*IR.1*OD.null*FLO.7992032*TRA.true*LD.7992032*EAU._; TAUD=LA-1592058991899-1*RDD-1-2020_06_13*RD-10050-2020_06_13.1912643*HC-8462000*HDD-8621018-2020_06_21.2020_06_22*LD-75801061-2020.6.21.2020.6.22*LG-75801063-2.1.F.',
    })

    details_dict = parse(session, url + '?filterLang=' + lang)

    return details_dict


def parse(session, url):
    '''Get number of reviews and start getting subpages with reviews'''

    soup = get_soup(session, url)

    if not soup:
        print('[parse] no soup:', url)
        return

    restaurant_details = {}
    num_reviews_elem = soup.find('span', class_='reviews_header_count')
    if not num_reviews_elem:
        restaurant_details['number_of_reviews'] = 0
    else:
        num_reviews = num_reviews_elem.text
        num_reviews = num_reviews[1:-1] 
        num_reviews = num_reviews.replace(',', '')
        num_reviews = int(num_reviews)
        restaurant_details['number_of_reviews'] = num_reviews

    restaurant_detail = soup.find_all("a", class_='restaurants-detail-top-info-TopInfo__tagLink--2LkIo')
    
    restaurant_details['price_range'] = None
    restaurant_details['cuisines_style'] = None
    
    if restaurant_detail:
        cuisines = []
        for item in restaurant_detail:
            if '$' in item.text:
                restaurant_details['price_range'] = item.text
            else:
                cuisines.append(item.text)
        restaurant_details['cuisines_style'] = cuisines
    
    url_parts = url.split('-')
    url_template = '-'.join(url_parts[:4] + ['or{}'] + url_parts[4:])

    items = [[], []]
    
    #  Не будем парсить отзывы, если их нет.
    if restaurant_details['number_of_reviews'] > 0:
        offset = 0

        while(True):
            subpage_url = url_template.format(offset)

            subpage_items = parse_reviews(session, subpage_url)
            if not subpage_items:
                break

            # items[0] += subpage_items[0]
            items[1] += subpage_items[1]

            if len(subpage_items[0]) < 10:
                break

            offset += 10
        
    restaurant_details['reviews_data'] = items
    # restaurant_details['reviews_data'] = None
    return restaurant_details


def get_reviews_ids(soup):
    
    items = soup.find_all('div', attrs={'data-reviewid': True})

    if items:
        reviews_ids = [x.attrs['data-reviewid'] for x in items][::2]
        
        return reviews_ids


def get_more(session, reviews_ids):

    url = 'https://www.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer=Hotel_Review'

    payload = {
        'reviews': ','.join(reviews_ids), # ie. "577882734,577547902,577300887",
        'widgetChoice': 'EXPANDED_HOTEL_REVIEW_HSX',  # ???
        'haveJses': 'earlyRequireDefine,amdearly,global_error,long_lived_global,apg-Hotel_Review,apg-Hotel_Review-in,bootstrap,desktop-rooms-guests-dust-en_US,responsive-calendar-templates-dust-en_US,taevents',
        'haveCsses': 'apg-Hotel_Review-in',
        'Action': 'install',
    }

    soup = post_soup(session, url, payload)

    return soup


def parse_reviews(session, url):
    '''Get all reviews from one page'''

    soup = get_soup(session, url)

    if not soup:
        print('[parse_reviews] no soup:', url)
        return
    
    reviews_ids = get_reviews_ids(soup)
    if not reviews_ids:
        return

    soup = get_more(session, reviews_ids)

    if not soup:
        print('[parse_reviews] no soup:', url)
        return

    items = []
    reviews = []
    dates = []
    
    try:
        reviews_on_page = soup.find_all('div', class_='reviewSelector')
    except:
        reviews_on_page = None
    
    # if reviews_on_page:
    #     for review in reviews_on_page:
    #         review_body = review.find('p', class_='partial_entry').text
    #         if len(review_body) > 125:
    #             review_body = review_body[:125] + '...' # make a review smaller
    #         reviews.insert(0, review_body)
    #         dates.insert(0, review.find('span', class_='ratingDate')['title'])

    # parse date only ( without review body)
    if reviews_on_page:
        for review in reviews_on_page:
            # review_body = review.find('p', class_='partial_entry').text
            # if len(review_body) > 125:
            #     review_body = review_body[:125] + '...' # make a review smaller
            # reviews.insert(0, review_body)
            dates.insert(0, review.find('span', class_='ratingDate')['title'])

    items.append(reviews)
    items.append(dates)

    return items


def get_restaurant_data_by_link(link):
    lang = 'ALL'
    restaurant_details_dict = scrape(link, lang)
    
    return restaurant_details_dict


def write_csv(data):
    with open('restaurant_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow( (data['id_ta'],
                         data['number_of_reviews'],
                         data['cuisines_style'],
                         data['price_range'],
                         data['reviews_data'])
                       )


def parse_data(tuple_data):
    # print('[ parse_data ] run')

    item_dict = get_restaurant_data_by_link(tuple_data[1])
    item_dict['id_ta'] = tuple_data[0]
    
    write_csv(item_dict)


def start_parsing(data_tuples):
    print(f"[ start_parsing ]: run")
    start = datetime.now()

    with Pool(40) as p:
        p.map(parse_data, data_tuples)

    end = datetime.now()
    total_time = end - start
    print(f"\n[ start_parsing ]: end")
    print('Всего времени заняло:', str(total_time))


def main():
    # read the csv file
    print('[ main ] run')
    print(f"Read the csv file")
    empty_df = pd.read_csv('empty_reviews.csv')

    # create a tuple of ids and urls
    ids = empty_df.id_ta.to_list()
    paths = empty_df.url_ta.to_list()
    urls = [f"https://www.tripadvisor.com{path}" for path in paths]
    data_tuples = list(zip(ids, urls))
    print(f"Made data_tuples")

    # call start_parsing
    start_parsing(data_tuples)


if __name__ == "__main__":
    main()
