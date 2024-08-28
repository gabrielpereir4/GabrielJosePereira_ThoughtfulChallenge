from datetime import datetime
from RPA.Browser.Selenium import Selenium
from dateutil.relativedelta import relativedelta
import pandas as pd



class Tasks:
    def __init__(self, logger):
        self.logger = logger
        self.browser = None
        self.data =  []


    def open_browser(self):
        browser = Selenium()
        browser.open_chrome_browser("https://www.aljazeera.com/")
        browser.delete_all_cookies()
        browser.maximize_browser_window()
        browser.set_selenium_implicit_wait("2 seconds")
        browser.set_screenshot_directory('.\\screenshots')
        self.logger.info('Browser open!')
        self.browser = browser
        return browser


    def close_browser(self):
        self.browser.close_all_browsers()


    def search(self, search):
        browser = self.browser
        # Cookies popup
        self.logger.info('Looking for Cookies popup')
        browser.click_element_if_visible('xpath://*[@id="onetrust-accept-btn-handler"]')
        # Opens search bar
        browser.click_element_when_clickable('xpath://*[@id="root"]'
                              '/div/div[1]/div[1]'
                              '/div/header/div[4]'
                              '/div[2]/button')
        # Texts into bar
        browser.input_text_when_element_is_visible('xpath://*[@id="root"]'
                                                   '/div/div[1]/div[2]'
                                                   '/div/div/form'
                                                   '/div[1]/input', search)
        # Search action
        browser.click_element_when_clickable('xpath://*[@id="root"]/div/div[1]/div[2]'
                              '/div/div/form/div[2]/button')


    def iterate_news(self, time_period, search_word):
        browser = self.browser
        # Waits until 'Sort By' select is available
        browser.wait_until_element_is_visible('id:search-sort-option')
        sortby = browser.get_webelement('id:search-sort-option')
        browser.select_from_list_by_value(sortby, 'date')

        # Auxiliary variables
        i = 1
        end = False

        # Getting minimal desired date
        current_date = datetime.now().date()
        if time_period == 0:
            # For subtracting (period of one month)
            time_period = 1
        aim_date = current_date - relativedelta(months=time_period)
        self.logger.info(f'Current date: {current_date} - Max date is:{aim_date}')
        while True:
            # Building the xpath for each article
            xpath = ('//*[@id="main-content-area"]/div[2]/div[2]/article['
                        + str(i) + ']'
                )
            self.logger.info(f'Current Xpath: {xpath}')

            browser.wait_until_element_is_visible(xpath, 6)
            while browser.is_element_visible(xpath):
                self.logger.info(f'Auxiliary value: {i}')
                self.logger.info('Looking for popup')
                # Clicks out popup that may appear
                if browser.is_element_enabled('xpath://*[@id="root"]'
                                                 '/div/div[4]/div[2]'
                                                 '/div/button'):
                    browser.scroll_element_into_view('xpath://*[@id="root"]'
                                                 '/div/div[4]/div[2]'
                                                 '/div/button')
                    browser.click_element_if_visible('xpath://*[@id="root"]'
                                                    '/div/div[4]/div[2]'
                                                    '/div/button')
                title_xpath = xpath + '/div[2]/div[1]'
                browser.scroll_element_into_view(xpath)

                # Waits until article has loaded
                browser.wait_until_element_is_visible(title_xpath)

                # Date
                time_xpath = xpath + '/div[2]/footer/div/div/div/div/span[2]'
                self.logger.info('Looking for date field')
                if browser.is_element_visible(time_xpath):
                    t = browser.get_webelement(time_xpath)
                    time_text = browser.get_text(t)
                    self.logger.info(f'Time: {time_text}')
                    if 'Last update' in time_text:
                        time_text = time_text.replace("Last update ", "")
                    date_object = datetime.strptime(time_text, "%d %b %Y")
                    date_object = date_object.date()
                    self.logger.info(f'Formatted Time: {date_object}')
                    # If current date is less than the aim date, breaks loop
                    if date_object < aim_date:
                        end = True
                        break
                # If there is no Time element, this article is skipped
                if not browser.is_element_visible(time_xpath):
                    i += 1
                    xpath = ('//*[@id="main-content-area"]/div[2]/div[2]/article['
                        + str(i) + ']'
                    )
                    self.logger.info('Continue: News has no time info')
                    continue

                # Title
                title = browser.get_webelement(title_xpath)
                title_text = browser.get_text(title)
                self.logger.info(f'Title: {title_text}')

                # Description
                description_xpath = xpath + '/div[2]/div[2]'
                description = browser.get_webelement(description_xpath)
                description_text = browser.get_text(description)
                self.logger.info(f'Description: {description_text}')

                # Image
                try:
                    image_xpath = xpath + '/div[1]'
                    image = browser.get_webelement(image_xpath)
                    img = browser.capture_element_screenshot(image)
                    self.logger.info(f'Image: {img}')
                except Exception:
                    self.logger.info('No image')

                # Sums 1 to i for finding the next article
                i += 1
                xpath = ('//*[@id="main-content-area"]/div[2]/div[2]/article['
                        + str(i) + ']'
                )
                # Sends data to excel handler
                excel_data = [title_text, description_text, date_object, img]
                self.fill_excel(excel_data, search_word)

            # If there are no more articles, loads more clicking on 'Show More'
            show_more = browser.get_webelement('xpath://*[@id="main-content-area"]'
                                             '/div[2]/div[2]/button')
            # If end is assigned as True (date/time - line 98), breaks loop
            if end:
                self.logger.info('Breaking')
                self.save_to_excel()
                break
            # For clicking the 'Show More' button
            for attempt in range(1, 5):
                try:
                    self.logger.info(f"Attempt {attempt} of {5}")
                    # Clicks out popup that may appear
                    self.logger.info('Looking for popup')
                    browser.click_element_if_visible('xpath://*[@id="root"]'
                                                    '/div/div[4]/div[2]'
                                                    '/div/button')
                    browser.scroll_element_into_view(show_more)
                    browser.click_element_if_visible(show_more)
                    self.logger.info(f'Success at attempt {attempt}')
                    break
                except Exception as e:
                    self.logger.error(f"Error at attempt {attempt}: {e}")
                    if attempt == 5:
                        self.logger.critical("Max attempt reached. Breaking")
                    else:
                        self.logger.info("Retrying...")
            # Sums 1 to i for finding the next article
            i += 1


    def fill_excel(self, data, search_word):
        # See iterate_news for list references
        title = data[0]
        description = data[1]
        date = data[2]
        img = data[3]

        # Counts search_word appearances in both title and description
        count = (
            title.upper().count(search_word.upper()) +
            description.upper().count(search_word.upper())
        )
        if count == 0:
            return
        self.logger.info(f'Search word count: {count}')

        # Checks if any money amount is in title or description
        money = False
        if '$' in title or 'USD' in title or 'dollars' in title:
            money = True
        elif '$' in description or 'USD' in description or 'dollars' in description:
            money = True

        row_data = {
            "Title": title,
            "Date": date,
            "Description": description,
            "Picture Filename": img,
            "Count of Phrases": count,
            "Contains Money": money
        }
        self.logger.info(f'Writing row: {row_data}')
        self.data.append(row_data)

    def save_to_excel(self):
        df = pd.DataFrame(self.data)
        file_path = './output/excel.xlsx'

        with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        self.logger.info('Data successfully written to Excel')
