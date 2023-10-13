from bs4 import BeautifulSoup
import os
import pandas as pd
import pickle
import re
import requests

class scraper_class:
    class new:
        class egypt:
            def _2b(self):
                def first_level_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    a = (
                        soup
                        .find("div", {"class" : "filter-options-content"})
                        .find("ol", {"class" : "items"})
                        .find_all("li")
                    )
                    d = {}
                    for i in a:
                        b = ''.join(
                            [
                                i for i in i.find("a").get_text().strip() 
                                if i and not i.isnumeric()
                            ]
                        )
                        d[b[:b.find(" ")]] = i.find("a")['href']
                    pickle.dump(d, open("new-egypt-2b-1st-level-links.pkl", 'wb'))

                def mobiles_and_prices():
                    d = pickle.load(open("new-egypt-2b-1st-level-links.pkl", 'rb'))
                    mobiles = []
                    prices = []
                    currency = []
                    for url in d.values():
                        try:
                            soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                            a = (
                                soup
                                .find("ol", {"class" : "products list items product-items"})
                                .find_all("li")
                            )
                            for mobile in a:
                                m = (
                                    mobile
                                    .find("a", {"class" : "product-item-link"})
                                    .get_text()
                                    .strip()
                                )
                                cp = (
                                    mobile
                                    .find("span", {"class" : "price"})
                                    .get_text()
                                )
                                p = ''.join([i for i in cp if i.isnumeric()])
                                c = cp[:cp.find(re.findall(r'\d+', cp)[0])]
                                prices.append(p)
                                currency.append(c)
                                mobiles.append(m)
                        except:
                            pass
                    pickle.dump(mobiles, open("new-egypt-2b-mobiles.pkl", 'wb'))
                    pickle.dump(prices, open("new-egypt-2b-prices.pkl", 'wb'))
                    pickle.dump(currency, open("new-egypt-2b-currency.pkl", 'wb'))


                def list_to_csv():
                    mobiles = pickle.load(open("new-egypt-2b-mobiles.pkl", 'rb'))
                    prices = pickle.load(open("new-egypt-2b-prices.pkl", 'rb'))
                    currency = pickle.load(open("new-egypt-2b-currency.pkl", 'rb'))
                    df = pd.DataFrame()
                    new_used = ['new']*len(mobiles)
                    for i in ['mobiles', 'prices', 'currency', 'new_used']:
                        df[i] = eval(i)
                    df['web'] = url
                    df.to_csv("new-egypt-2b-data.csv", index=False)

                url = "https://2b.com.eg/en/mobile-and-tablet/mobiles.html"
                first_level_links()
                mobiles_and_prices()
                list_to_csv()

            def ennap(self):
                def all_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    a = (
                        soup
                        .find("ul", {"class" : "nav nav-pills nav-stacked"})
                        .find_all("li")
                    )
                    links = [url]
                    results_qty = int(soup.find_all("span", {"class" : "xt_product_count"})[-1].get_text())
                    if results_qty % 20 == 0:
                        q = results_qty
                    else:
                        q = int(results_qty / 20) + 1
                    for i in range(2, q+1):
                        links.append(url + "/page/" + str(i))
                    pickle.dump(links, open("new-egypt-ennap-all_links.pkl", "wb"))

                def data_from_links():
                    currency = []
                    mobiles = []
                    price = []
                    links = pickle.load(open("new-egypt-ennap-all_links.pkl", 'rb'))
                    for url in links:
                        soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                        a = (
                            soup
                            .find("div", {"id" : "products_grid"})
                            .select("div", {"class" : "oe_product oe_list oe_product_cart list-view-css"})
                        )
                        for i in a:
                            try:
                                b = i.find("div", {"itemscope" : "itemscope"}).find("section")
                                m = b.find("a").get_text()
                                c = b.find("span", {"data-oe-type" : "monetary"}).get_text()
                                p = ''.join([i for i in c if i.isnumeric()])
                                cc = c.split()[0]
                                mobiles.append(m)
                                price.append(p)
                                currency.append(cc)
                            except:
                                pass
                    url = [url]*len(mobiles)
                    pickle.dump(mobiles, open("new-egypt-ennap-mobiles.pkl", "wb"))
                    pickle.dump(price, open("new-egypt-ennap-prices.pkl", "wb"))
                    pickle.dump(currency, open("new-egypt-ennap-currency.pkl", "wb"))
                    pickle.dump(url, open("new-egypt-ennap-url.pkl", "wb"))


                def data_to_csv():
                    mobiles = pickle.load(open("new-egypt-ennap-mobiles.pkl", "rb"))
                    prices = pickle.load(open("new-egypt-ennap-prices.pkl", "rb"))
                    currency = pickle.load(open("new-egypt-ennap-currency.pkl", "rb"))
                    web = pickle.load(open("new-egypt-ennap-url.pkl", "rb"))
                    new_used = ['new']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles','prices','currency', 'new_used','web']:
                        df[i] = eval(i)
                    df.to_csv("new-egypt-ennap-data.csv", index=False)

                url = "https://www.ennap.com/mobiles-tablets-mobile-phones-1"
                all_links()
                data_from_links()
                data_to_csv()

            def jumia(self):
                def extract_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    a = soup.find("form", {"class" : "facet-form"})
                    b = a.find_all("div", {"class":"facet-el"})
                    links = []
                    links =  [i.find("a")['href'] for i in b]
                    pickle.dump(links,open("new-egypt-jumia-links.pkl", "wb"))

                def all_pages():
                    links = pickle.load(open("new-egypt-jumia-links.pkl", "rb"))
                    d = {}
                    for link in links:
                        soup = BeautifulSoup(requests.get(link,timeout=5).text, "lxml")
                        try:
                            a = soup.find("ul", {"class" : "osh-pagination -horizontal"})
                            base_link = a.find("a")['href'] + "?page={}"
                            d[link.split("/")[-2]] = [
                                base_link.format(i) 
                                for i in range(1, int(a.get_text().strip()[-1])+1)
                            ]
                        except:
                            d[link.split("/")[-2]] = [link]
                    pickle.dump(d, open("new-egypt-jumia-all_pages.pkl", "wb"))

                def extract_data():
                    mobiles = []
                    prices = []
                    currency = []
                    dd = pickle.load(open("new-egypt-jumia-all_pages.pkl", "rb"))
                    for link in [z for i in list(dd.values()) for z in i]:
                        try:
                            soup = BeautifulSoup(requests.get(link,timeout=5).text, "lxml")
                            a = (
                                soup
                                .find("section", {"class" : "products -mabaya"})
                                .find_all("div", {"class" : "sku -gallery"})
                            )
                            a += (
                                soup
                                .find("section", {"class" : "products -mabaya"})
                                .find_all("div", {"class" : "sku -gallery -has-offers"})
                            )
                            for i in a:
                                n = i.find("span", {"class" : "name"}).get_text()
                                p = i.find("span", {"class" : "price"}).get_text()
                                c = p[:p.find(" ")]
                                p = ''.join([i for i in p[p.find(" "):].strip() if i.isnumeric()])
                                mobiles.append(n)
                                prices.append(p)
                                currency.append(c)
                        except:
                            pass
                    web = [url]*len(mobiles)
                    pickle.dump(mobiles, open("new-egypt-jumia-mobiles.pkl", "wb"))
                    pickle.dump(prices, open("new-egypt-jumia-prices.pkl", "wb"))
                    pickle.dump(currency, open("new-egypt-jumia-currency.pkl", "wb"))
                    pickle.dump(web, open("new-egypt-jumia-web.pkl", "wb"))


                def lists_to_csv():
                    mobiles = pickle.load(open("new-egypt-jumia-mobiles.pkl", "rb"))
                    prices = pickle.load(open("new-egypt-jumia-prices.pkl", "rb"))
                    currency = pickle.load(open("new-egypt-jumia-currency.pkl", "rb"))
                    web = pickle.load(open("new-egypt-jumia-web.pkl", "rb"))
                    new_used = ['new']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles','prices','currency', 'new_used','web']:
                        df[i] = eval(i)
                    df.to_csv("new-egypt-jumia-data.csv", index=False)

                url = "https://www.jumia.com.eg/mobile-phones/"
                extract_links()
                all_pages()
                extract_data()
                lists_to_csv()

            def priceNa(self):

                def get_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    all_links = ["https://eg.pricena.com/en/mobile-tablets/mobile-phones"]
                    c = 1
                    while True:
                        c += 1
                        ur = "https://eg.pricena.com/en/mobile-tablets/mobile-phones/page/" + str(c)
                        u = requests.get(ur,timeout=5).history
                        if not u:
                            all_links.append(ur)
                        else:
                            break
                    pickle.dump(all_links,open("new-egypt-priceNa-links.pkl", "wb"))

                def links_to_data():
                    links = pickle.load(open("new-egypt-priceNa-links.pkl", "rb"))
                    mobiles = []
                    prices = []
                    currency =  []
                    for link in links:
                        try:
                            soup = BeautifulSoup(requests.get(link,timeout=5).text, "lxml")
                            a = soup.find("div", {"id" : "results"})
                            b = a.find_all("div", {"class" : "item desktop"})
                            for c in b:
                                m = c.find("div", {"class" : "name leftdirection"}).get_text().strip()
                                p = c.find("div", {"class" : "price"}).get_text().strip()
                                mobiles.append(m)
                                prices.append(p.split()[1])
                                currency.append(p.split()[0])
                        except: 
                            pass
                    web = [url]*len(mobiles)
                    pickle.dump(mobiles, open("new-egypt-priceNa-mobiles.pkl", "wb"))
                    pickle.dump(prices, open("new-egypt-priceNa-prices.pkl", "wb"))
                    pickle.dump(currency, open("new-egypt-priceNa-currency.pkl", "wb"))
                    pickle.dump(web, open("new-egypt-priceNa-web.pkl", "wb"))

                def data_to_csv():
                    mobiles = pickle.load(open("new-egypt-priceNa-mobiles.pkl", "rb"))
                    prices = pickle.load(open("new-egypt-priceNa-prices.pkl", "rb"))
                    currency = pickle.load(open("new-egypt-priceNa-currency.pkl", "rb"))
                    web = pickle.load(open("new-egypt-priceNa-web.pkl", "rb"))
                    df = pd.DataFrame()
                    new_used = ['new']*len(mobiles)
                    for i in ['mobiles', 'prices', 'currency','new_used', 'web']:
                        df[i] = eval(i)
                    df.to_csv("new-egypt-priceNa-data.csv", index=False)

                url = "https://eg.pricena.com/en/mobile-tablets/mobile-phones"
                get_links()
                links_to_data()
                data_to_csv()

            def souq(self):

                def all_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    mobiles_qty = int(''.join([i for i in soup.find("li", {"class" : "total"}).get_text() if i.isnumeric()]))
                    if mobiles_qty % 60 == 0:
                        pages = mobiles_qty // 60
                    else:
                        pages = (mobiles_qty // 60) + 1
                    all_urls = [url]
                    for i in range(2, pages+1):
                        all_urls.append("https://egypt.souq.com/eg-en/mobile-phone/l/?page={}".format(i))
                    pickle.dump(all_urls, open("new-egypt-souq-all-links.pkl", 'wb'))



                def data_from_links():
                    names = []
                    price = []
                    currency = []
                    all_urls = pickle.load(open("new-egypt-souq-all-links.pkl", 'rb'))
                    for url in all_urls:
                        soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                        a = (
                            soup
                            .find("div", {"class" : "row collapse content flex-box-grid medium-up-1 large-up-1"})
                            .find_all("div", {"class" : "column column-block block-list-large single-item"})
                        )
                        for z in a:
                            names.append(''.join([
                                i 
                                for i in z.find("div", {"class" : "col col-info item-content"}).find("a").get_text().strip() 
                                if i.isprintable()
                            ]))
                            b = z.find("div", {"class" : "col col-buy"}).find("div", {"class" : "is sk-clr1"})
                            c = b.find("h3").get_text()
                            price.append(''.join([i for i in c[:c.find(".")] if i.isnumeric()]))
                            currency.append(b.find("small", {"class" : "currency-text sk-clr1 itemCurrency"}).get_text())
                    pickle.dump(names, open("new-egypt-souq-names.pkl", 'wb'))
                    pickle.dump(price, open("new-egypt-souq-price.pkl", 'wb'))
                    pickle.dump(currency, open("new-egypt-souq-currency.pkl", 'wb'))

                def list_to_csv():
                    mobiles = pickle.load(open("new-egypt-souq-names.pkl", 'rb'))
                    prices = pickle.load(open("new-egypt-souq-price.pkl", 'rb'))
                    currency = pickle.load(open("new-egypt-souq-currency.pkl", 'rb'))
                    new_used = ['new']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles', 'prices', 'currency', 'new_used']:
                        df[i] = eval(i)
                    df['web'] = [url]*len(mobiles)
                    df.to_csv("new-egypt-souq-data.csv", index=False)

                url = "https://egypt.souq.com/eg-en/mobile-phone/l/?section=2&page=1"
                all_links()
                data_from_links()
                list_to_csv()

            def yaoota(self):

                def get_all_links():
                    url1 = url + "?category=374"
                    url2 = url + "?category=375"
                    links = [url1, url2]
                    e = 0
                    while True:
                        e += 1
                        print(e, end=", ")
                        if not requests.get(url1 + "&page= " + str(e),timeout=5).history:
                            links.append(url1 + "&page= " + str(e))
                        else:
                            break
                    e = 0
                    while True:
                        e += 1
                        print(e, end=", ")
                        if not requests.get(url2 + "&page= " + str(e),timeout=5).history:
                            links.append(url2 + "&page= " + str(e))
                        else:
                            break
                    pickle.dump(links, open("new-egypt-yaoota-all_links.pkl", "wb"))

                def links_to_data():
                    names = []
                    cc = []
                    currency = []
                    price = []
                    all_links = pickle.load(open("new-egypt-yaoota-all_links.pkl", 'rb'))

                    for link in all_links:
                        soup = BeautifulSoup(requests.get(link,timeout=5).text, "lxml")
                        a = (
                            soup
                            .find("div", {"class" : "search__container__result__products"})
                            .find_all("div", {"class" : "search__container__result__products__single media hasProductRating"})
                        )
                        for b in a:
                            n = (
                                b
                                .find("div", {"class" : "media-body"})
                                .find("h4", {"class" : "search__container__result__products__single__title media-heading"})
                                .get_text()
                                .strip()
                            )
                            c = (
                                b
                                .find("div", {"class" : "media-right hidden-xs"})
                                .find("div", {"class" : "price-box"})
                                .find("h3", {"class" : "search__container__result__products__single__price"})
                                .get_text()
                                .strip()
                            )
                            names.append(n)
                            cc.append(c)

                    for i in cc:
                        currency.append(i.split()[-1].strip())
                        price.append(float(i.split()[0].strip().replace(",", "")))
                    pickle.dump(names, open("new-egypt-yaoota-names.pkl", "wb"))
                    pickle.dump(currency, open("new-egypt-yaoota-currency.pkl", "wb"))
                    pickle.dump(price, open("new-egypt-yaoota-price.pkl", "wb"))

                def data_to_csv():
                    mobiles = pickle.load(open("new-egypt-yaoota-names.pkl", "rb"))
                    currency = pickle.load(open("new-egypt-yaoota-currency.pkl", "rb"))
                    prices = pickle.load(open("new-egypt-yaoota-price.pkl", "rb"))
                    new_used = ['new']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles', 'prices', 'currency', 'new_used']:
                        df[i] = eval(i)
                    df['web'] = [url]*len(mobiles)
                    df.to_csv("new-egypt-yaoota-data.csv", index=False)

                url = "https://yaoota.com/en-eg/category/mobiles-and-tablets/mobiles/"
                get_all_links()
                links_to_data()
                data_to_csv()

        class pak:
            def mobile_phone(self):

                def get_brands_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    brands_links = []
                    a = soup.find_all("div", {"class" : "block_wrapper"})[1].find_all("div", {"class" : "table_cell"})
                    for i in a:
                        brands_links.append(i.find("a")['href'])
                    pickle.dump(brands_links, open("new-pak-mobile_phone-brands_links.pkl", "wb"))

                def get_all_links():
                    all_links = []
                    brands_links = pickle.load(open("new-pak-mobile_phone-brands_links.pkl", "rb"))

                    for brand_url in brands_links:
                        try:
                            soup = BeautifulSoup(requests.get(brand_url,timeout=5).text, "lxml")
                            one_brand_links = [brand_url]
                            b = soup.find("span", {"style" : "float: left; margin-left: 5px; line-height: 22px;width: 100%;"}).                                                                    find_all("a")[-1]['href']
                            pages = int(re.findall('\d+',b)[0])
                            for i in range(1, pages+1):
                                one_brand_links.append("{}-{}/".format(brand_url, i))
                            all_links += one_brand_links
                        except:
                            all_links.append(brand_url)
                    pickle.dump(all_links, open("new-pak-mobile_phone-all_links.pkl", "wb"))

                def links_to_data():
                    all_links = pickle.load(open("new-pak-mobile_phone-all_links.pkl", "rb"))

                    mobiles = []
                    prices = []
                    currency = []
                    errors = []
                    ee = 0
                    for link in all_links:
                        ee += 1
                        print(ee, end=", ")
                        try:
                            soup = BeautifulSoup(requests.get(link,timeout=5).text, "lxml")
                            a = (
                                soup
                                .find("div", {"class" : "center_mobs"})
                                .find_all("div", {"class" : "home_page_blocks"})
                            )
                            m1 = []
                            cc1 = []
                            p1 = []
                            for i in a:
                                b = i.get_text().strip()
                                m = b[:b.rfind("\n")].strip()
                                c = b[b.find("\n"):].strip()
                                if not "Coming" in c:
                                    cc = c[:c.find(" ")].replace(".", "").strip()
                                    p = c[c.find(" "):].strip()
                                else:
                                    cc = "Coming Soon"
                                    p = "Coming Soon"
                                m1.append(m)
                                cc1.append(cc)
                                p1.append(p)
                            mobiles += m1
                            currency += cc1
                            prices += p1
                        except:
                            errors.append(link)
                            pass
                    if errors:
                        print("There is {} errors, those links with error saved in file *errors.pkl*".format(len(errors)))
                        pickle.dump(errors, open("new-pak-mobile_phone-errors3.pkl", "wb"))

                    pickle.dump(currency, open("new-pak-mobile_phone-currency.pkl", "wb"))
                    pickle.dump(prices, open("new-pak-mobile_phone-prices.pkl", "wb"))
                    pickle.dump(mobiles, open("new-pak-mobile_phone-mobiles.pkl", "wb"))

                def data_to_csv():
                    currency = pickle.load(open("new-pak-mobile_phone-currency.pkl", "rb"))
                    prices = pickle.load(open("new-pak-mobile_phone-prices.pkl", "rb"))
                    mobiles = pickle.load(open("new-pak-mobile_phone-mobiles.pkl", "rb"))
                    new_used = ['new']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles', 'prices', 'currency', 'new_used']:
                        df[i] = eval(i)
                    df['web'] = [url]*len(mobiles)
                    df.to_csv("new-pak-mobile_phone-data.csv", index=False)

                url = "http://www.mobile-phone.pk/mobile_brands/"
                get_brands_links()
                get_all_links()
                links_to_data()
                data_to_csv()

            def telemart(self):
                def links_to_data():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    prices = []
                    mobiles = []
                    currency = []
                    a = soup.find("div", {"id" : "catalog-listing"})
                    b = a.find_all("li", {"class" : "col-lg-3 col-md-3 col-sm-5 col-xs-12 item"})
                    for mobile in b:
                        c = mobile.find("div", {"class" : "pro-inner"})
                        nam = c.find("div", {"class" : "pro-title product-name"}).get_text().strip()
                        d = c.find("div", {"class" : "pro-content"}).get_text().strip()
                        cur = d.split()[0].strip()
                        prc = d.split()[-1].strip().replace(",", "")
                        prices.append(prc)
                        currency.append(cur)
                        mobiles.append(nam)

                    pickle.dump(prices, open("new-pak-telemart-prices.pkl", "wb"))
                    pickle.dump(currency, open("new-pak-telemart-currency.pkl", "wb"))
                    pickle.dump(mobiles, open("new-pak-telemart-mobiles.pkl", "wb"))

                def data_to_csv():
                    prices = pickle.load(open("new-pak-telemart-prices.pkl", "rb"))
                    currency = pickle.load(open("new-pak-telemart-currency.pkl", "rb"))
                    mobiles = pickle.load(open("new-pak-telemart-mobiles.pkl", "rb"))
                    new_used = ['new']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles', 'prices', 'currency', 'new_used']:
                        df[i] = eval(i)
                    df['web'] = [url]*len(mobiles)
                    df.to_csv("new-pak-telemart-data.csv", index=False)

                url = "https://www.telemart.pk/mobile-and-tablets/mobile-phone.html?limit=all" # all result in one page
                links_to_data()
                data_to_csv()

            def whatmobile(self):
                def data_from_link():
                    url = "https://www.whatmobile.com.pk/"
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    
                    url = (
                        soup
                        .find("div", {"class" : "verticalMenu"})
                        .find_all("section")[2]
                        .find_all("li")[-1]
                        .find("a")['href']
                    )
                    url = "https://www.whatmobile.com.pk/" + url
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    a = soup.find("td", {"width" : "655"}).find_all("td", {"class" : "BiggerText"})
                    mobiles = []
                    prices = []
                    currency = []
                    for b in a:
                        try:
                            n = (
                                b
                                .find("a", {"class" : "BiggerText"})
                                .get_text()
                                .strip()
                            )
                            c = (
                                b
                                .find("span", {"class" : "PriceFont"})
                                .get_text()
                                .strip()
                            )
                            cc = c.split()[0]
                            p = ''.join([i for i in c.split()[-1] if i.isnumeric()])
                            mobiles.append(n)
                            prices.append(p)
                            currency.append(cc)
                        except:
                            pass
                    web = [url]*len(mobiles)
                    pickle.dump(mobiles, open("new-pak-whatmobile-mobiles.pkl", "wb"))
                    pickle.dump(prices, open("new-pak-whatmobile-prices.pkl", "wb"))
                    pickle.dump(currency, open("new-pak-whatmobile-currency.pkl", "wb"))
                    pickle.dump(web, open("new-pak-whatmobile-web.pkl", "wb"))

                def data_to_csv():
                    mobiles= pickle.load(open("new-pak-whatmobile-mobiles.pkl", "rb"))
                    prices= pickle.load(open("new-pak-whatmobile-prices.pkl", "rb"))
                    currency= pickle.load(open("new-pak-whatmobile-currency.pkl", "rb"))
                    web= pickle.load(open("new-pak-whatmobile-web.pkl", "rb"))
                    new_used = ['new']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles', 'prices', 'currency','new_used', 'web']:
                        df[i] = eval(i)
                    df.to_csv("new-pak-whatmobile-data.csv", index=False)
                    
                data_from_link()
                data_to_csv()

    class uesd:
        class egypt:
            def olx(self):

                def get_all_pages_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    pages = int(soup
                        .find("div", {"class" : "pager rel clr"})
                        .find_all("span", {"class" : "item fleft"})[-1]
                        .get_text()
                        .replace("\n", "")
                    )
                    all_pages = [url]
                    for i in range(2, pages+1):
                        all_pages.append(url + "?page=" + str(i))
                    pickle.dump(all_pages, open("used-egypt-olx-all_links.pkl", "wb"))


                def links_to_data():
                    all_pages = pickle.load(open("used-egypt-olx-all_links.pkl", "rb"))
                    names = []
                    currency = []
                    prices = []
                    for e, link in enumerate(all_pages):
                        print(round(e/len(all_pages), 2), end=", ")
                        n1 = []
                        cc1 = []
                        p1 = []
                        try:
                            soup = BeautifulSoup(requests.get(link,timeout=5).text, "lxml")
                            a = soup.find("div", {"class" : "rel listHandler"})
                            f = (
                                a
                                .find("table", {"class" : "fixed offers breakword"})
                                .find("tbody")
                                .find_all("tr")[-1]
                            )
                            featured_ads = f.find_all("div", {"class" : "ads__item"})
                            for f_add in featured_ads:
                                b = f_add.find("div", {"class" : "ads__item__info"})
                                n = (
                                    b
                                    .find("a", {"class" : "ads__item__title"})
                                    .get_text()
                                    .strip()
                                )
                                c = b.find_all("p")[0].get_text().strip()
                                cc = c.split()[-1]
                                p = c.split()[0].replace(",", "")
                                n1.append(n)
                                cc1.append(cc)
                                p1.append(p)
                            normal_adds = (
                                a
                                .find("table", {"id" : "offers_table"})
                                .find("tbody")
                                .find("div", {"class" : "ads ads--list"})
                                .find_all("div", {"class" : "ads__item"})
                            )
                            
                            for n_adds in normal_adds:
                                b_2 = n_adds.find("div", {"class" : "ads__item__info"})
                                n_2 = (
                                    b_2
                                    .find("a", {"class" : "ads__item__title"})
                                    .get_text()
                                    .strip()
                                )
                                c_2 = b_2.find_all("p")[0].get_text().strip()
                                cc_2 = c_2.split()[-1]
                                p_2 = c_2.split()[0].replace(",", "")
                                n1.append(n_2)
                                cc1.append(cc_2)
                                p1.append(p_2)
                            names += [n_2]
                            currency += [cc_2]
                            prices += [p_2]
                        
                        except:
                            pass
                    pickle.dump(names, open("used-egypt-olx-names.pkl", "wb"))
                    pickle.dump(currency, open("used-egypt-olx-currency.pkl", "wb"))
                    pickle.dump(prices, open("used-egypt-olx-prices.pkl", "wb"))    


                def data_to_csv():
                    mobiles = pickle.load(open("used-egypt-olx-names.pkl", "rb"))
                    prices = pickle.load(open("used-egypt-olx-prices.pkl", "rb"))
                    currency = pickle.load(open("used-egypt-olx-currency.pkl", "rb"))
                    web = [url]*len(mobiles)
                    new_used = ['used']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles', 'prices', 'currency','new_used', 'web']:
                        df[i] = eval(i)
                    df.to_csv("used-egypt-olx-data.csv", index=False)

                url = "https://olx.com.eg/en/mobile-phones-accessories/mobile-phones/"
                get_all_pages_links()
                links_to_data()
                data_to_csv()

        class pak:
            def best_mobile(self):

                def get_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    links = [url]
                    pages = int(soup
                        .find("ul", {"class" : "pagination pagination-lg"})
                        .find_all("li")[-2]
                        .get_text()
                    )
                    for i in range(2, pages+1):
                        links.append(url + "/page/" + str(i))
                    pickle.dump(links, open("used-pak-best_mobile-links.pkl", "wb"))

                def links_to_data():
                    names = []
                    prices = []
                    currency = []
                    errors = []
                    links = pickle.load(open("used-pak-best_mobile-links.pkl", "rb"))
                    for link in links:
                        soup = BeautifulSoup(requests.get(link,timeout=5).text, "lxml")
                        a = (
                            soup
                            .find("div", {"class" : "classified-list"})
                            .find_all("div", {"class" : "media"})
                        )
                        for b in a:
                            n = b.find("h4", {"class" : "media-heading"}).get_text().strip()
                            p = b.find("strong", {"class" : "ribbon-content"}).get_text()
                            if not "sold" in p.lower():
                                c = p.split()[0].replace(".", "")
                                try:
                                    pp = int(p.split()[1].replace(",", ""))   
                                except:
                                    pp = p.split()[1].replace(",", "")
                                names.append(n)
                                prices.append(pp)
                                currency.append(c)
                    pickle.dump(names, open("used-pak-best_mobile-names.pkl", "wb"))
                    pickle.dump(prices, open("used-pak-best_mobile-prices.pkl", "wb"))
                    pickle.dump(currency, open("used-pak-best_mobile-currency.pkl", "wb"))

                def data_to_csv():
                    mobiles = pickle.load(open("used-pak-best_mobile-names.pkl", "rb"))
                    prices = pickle.load(open("used-pak-best_mobile-prices.pkl", "rb"))
                    currency = pickle.load(open("used-pak-best_mobile-currency.pkl", "rb"))
                    web = [url]*len(mobiles)
                    new_used = ['used']*len(mobiles)
                    df = pd.DataFrame()
                    for i in ['mobiles', 'prices', 'currency', 'new_used', 'web']:
                        df[i] = eval(i)
                    df.to_csv("used-pak-best_mobile-data.csv", index=False)

                url = "https://www.bestmobile.pk/used-mobiles"
                get_links()
                links_to_data()
                data_to_csv()

            def shopbuzz(self):

                def get_all_links():
                    soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                    a = (
                        soup
                        .find("div", {"id" : "yw0"})
                        .find("ul")
                        .find_all("li")[-1]
                        .find("a")['href']
                    )
                    pages = int(re.findall('\\d+',a)[0])
                    all_links = [url]
                    for i in range(2, pages+1):
                        all_links.append("http://www.shopbuzz.pk/usedproduct/index?category=mobile-phones&UsedProduct_page=" + str(i))
                    pickle.dump(all_links, open("used-pak-shopbuzz-all_links.pkl", "wb"))

                def data_from_links():
                    all_links = pickle.load(open("used-pak-shopbuzz-all_links.pkl", "rb"))
                    mobiles = []
                    prices = []
                    currency = []
                    for link in all_links:
                        try:
                            soup = BeautifulSoup(requests.get(url,timeout=5).text, "lxml")
                            a = (
                                soup
                                .find("table", {"class" : "items table table-bordered"})
                                .find("tbody")
                            )
                            b = a.find_all("tr", {"class" : "odd"})
                            b += a.find_all("tr", {"class" : "even"})
                            m1 = []
                            cc1 = []
                            pp1 = []
                            for i in b:
                                d = i.find_all("td")
                                m = d[0].get_text().strip()
                                c = d[-1].get_text().strip()
                                cc = c.split()[0].replace(".", "").strip()
                                p = c.split()[1].replace(".", "").strip()
                                pp = int(''.join(re.findall('\\d+',p)))

                                m1.append(m)
                                cc1.append(cc)
                                pp1.append(pp)
                            mobiles += m1
                            currency += cc1
                            prices += pp1
                        except:
                            pass

                    pickle.dump(mobiles, open("used-pak-shopbuzz-mobiles.pkl", "wb"))
                    pickle.dump(currency, open("used-pak-shopbuzz-currency.pkl", "wb"))
                    pickle.dump(prices, open("used-pak-shopbuzz-prices.pkl", "wb"))

                def data_to_csv():
                    mobiles = pickle.load( open("used-pak-shopbuzz-mobiles.pkl", "rb"))
                    currency = pickle.load( open("used-pak-shopbuzz-currency.pkl", "rb"))
                    prices = pickle.load( open("used-pak-shopbuzz-prices.pkl", "rb"))
                    web = [url]*len(mobiles)
                    df = pd.DataFrame()
                    new_used = ['used']*len(mobiles)
                    for i in ['mobiles','prices','currency','new_used', 'web']:
                        df[i] = eval(i)
                    df.to_csv("used-pak-shopbuzz-data.csv", index=False)

                url = "http://www.shopbuzz.pk/usedproduct/index?category=mobile-phones"
                get_all_links()
                data_from_links()
                data_to_csv()
                
obj = scraper_class()

obj.new.egypt()._2b()
obj.new.egypt().ennap()
obj.new.egypt().jumia()
obj.new.egypt().priceNa()
obj.new.egypt().souq()
obj.new.egypt().yaoota()
obj.new.pak().mobile_phone()
obj.new.pak().telemart()
obj.new.pak().whatmobile()

obj.uesd.egypt().olx()
obj.uesd.pak().best_mobile()
obj.uesd.pak().shopbuzz()



