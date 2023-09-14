from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import argparse
import os
from dotenv import load_dotenv

load_dotenv()
# getting th eway bill user id
ewayBillPass = os.getenv('EWAY_BILL_PASSWORD')
# getting th eway bill password
ewayBillID =os.getenv('EWAY_BILL_ID')


# initializing the webdriver
driver = webdriver.Chrome('/Users/mayankkhanna/Downloads/chromedriver-mac-arm641/chromedriver')

def generate_new_eway_bill(docNo, gst, taxVal, hsn, transID):
    website_url = "https://www.ewaybillgst.gov.in/BillGeneration/BillGeneration.aspx"
    driver.get(website_url)

    username_field = driver.find_element_by_id("txt_username")
    password_field = driver.find_element_by_id("txt_password")

    username_field.send_keys(ewayBillID)
    password_field.send_keys(ewayBillPass)
    time.sleep(8)

    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    website_url = "https://www.ewaybillgst.gov.in/BillGeneration/BillGeneration.aspx"
    driver.get(website_url)

    txtDocNo_field = driver.find_element_by_id("txtDocNo")
    billToGST_field = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtToGSTIN")
    taxableValue_field = driver.find_element_by_id("txt_TRC_1")
    hsn_field = driver.find_element_by_id("txt_HSN_1")
    transporterID_field = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtTransid")


    txtDocNo_field.send_keys(docNo)
    billToGST_field.send_keys(gst)
    time.sleep(1)

    taxableValue_field.send_keys(str(taxVal))
    time.sleep(0.5)

    hsn_field.send_keys(hsn)
    dropdown_IGST = Select(driver.find_element_by_id("SelectIGST_1"))
    desired_option = "5"
    dropdown_IGST.select_by_visible_text(desired_option)
    time.sleep(0.2)

    transporterID_field.send_keys(transID)
    time.sleep(0.6)

    scroll_distance = 500
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

    submit_button = driver.find_element_by_xpath("//button[text()='Submit']")
    submit_button.click()

    for _ in range(3):
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass


# # Wait for the element to be present and clickable
#     scroll_distance = 500
#     driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

# # Wait for the "Print" link to be clickable
#     tr_element = driver.find_element_by_id("ctl00_ContentPlaceHolder1_printtr")

#     # Find the "Print" link within the <tr> element
#     print_link = tr_element.find_element(By.LINK_TEXT, "Print")

#     # Click the "Print" link
#     print_link.click()
#     # print_link = driver.find_element_by_class_name("btnprint")
#     # print_link.click()

def main():
    parser = argparse.ArgumentParser(description='Generate Eway Bill')
    parser.add_argument('--docNo', type=str, help='Doc No')
    parser.add_argument('--gst', type=str, help='GST of the client')
    parser.add_argument('--taxVal', type=float, help='Taxable Value')
    parser.add_argument('--hsn', type=str, help='HSN Code')
    parser.add_argument('--transID', type=str, help='Transporter ID')

    args = parser.parse_args()

    generate_new_eway_bill(args.docNo, args.gst, args.taxVal, args.hsn, args.transID)

if __name__ == '__main__':
    main()