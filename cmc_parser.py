from bs4 import BeautifulSoup
import pandas

columns = ['token', 'url', 'chain', 'ico_price', 'end_date', 'goal']

def parse_page(file):
    with open(file) as fp:
        soup = BeautifulSoup(fp, features="lxml")
        tbody = soup.find('tbody')
        rows = tbody("tr")
        page = pandas.DataFrame(columns = columns)
        for row in rows:
            tds = row("td")
            td_0 = tds[0]
            token = td_0("span")[1].string
            a = td_0.a
            project_url = a['href']
            chain_parent_div = a.div.contents[1]

            chain = "nA"
            if len(chain_parent_div.contents) != 0:
                for string in chain_parent_div.div.strings:
                    chain = string
            ico_price = tds[1].string
            end_date = tds[4].string
            goal = tds[5].string
            row_df = pandas.DataFrame([[
                token, project_url, chain, ico_price, end_date, goal]], columns = columns)
            page = page.append(row_df, ignore_index = True)
        return page

def parse_pages(urls):
    dataframe = pandas.DataFrame(columns = columns)
    for url in urls:
        dataframe = dataframe.append(parse_page(url), ignore_index = True)
    return dataframe

